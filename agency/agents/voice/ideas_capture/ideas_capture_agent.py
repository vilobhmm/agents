"""
Ideas Capture Agent - Voice-to-Notes

Transcribes new ideas and writes them to Google Docs or Apple Notes.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime
import json

from agency.voice.voice_skills import VoiceSkills

logger = logging.getLogger(__name__)


class IdeasCaptureAgent:
    """
    Agent that captures ideas via voice and saves to notes.

    Features:
    - Voice-to-Google Docs
    - Voice-to-Apple Notes
    - Auto-categorization of ideas
    - Idea organization by topic
    - Quick capture mode
    - Batch processing
    """

    def __init__(self):
        """Initialize ideas capture agent."""
        self.voice_skills = VoiceSkills()
        self.default_target = os.getenv("IDEAS_TARGET", "google_docs")  # or "apple_notes"

        # Try to import Google services
        try:
            from openclaw.integrations import GoogleServices
            self.google = GoogleServices()
            self.has_google = True
        except:
            self.google = None
            self.has_google = False
            logger.warning("Google services not available")

        logger.info(f"Ideas Capture Agent initialized (target={self.default_target})")

    async def capture_idea(
        self,
        audio_file: str,
        target: Optional[str] = None,
        category: Optional[str] = None,
        auto_categorize: bool = True
    ) -> Dict:
        """
        Capture idea from audio and save to notes.

        Args:
            audio_file: Path to audio recording
            target: Where to save (google_docs, apple_notes, or None for default)
            category: Category/tag for the idea
            auto_categorize: Automatically categorize the idea

        Returns:
            {
                "idea": "transcribed text",
                "category": "productivity",
                "saved_to": "google_docs",
                "doc_url": "https://docs.google.com/...",
                "timestamp": "2026-02-27T10:30:00"
            }
        """
        logger.info("Capturing idea from audio")

        # Transcribe the idea
        result = await self.voice_skills.transcribe_audio(
            audio_file,
            prompt="User recording a new idea or thought."
        )

        if "error" in result:
            return result

        idea_text = result["text"]
        timestamp = datetime.now()

        # Auto-categorize if requested
        if auto_categorize and not category:
            category = await self._auto_categorize_idea(idea_text)

        # Determine target
        save_target = target or self.default_target

        # Save to appropriate target
        if save_target == "google_docs":
            save_result = await self._save_to_google_docs(idea_text, category, timestamp)
        elif save_target == "apple_notes":
            save_result = await self._save_to_apple_notes(idea_text, category, timestamp)
        else:
            save_result = await self._save_to_local_file(idea_text, category, timestamp)

        return {
            "idea": idea_text,
            "category": category,
            "saved_to": save_target,
            **save_result,
            "timestamp": timestamp.isoformat()
        }

    async def _auto_categorize_idea(self, idea_text: str) -> str:
        """
        Auto-categorize idea using Claude.

        Categories: work, personal, project, code, business, random
        """
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            prompt = f"""Categorize this idea into ONE category: work, personal, project, code, business, or random.

Idea: "{idea_text}"

Respond with just the category name, nothing else."""

            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )

            category = message.content[0].text.strip().lower()
            logger.info(f"Auto-categorized as: {category}")
            return category

        except Exception as e:
            logger.error(f"Auto-categorization failed: {e}")
            return "general"

    async def _save_to_google_docs(
        self,
        idea_text: str,
        category: str,
        timestamp: datetime
    ) -> Dict:
        """Save idea to Google Docs."""
        if not self.has_google:
            logger.error("Google services not configured")
            return {"error": "Google services not configured"}

        try:
            # Format idea entry
            formatted_idea = self._format_idea_entry(idea_text, category, timestamp)

            # Get or create Ideas document
            doc_id = await self._get_or_create_ideas_doc()

            # Append to document
            await self.google.append_to_doc(doc_id, formatted_idea)

            doc_url = f"https://docs.google.com/document/d/{doc_id}"

            logger.info(f"Saved idea to Google Docs: {doc_url}")

            return {
                "doc_id": doc_id,
                "doc_url": doc_url,
                "status": "saved"
            }

        except Exception as e:
            logger.error(f"Failed to save to Google Docs: {e}")
            # Fallback to local file
            return await self._save_to_local_file(idea_text, category, timestamp)

    async def _save_to_apple_notes(
        self,
        idea_text: str,
        category: str,
        timestamp: datetime
    ) -> Dict:
        """Save idea to Apple Notes."""
        try:
            # Use AppleScript to create note
            formatted_idea = self._format_idea_entry(idea_text, category, timestamp)

            applescript = f'''
            tell application "Notes"
                tell account "iCloud"
                    tell folder "Ideas"
                        make new note with properties {{name:"{category.title()}", body:"{formatted_idea}"}}
                    end tell
                end tell
            end tell
            '''

            # Execute AppleScript
            import subprocess
            subprocess.run(["osascript", "-e", applescript], check=True)

            logger.info(f"Saved idea to Apple Notes (category: {category})")

            return {
                "note_folder": "Ideas",
                "note_category": category,
                "status": "saved"
            }

        except Exception as e:
            logger.error(f"Failed to save to Apple Notes: {e}")
            # Fallback to local file
            return await self._save_to_local_file(idea_text, category, timestamp)

    async def _save_to_local_file(
        self,
        idea_text: str,
        category: str,
        timestamp: datetime
    ) -> Dict:
        """Save idea to local markdown file."""
        ideas_dir = Path.home() / "Documents" / "Ideas"
        ideas_dir.mkdir(parents=True, exist_ok=True)

        # Create category file
        category_file = ideas_dir / f"{category}.md"

        formatted_idea = self._format_idea_entry(idea_text, category, timestamp)

        # Append to file
        with open(category_file, "a", encoding="utf-8") as f:
            f.write(formatted_idea + "\n\n")

        logger.info(f"Saved idea to local file: {category_file}")

        return {
            "file_path": str(category_file),
            "status": "saved"
        }

    def _format_idea_entry(
        self,
        idea_text: str,
        category: str,
        timestamp: datetime
    ) -> str:
        """Format idea for saving."""
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M")

        entry = f"""### {category.title()} Idea - {formatted_timestamp}

{idea_text}

---
"""
        return entry

    async def _get_or_create_ideas_doc(self) -> str:
        """Get or create the main Ideas Google Doc."""
        # Search for existing Ideas document
        try:
            docs = await self.google.search_documents("Ideas Journal")
            if docs:
                return docs[0]["id"]
        except:
            pass

        # Create new Ideas document
        try:
            doc = await self.google.create_document(
                title="Ideas Journal",
                content="# My Ideas\n\nCapturing thoughts and ideas via voice.\n\n"
            )
            return doc["id"]
        except Exception as e:
            logger.error(f"Failed to create Ideas doc: {e}")
            raise

    async def quick_capture(self, duration: int = 30) -> Dict:
        """
        Quick capture mode - record and save immediately.

        Args:
            duration: Max recording duration (seconds)

        Returns:
            Result of capture operation
        """
        logger.info(f"Quick capture mode ({duration}s)")

        # Record audio
        print(f"🎤 Recording idea ({duration}s max)...")
        audio_file = await self.voice_skills.record_audio(
            duration=duration,
            stop_on_silence=True
        )

        # Capture and save
        print("💾 Saving idea...")
        result = await self.capture_idea(audio_file, auto_categorize=True)

        return result

    async def batch_capture(self, num_ideas: int = 5) -> List[Dict]:
        """
        Batch capture multiple ideas in succession.

        Args:
            num_ideas: Number of ideas to capture

        Returns:
            List of capture results
        """
        logger.info(f"Batch capturing {num_ideas} ideas")

        results = []

        for i in range(num_ideas):
            print(f"\n💡 Idea {i + 1}/{num_ideas}")
            print("🎤 Recording...")

            audio_file = await self.voice_skills.record_audio(
                duration=30,
                stop_on_silence=True
            )

            print("💾 Saving...")
            result = await self.capture_idea(audio_file, auto_categorize=True)

            results.append(result)
            print(f"✅ Saved: {result.get('category', 'unknown')} - {result.get('idea', '')[:50]}...")

            # Brief pause between ideas
            await asyncio.sleep(2)

        return results

    async def review_recent_ideas(self, days: int = 7) -> Dict:
        """
        Review ideas from the past N days.

        Returns transcription of recent ideas via voice.
        """
        logger.info(f"Reviewing ideas from past {days} days")

        # This would fetch and read out recent ideas
        # Simplified implementation
        summary = f"Here are your ideas from the past {days} days"

        await self.voice_skills.synthesize_speech(summary)

        return {
            "days": days,
            "summary": summary
        }

    async def search_ideas(self, query: str) -> List[Dict]:
        """
        Search through saved ideas.

        Args:
            query: Search query

        Returns:
            Matching ideas
        """
        logger.info(f"Searching ideas: {query}")

        # This would search Google Docs or local files
        # Simplified implementation
        return []


# CLI interface
async def ideas_cli():
    """
    CLI for ideas capture agent.

    Usage:
        python -m agency.agents.voice.ideas_capture.ideas_capture_agent
    """
    agent = IdeasCaptureAgent()

    print("💡 Ideas Capture Agent")
    print("=" * 50)
    print("Commands:")
    print("  1 - Quick capture (single idea)")
    print("  2 - Batch capture (5 ideas)")
    print("  3 - Set target (Google Docs / Apple Notes)")
    print("  q - Quit")
    print("=" * 50)

    while True:
        choice = input("\n> ").strip()

        if choice == "1":
            print("\n💡 Quick capture mode")
            result = await agent.quick_capture(duration=30)

            if "error" not in result:
                print(f"\n✅ Idea saved!")
                print(f"   Category: {result['category']}")
                print(f"   Saved to: {result['saved_to']}")
                print(f"   Idea: {result['idea'][:100]}...")
            else:
                print(f"\n❌ Error: {result['error']}")

        elif choice == "2":
            print("\n💡 Batch capture mode (5 ideas)")
            results = await agent.batch_capture(num_ideas=5)
            print(f"\n✅ Captured {len(results)} ideas!")

        elif choice == "3":
            print("\nSelect target:")
            print("  1 - Google Docs")
            print("  2 - Apple Notes")
            print("  3 - Local files")

            target_choice = input("> ").strip()

            if target_choice == "1":
                agent.default_target = "google_docs"
                print("✅ Set to Google Docs")
            elif target_choice == "2":
                agent.default_target = "apple_notes"
                print("✅ Set to Apple Notes")
            elif target_choice == "3":
                agent.default_target = "local"
                print("✅ Set to local files")

        elif choice.lower() == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    from pathlib import Path
    asyncio.run(ideas_cli())
