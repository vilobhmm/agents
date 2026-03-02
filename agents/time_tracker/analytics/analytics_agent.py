"""
Analytics Agent

Provides insights, patterns, and trends from time tracking data:
- Daily/weekly/monthly trends
- Peak productivity hours
- Time waste identification
- Goal tracking
- Comparative analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict
import statistics


class AnalyticsAgent:
    """Agent for analyzing time tracking data and providing insights."""

    def __init__(self, storage_manager):
        """
        Initialize the Analytics Agent.

        Args:
            storage_manager: Storage manager for accessing activity data
        """
        self.storage = storage_manager

    async def get_daily_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get a comprehensive daily summary.

        Args:
            date: Date to analyze (defaults to today)

        Returns:
            Daily summary with key metrics
        """
        if date is None:
            date = datetime.now()

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        activities = await self.storage.get_activities_by_period(start, end)

        # Calculate metrics
        total_time = sum(a.get('duration_minutes', 0) for a in activities)
        activity_count = len(activities)

        # Category breakdown
        category_time = defaultdict(float)
        for activity in activities:
            category = activity.get('category', 'uncategorized')
            category_time[category] += activity.get('duration_minutes', 0)

        # Most productive hour
        hourly_work = defaultdict(float)
        for activity in activities:
            if activity.get('category') in ['work', 'learning']:
                start_hour = datetime.fromisoformat(activity['start_time']).hour
                hourly_work[start_hour] += activity.get('duration_minutes', 0)

        peak_hour = max(hourly_work.items(), key=lambda x: x[1])[0] if hourly_work else None

        return {
            'date': date.date().isoformat(),
            'total_tracked_minutes': round(total_time, 2),
            'total_tracked_hours': round(total_time / 60, 2),
            'activity_count': activity_count,
            'average_activity_duration': round(total_time / activity_count, 2) if activity_count > 0 else 0,
            'category_breakdown': {
                cat: round(mins, 2) for cat, mins in category_time.items()
            },
            'most_productive_hour': peak_hour,
            'top_activities': sorted(
                [(a['activity'], a.get('duration_minutes', 0)) for a in activities],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

    async def get_weekly_trends(self, week_start: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Analyze weekly trends and patterns.

        Args:
            week_start: Start of week (defaults to current week)

        Returns:
            Weekly trend analysis
        """
        if week_start is None:
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())

        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)

        daily_summaries = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            summary = await self.get_daily_summary(day)
            daily_summaries.append(summary)

        # Calculate weekly aggregates
        total_time = sum(d['total_tracked_minutes'] for d in daily_summaries)
        avg_daily_time = total_time / 7

        # Category trends
        category_totals = defaultdict(float)
        for day in daily_summaries:
            for cat, mins in day['category_breakdown'].items():
                category_totals[cat] += mins

        return {
            'week_start': week_start.date().isoformat(),
            'week_end': (week_end - timedelta(days=1)).date().isoformat(),
            'total_tracked_hours': round(total_time / 60, 2),
            'average_daily_hours': round(avg_daily_time / 60, 2),
            'daily_breakdown': daily_summaries,
            'category_totals': {
                cat: round(mins, 2) for cat, mins in category_totals.items()
            },
            'most_productive_day': max(
                daily_summaries,
                key=lambda d: d['category_breakdown'].get('work', 0) + d['category_breakdown'].get('learning', 0)
            )['date']
        }

    async def identify_time_wasters(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Identify activities that might be time wasters.

        Args:
            days: Number of days to analyze

        Returns:
            List of potential time wasters with recommendations
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        activities = await self.storage.get_activities_by_period(start, end)

        # Identify patterns of time waste
        time_wasters = []

        # 1. Excessive entertainment
        entertainment_time = defaultdict(float)
        for activity in activities:
            if activity.get('category') == 'entertainment':
                entertainment_time[activity['activity']] += activity.get('duration_minutes', 0)

        for activity, minutes in entertainment_time.items():
            if minutes > 120:  # More than 2 hours in the period
                time_wasters.append({
                    'activity': activity,
                    'category': 'entertainment',
                    'total_minutes': round(minutes, 2),
                    'recommendation': f'Consider reducing {activity} time',
                    'severity': 'high' if minutes > 300 else 'medium'
                })

        # 2. Fragmented work sessions
        work_sessions = [a for a in activities if a.get('category') == 'work']
        short_sessions = [s for s in work_sessions if s.get('duration_minutes', 0) < 15]

        if len(short_sessions) > 10:
            time_wasters.append({
                'activity': 'Fragmented work sessions',
                'category': 'work',
                'total_minutes': sum(s.get('duration_minutes', 0) for s in short_sessions),
                'recommendation': 'Try to batch work into longer, focused sessions',
                'severity': 'medium'
            })

        # 3. Excessive context switching
        if len(activities) > days * 20:  # More than 20 activities per day
            time_wasters.append({
                'activity': 'Frequent context switching',
                'category': 'productivity',
                'total_minutes': None,
                'recommendation': 'Reduce task switching to improve focus',
                'severity': 'high'
            })

        return sorted(time_wasters, key=lambda x: x.get('severity') == 'high', reverse=True)

    async def get_productivity_patterns(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze productivity patterns over time.

        Args:
            days: Number of days to analyze

        Returns:
            Productivity pattern analysis
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        activities = await self.storage.get_activities_by_period(start, end)

        # Hour of day analysis
        hourly_productivity = defaultdict(float)
        for activity in activities:
            if activity.get('category') in ['work', 'learning']:
                hour = datetime.fromisoformat(activity['start_time']).hour
                hourly_productivity[hour] += activity.get('duration_minutes', 0)

        # Day of week analysis
        dow_productivity = defaultdict(float)
        for activity in activities:
            if activity.get('category') in ['work', 'learning']:
                dow = datetime.fromisoformat(activity['start_time']).weekday()
                dow_productivity[dow] += activity.get('duration_minutes', 0)

        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        return {
            'analysis_period_days': days,
            'peak_productivity_hours': sorted(
                hourly_productivity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            'most_productive_days': [
                (day_names[dow], round(mins, 2))
                for dow, mins in sorted(dow_productivity.items(), key=lambda x: x[1], reverse=True)
            ],
            'hourly_breakdown': {
                f'{hour:02d}:00': round(mins, 2)
                for hour, mins in sorted(hourly_productivity.items())
            }
        }

    async def compare_periods(self, period1_start: datetime, period1_end: datetime,
                             period2_start: datetime, period2_end: datetime) -> Dict[str, Any]:
        """
        Compare two time periods.

        Args:
            period1_start: Start of first period
            period1_end: End of first period
            period2_start: Start of second period
            period2_end: End of second period

        Returns:
            Comparative analysis
        """
        activities1 = await self.storage.get_activities_by_period(period1_start, period1_end)
        activities2 = await self.storage.get_activities_by_period(period2_start, period2_end)

        def analyze_period(activities):
            total_time = sum(a.get('duration_minutes', 0) for a in activities)
            category_time = defaultdict(float)
            for a in activities:
                category_time[a.get('category', 'uncategorized')] += a.get('duration_minutes', 0)

            return {
                'total_minutes': total_time,
                'activity_count': len(activities),
                'categories': dict(category_time)
            }

        p1_analysis = analyze_period(activities1)
        p2_analysis = analyze_period(activities2)

        # Calculate differences
        category_changes = {}
        all_categories = set(p1_analysis['categories'].keys()) | set(p2_analysis['categories'].keys())

        for cat in all_categories:
            p1_time = p1_analysis['categories'].get(cat, 0)
            p2_time = p2_analysis['categories'].get(cat, 0)
            change = p2_time - p1_time
            change_pct = (change / p1_time * 100) if p1_time > 0 else 0

            category_changes[cat] = {
                'period1_minutes': round(p1_time, 2),
                'period2_minutes': round(p2_time, 2),
                'change_minutes': round(change, 2),
                'change_percentage': round(change_pct, 2)
            }

        return {
            'period1': {
                'start': period1_start.isoformat(),
                'end': period1_end.isoformat(),
                **p1_analysis
            },
            'period2': {
                'start': period2_start.isoformat(),
                'end': period2_end.isoformat(),
                **p2_analysis
            },
            'category_changes': category_changes,
            'total_time_change': {
                'minutes': round(p2_analysis['total_minutes'] - p1_analysis['total_minutes'], 2),
                'percentage': round(
                    (p2_analysis['total_minutes'] - p1_analysis['total_minutes']) / p1_analysis['total_minutes'] * 100,
                    2
                ) if p1_analysis['total_minutes'] > 0 else 0
            }
        }

    async def get_focus_metrics(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Calculate focus and concentration metrics.

        Args:
            date: Date to analyze (defaults to today)

        Returns:
            Focus metrics including deep work time, interruptions, etc.
        """
        if date is None:
            date = datetime.now()

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59)

        activities = await self.storage.get_activities_by_period(start, end)

        # Deep work sessions (work activities > 25 minutes)
        deep_work_sessions = [
            a for a in activities
            if a.get('category') == 'work' and a.get('duration_minutes', 0) >= 25
        ]

        # Short sessions (< 15 minutes)
        short_sessions = [
            a for a in activities
            if a.get('duration_minutes', 0) < 15
        ]

        # Calculate average session length
        session_lengths = [a.get('duration_minutes', 0) for a in activities if a.get('duration_minutes', 0) > 0]
        avg_session_length = statistics.mean(session_lengths) if session_lengths else 0

        return {
            'date': date.date().isoformat(),
            'deep_work_sessions': len(deep_work_sessions),
            'deep_work_minutes': sum(a.get('duration_minutes', 0) for a in deep_work_sessions),
            'total_sessions': len(activities),
            'short_sessions': len(short_sessions),
            'average_session_length': round(avg_session_length, 2),
            'context_switches': len(activities) - 1,  # Transitions between activities
            'focus_score': round(
                (sum(a.get('duration_minutes', 0) for a in deep_work_sessions) /
                 sum(a.get('duration_minutes', 0) for a in activities) * 100)
                if activities else 0,
                2
            )
        }

    async def suggest_improvements(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Generate personalized improvement suggestions.

        Args:
            days: Number of days to analyze

        Returns:
            List of actionable suggestions
        """
        suggestions = []

        # Analyze recent patterns
        end = datetime.now()
        start = end - timedelta(days=days)

        activities = await self.storage.get_activities_by_period(start, end)

        # Check for low deep work time
        work_activities = [a for a in activities if a.get('category') == 'work']
        deep_work = [a for a in work_activities if a.get('duration_minutes', 0) >= 25]

        if work_activities and len(deep_work) / len(work_activities) < 0.3:
            suggestions.append({
                'type': 'focus',
                'priority': 'high',
                'suggestion': 'Increase deep work sessions (25+ minutes)',
                'reason': 'Only {:.1f}% of work sessions are focused deep work'.format(
                    len(deep_work) / len(work_activities) * 100
                ),
                'action': 'Try time-blocking 2-hour deep work sessions in your calendar'
            })

        # Check for entertainment time
        entertainment = [a for a in activities if a.get('category') == 'entertainment']
        entertainment_time = sum(a.get('duration_minutes', 0) for a in entertainment)

        if entertainment_time > 10 * 60:  # More than 10 hours per week
            suggestions.append({
                'type': 'time_waste',
                'priority': 'medium',
                'suggestion': 'Reduce entertainment time',
                'reason': f'Spent {entertainment_time / 60:.1f} hours on entertainment in {days} days',
                'action': 'Set a daily limit of 1-2 hours for entertainment activities'
            })

        # Check for breaks
        breaks = [a for a in activities if a.get('category') == 'breaks']
        if len(breaks) < days * 3:  # Less than 3 breaks per day
            suggestions.append({
                'type': 'health',
                'priority': 'medium',
                'suggestion': 'Take more regular breaks',
                'reason': f'Only {len(breaks) / days:.1f} breaks per day on average',
                'action': 'Use Pomodoro technique: 25min work + 5min break'
            })

        return suggestions
