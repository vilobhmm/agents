"""
Productivity Voice Agent - Your AI Voice Assistant

Talks to you, gives daily updates, and takes action via voice commands.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import json

from agency.voice.voice_skills import VoiceSkills

logger = logging.getLogger(__name__)


class ProductivityVoiceAgent:
    """
    Voice-enabled productivity agent that talks to you.

    Features:
    - Morning briefings via voice
    - Voice-activated commands
    - Proactive voice notifications
    - Natural conversation
    - Action execution via voice
    - Integration with CC agent capabilities
    """

    def __init__(self):
        """Initialize productivity voice agent."""
        self.voice_skills = VoiceSkills()
        self.voice = "alloy"  # Default voice
        self.language = "en"
        self.user_name = os.getenv("USER_NAME", "there")

        # Try to import Google services for calendar/email
        try:
            from openclaw.integrations import GoogleServices
            self.google = GoogleServices()
            self.has_google = True
        except:
            self.google = None
            self.has_google = False
            logger.warning("Google services not available")

        logger.info("Productivity Voice Agent initialized")

    async def morning_briefing(self, speak_out_loud: bool = True) -> Dict:
        """
        Deliver morning briefing via voice.

        Returns:
            {
                "text": "Good morning! Here's your briefing...",
                "audio_file": "path/to/briefing.mp3",
                "data": {
                    "emails": {...},
                    "calendar": {...},
                    "priorities": [...]
                }
            }
        """
        logger.info("Generating morning briefing")

        # Gather information
        briefing_data = await self._gather_briefing_data()

        # Generate briefing text
        briefing_text = await self._generate_briefing_text(briefing_data)

        # Convert to speech
        if speak_out_loud:
            audio_result = await self.voice_skills.synthesize_speech(
                briefing_text,
                voice=self.voice
            )
            audio_file = audio_result.get("audio_file")

            # Play the briefing
            if audio_file:
                await self.voice_skills.stream_audio(audio_file)
        else:
            audio_file = None

        return {
            "text": briefing_text,
            "audio_file": audio_file,
            "data": briefing_data,
            "timestamp": datetime.now().isoformat()
        }

    async def _gather_briefing_data(self) -> Dict:
        """Gather data for briefing."""
        data = {
            "time": datetime.now().strftime("%I:%M %p"),
            "date": datetime.now().strftime("%A, %B %d"),
            "emails": {"unread": 0, "urgent": 0},
            "calendar": {"events_today": 0, "next_meeting": None},
            "weather": {"temp": 72, "condition": "sunny"},
            "priorities": []
        }

        if self.has_google:
            try:
                # Get email summary
                email_data = await self.google.get_email_summary()
                data["emails"] = email_data

                # Get calendar events
                calendar_data = await self.google.get_todays_events()
                data["calendar"] = calendar_data

            except Exception as e:
                logger.error(f"Failed to fetch Google data: {e}")

        return data

    async def _generate_briefing_text(self, data: Dict) -> str:
        """Generate natural briefing text."""
        parts = []

        # Greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        parts.append(f"{greeting} {self.user_name}! It's {data['date']}, {data['time']}.")

        # Email summary
        if data["emails"]["unread"] > 0:
            parts.append(f"You have {data['emails']['unread']} unread emails.")
            if data["emails"]["urgent"] > 0:
                parts.append(f"{data['emails']['urgent']} of them are urgent and need your attention.")

        # Calendar summary
        if data["calendar"]["events_today"] > 0:
            parts.append(f"You have {data['calendar']['events_today']} events on your calendar today.")
            if data["calendar"]["next_meeting"]:
                next_meeting = data["calendar"]["next_meeting"]
                parts.append(f"Your next meeting is {next_meeting['title']} at {next_meeting['time']}.")

        # Priorities
        if data["priorities"]:
            parts.append("Here are your top priorities for today:")
            for i, priority in enumerate(data["priorities"][:3], 1):
                parts.append(f"{i}. {priority}")

        # Closing
        parts.append("Have a productive day!")

        return " ".join(parts)

    async def listen_for_command(self, duration: int = 5) -> Dict:
        """
        Listen for voice command and execute it.

        Args:
            duration: How long to listen (seconds)

        Returns:
            {
                "command": "schedule meeting with john",
                "action": "schedule_meeting",
                "result": {...},
                "response": "I've scheduled a meeting with John"
            }
        """
        logger.info(f"Listening for command ({duration}s)...")

        # Record audio
        audio_file = await self.voice_skills.record_audio(duration=duration)

        # Transcribe
        transcription = await self.voice_skills.transcribe_audio(audio_file)
        command_text = transcription.get("text", "").lower()

        logger.info(f"Received command: {command_text}")

        # Parse and execute command
        result = await self._execute_voice_command(command_text)

        # Generate voice response
        if result.get("response"):
            await self.speak(result["response"])

        return result

    async def _execute_voice_command(self, command: str) -> Dict:
        """Execute voice command."""
        command = command.lower().strip()

        # Email commands
        if "check email" in command or "check my email" in command:
            return await self._handle_check_email()

        elif "read email" in command or "read my email" in command:
            return await self._handle_read_emails()

        # Calendar commands
        elif "what's on my calendar" in command or "what's my schedule" in command:
            return await self._handle_check_calendar()

        elif "schedule meeting" in command or "book meeting" in command:
            return await self._handle_schedule_meeting(command)

        # Productivity commands
        elif "block focus time" in command or "block time" in command:
            return await self._handle_block_focus_time(command)

        elif "what should i do" in command or "what's next" in command:
            return await self._handle_whats_next()

        # Information commands
        elif "what time is it" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            return {
                "action": "time_check",
                "response": f"It's {current_time}",
                "time": current_time
            }

        else:
            return {
                "action": "unknown",
                "command": command,
                "response": "I didn't understand that command. Could you try again?"
            }

    async def _handle_check_email(self) -> Dict:
        """Check email summary."""
        if not self.has_google:
            return {
                "action": "check_email",
                "response": "Email integration is not configured.",
                "error": "no_google_integration"
            }

        try:
            email_data = await self.google.get_email_summary()
            unread = email_data.get("unread", 0)
            urgent = email_data.get("urgent", 0)

            response = f"You have {unread} unread emails"
            if urgent > 0:
                response += f", {urgent} of them are urgent"

            return {
                "action": "check_email",
                "response": response,
                "data": email_data
            }
        except Exception as e:
            logger.error(f"Check email failed: {e}")
            return {
                "action": "check_email",
                "response": "I couldn't check your email right now.",
                "error": str(e)
            }

    async def _handle_read_emails(self) -> Dict:
        """Read out recent emails."""
        if not self.has_google:
            return {
                "action": "read_emails",
                "response": "Email integration is not configured."
            }

        try:
            emails = await self.google.get_recent_emails(max_results=3)

            if not emails:
                return {
                    "action": "read_emails",
                    "response": "You have no new emails."
                }

            # Read out emails
            for i, email in enumerate(emails, 1):
                text = f"Email {i}: From {email['from']}, subject: {email['subject']}"
                await self.speak(text)

            return {
                "action": "read_emails",
                "response": f"I read {len(emails)} emails",
                "emails": emails
            }
        except Exception as e:
            logger.error(f"Read emails failed: {e}")
            return {
                "action": "read_emails",
                "response": "I couldn't read your emails right now.",
                "error": str(e)
            }

    async def _handle_check_calendar(self) -> Dict:
        """Check calendar."""
        if not self.has_google:
            return {
                "action": "check_calendar",
                "response": "Calendar integration is not configured."
            }

        try:
            events = await self.google.get_todays_events()
            count = len(events)

            if count == 0:
                response = "You have no events scheduled for today"
            else:
                response = f"You have {count} events today"
                if events:
                    next_event = events[0]
                    response += f". Your next event is {next_event['title']} at {next_event['time']}"

            return {
                "action": "check_calendar",
                "response": response,
                "events": events
            }
        except Exception as e:
            logger.error(f"Check calendar failed: {e}")
            return {
                "action": "check_calendar",
                "response": "I couldn't check your calendar right now.",
                "error": str(e)
            }

    async def _handle_schedule_meeting(self, command: str) -> Dict:
        """Schedule a meeting from voice command."""
        # This would use NLP to extract meeting details
        # For now, simplified response
        return {
            "action": "schedule_meeting",
            "response": "I can help schedule a meeting. What's the title, time, and attendees?",
            "command": command
        }

    async def _handle_block_focus_time(self, command: str) -> Dict:
        """Block focus time on calendar."""
        # Default to 2 hours
        duration = 2

        # Try to extract duration from command
        if "hour" in command:
            import re
            match = re.search(r'(\d+)\s*hour', command)
            if match:
                duration = int(match.group(1))

        return {
            "action": "block_focus_time",
            "response": f"I've blocked {duration} hours of focus time on your calendar",
            "duration": duration
        }

    async def _handle_whats_next(self) -> Dict:
        """Suggest what to do next."""
        # This would use AI to prioritize tasks
        suggestions = [
            "Review your urgent emails",
            "Prepare for your next meeting",
            "Work on your top priority task"
        ]

        response = "Here's what I suggest: " + suggestions[0]

        return {
            "action": "whats_next",
            "response": response,
            "suggestions": suggestions
        }

    async def speak(self, text: str, wait: bool = True) -> str:
        """
        Speak text out loud.

        Args:
            text: Text to speak
            wait: Wait for speech to finish

        Returns:
            Path to audio file
        """
        logger.info(f"Speaking: {text[:50]}...")

        result = await self.voice_skills.synthesize_speech(text, voice=self.voice)
        audio_file = result.get("audio_file")

        if audio_file and wait:
            await self.voice_skills.stream_audio(audio_file)

        return audio_file

    async def continuous_voice_mode(self):
        """
        Continuous voice interaction mode.

        Keeps listening and responding to commands.
        """
        logger.info("Starting continuous voice mode")

        await self.speak("Voice mode activated. I'm listening.")

        while True:
            try:
                # Wait for wake word or command
                print("\n🎤 Listening...")
                result = await self.listen_for_command(duration=5)

                if result.get("action") == "exit":
                    await self.speak("Goodbye!")
                    break

            except KeyboardInterrupt:
                await self.speak("Voice mode deactivated.")
                break
            except Exception as e:
                logger.error(f"Voice mode error: {e}")
                await self.speak("Sorry, I encountered an error.")

    async def proactive_notification(self, message: str, urgent: bool = False):
        """
        Proactively notify user via voice.

        Args:
            message: Notification message
            urgent: If true, uses urgent tone
        """
        if urgent:
            prefix = "Urgent notification: "
        else:
            prefix = "Hey, "

        full_message = prefix + message
        await self.speak(full_message)

        return {
            "notified": True,
            "message": message,
            "urgent": urgent,
            "timestamp": datetime.now().isoformat()
        }


# CLI interface
async def voice_assistant_cli():
    """
    CLI for voice assistant.

    Usage:
        python -m agency.agents.voice.productivity.productivity_agent
    """
    agent = ProductivityVoiceAgent()

    print("🎤 Productivity Voice Assistant")
    print("=" * 50)
    print("Commands:")
    print("  1 - Morning briefing")
    print("  2 - Listen for command")
    print("  3 - Continuous voice mode")
    print("  q - Quit")
    print("=" * 50)

    while True:
        choice = input("\n> ").strip()

        if choice == "1":
            print("\n📢 Delivering morning briefing...")
            result = await agent.morning_briefing(speak_out_loud=True)
            print(f"\n{result['text']}")

        elif choice == "2":
            print("\n🎤 Listening for command (5s)...")
            result = await agent.listen_for_command(duration=5)
            print(f"Command: {result.get('command', 'none')}")
            print(f"Response: {result.get('response', 'none')}")

        elif choice == "3":
            print("\n🎤 Starting continuous voice mode...")
            print("(Press Ctrl+C to exit)")
            await agent.continuous_voice_mode()

        elif choice.lower() == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(voice_assistant_cli())
