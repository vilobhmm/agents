"""Proactive Meeting Prep Agent"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.slack import SlackIntegration
from openclaw.integrations.telegram import TelegramIntegration
from openclaw.tools.summarization import Summarizer


logger = logging.getLogger(__name__)


class MeetingPrepAgent(Agent):
    """Proactive Meeting Prep Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Meeting Prep Assistant",
            description="I scan your calendar, gather context, and prepare briefings for meetings.",
            proactive=True,
        )

        super().__init__(config, api_key)

        # Initialize integrations
        self.calendar = CalendarIntegration()
        self.email = EmailIntegration()
        self.slack = SlackIntegration()
        self.telegram = TelegramIntegration()
        self.summarizer = Summarizer(api_key)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Scanning calendar for upcoming meetings")

        # Get meetings in next 24 hours
        upcoming_events = await self.calendar.get_upcoming_events(hours=24)

        if not upcoming_events:
            logger.info("No upcoming meetings")
            return {"status": "no_meetings"}

        # Prepare briefings for each meeting
        briefings = []
        for event in upcoming_events:
            briefing = await self.prepare_meeting_briefing(event)
            if briefing:
                briefings.append(briefing)

        # Send morning summary
        if briefings:
            await self.send_daily_summary(briefings)

        return {"status": "success", "meetings_prepared": len(briefings)}

    async def prepare_meeting_briefing(self, event: Dict) -> Dict:
        """Prepare briefing for a single meeting"""
        summary = event.get("summary", "Untitled Meeting")
        description = event.get("description", "")
        attendees = event.get("attendees", [])
        start_time = event.get("start", {}).get("dateTime", "")

        logger.info(f"Preparing briefing for: {summary}")

        # Extract attendee emails
        attendee_emails = [a.get("email") for a in attendees if a.get("email")]

        # Search for related emails
        related_emails = await self.find_related_emails(summary, attendee_emails)

        # Search for related Slack messages
        related_slack = await self.find_related_slack_messages(summary)

        # Generate context summary
        context = await self.generate_context_summary(
            summary, description, related_emails, related_slack
        )

        # Suggest agenda items
        agenda = await self.suggest_agenda(summary, context)

        return {
            "title": summary,
            "time": start_time,
            "attendees": attendee_emails,
            "context": context,
            "agenda": agenda,
            "related_emails": len(related_emails),
            "related_slack": len(related_slack),
        }

    async def find_related_emails(
        self, meeting_title: str, attendees: List[str]
    ) -> List[Dict]:
        """Find emails related to the meeting"""
        related_emails = []

        # Search for emails from attendees
        for attendee in attendees[:5]:  # Limit to avoid rate limits
            emails = await self.email.search_emails(
                sender=attendee, max_results=5
            )
            related_emails.extend(emails)

        # Search for emails mentioning meeting topic
        topic_emails = await self.email.search_emails(
            subject=meeting_title, max_results=10
        )
        related_emails.extend(topic_emails)

        return related_emails[:20]  # Limit total

    async def find_related_slack_messages(self, meeting_title: str) -> List[Dict]:
        """Find Slack messages related to the meeting"""
        try:
            messages = await self.slack.search_messages(meeting_title, count=10)
            return messages
        except Exception as e:
            logger.warning(f"Could not search Slack: {e}")
            return []

    async def generate_context_summary(
        self,
        title: str,
        description: str,
        emails: List[Dict],
        slack_messages: List[Dict],
    ) -> str:
        """Generate context summary using Claude"""

        # Prepare context
        email_context = "\n".join(
            [
                f"- From {e.get('from', 'Unknown')}: {e.get('subject', 'No subject')} - {e.get('snippet', '')}"
                for e in emails[:10]
            ]
        )

        slack_context = "\n".join(
            [f"- {m.get('text', '')[:200]}" for m in slack_messages[:10]]
        )

        prompt = f"""Prepare a context summary for this meeting:

**Meeting:** {title}
**Description:** {description}

**Related Emails:**
{email_context if email_context else "None found"}

**Related Slack Messages:**
{slack_context if slack_context else "None found"}

Provide a concise summary of the key context and background information."""

        summary = await self.chat(prompt)
        return summary

    async def suggest_agenda(self, title: str, context: str) -> List[str]:
        """Suggest agenda items using Claude"""

        prompt = f"""Based on this meeting context, suggest 3-5 specific agenda items:

**Meeting:** {title}
**Context:** {context}

Return only the agenda items as a numbered list."""

        response = await self.chat(prompt)

        # Parse agenda items
        lines = response.strip().split("\n")
        agenda_items = [
            line.strip("0123456789. ").strip()
            for line in lines
            if line.strip() and any(c.isalpha() for c in line)
        ]

        return agenda_items[:5]

    async def send_daily_summary(self, briefings: List[Dict]):
        """Send daily meeting prep summary"""

        # Format summary
        summary_text = "Good morning! Here are your meetings for today:\n\n"

        for i, briefing in enumerate(briefings, 1):
            summary_text += f"{i}. *{briefing['title']}*\n"
            summary_text += f"   Time: {briefing['time']}\n"
            summary_text += f"   Attendees: {len(briefing['attendees'])} people\n"
            summary_text += f"\n   Context:\n   {briefing['context'][:300]}...\n"

            if briefing.get("agenda"):
                summary_text += f"\n   Suggested Agenda:\n"
                for item in briefing["agenda"]:
                    summary_text += f"   - {item}\n"

            summary_text += "\n"

        # Send via Telegram
        await self.telegram.send_message(summary_text)
        logger.info("Sent daily meeting summary")
