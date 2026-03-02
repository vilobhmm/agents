"""
Time Tracker Multi-Agent Coordinator

Orchestrates the activity monitor, categorizer, analytics, and reporter agents
to provide a comprehensive time tracking solution.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from agents.time_tracker.storage import StorageManager
from agents.time_tracker.activity_monitor.activity_monitor_agent import ActivityMonitorAgent
from agents.time_tracker.categorizer.categorizer_agent import CategorizerAgent
from agents.time_tracker.analytics.analytics_agent import AnalyticsAgent
from agents.time_tracker.reporter.reporter_agent import ReporterAgent


class TimeTrackerCoordinator:
    """
    Main coordinator for the Time Tracker multi-agent system.

    Provides a unified interface to all time tracking capabilities:
    - Activity logging and monitoring
    - Automatic categorization
    - Analytics and insights
    - Report generation
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the Time Tracker Coordinator.

        Args:
            data_dir: Directory to store data (defaults to ~/.time_tracker)
        """
        # Initialize storage
        self.storage = StorageManager(data_dir)

        # Initialize agents
        self.activity_monitor = ActivityMonitorAgent(self.storage)
        self.categorizer = CategorizerAgent(self.storage)
        self.analytics = AnalyticsAgent(self.storage)
        self.reporter = ReporterAgent(self.storage, self.categorizer, self.analytics)

    # ============================================================
    # ACTIVITY LOGGING
    # ============================================================

    async def start_activity(self, activity: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Start tracking a new activity.

        Args:
            activity: Description of what you're doing
            category: Optional category (will be auto-categorized if not provided)

        Returns:
            Activity start confirmation

        Example:
            >>> await tracker.start_activity("Writing documentation", "work")
        """
        # Auto-categorize if no category provided
        if category is None:
            category = await self.activity_monitor.auto_categorize_activity(activity)

        result = await self.activity_monitor.start_activity(activity, category)

        return {
            **result,
            'category': category,
            'tip': 'Activity started! Use stop_activity() when done, or start another activity to auto-stop this one.'
        }

    async def stop_activity(self) -> Optional[Dict[str, Any]]:
        """
        Stop the current activity.

        Returns:
            Completed activity record

        Example:
            >>> await tracker.stop_activity()
        """
        completed = await self.activity_monitor.end_current_activity()

        if completed:
            # Categorize if needed
            if not completed.get('category'):
                await self.categorizer.categorize_activity(completed)

        return completed

    async def quick_log(self, activity: str, minutes: int, minutes_ago: int = 0) -> Dict[str, Any]:
        """
        Quickly log a past activity.

        Args:
            activity: What you were doing
            minutes: How long it took
            minutes_ago: How many minutes ago it started (default: 0 = just now)

        Returns:
            Logged activity

        Example:
            >>> await tracker.quick_log("Coffee break", 15, minutes_ago=30)
        """
        logged = await self.activity_monitor.quick_log(activity, minutes_ago, minutes)

        # Auto-categorize
        logged = await self.categorizer.categorize_activity(logged)

        return logged

    async def what_am_i_doing(self) -> Optional[Dict[str, Any]]:
        """
        Get the current active activity.

        Returns:
            Current activity or None

        Example:
            >>> current = await tracker.what_am_i_doing()
        """
        return await self.activity_monitor.get_current_activity()

    # ============================================================
    # DAILY TRACKING
    # ============================================================

    async def get_today(self) -> List[Dict[str, Any]]:
        """
        Get all activities for today.

        Returns:
            List of today's activities

        Example:
            >>> today = await tracker.get_today()
        """
        return await self.activity_monitor.get_today_activities()

    async def fill_gaps(self) -> List[Dict[str, Any]]:
        """
        Identify time gaps that need to be filled in.

        Returns:
            List of time gaps

        Example:
            >>> gaps = await tracker.fill_gaps()
        """
        return await self.activity_monitor.suggest_missing_time()

    async def daily_report(self, date: Optional[datetime] = None) -> str:
        """
        Generate a comprehensive daily report.

        Args:
            date: Date to report on (defaults to today)

        Returns:
            Formatted text report

        Example:
            >>> print(await tracker.daily_report())
        """
        return await self.reporter.generate_daily_report(date)

    # ============================================================
    # WEEKLY TRACKING
    # ============================================================

    async def weekly_report(self, week_start: Optional[datetime] = None) -> str:
        """
        Generate a weekly summary report.

        Args:
            week_start: Start of week (defaults to current week)

        Returns:
            Formatted text report

        Example:
            >>> print(await tracker.weekly_report())
        """
        return await self.reporter.generate_weekly_report(week_start)

    async def weekly_trends(self, week_start: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get weekly trends and patterns.

        Args:
            week_start: Start of week (defaults to current week)

        Returns:
            Weekly trend data

        Example:
            >>> trends = await tracker.weekly_trends()
        """
        return await self.analytics.get_weekly_trends(week_start)

    # ============================================================
    # ANALYTICS & INSIGHTS
    # ============================================================

    async def productivity_score(self, days: int = 7) -> Dict[str, Any]:
        """
        Get your productivity score.

        Args:
            days: Number of days to analyze (default: 7)

        Returns:
            Productivity metrics and score

        Example:
            >>> score = await tracker.productivity_score()
            >>> print(f"Your productivity score: {score['productivity_score']}/100")
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.categorizer.get_productivity_score(start, end)

    async def time_wasters(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Identify activities that might be wasting time.

        Args:
            days: Number of days to analyze (default: 7)

        Returns:
            List of potential time wasters

        Example:
            >>> wasters = await tracker.time_wasters()
        """
        return await self.analytics.identify_time_wasters(days)

    async def productivity_report(self, days: int = 7) -> str:
        """
        Generate a detailed productivity report.

        Args:
            days: Number of days to analyze (default: 7)

        Returns:
            Formatted productivity report

        Example:
            >>> print(await tracker.productivity_report())
        """
        return await self.reporter.generate_productivity_report(days)

    async def get_insights(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get personalized improvement suggestions.

        Args:
            days: Number of days to analyze (default: 7)

        Returns:
            List of actionable suggestions

        Example:
            >>> insights = await tracker.get_insights()
        """
        return await self.analytics.suggest_improvements(days)

    # ============================================================
    # CATEGORIZATION
    # ============================================================

    async def breakdown(self, days: int = 1) -> Dict[str, Any]:
        """
        Get a breakdown of time by category.

        Args:
            days: Number of days to analyze (default: 1 = today)

        Returns:
            Category breakdown

        Example:
            >>> breakdown = await tracker.breakdown(days=7)
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.categorizer.get_category_breakdown(start, end)

    async def top_activities(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get your top activities by time spent.

        Args:
            days: Number of days to analyze (default: 7)
            limit: Number of top activities to return (default: 10)

        Returns:
            List of top activities

        Example:
            >>> top = await tracker.top_activities(days=30)
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.categorizer.get_top_activities(start, end, limit)

    async def categories(self) -> Dict[str, List[str]]:
        """
        Get available categories and subcategories.

        Returns:
            Category structure

        Example:
            >>> cats = await tracker.categories()
        """
        return await self.categorizer.suggest_categories()

    # ============================================================
    # PATTERNS & TRENDS
    # ============================================================

    async def productivity_patterns(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze your productivity patterns.

        Args:
            days: Number of days to analyze (default: 30)

        Returns:
            Pattern analysis including peak hours and days

        Example:
            >>> patterns = await tracker.productivity_patterns()
        """
        return await self.analytics.get_productivity_patterns(days)

    async def focus_metrics(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get focus and concentration metrics.

        Args:
            date: Date to analyze (defaults to today)

        Returns:
            Focus metrics

        Example:
            >>> focus = await tracker.focus_metrics()
        """
        return await self.analytics.get_focus_metrics(date)

    async def compare_weeks(self, week1_start: Optional[datetime] = None,
                           week2_start: Optional[datetime] = None) -> str:
        """
        Compare two weeks side by side.

        Args:
            week1_start: Start of first week (defaults to last week)
            week2_start: Start of second week (defaults to this week)

        Returns:
            Comparison report

        Example:
            >>> print(await tracker.compare_weeks())
        """
        if week2_start is None:
            today = datetime.now()
            week2_start = today - timedelta(days=today.weekday())

        if week1_start is None:
            week1_start = week2_start - timedelta(days=7)

        week1_end = week1_start + timedelta(days=7)
        week2_end = week2_start + timedelta(days=7)

        return await self.reporter.generate_comparison_report(
            week1_start, week1_end,
            week2_start, week2_end
        )

    # ============================================================
    # EXPORT & REPORTING
    # ============================================================

    async def export_json(self, days: int = 30, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Export data to JSON format.

        Args:
            days: Number of days to export (default: 30)
            file_path: Output file path (defaults to time_tracker_export.json)

        Returns:
            Export summary

        Example:
            >>> await tracker.export_json(days=90, file_path="my_data.json")
        """
        if file_path is None:
            file_path = f"time_tracker_export_{datetime.now().strftime('%Y%m%d')}.json"

        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.reporter.export_to_json(start, end, file_path)

    async def export_csv(self, days: int = 30, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Export data to CSV format.

        Args:
            days: Number of days to export (default: 30)
            file_path: Output file path (defaults to time_tracker_export.csv)

        Returns:
            Export summary

        Example:
            >>> await tracker.export_csv(days=90)
        """
        if file_path is None:
            file_path = f"time_tracker_export_{datetime.now().strftime('%Y%m%d')}.csv"

        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.reporter.export_to_csv(start, end, file_path)

    async def chart(self, days: int = 7) -> str:
        """
        Generate an ASCII chart of time allocation.

        Args:
            days: Number of days to chart (default: 7)

        Returns:
            ASCII chart string

        Example:
            >>> print(await tracker.chart())
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        return await self.reporter.get_time_allocation_chart(start, end)

    # ============================================================
    # STORAGE & MANAGEMENT
    # ============================================================

    async def stats(self) -> Dict[str, Any]:
        """
        Get storage and tracking statistics.

        Returns:
            Statistics summary

        Example:
            >>> stats = await tracker.stats()
        """
        return await self.storage.get_storage_stats()

    async def backup(self, backup_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a backup of all data.

        Args:
            backup_path: Backup file path (defaults to time_tracker_backup.json)

        Returns:
            Backup summary

        Example:
            >>> await tracker.backup()
        """
        if backup_path is None:
            backup_path = f"time_tracker_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        return await self.storage.export_backup(backup_path)

    async def restore(self, backup_path: str) -> Dict[str, Any]:
        """
        Restore data from a backup.

        Args:
            backup_path: Path to backup file

        Returns:
            Restore summary

        Example:
            >>> await tracker.restore("time_tracker_backup_20260302_120000.json")
        """
        return await self.storage.restore_from_backup(backup_path)
