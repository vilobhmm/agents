"""
Activity Monitor Agent

Tracks user activities throughout the day with minute-level granularity.
Monitors:
- Manual activity logging (user inputs what they're doing)
- Calendar events (from Google Calendar)
- Computer activity (active applications, idle time)
- Context switches and focus periods
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json


class ActivityMonitorAgent:
    """Agent for monitoring and logging user activities."""

    def __init__(self, storage_manager):
        """
        Initialize the Activity Monitor Agent.

        Args:
            storage_manager: Storage manager for persisting activity data
        """
        self.storage = storage_manager
        self.current_activity = None
        self.activity_start_time = None
        self.monitoring_active = False

    async def start_activity(self, activity: str, category: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Start tracking a new activity.

        Args:
            activity: Description of the activity
            category: Optional category (e.g., "work", "personal", "break")
            metadata: Optional additional metadata

        Returns:
            Activity record with start time
        """
        # End previous activity if one exists
        if self.current_activity:
            await self.end_current_activity()

        self.current_activity = {
            'activity': activity,
            'category': category,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration_minutes': 0,
            'metadata': metadata or {}
        }
        self.activity_start_time = datetime.now()

        return {
            'status': 'started',
            'activity': activity,
            'start_time': self.current_activity['start_time']
        }

    async def end_current_activity(self) -> Optional[Dict[str, Any]]:
        """
        End the current activity and save it.

        Returns:
            Completed activity record
        """
        if not self.current_activity:
            return None

        end_time = datetime.now()
        duration = (end_time - self.activity_start_time).total_seconds() / 60

        self.current_activity['end_time'] = end_time.isoformat()
        self.current_activity['duration_minutes'] = round(duration, 2)

        # Save to storage
        await self.storage.save_activity(self.current_activity)

        completed = self.current_activity.copy()
        self.current_activity = None
        self.activity_start_time = None

        return completed

    async def quick_log(self, activity: str, minutes_ago: int = 0,
                       duration_minutes: int = 5) -> Dict[str, Any]:
        """
        Quickly log a past activity.

        Args:
            activity: What you were doing
            minutes_ago: How many minutes ago did it start
            duration_minutes: How long it lasted

        Returns:
            Logged activity record
        """
        end_time = datetime.now() - timedelta(minutes=minutes_ago)
        start_time = end_time - timedelta(minutes=duration_minutes)

        activity_record = {
            'activity': activity,
            'category': None,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_minutes': duration_minutes,
            'metadata': {'logged_retrospectively': True}
        }

        await self.storage.save_activity(activity_record)

        return activity_record

    async def get_current_activity(self) -> Optional[Dict[str, Any]]:
        """Get the currently active activity."""
        if not self.current_activity:
            return None

        # Calculate current duration
        current_duration = (datetime.now() - self.activity_start_time).total_seconds() / 60

        return {
            **self.current_activity,
            'current_duration_minutes': round(current_duration, 2),
            'is_active': True
        }

    async def import_calendar_events(self, date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Import events from calendar as activities.

        Args:
            date: Date to import events for (defaults to today)

        Returns:
            List of imported activities
        """
        if date is None:
            date = datetime.now()

        # This would integrate with Google Calendar API
        # For now, returning a placeholder structure
        imported_activities = []

        # TODO: Implement actual calendar integration
        # from core.agent_tools.google_tools import get_calendar_events
        # events = await get_calendar_events(date)

        return imported_activities

    async def track_idle_time(self) -> Dict[str, Any]:
        """
        Track idle/inactive periods.

        Returns:
            Idle time information
        """
        # This would integrate with system idle detection
        # For now, returning a placeholder
        return {
            'idle_detected': False,
            'idle_duration_minutes': 0,
            'last_activity_time': datetime.now().isoformat()
        }

    async def get_activities_for_period(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """
        Get all activities within a time period.

        Args:
            start: Period start time
            end: Period end time

        Returns:
            List of activities in the period
        """
        return await self.storage.get_activities_by_period(start, end)

    async def get_today_activities(self) -> List[Dict[str, Any]]:
        """Get all activities for today."""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now()

        return await self.get_activities_for_period(today_start, today_end)

    async def suggest_missing_time(self) -> List[Dict[str, Any]]:
        """
        Identify time gaps where no activity was logged.

        Returns:
            List of time gaps that need to be filled
        """
        activities = await self.get_today_activities()

        if not activities:
            return [{
                'gap_start': datetime.now().replace(hour=0, minute=0).isoformat(),
                'gap_end': datetime.now().isoformat(),
                'duration_minutes': (datetime.now() - datetime.now().replace(hour=0, minute=0)).total_seconds() / 60,
                'suggestion': 'No activities logged today yet'
            }]

        # Sort activities by start time
        sorted_activities = sorted(activities, key=lambda x: x['start_time'])

        gaps = []
        day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Check gap from day start to first activity
        first_activity_start = datetime.fromisoformat(sorted_activities[0]['start_time'])
        if first_activity_start > day_start:
            gap_minutes = (first_activity_start - day_start).total_seconds() / 60
            if gap_minutes > 5:  # Only report gaps longer than 5 minutes
                gaps.append({
                    'gap_start': day_start.isoformat(),
                    'gap_end': first_activity_start.isoformat(),
                    'duration_minutes': round(gap_minutes, 2),
                    'suggestion': 'What were you doing at the start of the day?'
                })

        # Check gaps between activities
        for i in range(len(sorted_activities) - 1):
            current_end = datetime.fromisoformat(sorted_activities[i]['end_time'])
            next_start = datetime.fromisoformat(sorted_activities[i + 1]['start_time'])

            gap_minutes = (next_start - current_end).total_seconds() / 60
            if gap_minutes > 5:
                gaps.append({
                    'gap_start': current_end.isoformat(),
                    'gap_end': next_start.isoformat(),
                    'duration_minutes': round(gap_minutes, 2),
                    'suggestion': f'Gap between {sorted_activities[i]["activity"]} and {sorted_activities[i+1]["activity"]}'
                })

        # Check gap from last activity to now
        if sorted_activities[-1]['end_time']:
            last_activity_end = datetime.fromisoformat(sorted_activities[-1]['end_time'])
            now = datetime.now()
            gap_minutes = (now - last_activity_end).total_seconds() / 60
            if gap_minutes > 5:
                gaps.append({
                    'gap_start': last_activity_end.isoformat(),
                    'gap_end': now.isoformat(),
                    'duration_minutes': round(gap_minutes, 2),
                    'suggestion': 'What have you been doing recently?'
                })

        return gaps

    async def auto_categorize_activity(self, activity: str) -> str:
        """
        Automatically suggest a category for an activity using AI.

        Args:
            activity: Activity description

        Returns:
            Suggested category
        """
        # Simple keyword-based categorization
        # Could be enhanced with Claude API for better categorization

        activity_lower = activity.lower()

        # Work-related keywords
        work_keywords = ['meeting', 'email', 'code', 'coding', 'debug', 'review',
                        'documentation', 'planning', 'call', 'presentation']
        if any(keyword in activity_lower for keyword in work_keywords):
            return 'work'

        # Personal development keywords
        learning_keywords = ['learn', 'study', 'course', 'reading', 'tutorial',
                           'practice', 'research']
        if any(keyword in activity_lower for keyword in learning_keywords):
            return 'learning'

        # Break keywords
        break_keywords = ['break', 'lunch', 'coffee', 'walk', 'rest', 'snack']
        if any(keyword in activity_lower for keyword in break_keywords):
            return 'break'

        # Exercise keywords
        exercise_keywords = ['exercise', 'gym', 'workout', 'run', 'yoga', 'sport']
        if any(keyword in activity_lower for keyword in exercise_keywords):
            return 'health'

        # Entertainment keywords
        entertainment_keywords = ['video', 'game', 'movie', 'youtube', 'social media',
                                'browse', 'scrolling', 'netflix']
        if any(keyword in activity_lower for keyword in entertainment_keywords):
            return 'entertainment'

        return 'uncategorized'
