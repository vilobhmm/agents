"""
CC Skills - Personalized daily briefings and action-taking.

Inspired by Google Labs CC - your AI productivity agent that connects
Gmail, Calendar, and Drive to help you get ahead of your day.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class CCSkills:
    """
    Skills for CC (Chief Coordinator) agent.

    Delivers personalized morning briefings and takes actions.
    """

    def __init__(self):
        """Initialize CC with access to Google services"""
        try:
            from openclaw.integrations import GoogleServices
            self.google = GoogleServices()
            self.has_google = True
        except ImportError:
            logger.warning("Google services not available")
            self.has_google = False

    async def get_morning_briefing(self) -> Dict:
        """
        Generate personalized morning briefing.

        Analyzes:
        - Unread/important emails
        - Today's calendar events
        - Recently modified documents
        - Upcoming deadlines

        Returns comprehensive briefing dict
        """
        logger.info("Generating morning briefing...")

        briefing = {
            "timestamp": datetime.now().isoformat(),
            "greeting": self._get_greeting(),
            "emails": {},
            "calendar": {},
            "drive": {},
            "priorities": [],
            "suggestions": [],
        }

        if not self.has_google:
            briefing["note"] = "Google services not configured. Set up to get full briefings."
            return briefing

        try:
            # Get email context
            briefing["emails"] = await self._analyze_emails()

            # Get calendar context
            briefing["calendar"] = await self._analyze_calendar()

            # Get drive context
            briefing["drive"] = await self._analyze_drive()

            # Generate priorities
            briefing["priorities"] = self._identify_priorities(briefing)

            # Generate suggestions
            briefing["suggestions"] = self._generate_suggestions(briefing)

        except Exception as e:
            logger.error(f"Error generating briefing: {e}")
            briefing["error"] = str(e)

        return briefing

    async def _analyze_emails(self) -> Dict:
        """Analyze emails for important information"""
        try:
            unread = await self.google.get_unread_emails(max_results=20)

            # Categorize emails
            urgent = []
            important = []
            normal = []

            for email in unread:
                # Simple categorization (in production, would use NLP/AI)
                subject = email.get('subject', '').lower()
                sender = email.get('from', '').lower()

                if any(word in subject for word in ['urgent', 'asap', 'deadline', 'action required']):
                    urgent.append(email)
                elif any(word in subject for word in ['important', 'meeting', 'review', 'approval']):
                    important.append(email)
                else:
                    normal.append(email)

            return {
                "total_unread": len(unread),
                "urgent": len(urgent),
                "important": len(important),
                "urgent_emails": urgent[:5],  # Top 5
                "important_emails": important[:5],
            }
        except Exception as e:
            logger.error(f"Error analyzing emails: {e}")
            return {"error": str(e)}

    async def _analyze_calendar(self) -> Dict:
        """Analyze calendar for today and upcoming events"""
        try:
            today_events = await self.google.get_todays_events()
            upcoming = await self.google.get_upcoming_events(hours=48)

            # Find next meeting
            next_meeting = None
            now = datetime.now()
            for event in sorted(today_events, key=lambda e: e.get('start', {}).get('dateTime', '')):
                event_time = event.get('start', {}).get('dateTime')
                if event_time:
                    # In production, would parse datetime properly
                    next_meeting = event
                    break

            return {
                "events_today": len(today_events),
                "events_tomorrow": len([e for e in upcoming if e not in today_events]),
                "next_meeting": next_meeting,
                "todays_events": today_events,
            }
        except Exception as e:
            logger.error(f"Error analyzing calendar: {e}")
            return {"error": str(e)}

    async def _analyze_drive(self) -> Dict:
        """Analyze Drive for recent activity"""
        try:
            recent_files = await self.google.list_recent_files(max_results=10)

            # Categorize by type
            docs = [f for f in recent_files if 'document' in f.get('mimeType', '')]
            sheets = [f for f in recent_files if 'spreadsheet' in f.get('mimeType', '')]
            slides = [f for f in recent_files if 'presentation' in f.get('mimeType', '')]

            return {
                "recent_files": len(recent_files),
                "recent_docs": len(docs),
                "recent_sheets": len(sheets),
                "recent_slides": len(slides),
                "top_files": recent_files[:5],
            }
        except Exception as e:
            logger.error(f"Error analyzing drive: {e}")
            return {"error": str(e)}

    def _get_greeting(self) -> str:
        """Get time-appropriate greeting"""
        hour = datetime.now().hour

        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def _identify_priorities(self, briefing: Dict) -> List[str]:
        """Identify priorities from briefing data"""
        priorities = []

        # Check urgent emails
        urgent_count = briefing["emails"].get("urgent", 0)
        if urgent_count > 0:
            priorities.append(f"🔴 {urgent_count} urgent email{'s' if urgent_count > 1 else ''} need immediate attention")

        # Check meetings
        next_meeting = briefing["calendar"].get("next_meeting")
        if next_meeting:
            meeting_title = next_meeting.get('summary', 'Untitled')
            priorities.append(f"📅 Next meeting: {meeting_title}")

        # Check calendar load
        events_today = briefing["calendar"].get("events_today", 0)
        if events_today > 5:
            priorities.append(f"⚠️ Busy day ahead: {events_today} meetings scheduled")

        return priorities

    def _generate_suggestions(self, briefing: Dict) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []

        # Email suggestions
        urgent_count = briefing["emails"].get("urgent", 0)
        if urgent_count > 0:
            suggestions.append("Review and respond to urgent emails first")

        # Meeting prep suggestions
        next_meeting = briefing["calendar"].get("next_meeting")
        if next_meeting:
            suggestions.append(f"Prepare for upcoming meeting: {next_meeting.get('summary')}")

        # Time management
        events_today = briefing["calendar"].get("events_today", 0)
        if events_today > 3:
            suggestions.append("Consider blocking focus time between meetings")

        return suggestions

    def format_briefing(self, briefing: Dict) -> str:
        """Format briefing as readable text"""
        lines = []

        # Greeting
        lines.append(f"{briefing['greeting']}! Here's your daily briefing:\n")

        # Email summary
        emails = briefing.get("emails", {})
        if "error" not in emails:
            lines.append(f"📧 **Emails:**")
            lines.append(f"  • {emails.get('total_unread', 0)} unread")
            if emails.get('urgent', 0) > 0:
                lines.append(f"  • 🔴 {emails['urgent']} urgent")
            if emails.get('important', 0) > 0:
                lines.append(f"  • ⭐ {emails['important']} important")
            lines.append("")

        # Calendar summary
        calendar = briefing.get("calendar", {})
        if "error" not in calendar:
            lines.append(f"📅 **Calendar:**")
            lines.append(f"  • {calendar.get('events_today', 0)} events today")

            next_meeting = calendar.get('next_meeting')
            if next_meeting:
                title = next_meeting.get('summary', 'Untitled')
                lines.append(f"  • Next: {title}")
            lines.append("")

        # Drive summary
        drive = briefing.get("drive", {})
        if "error" not in drive:
            lines.append(f"📁 **Drive:**")
            lines.append(f"  • {drive.get('recent_files', 0)} recently modified files")
            lines.append("")

        # Priorities
        if briefing.get("priorities"):
            lines.append("🎯 **Priorities:**")
            for priority in briefing["priorities"]:
                lines.append(f"  • {priority}")
            lines.append("")

        # Suggestions
        if briefing.get("suggestions"):
            lines.append("💡 **Suggestions:**")
            for suggestion in briefing["suggestions"]:
                lines.append(f"  • {suggestion}")
            lines.append("")

        return "\n".join(lines)


class ActionTakerSkills:
    """Skills for taking actions on user's behalf"""

    def __init__(self):
        """Initialize with access to services"""
        try:
            from openclaw.integrations import GoogleServices
            self.google = GoogleServices()
            self.has_google = True
        except ImportError:
            logger.warning("Google services not available")
            self.has_google = False

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email via Gmail"""
        if not self.has_google:
            logger.warning("Google services not configured")
            return False

        try:
            success = await self.google.send_email(to, subject, body)
            return success
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    async def schedule_meeting(
        self,
        title: str,
        start_time: datetime,
        duration_minutes: int = 30,
        attendees: List[str] = None,
        description: str = None
    ) -> Optional[str]:
        """Schedule a calendar meeting"""
        if not self.has_google:
            logger.warning("Google services not configured")
            return None

        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            event_id = await self.google.create_event(
                title=title,
                start=start_time,
                end=end_time,
                description=description,
            )
            return event_id
        except Exception as e:
            logger.error(f"Error scheduling meeting: {e}")
            return None

    async def block_focus_time(
        self,
        title: str = "Focus Time",
        duration_hours: float = 2
    ) -> Optional[str]:
        """Block time on calendar for focused work"""
        if not self.has_google:
            return None

        try:
            event_id = await self.google.block_time(
                title=title,
                duration_minutes=int(duration_hours * 60)
            )
            return event_id
        except Exception as e:
            logger.error(f"Error blocking time: {e}")
            return None


# CC Agent Guide for system prompts
CC_AGENT_GUIDE = """
## CC (Chief Coordinator) Capabilities

You are CC, an AI productivity agent that helps users get ahead of their day.

### Morning Briefing
Use `get_morning_briefing()` to deliver personalized daily briefs including:
- Urgent and important emails
- Today's calendar with next meeting
- Recently modified Drive files
- Identified priorities
- Actionable suggestions

### Taking Actions
You can take concrete actions:
- `send_email(to, subject, body)` - Send emails
- `schedule_meeting(title, start_time, duration)` - Create calendar events
- `block_focus_time(title, duration_hours)` - Block focus time

### Proactive Assistance
- Deliver morning briefing automatically
- Alert on urgent emails
- Remind before meetings
- Suggest daily priorities
- Coordinate with other agents for complex tasks

### Example Usage:
User: "Give me my morning briefing"
CC: [Generates and formats comprehensive briefing]

User: "Schedule a meeting with Sarah tomorrow at 2pm"
CC: [Creates calendar event and confirms]

User: "Draft an email to John about the project update"
CC: [Drafts email using context from Drive and Calendar]
"""
