"""Email Triaging & Auto-Response System Agent"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration


logger = logging.getLogger(__name__)


class EmailTriageAgent(Agent):
    """Email Triaging & Auto-Response Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Email Triage Assistant",
            description="I categorize emails, draft responses, and manage follow-ups.",
            proactive=True,
        )

        super().__init__(config, api_key)

        self.email = EmailIntegration()
        self.whatsapp = WhatsAppIntegration()

        # Track pending responses
        self.waiting_for_response = {}

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Triaging emails")

        # Get unread emails
        emails = await self.email.get_messages(max_results=50, unread_only=True)

        if not emails:
            logger.info("No unread emails")
            return {"status": "no_emails"}

        # Process each email
        categorized = {
            "urgent": [],
            "action_needed": [],
            "fyi": [],
            "archive": [],
        }

        drafted_responses = []

        for email_data in emails:
            category = await self.categorize_email(email_data)
            categorized[category].append(email_data)

            # Draft response if needed
            if category == "action_needed":
                draft = await self.draft_response(email_data)
                if draft:
                    drafted_responses.append(
                        {
                            "email_id": email_data.get("id"),
                            "subject": email_data.get("subject"),
                            "draft": draft,
                        }
                    )

        # Send urgent notifications
        if categorized["urgent"]:
            await self.notify_urgent(categorized["urgent"])

        # Check for follow-ups needed
        await self.check_followups()

        return {
            "status": "success",
            "urgent": len(categorized["urgent"]),
            "action_needed": len(categorized["action_needed"]),
            "fyi": len(categorized["fyi"]),
            "archive": len(categorized["archive"]),
            "drafts": len(drafted_responses),
        }

    async def categorize_email(self, email_data: Dict) -> str:
        """Categorize an email"""

        subject = email_data.get("subject", "")
        sender = email_data.get("from", "")
        body = email_data.get("body", "")[:1000]

        prompt = f"""Categorize this email:

From: {sender}
Subject: {subject}
Body: {body}

Choose ONE category:
- urgent: Requires immediate attention (deadlines, emergencies, boss emails)
- action_needed: Requires a response or action within 24-48 hours
- fyi: Informational, no action needed
- archive: Newsletters, notifications, can be archived

Return ONLY the category name."""

        response = await self.chat(prompt)

        category = response.strip().lower()

        # Validate category
        if category not in ["urgent", "action_needed", "fyi", "archive"]:
            category = "fyi"

        logger.info(f"Categorized '{subject}' as: {category}")

        return category

    async def draft_response(self, email_data: Dict) -> Optional[str]:
        """Draft a response to an email"""

        subject = email_data.get("subject", "")
        sender = email_data.get("from", "")
        body = email_data.get("body", "")

        prompt = f"""Draft a professional response to this email:

From: {sender}
Subject: {subject}
Body: {body}

The response should:
- Be professional and concise
- Address the key points
- Be ready to send (but mark it as a draft for review)

If this is not a type of email that needs a response (spam, newsletter, etc.), respond with "NO_RESPONSE_NEEDED"."""

        draft = await self.chat(prompt)

        if "NO_RESPONSE_NEEDED" in draft:
            return None

        logger.info(f"Drafted response for: {subject}")

        return draft

    async def notify_urgent(self, urgent_emails: List[Dict]):
        """Send notification about urgent emails"""

        message = "⚠️ Urgent Emails:\n\n"

        for email in urgent_emails[:5]:
            message += f"From: {email.get('from', 'Unknown')}\n"
            message += f"Subject: {email.get('subject', 'No subject')}\n"
            message += f"Preview: {email.get('snippet', '')[:100]}...\n\n"

        await self.whatsapp.send_message(
            os.getenv("WHATSAPP_RECIPIENT"), message
        )

        logger.info(f"Sent urgent email notification for {len(urgent_emails)} emails")

    async def check_followups(self):
        """Check for emails needing follow-up"""

        # Check waiting_for_response tracker
        now = datetime.now()
        followups_needed = []

        for email_id, data in list(self.waiting_for_response.items()):
            sent_date = data.get("sent_date")
            days_waiting = (now - sent_date).days

            if days_waiting >= 3:  # Follow up after 3 days
                followups_needed.append(data)
                del self.waiting_for_response[email_id]

        # Send follow-up reminders
        for followup in followups_needed:
            await self.send_followup_reminder(followup)

    async def send_followup_reminder(self, followup_data: Dict):
        """Send a follow-up reminder"""

        subject = followup_data.get("subject", "")
        recipient = followup_data.get("recipient", "")

        prompt = f"""Draft a gentle follow-up email:

Original subject: {subject}
Sent to: {recipient}
Days since sent: {(datetime.now() - followup_data.get('sent_date')).days}

The follow-up should:
- Be polite and professional
- Reference the original email
- Gently inquire about status"""

        followup_draft = await self.chat(prompt)

        # In production, you might want to auto-send or queue for approval
        logger.info(f"Generated follow-up for: {subject}")

        await self.whatsapp.send_message(
            os.getenv("WHATSAPP_RECIPIENT"),
            f"Follow-up needed for: {subject}\n\nDraft:\n{followup_draft}",
        )

    def track_sent_email(self, email_id: str, recipient: str, subject: str):
        """Track sent email for follow-up"""

        self.waiting_for_response[email_id] = {
            "recipient": recipient,
            "subject": subject,
            "sent_date": datetime.now(),
        }
