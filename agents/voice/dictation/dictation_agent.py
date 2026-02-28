"""
Dictation Agent - Audio Understanding and Transcription

Replaces typing by transcribing voice to text for any chat interface.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from pathlib import Path

from integrations.voice_core.voice_skills import VoiceSkills

logger = logging.getLogger(__name__)


class DictationAgent:
    """
    Agent that transcribes voice to text for seamless dictation.

    Features:
    - Real-time audio transcription
    - Punctuation and formatting
    - Multi-language support
    - Integration with chat interfaces (Claude, ChatGPT, etc.)
    - Continuous dictation mode
    - Voice commands for editing
    """

    def __init__(self):
        """Initialize dictation agent."""
        self.voice_skills = VoiceSkills()
        self.is_listening = False
        self.dictation_buffer = []
        self.language = "en"

        logger.info("Dictation Agent initialized")

    async def start_dictation(
        self,
        target: str = "clipboard",
        language: str = "en",
        continuous: bool = False
    ) -> Dict:
        """
        Start dictation mode.

        Args:
            target: Where to send transcribed text (clipboard, file, direct)
            language: Language code (en, es, fr, etc.)
            continuous: Enable continuous dictation

        Returns:
            {
                "status": "listening",
                "target": "clipboard",
                "language": "en"
            }
        """
        self.is_listening = True
        self.language = language
        self.dictation_buffer = []

        logger.info(f"Dictation started: target={target}, language={language}, continuous={continuous}")

        return {
            "status": "listening",
            "target": target,
            "language": language,
            "continuous": continuous
        }

    async def stop_dictation(self) -> Dict:
        """
        Stop dictation mode.

        Returns:
            {
                "status": "stopped",
                "total_transcribed": 150,
                "buffer": "transcribed text..."
            }
        """
        self.is_listening = False
        full_text = " ".join(self.dictation_buffer)

        result = {
            "status": "stopped",
            "total_transcribed": len(full_text),
            "buffer": full_text
        }

        logger.info(f"Dictation stopped: transcribed {len(full_text)} characters")
        return result

    async def dictate_to_claude(self, audio_file: str) -> Dict:
        """
        Transcribe audio and format for Claude chat.

        Args:
            audio_file: Path to audio recording

        Returns:
            {
                "transcription": "Hey Claude, can you help me...",
                "ready_to_send": true,
                "chat_interface": "claude"
            }
        """
        # Transcribe audio
        result = await self.voice_skills.transcribe_audio(
            audio_file,
            language=self.language,
            prompt="User dictating a message to Claude AI assistant."
        )

        if "error" in result:
            return result

        transcription = result["text"]

        # Format for chat
        formatted = self._format_for_chat(transcription)

        return {
            "transcription": formatted,
            "ready_to_send": True,
            "chat_interface": "claude",
            "confidence": result.get("confidence", 0.95)
        }

    async def dictate_to_chatgpt(self, audio_file: str) -> Dict:
        """
        Transcribe audio and format for ChatGPT.

        Similar to dictate_to_claude but with ChatGPT-specific formatting.
        """
        result = await self.voice_skills.transcribe_audio(
            audio_file,
            language=self.language,
            prompt="User dictating a message to ChatGPT."
        )

        if "error" in result:
            return result

        transcription = result["text"]
        formatted = self._format_for_chat(transcription)

        return {
            "transcription": formatted,
            "ready_to_send": True,
            "chat_interface": "chatgpt",
            "confidence": result.get("confidence", 0.95)
        }

    async def dictate_to_any_chatbot(
        self,
        audio_file: str,
        chatbot_name: str = "AI Assistant"
    ) -> Dict:
        """
        Universal dictation for any chatbot.

        Args:
            audio_file: Path to audio recording
            chatbot_name: Name of the chatbot

        Returns:
            {
                "transcription": "formatted text",
                "ready_to_send": true,
                "chat_interface": "custom"
            }
        """
        result = await self.voice_skills.transcribe_audio(
            audio_file,
            language=self.language,
            prompt=f"User dictating a message to {chatbot_name}."
        )

        if "error" in result:
            return result

        transcription = result["text"]
        formatted = self._format_for_chat(transcription)

        return {
            "transcription": formatted,
            "ready_to_send": True,
            "chat_interface": chatbot_name,
            "confidence": result.get("confidence", 0.95)
        }

    async def continuous_dictation(
        self,
        output_callback=None,
        stop_on_silence_duration: int = 3
    ):
        """
        Continuous dictation mode - keeps listening and transcribing.

        Args:
            output_callback: Function to call with each transcription
            stop_on_silence_duration: Seconds of silence before stopping

        Yields:
            Transcribed text segments
        """
        logger.info("Starting continuous dictation mode")

        while self.is_listening:
            try:
                # Record audio segment
                audio_file = await self.voice_skills.record_audio(
                    duration=None,
                    stop_on_silence=True
                )

                # Transcribe
                result = await self.voice_skills.transcribe_audio(
                    audio_file,
                    language=self.language
                )

                if "text" in result:
                    text = result["text"]
                    self.dictation_buffer.append(text)

                    if output_callback:
                        await output_callback(text)

                    yield text

            except Exception as e:
                logger.error(f"Continuous dictation error: {e}")
                break

    async def transcribe_and_copy_to_clipboard(self, audio_file: str) -> Dict:
        """
        Transcribe audio and copy to clipboard.

        Args:
            audio_file: Path to audio recording

        Returns:
            {
                "transcription": "text",
                "copied_to_clipboard": true
            }
        """
        result = await self.voice_skills.transcribe_audio(
            audio_file,
            language=self.language
        )

        if "error" in result:
            return result

        transcription = result["text"]

        # Copy to clipboard (using pyperclip or similar)
        try:
            import pyperclip
            pyperclip.copy(transcription)
            copied = True
        except Exception as e:
            logger.warning(f"Could not copy to clipboard: {e}")
            copied = False

        return {
            "transcription": transcription,
            "copied_to_clipboard": copied,
            "length": len(transcription)
        }

    def _format_for_chat(self, text: str) -> str:
        """
        Format transcribed text for chat interface.

        - Capitalize first letter
        - Add proper punctuation
        - Remove filler words
        - Format paragraphs
        """
        # Basic formatting
        text = text.strip()

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        # Remove common filler words
        fillers = ["um", "uh", "like", "you know"]
        for filler in fillers:
            text = text.replace(f" {filler} ", " ")
            text = text.replace(f" {filler},", ",")

        return text

    async def voice_command_handler(self, audio_file: str) -> Dict:
        """
        Handle voice commands for editing dictation.

        Commands:
        - "new line" - insert line break
        - "delete that" - delete last sentence
        - "caps on/off" - toggle capitalization
        - "send message" - send to chat
        """
        result = await self.voice_skills.transcribe_audio(audio_file)

        if "error" in result:
            return result

        command = result["text"].lower().strip()

        # Process commands
        if "new line" in command or "new paragraph" in command:
            self.dictation_buffer.append("\n")
            return {"action": "newline", "status": "executed"}

        elif "delete that" in command or "scratch that" in command:
            if self.dictation_buffer:
                deleted = self.dictation_buffer.pop()
                return {"action": "delete", "deleted": deleted, "status": "executed"}

        elif "send message" in command or "send it" in command:
            full_text = " ".join(self.dictation_buffer)
            return {
                "action": "send",
                "message": full_text,
                "status": "ready_to_send"
            }

        else:
            # Not a command, treat as regular dictation
            self.dictation_buffer.append(command)
            return {
                "action": "dictation",
                "text": command,
                "status": "added_to_buffer"
            }


# CLI integration
async def dictate_cli(
    duration: int = 10,
    target: str = "claude",
    output_file: Optional[str] = None
):
    """
    CLI tool for quick dictation.

    Usage:
        python -m agency.agents.voice.dictation.dictation_agent --duration 10 --target claude

    Args:
        duration: Recording duration in seconds
        target: Target chatbot (claude, chatgpt, clipboard)
        output_file: Optional file to save transcription
    """
    agent = DictationAgent()

    # Record audio
    print(f"🎤 Recording for {duration} seconds...")
    skills = VoiceSkills()
    audio_file = await skills.record_audio(duration=duration)

    # Transcribe
    print("📝 Transcribing...")
    if target == "claude":
        result = await agent.dictate_to_claude(audio_file)
    elif target == "chatgpt":
        result = await agent.dictate_to_chatgpt(audio_file)
    elif target == "clipboard":
        result = await agent.transcribe_and_copy_to_clipboard(audio_file)
    else:
        result = await agent.dictate_to_any_chatbot(audio_file, target)

    # Output
    if "transcription" in result:
        print(f"\n✅ Transcription:\n{result['transcription']}\n")

        if output_file:
            with open(output_file, "w") as f:
                f.write(result["transcription"])
            print(f"💾 Saved to {output_file}")

        if result.get("copied_to_clipboard"):
            print("📋 Copied to clipboard!")

        if result.get("ready_to_send"):
            print(f"✉️  Ready to send to {result['chat_interface']}")

    return result


if __name__ == "__main__":
    import sys

    # Simple CLI
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    target = sys.argv[2] if len(sys.argv) > 2 else "claude"

    asyncio.run(dictate_cli(duration=duration, target=target))
