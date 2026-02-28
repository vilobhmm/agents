"""Google Services tools for CC agent - Real Gmail, Calendar, Drive access."""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class GoogleTools:
    """
    Real Google services tools for CC agent.

    Provides actual API access to:
    - Gmail (read, send, search, draft)
    - Calendar (events, scheduling, availability)
    - Drive (files, search, documents)
    """

    def __init__(self):
        """Initialize Google tools"""
        self.google_services = None
        self._initialize_google_services()

    def _initialize_google_services(self):
        """Lazy initialize Google services"""
        try:
            from openclaw.integrations.google_services import GoogleServices

            # Get credentials from environment
            creds_path = os.getenv("GOOGLE_OAUTH_CREDENTIALS_FILE", "google_oauth_credentials.json")
            token_path = os.getenv("GOOGLE_TOKEN_FILE", "google_token.pickle")

            self.google_services = GoogleServices(
                credentials_path=creds_path,
                token_path=token_path
            )
            logger.info("✅ Google Tools initialized")
        except Exception as e:
            logger.warning(f"Google services not available: {e}")
            logger.warning("To enable Google services, set up OAuth credentials and environment variables")
            self.google_services = None

    async def get_daily_briefing(self) -> Dict:
        """
        Get comprehensive daily briefing.

        Returns:
            Dict with unread emails, today's events, recent files
        """
        if not self.google_services:
            return {"error": "Google services not configured"}

        try:
            return await self.google_services.get_daily_context()
        except Exception as e:
            logger.error(f"Error getting daily briefing: {e}")
            return {"error": str(e)}

    async def get_unread_emails(self, max_results: int = 10) -> List[Dict]:
        """Get unread emails"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.get_unread_emails(max_results)
        except Exception as e:
            logger.error(f"Error getting emails: {e}")
            return []

    async def search_emails(self, query: str, sender: Optional[str] = None) -> List[Dict]:
        """Search emails by query or sender"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.search_emails(query=query, sender=sender)
        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            return []

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email"""
        if not self.google_services:
            return False

        try:
            return await self.google_services.send_email(to, subject, body)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    async def get_todays_events(self) -> List[Dict]:
        """Get today's calendar events"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.get_todays_events()
        except Exception as e:
            logger.error(f"Error getting events: {e}")
            return []

    async def get_upcoming_events(self, hours: int = 24) -> List[Dict]:
        """Get upcoming events in next N hours"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.get_upcoming_events(hours)
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            return []

    async def create_calendar_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: Optional[str] = None
    ) -> Optional[str]:
        """Create a calendar event"""
        if not self.google_services:
            return None

        try:
            return await self.google_services.create_event(title, start, end, description)
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return None

    async def block_time(self, title: str, duration_minutes: int) -> Optional[str]:
        """Block time on calendar starting now"""
        if not self.google_services:
            return None

        try:
            return await self.google_services.block_time(title, duration_minutes)
        except Exception as e:
            logger.error(f"Error blocking time: {e}")
            return None

    async def search_drive_files(self, query: str) -> List[Dict]:
        """Search Drive files"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.search_files(query)
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []

    async def get_recent_files(self, max_results: int = 20) -> List[Dict]:
        """Get recently modified files"""
        if not self.google_services:
            return []

        try:
            return await self.google_services.list_recent_files(max_results)
        except Exception as e:
            logger.error(f"Error getting recent files: {e}")
            return []

    async def prepare_for_meeting(self, meeting_title: str) -> Dict:
        """Prepare comprehensive context for a meeting"""
        if not self.google_services:
            return {}

        try:
            return await self.google_services.prepare_for_meeting(meeting_title)
        except Exception as e:
            logger.error(f"Error preparing for meeting: {e}")
            return {}

    async def get_next_meeting(self) -> Optional[Dict]:
        """Get information about next meeting"""
        if not self.google_services:
            return None

        try:
            return await self.google_services.get_next_meeting_info()
        except Exception as e:
            logger.error(f"Error getting next meeting: {e}")
            return None

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [
            "get_daily_briefing",
            "get_unread_emails",
            "search_emails",
            "send_email",
            "get_todays_events",
            "get_upcoming_events",
            "create_calendar_event",
            "block_time",
            "search_drive_files",
            "get_recent_files",
            "prepare_for_meeting",
            "get_next_meeting",
        ]

    def get_tools_description(self) -> str:
        """Get description of available tools for agent prompt"""
        return """
You have access to the following Google services tools:

**Email Tools:**
- get_daily_briefing() - Get comprehensive daily context (emails, calendar, files)
- get_unread_emails(max_results=10) - Get unread emails
- search_emails(query, sender=None) - Search emails by query or sender
- send_email(to, subject, body) - Send an email

**Calendar Tools:**
- get_todays_events() - Get today's calendar events
- get_upcoming_events(hours=24) - Get upcoming events
- create_calendar_event(title, start, end, description=None) - Create event
- block_time(title, duration_minutes) - Block time on calendar
- get_next_meeting() - Get info about next meeting
- prepare_for_meeting(meeting_title) - Get context for meeting

**Drive Tools:**
- search_drive_files(query) - Search Drive files
- get_recent_files(max_results=20) - Get recently modified files

Use these tools to provide personalized, context-aware assistance!
"""
