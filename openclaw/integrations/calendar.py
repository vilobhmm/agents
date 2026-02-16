"""Calendar integration using Google Calendar API"""

import logging
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarIntegration:
    """Google Calendar integration"""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        credentials: Optional[Credentials] = None,
    ):
        """
        Initialize Calendar integration.

        Args:
            credentials_path: Path to OAuth credentials JSON (for standalone use)
            token_path: Path to token file (for standalone use)
            credentials: Pre-authenticated Credentials object (for unified auth)
        """
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_CALENDAR_CREDENTIALS_PATH", "calendar_credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GOOGLE_CALENDAR_TOKEN_PATH", "calendar_token.json"
        )
        self.service = None

        # Use pre-authenticated credentials if provided, otherwise authenticate
        if credentials:
            self.service = build("calendar", "v3", credentials=credentials)
            logger.info("Google Calendar API authenticated successfully (unified auth)")
        else:
            self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None

        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    logger.warning(
                        f"Credentials file not found: {self.credentials_path}"
                    )
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("calendar", "v3", credentials=creds)
        logger.info("Google Calendar API authenticated successfully")

    async def get_events(
        self,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 10,
    ) -> List[Dict]:
        """
        Get calendar events.

        Args:
            time_min: Start time (defaults to now)
            time_max: End time (defaults to 7 days from now)
            max_results: Maximum number of events

        Returns:
            List of event dictionaries
        """
        if not self.service:
            logger.error("Calendar service not initialized")
            return []

        try:
            if not time_min:
                time_min = datetime.utcnow()
            if not time_max:
                time_max = time_min + timedelta(days=7)

            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=time_min.isoformat() + "Z",
                    timeMax=time_max.isoformat() + "Z",
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])
            return events

        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return []

    async def create_event(
        self,
        summary: str,
        start: datetime,
        end: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
    ) -> Optional[str]:
        """
        Create a calendar event.

        Args:
            summary: Event title
            start: Start datetime
            end: End datetime
            description: Event description
            location: Event location
            attendees: List of attendee email addresses

        Returns:
            Event ID if successful, None otherwise
        """
        if not self.service:
            logger.error("Calendar service not initialized")
            return None

        try:
            event = {
                "summary": summary,
                "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
            }

            if description:
                event["description"] = description
            if location:
                event["location"] = location
            if attendees:
                event["attendees"] = [{"email": email} for email in attendees]

            created_event = (
                self.service.events()
                .insert(calendarId="primary", body=event)
                .execute()
            )

            logger.info(f"Created event: {summary}")
            return created_event["id"]

        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return None

    async def get_upcoming_events(self, hours: int = 24) -> List[Dict]:
        """Get events in the next N hours"""
        time_min = datetime.utcnow()
        time_max = time_min + timedelta(hours=hours)
        return await self.get_events(time_min=time_min, time_max=time_max)

    async def create_block(
        self, title: str, duration_minutes: int, start_time: Optional[datetime] = None
    ) -> Optional[str]:
        """Create a time block on the calendar"""
        if not start_time:
            start_time = datetime.utcnow()

        end_time = start_time + timedelta(minutes=duration_minutes)
        return await self.create_event(summary=title, start=start_time, end=end_time)
