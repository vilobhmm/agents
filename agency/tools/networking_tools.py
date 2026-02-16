"""
Professional Networking Tools - Manage outreach, referrals, and follow-ups.

Provides tools for networker agent to:
- Track contacts (recruiters, referrers, friends, family)
- Generate personalized outreach messages
- Schedule follow-ups
- Track conversation history
- Send thank you messages
- Manage referral requests
"""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class NetworkingTools:
    """
    Professional networking and relationship management toolkit.

    Features:
    - Contact database management
    - Outreach message generation
    - Follow-up scheduling and reminders
    - Conversation history tracking
    - Referral management
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize networking tools"""
        self.storage_path = Path(storage_path or os.path.expanduser("~/.agency/networking"))
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.contacts_file = self.storage_path / "contacts.json"
        self.interactions_file = self.storage_path / "interactions.json"
        self.follow_ups_file = self.storage_path / "follow_ups.json"

        logger.info("✅ Networking Tools initialized")

    # ===== Contact Management =====

    async def add_contact(
        self,
        name: str,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        company: Optional[str] = None,
        role: Optional[str] = None,
        contact_type: str = "professional",
        relationship: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Add a contact to the network database.

        Args:
            name: Contact's name
            email: Email address
            linkedin_url: LinkedIn profile URL
            company: Current company
            role: Job title/role
            contact_type: Type (recruiter, referrer, friend, family, colleague)
            relationship: Description of relationship
            notes: Additional notes

        Returns:
            Success boolean
        """
        try:
            contacts = self._load_json(self.contacts_file, [])

            # Check if contact already exists
            existing = [c for c in contacts if c.get("name") == name and c.get("email") == email]
            if existing:
                logger.info(f"Contact {name} already exists")
                return True

            contact = {
                "id": self._generate_id(name),
                "name": name,
                "email": email,
                "linkedin_url": linkedin_url,
                "company": company,
                "role": role,
                "contact_type": contact_type,
                "relationship": relationship,
                "notes": notes,
                "added_date": datetime.now().isoformat(),
                "last_contact": None,
            }

            contacts.append(contact)
            self._save_json(self.contacts_file, contacts)

            logger.info(f"✅ Added contact: {name} ({contact_type})")
            return True

        except Exception as e:
            logger.error(f"❌ Error adding contact: {e}")
            return False

    async def get_contacts(
        self,
        contact_type: Optional[str] = None,
        company: Optional[str] = None
    ) -> List[Dict]:
        """
        Get contacts from database.

        Args:
            contact_type: Filter by type (recruiter, referrer, etc.)
            company: Filter by company

        Returns:
            List of contacts
        """
        contacts = self._load_json(self.contacts_file, [])

        if contact_type:
            contacts = [c for c in contacts if c.get("contact_type") == contact_type]

        if company:
            contacts = [c for c in contacts if c.get("company", "").lower() == company.lower()]

        return contacts

    async def update_last_contact(self, contact_id: str) -> bool:
        """Update last contact date"""
        try:
            contacts = self._load_json(self.contacts_file, [])

            for contact in contacts:
                if contact.get("id") == contact_id:
                    contact["last_contact"] = datetime.now().isoformat()
                    break

            self._save_json(self.contacts_file, contacts)
            return True

        except Exception as e:
            logger.error(f"Error updating contact: {e}")
            return False

    # ===== Message Generation =====

    def generate_outreach_message(
        self,
        contact_name: str,
        contact_type: str,
        purpose: str,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        tone: str = "professional"
    ) -> str:
        """
        Generate personalized outreach message.

        Args:
            contact_name: Recipient's name
            contact_type: Type (recruiter, referrer, etc.)
            purpose: Purpose (referral_request, follow_up, thank_you, introduction)
            job_title: Job title (for job-related outreach)
            company: Company name
            tone: Message tone (professional, casual, warm)

        Returns:
            Generated message template
        """
        logger.info(f"✍️  Generating {purpose} message for {contact_name}")

        messages = {
            "referral_request": self._template_referral_request,
            "follow_up": self._template_follow_up,
            "thank_you": self._template_thank_you,
            "introduction": self._template_introduction,
            "recruiter_outreach": self._template_recruiter_outreach,
        }

        template_func = messages.get(purpose)

        if not template_func:
            logger.warning(f"Unknown purpose: {purpose}")
            return ""

        return template_func(contact_name, contact_type, job_title, company, tone)

    def _template_referral_request(
        self,
        name: str,
        contact_type: str,
        job_title: Optional[str],
        company: Optional[str],
        tone: str
    ) -> str:
        """Generate referral request message"""

        if tone == "casual" and contact_type in ["friend", "family"]:
            return f"""Hi {name}!

Hope you're doing well! I wanted to reach out because I'm currently exploring new opportunities and came across a {job_title} role at {company}.

I remember you mentioned working with/knowing people at {company}. Would you be comfortable providing a referral or introduction? I'd really appreciate any support you can offer!

I'm happy to send over my resume and can share more details about why I'm excited about this role.

Thanks so much for considering!

Best,
[Your name]"""

        else:  # Professional tone
            return f"""Hi {name},

I hope this message finds you well. I'm reaching out because I recently came across a {job_title} position at {company} that aligns well with my background and interests.

I understand you may have connections at {company}, and I would greatly appreciate if you could provide a referral or introduce me to someone on the hiring team. I believe my experience in [mention relevant experience] makes me a strong fit for this role.

I'm happy to provide my resume and discuss how my background aligns with the position.

Thank you for considering, and I appreciate any assistance you can provide.

Best regards,
[Your name]"""

    def _template_thank_you(
        self,
        name: str,
        contact_type: str,
        job_title: Optional[str],
        company: Optional[str],
        tone: str
    ) -> str:
        """Generate thank you message"""

        if contact_type in ["friend", "family"]:
            return f"""Hi {name}!

I just wanted to send a quick thank you for {context}. Your support really means a lot to me, and I'm so grateful to have you in my corner!

I'll keep you posted on how things progress. Thanks again for everything!

Best,
[Your name]"""

        else:
            return f"""Hi {name},

I wanted to express my sincere gratitude for your help with the {job_title} position at {company}. Your referral/support has been invaluable, and I truly appreciate you taking the time to assist me.

I will keep you updated on the progress of my application. Thank you again for your generosity and support.

Best regards,
[Your name]"""

    def _template_follow_up(
        self,
        name: str,
        contact_type: str,
        job_title: Optional[str],
        company: Optional[str],
        tone: str
    ) -> str:
        """Generate follow-up message"""

        return f"""Hi {name},

I wanted to follow up on my previous message regarding the {job_title} position at {company}.

I remain very interested in this opportunity and would appreciate any updates you might have. Please let me know if there's any additional information I can provide.

Thank you for your time and consideration.

Best regards,
[Your name]"""

    def _template_introduction(
        self,
        name: str,
        contact_type: str,
        job_title: Optional[str],
        company: Optional[str],
        tone: str
    ) -> str:
        """Generate introduction message"""

        return f"""Hi {name},

My name is [Your name] and I'm a [your current role/background]. I came across your profile and was impressed by your work at {company}.

I'm currently exploring opportunities in [your field], particularly roles like {job_title}. I would love to learn more about your experience at {company} and the work your team is doing.

Would you be open to a brief conversation? I'd be happy to work around your schedule.

Thank you for considering!

Best regards,
[Your name]"""

    def _template_recruiter_outreach(
        self,
        name: str,
        contact_type: str,
        job_title: Optional[str],
        company: Optional[str],
        tone: str
    ) -> str:
        """Generate recruiter outreach message"""

        return f"""Hi {name},

I noticed you're recruiting for {job_title} positions at {company}. I'm very interested in this opportunity and believe my background aligns well with what you're looking for.

Key highlights of my experience:
- [Highlight 1]
- [Highlight 2]
- [Highlight 3]

I've attached my resume for your review. I'd welcome the opportunity to discuss how I can contribute to your team.

Would you be available for a brief conversation this week?

Thank you for your time!

Best regards,
[Your name]"""

    # ===== Interaction Tracking =====

    async def log_interaction(
        self,
        contact_id: str,
        interaction_type: str,
        message_sent: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Log an interaction with a contact.

        Args:
            contact_id: Contact identifier
            interaction_type: Type (email_sent, linkedin_message, meeting, call, etc.)
            message_sent: Copy of message sent
            notes: Additional notes

        Returns:
            Success boolean
        """
        try:
            interactions = self._load_json(self.interactions_file, [])

            interaction = {
                "contact_id": contact_id,
                "interaction_type": interaction_type,
                "date": datetime.now().isoformat(),
                "message_sent": message_sent,
                "notes": notes,
            }

            interactions.append(interaction)
            self._save_json(self.interactions_file, interactions)

            # Update last contact date
            await self.update_last_contact(contact_id)

            logger.info(f"✅ Logged {interaction_type} with contact {contact_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error logging interaction: {e}")
            return False

    async def get_interaction_history(self, contact_id: str) -> List[Dict]:
        """Get interaction history for a contact"""
        interactions = self._load_json(self.interactions_file, [])
        return [i for i in interactions if i.get("contact_id") == contact_id]

    # ===== Follow-up Management =====

    async def schedule_follow_up(
        self,
        contact_id: str,
        follow_up_date: str,
        purpose: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Schedule a follow-up reminder.

        Args:
            contact_id: Contact identifier
            follow_up_date: Date to follow up (ISO format)
            purpose: Purpose of follow-up
            notes: Additional notes

        Returns:
            Success boolean
        """
        try:
            follow_ups = self._load_json(self.follow_ups_file, [])

            follow_up = {
                "id": f"followup_{datetime.now().timestamp()}",
                "contact_id": contact_id,
                "follow_up_date": follow_up_date,
                "purpose": purpose,
                "notes": notes,
                "status": "pending",
                "created_date": datetime.now().isoformat(),
            }

            follow_ups.append(follow_up)
            self._save_json(self.follow_ups_file, follow_ups)

            logger.info(f"✅ Scheduled follow-up for {follow_up_date}")
            return True

        except Exception as e:
            logger.error(f"❌ Error scheduling follow-up: {e}")
            return False

    async def get_pending_follow_ups(self, days_ahead: int = 7) -> List[Dict]:
        """
        Get pending follow-ups in the next N days.

        Args:
            days_ahead: Number of days to look ahead

        Returns:
            List of pending follow-ups
        """
        follow_ups = self._load_json(self.follow_ups_file, [])

        # Filter pending follow-ups
        pending = [f for f in follow_ups if f.get("status") == "pending"]

        # Filter by date
        cutoff = datetime.now() + timedelta(days=days_ahead)
        upcoming = [
            f for f in pending
            if datetime.fromisoformat(f["follow_up_date"]) <= cutoff
        ]

        # Sort by date
        upcoming.sort(key=lambda x: x["follow_up_date"])

        return upcoming

    async def mark_follow_up_complete(self, follow_up_id: str) -> bool:
        """Mark a follow-up as complete"""
        try:
            follow_ups = self._load_json(self.follow_ups_file, [])

            for follow_up in follow_ups:
                if follow_up.get("id") == follow_up_id:
                    follow_up["status"] = "completed"
                    follow_up["completed_date"] = datetime.now().isoformat()
                    break

            self._save_json(self.follow_ups_file, follow_ups)
            return True

        except Exception as e:
            logger.error(f"Error marking follow-up complete: {e}")
            return False

    # ===== Utility Methods =====

    def _generate_id(self, name: str) -> str:
        """Generate contact ID"""
        return name.lower().replace(" ", "_") + "_" + str(int(datetime.now().timestamp()))

    def _load_json(self, filepath: Path, default=None):
        """Load JSON file"""
        if not filepath.exists():
            return default if default is not None else {}

        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return default if default is not None else {}

    def _save_json(self, filepath: Path, data):
        """Save JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
