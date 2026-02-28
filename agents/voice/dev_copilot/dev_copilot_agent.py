"""
Developer Co-pilot Agent - Voice-Based Code Discussion

A thoughtful development partner you can discuss code and ideas with via voice.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

from integrations.voice_core.voice_skills import VoiceSkills

logger = logging.getLogger(__name__)


class DeveloperCopilotAgent:
    """
    Voice-enabled development partner.

    Features:
    - Voice-based code discussion
    - Architecture brainstorming
    - Code review via voice
    - Debugging conversations
    - Technical explanations
    - Pair programming via voice
    """

    def __init__(self):
        """Initialize developer copilot agent."""
        self.voice_skills = VoiceSkills()
        self.voice = "onyx"  # Deeper voice for developer persona
        self.conversation_history = []
        self.current_context = {
            "project": None,
            "files": [],
            "topic": None
        }

        # Initialize Claude
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False
            logger.warning("Claude API not configured")

        logger.info("Developer Copilot Agent initialized")

    async def start_coding_session(
        self,
        project_path: Optional[str] = None,
        topic: Optional[str] = None
    ) -> Dict:
        """
        Start a voice coding session.

        Args:
            project_path: Path to project directory
            topic: Topic to discuss

        Returns:
            Session info
        """
        self.current_context["project"] = project_path
        self.current_context["topic"] = topic
        self.conversation_history = []

        greeting = "Hey! I'm ready to help with your code. What are we working on today?"

        await self.speak(greeting)

        return {
            "status": "session_started",
            "project": project_path,
            "topic": topic,
            "greeting": greeting
        }

    async def discuss_code(
        self,
        audio_file: str,
        code_context: Optional[str] = None
    ) -> Dict:
        """
        Discuss code via voice.

        Args:
            audio_file: Audio recording of your question
            code_context: Optional code snippet or file content

        Returns:
            {
                "your_question": "How should I structure this?",
                "my_response": "I'd suggest using...",
                "audio_response": "path/to/response.mp3"
            }
        """
        logger.info("Processing code discussion")

        # Transcribe question
        transcription = await self.voice_skills.transcribe_audio(
            audio_file,
            prompt="Developer discussing code architecture or implementation."
        )

        if "error" in transcription:
            return transcription

        question = transcription["text"]
        logger.info(f"Developer asked: {question}")

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        })

        # Get response from Claude
        response_text = await self._get_claude_response(question, code_context)

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })

        # Convert response to speech
        audio_result = await self.voice_skills.synthesize_speech(
            response_text,
            voice=self.voice
        )
        audio_file = audio_result.get("audio_file")

        # Play response
        if audio_file:
            await self.voice_skills.stream_audio(audio_file)

        return {
            "your_question": question,
            "my_response": response_text,
            "audio_response": audio_file,
            "timestamp": datetime.now().isoformat()
        }

    async def _get_claude_response(
        self,
        question: str,
        code_context: Optional[str] = None
    ) -> str:
        """Get response from Claude."""
        if not self.has_claude:
            return "I don't have access to Claude right now. Can you check the API configuration?"

        try:
            # Build context
            system_prompt = """You are an experienced software engineer and thoughtful development partner.

You're having a voice conversation with a developer. Your responses should be:
- Conversational and natural (like talking to a colleague)
- Technically accurate
- Concise but complete
- Helpful and constructive
- Include code examples when relevant

Keep responses under 200 words unless asked for more detail."""

            # Build message with context
            user_message = question

            if code_context:
                user_message = f"Here's the code context:\n\n```\n{code_context}\n```\n\nQuestion: {question}"

            # Include conversation history
            messages = []

            # Add last few exchanges for context
            for entry in self.conversation_history[-4:]:  # Last 2 exchanges
                messages.append({
                    "role": entry["role"],
                    "content": entry["content"]
                })

            # Add current question
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Get response from Claude
            response = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                system=system_prompt,
                messages=messages
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return "Sorry, I encountered an error. Could you try asking again?"

    async def review_code(self, code_file: str) -> Dict:
        """
        Voice-based code review.

        Args:
            code_file: Path to code file to review

        Returns:
            Review results with voice feedback
        """
        logger.info(f"Reviewing code: {code_file}")

        # Read code file
        try:
            with open(code_file, "r") as f:
                code_content = f.read()
        except Exception as e:
            return {"error": f"Could not read file: {e}"}

        # Get review from Claude
        review_prompt = f"""Review this code and provide constructive feedback.

Focus on:
- Code quality and readability
- Potential bugs or issues
- Best practices
- Suggestions for improvement

Keep the review conversational, like you're pair programming.

```python
{code_content}
```"""

        review_text = await self._get_claude_response(review_prompt)

        # Speak the review
        await self.speak(review_text)

        return {
            "file": code_file,
            "review": review_text,
            "timestamp": datetime.now().isoformat()
        }

    async def explain_code(
        self,
        audio_file: str,
        code_snippet: Optional[str] = None
    ) -> Dict:
        """
        Explain code via voice conversation.

        Args:
            audio_file: Audio asking for explanation
            code_snippet: Code to explain

        Returns:
            Explanation
        """
        # Transcribe question
        transcription = await self.voice_skills.transcribe_audio(audio_file)
        question = transcription.get("text", "")

        # Build explanation prompt
        if code_snippet:
            prompt = f"Explain this code:\n\n```\n{code_snippet}\n```\n\n{question}"
        else:
            prompt = question

        explanation = await self._get_claude_response(prompt)

        # Speak explanation
        await self.speak(explanation)

        return {
            "question": question,
            "explanation": explanation,
            "code": code_snippet
        }

    async def brainstorm_architecture(self, audio_file: str) -> Dict:
        """
        Brainstorm architecture decisions via voice.

        Args:
            audio_file: Audio describing the problem

        Returns:
            Architecture suggestions
        """
        # Transcribe problem description
        transcription = await self.voice_skills.transcribe_audio(
            audio_file,
            prompt="Developer describing an architecture or design problem."
        )
        problem = transcription.get("text", "")

        # Get architecture suggestions
        prompt = f"""Let's brainstorm architecture for this:

{problem}

Suggest 2-3 different approaches, with pros and cons of each. Keep it conversational."""

        suggestions = await self._get_claude_response(prompt)

        # Speak suggestions
        await self.speak(suggestions)

        return {
            "problem": problem,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }

    async def debug_conversation(self, audio_file: str, error_log: Optional[str] = None) -> Dict:
        """
        Debug via voice conversation.

        Args:
            audio_file: Audio describing the bug
            error_log: Optional error log or stack trace

        Returns:
            Debugging suggestions
        """
        # Transcribe bug description
        transcription = await self.voice_skills.transcribe_audio(
            audio_file,
            prompt="Developer describing a bug or error."
        )
        bug_description = transcription.get("text", "")

        # Build debugging prompt
        prompt = f"Here's a bug I'm facing:\n\n{bug_description}"

        if error_log:
            prompt += f"\n\nError log:\n```\n{error_log}\n```"

        prompt += "\n\nWhat should I check?"

        debugging_advice = await self._get_claude_response(prompt)

        # Speak advice
        await self.speak(debugging_advice)

        return {
            "bug_description": bug_description,
            "advice": debugging_advice,
            "error_log": error_log
        }

    async def pair_programming_mode(self):
        """
        Continuous pair programming mode.

        Keeps conversation going while you code.
        """
        logger.info("Starting pair programming mode")

        await self.speak("Pair programming mode activated. I'm here to help!")

        while True:
            try:
                print("\n🎤 Listening... (or say 'exit' to stop)")

                # Record audio
                audio_file = await self.voice_skills.record_audio(duration=10)

                # Process
                result = await self.discuss_code(audio_file)

                # Check for exit command
                if "exit" in result.get("your_question", "").lower():
                    await self.speak("Great session! Happy coding!")
                    break

            except KeyboardInterrupt:
                await self.speak("Ending pair programming session. Good luck!")
                break
            except Exception as e:
                logger.error(f"Pair programming error: {e}")
                await self.speak("Sorry, I had an issue. Let's try again.")

    async def speak(self, text: str) -> str:
        """Speak text out loud."""
        logger.info(f"Speaking: {text[:50]}...")

        result = await self.voice_skills.synthesize_speech(text, voice=self.voice)
        audio_file = result.get("audio_file")

        if audio_file:
            await self.voice_skills.stream_audio(audio_file)

        return audio_file

    def save_conversation(self, output_file: str):
        """Save conversation history to file."""
        with open(output_file, "w") as f:
            import json
            json.dump({
                "context": self.current_context,
                "conversation": self.conversation_history
            }, f, indent=2)

        logger.info(f"Conversation saved to {output_file}")


# CLI interface
async def copilot_cli():
    """
    CLI for developer copilot agent.

    Usage:
        python -m agency.agents.voice.dev_copilot.dev_copilot_agent
    """
    agent = DeveloperCopilotAgent()

    print("👨‍💻 Developer Copilot Agent")
    print("=" * 50)
    print("Commands:")
    print("  1 - Start coding session")
    print("  2 - Discuss code (voice)")
    print("  3 - Review code file")
    print("  4 - Pair programming mode")
    print("  5 - Save conversation")
    print("  q - Quit")
    print("=" * 50)

    while True:
        choice = input("\n> ").strip()

        if choice == "1":
            print("\n👨‍💻 Starting coding session...")
            topic = input("What are we working on? ").strip()
            result = await agent.start_coding_session(topic=topic)
            print(f"\n{result['greeting']}")

        elif choice == "2":
            print("\n🎤 Recording your question (10s)...")
            audio_file = await agent.voice_skills.record_audio(duration=10)

            print("🤔 Thinking...")
            result = await agent.discuss_code(audio_file)

            print(f"\nYou: {result['your_question']}")
            print(f"\nCopilot: {result['my_response']}")

        elif choice == "3":
            file_path = input("Enter code file path: ").strip()
            print(f"\n📝 Reviewing {file_path}...")
            result = await agent.review_code(file_path)

            if "error" not in result:
                print(f"\n{result['review']}")
            else:
                print(f"\n❌ Error: {result['error']}")

        elif choice == "4":
            print("\n👨‍💻 Starting pair programming mode...")
            print("(Press Ctrl+C to exit)")
            await agent.pair_programming_mode()

        elif choice == "5":
            output = "conversation.json"
            agent.save_conversation(output)
            print(f"✅ Saved to {output}")

        elif choice.lower() == "q":
            print("Happy coding!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(copilot_cli())
