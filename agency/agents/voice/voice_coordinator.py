"""
Voice Agent Coordinator - Orchestrates All Voice Agents

Central hub for managing all voice-based agents and workflows.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime

from agency.voice.voice_skills import VoiceSkills
from agency.agents.voice.dictation.dictation_agent import DictationAgent
from agency.agents.voice.productivity.productivity_agent import ProductivityVoiceAgent
from agency.agents.voice.ideas_capture.ideas_capture_agent import IdeasCaptureAgent
from agency.agents.voice.dev_copilot.dev_copilot_agent import DeveloperCopilotAgent

logger = logging.getLogger(__name__)


class VoiceCoordinator:
    """
    Coordinates all voice agents and enables complex workflows.

    Features:
    - Unified voice interface
    - Multi-agent workflows
    - Context switching between agents
    - Voice routing
    - Session management
    """

    def __init__(self):
        """Initialize voice coordinator."""
        self.voice_skills = VoiceSkills()

        # Initialize all agents
        self.dictation = DictationAgent()
        self.productivity = ProductivityVoiceAgent()
        self.ideas = IdeasCaptureAgent()
        self.copilot = DeveloperCopilotAgent()

        self.current_agent = None
        self.session_history = []

        logger.info("Voice Coordinator initialized with all agents")

    async def start_voice_interface(self):
        """
        Start unified voice interface.

        Listens for commands and routes to appropriate agent.
        """
        logger.info("Starting unified voice interface")

        await self.productivity.speak("Voice interface ready. How can I help?")

        while True:
            try:
                print("\n🎤 Listening for command...")

                # Record command
                audio_file = await self.voice_skills.record_audio(duration=5)

                # Transcribe
                transcription = await self.voice_skills.transcribe_audio(audio_file)
                command = transcription.get("text", "").lower()

                logger.info(f"Received command: {command}")

                # Route to appropriate agent
                result = await self._route_command(command, audio_file)

                # Log to session history
                self.session_history.append({
                    "command": command,
                    "agent": self.current_agent,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

                # Check for exit
                if "exit" in command or "goodbye" in command:
                    await self.productivity.speak("Goodbye!")
                    break

            except KeyboardInterrupt:
                await self.productivity.speak("Voice interface closed.")
                break
            except Exception as e:
                logger.error(f"Voice interface error: {e}")
                await self.productivity.speak("Sorry, I had an error. Let's try again.")

    async def _route_command(self, command: str, audio_file: str) -> Dict:
        """Route command to appropriate agent."""

        # Dictation commands
        if "dictate" in command or "transcribe" in command:
            self.current_agent = "dictation"
            if "claude" in command:
                return await self.dictation.dictate_to_claude(audio_file)
            else:
                return await self.dictation.transcribe_and_copy_to_clipboard(audio_file)

        # Productivity commands
        elif any(word in command for word in ["briefing", "calendar", "email", "schedule"]):
            self.current_agent = "productivity"

            if "briefing" in command:
                return await self.productivity.morning_briefing()
            else:
                return await self.productivity.listen_for_command()

        # Ideas capture commands
        elif "idea" in command or "note" in command or "capture" in command:
            self.current_agent = "ideas"
            return await self.ideas.capture_idea(audio_file, auto_categorize=True)

        # Developer copilot commands
        elif any(word in command for word in ["code", "debug", "review", "architect"]):
            self.current_agent = "copilot"

            if "review" in command:
                # Would need file path from follow-up
                await self.copilot.speak("Which file should I review?")
                return {"action": "awaiting_file_path"}
            else:
                return await self.copilot.discuss_code(audio_file)

        # Help command
        elif "help" in command:
            return await self._show_help()

        # Unknown command
        else:
            await self.productivity.speak("I didn't understand that. Say 'help' for available commands.")
            return {"action": "unknown", "command": command}

    async def _show_help(self) -> Dict:
        """Show available voice commands."""
        help_text = """
        Here are the available voice commands:

        Dictation:
        - "Dictate to Claude" - Transcribe for Claude
        - "Transcribe this" - Copy to clipboard

        Productivity:
        - "Morning briefing" - Get daily briefing
        - "Check my email" - Email summary
        - "What's my schedule" - Calendar

        Ideas:
        - "Capture idea" - Save idea to notes
        - "Quick note" - Quick capture

        Developer:
        - "Discuss code" - Code discussion
        - "Review code" - Code review
        - "Debug this" - Debugging help

        Say 'exit' to quit.
        """

        await self.productivity.speak(help_text)

        return {
            "action": "help",
            "commands": help_text
        }

    async def workflow_morning_routine(self):
        """
        Complete morning routine workflow.

        1. Morning briefing
        2. Read urgent emails
        3. Review calendar
        4. Suggest priorities
        """
        logger.info("Starting morning routine workflow")

        # Step 1: Morning briefing
        await self.productivity.speak("Good morning! Starting your morning routine.")

        briefing = await self.productivity.morning_briefing(speak_out_loud=True)

        # Step 2: Check for urgent items
        if briefing["data"]["emails"]["urgent"] > 0:
            await self.productivity.speak(f"You have {briefing['data']['emails']['urgent']} urgent emails. Would you like me to read them?")

            # Wait for response
            response_audio = await self.voice_skills.record_audio(duration=3)
            response = await self.voice_skills.transcribe_audio(response_audio)

            if "yes" in response.get("text", "").lower():
                await self.productivity._handle_read_emails()

        # Step 3: Suggest focus
        await self.productivity.speak("I suggest blocking focus time before your first meeting. Should I do that?")

        response_audio = await self.voice_skills.record_audio(duration=3)
        response = await self.voice_skills.transcribe_audio(response_audio)

        if "yes" in response.get("text", "").lower():
            await self.productivity._handle_block_focus_time("2 hours")

        await self.productivity.speak("Your morning routine is complete. Have a great day!")

        return {
            "workflow": "morning_routine",
            "status": "completed",
            "briefing": briefing
        }

    async def workflow_idea_to_implementation(self, audio_file: str):
        """
        Workflow: Capture idea → Discuss with copilot → Create task.

        Args:
            audio_file: Audio describing the idea

        Returns:
            Complete workflow result
        """
        logger.info("Starting idea-to-implementation workflow")

        # Step 1: Capture the idea
        await self.productivity.speak("Let me capture that idea first.")
        idea_result = await self.ideas.capture_idea(audio_file, auto_categorize=True)

        # Step 2: Discuss implementation with copilot
        await self.productivity.speak("Now let's discuss how to implement it.")

        # Re-use the audio for copilot
        copilot_result = await self.copilot.discuss_code(
            audio_file,
            code_context=f"Idea: {idea_result['idea']}"
        )

        # Step 3: Summarize
        summary = f"""Okay, I've captured your idea about {idea_result['category']},
        and we discussed the implementation.
        The idea is saved to {idea_result['saved_to']}.
        Ready to start coding?"""

        await self.productivity.speak(summary)

        return {
            "workflow": "idea_to_implementation",
            "idea": idea_result,
            "discussion": copilot_result,
            "status": "ready"
        }

    async def workflow_code_review_session(self, file_path: str):
        """
        Workflow: Review code → Capture improvements → Create tasks.

        Args:
            file_path: Path to code file

        Returns:
            Review workflow result
        """
        logger.info(f"Starting code review workflow for {file_path}")

        # Step 1: Code review
        await self.productivity.speak(f"Reviewing {file_path}")
        review_result = await self.copilot.review_code(file_path)

        # Step 2: Capture action items
        await self.productivity.speak("Let me capture the action items from this review.")

        action_items = f"Code review action items for {file_path}:\n\n{review_result['review']}"

        # Save to ideas/notes
        await self.ideas._save_to_local_file(
            action_items,
            "code_review",
            datetime.now()
        )

        await self.productivity.speak("Review complete. Action items saved.")

        return {
            "workflow": "code_review",
            "file": file_path,
            "review": review_result,
            "status": "completed"
        }

    def save_session(self, output_file: str = "voice_session.json"):
        """Save session history."""
        import json

        with open(output_file, "w") as f:
            json.dump({
                "session_start": self.session_history[0]["timestamp"] if self.session_history else None,
                "session_end": datetime.now().isoformat(),
                "history": self.session_history
            }, f, indent=2)

        logger.info(f"Session saved to {output_file}")


# CLI interface
async def voice_coordinator_cli():
    """
    CLI for voice coordinator.

    Usage:
        python -m agency.agents.voice.voice_coordinator
    """
    coordinator = VoiceCoordinator()

    print("🎙️  Voice Agent Coordinator")
    print("=" * 50)
    print("Workflows:")
    print("  1 - Unified voice interface")
    print("  2 - Morning routine")
    print("  3 - Help")
    print("  q - Quit")
    print("=" * 50)

    while True:
        choice = input("\n> ").strip()

        if choice == "1":
            print("\n🎙️  Starting unified voice interface...")
            print("(Press Ctrl+C to exit)")
            await coordinator.start_voice_interface()

        elif choice == "2":
            print("\n☀️  Starting morning routine...")
            result = await coordinator.workflow_morning_routine()
            print("\n✅ Morning routine complete!")

        elif choice == "3":
            await coordinator._show_help()

        elif choice.lower() == "q":
            # Save session
            if coordinator.session_history:
                coordinator.save_session()
                print("📝 Session saved")

            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(voice_coordinator_cli())
