"""Unified Google Services - One-stop access to Gmail, Calendar, and Drive"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.drive import DriveIntegration


logger = logging.getLogger(__name__)


class GoogleServices:
    """
    Unified interface for all Google services.

    One class to access:
    - Gmail (read, send, search emails)
    - Calendar (events, scheduling)
    - Drive (files, documents)

    All authenticated with the same credentials.
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        """
        Initialize all Google services.

        Args:
            credentials_path: Path to OAuth credentials
            token_path: Path to token file
        """
        logger.info("Initializing Google Services...")

        # Initialize all services
        self.gmail = EmailIntegration(credentials_path, token_path)
        self.calendar = CalendarIntegration(credentials_path, token_path)
        self.drive = DriveIntegration(credentials_path, token_path)

        logger.info("✅ Google Services ready (Gmail, Calendar, Drive)")

    # ===== Gmail Methods =====

    async def get_unread_emails(self, max_results: int = 10) -> List[Dict]:
        """Get unread emails"""
        return await self.gmail.get_messages(unread_only=True, max_results=max_results)

    async def search_emails(
        self,
        query: Optional[str] = None,
        sender: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> List[Dict]:
        """Search emails"""
        if sender or subject:
            return await self.gmail.search_emails(sender=sender, subject=subject)
        return await self.gmail.get_messages(query=query)

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email"""
        return await self.gmail.send_message(to, subject, body)

    # ===== Calendar Methods =====

    async def get_todays_events(self) -> List[Dict]:
        """Get today's calendar events"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        return await self.calendar.get_events(time_min=today_start, time_max=today_end)

    async def get_upcoming_events(self, hours: int = 24) -> List[Dict]:
        """Get upcoming events in the next N hours"""
        return await self.calendar.get_upcoming_events(hours=hours)

    async def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: Optional[str] = None,
    ) -> Optional[str]:
        """Create a calendar event"""
        return await self.calendar.create_event(
            summary=title,
            start=start,
            end=end,
            description=description,
        )

    async def block_time(self, title: str, duration_minutes: int) -> Optional[str]:
        """Block time on calendar starting now"""
        return await self.calendar.create_block(title, duration_minutes)

    # ===== Drive Methods =====

    async def list_recent_files(self, max_results: int = 20) -> List[Dict]:
        """List recently modified files"""
        return await self.drive.get_recent_files(max_results)

    async def search_files(self, query: str) -> List[Dict]:
        """Search Drive files"""
        return await self.drive.search_files(name=query)

    async def search_documents(self, query: str) -> List[Dict]:
        """Search Google Docs"""
        return await self.drive.search_documents(query)

    async def download_file(self, file_id: str, output_path: str) -> bool:
        """Download a file from Drive"""
        result = await self.drive.download_file(file_id, output_path)
        return result is not None

    # ===== Combined Intelligence Methods =====

    async def get_daily_context(self) -> Dict:
        """
        Get comprehensive daily context from all services.

        Returns a dictionary with:
        - unread_emails: List of unread emails
        - todays_events: Today's calendar events
        - recent_files: Recently modified Drive files
        """
        logger.info("Gathering daily context from Google services...")

        try:
            # Gather all data in parallel would be ideal, but for simplicity, sequential
            unread_emails = await self.get_unread_emails(max_results=10)
            todays_events = await self.get_todays_events()
            recent_files = await self.list_recent_files(max_results=10)

            context = {
                "unread_emails": unread_emails,
                "unread_count": len(unread_emails),
                "todays_events": todays_events,
                "events_count": len(todays_events),
                "recent_files": recent_files,
                "recent_files_count": len(recent_files),
            }

            logger.info(
                f"Daily context: {context['unread_count']} unread emails, "
                f"{context['events_count']} events today, "
                f"{context['recent_files_count']} recent files"
            )

            return context

        except Exception as e:
            logger.error(f"Error gathering daily context: {e}")
            return {
                "unread_emails": [],
                "unread_count": 0,
                "todays_events": [],
                "events_count": 0,
                "recent_files": [],
                "recent_files_count": 0,
            }

    async def get_next_meeting_info(self) -> Optional[Dict]:
        """Get information about the next upcoming meeting"""
        upcoming = await self.get_upcoming_events(hours=24)

        if not upcoming:
            return None

        next_meeting = upcoming[0]

        # Try to find related emails about this meeting
        meeting_title = next_meeting.get("summary", "")
        related_emails = await self.search_emails(subject=meeting_title)

        return {
            "event": next_meeting,
            "related_emails": related_emails[:5],  # Top 5 related emails
        }

    async def prepare_for_meeting(self, meeting_title: str) -> Dict:
        """
        Prepare for a meeting by gathering relevant context.

        Args:
            meeting_title: Title of the meeting

        Returns:
            Dictionary with meeting info, related emails, and relevant files
        """
        logger.info(f"Preparing context for meeting: {meeting_title}")

        # Search for related content
        related_emails = await self.search_emails(subject=meeting_title)
        related_files = await self.search_files(query=meeting_title)

        return {
            "meeting_title": meeting_title,
            "related_emails": related_emails[:10],
            "related_files": related_files[:10],
        }

    async def get_weekly_summary(self) -> Dict:
        """Get a summary of the week ahead"""
        now = datetime.now()
        week_end = now + timedelta(days=7)

        events = await self.calendar.get_events(time_min=now, time_max=week_end)

        return {
            "total_events": len(events),
            "events": events,
            "days_with_meetings": len(set(
                event.get("start", {}).get("dateTime", "")[:10]
                for event in events
            )),
        }


# Simple interface functions
async def get_my_context() -> Dict:
    """Quick function to get daily Google context"""
    google = GoogleServices()
    return await google.get_daily_context()


async def whats_next() -> Optional[Dict]:
    """Quick function to see what's next on calendar"""
    google = GoogleServices()
    return await google.get_next_meeting_info()


async def prepare_meeting(meeting_title: str) -> Dict:
    """Quick function to prepare for a meeting"""
    google = GoogleServices()
    return await google.prepare_for_meeting(meeting_title)
