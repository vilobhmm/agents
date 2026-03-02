"""
Reporter Agent

Generates various reports and visualizations:
- Daily/weekly/monthly reports
- Productivity reports
- Time allocation charts
- Export capabilities (CSV, JSON, text)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json


class ReporterAgent:
    """Agent for generating reports from time tracking data."""

    def __init__(self, storage_manager, categorizer_agent, analytics_agent):
        """
        Initialize the Reporter Agent.

        Args:
            storage_manager: Storage manager for accessing data
            categorizer_agent: Categorizer agent for category data
            analytics_agent: Analytics agent for insights
        """
        self.storage = storage_manager
        self.categorizer = categorizer_agent
        self.analytics = analytics_agent

    async def generate_daily_report(self, date: Optional[datetime] = None) -> str:
        """
        Generate a comprehensive daily report.

        Args:
            date: Date for the report (defaults to today)

        Returns:
            Formatted text report
        """
        if date is None:
            date = datetime.now()

        # Get data from other agents
        summary = await self.analytics.get_daily_summary(date)
        breakdown = await self.categorizer.get_category_breakdown(
            date.replace(hour=0, minute=0, second=0),
            date.replace(hour=23, minute=59, second=59)
        )
        focus_metrics = await self.analytics.get_focus_metrics(date)

        # Generate report
        report = f"""
{'='*60}
DAILY TIME TRACKING REPORT
Date: {summary['date']}
{'='*60}

OVERVIEW
{'−'*60}
Total Time Tracked: {summary['total_tracked_hours']:.2f} hours ({summary['total_tracked_minutes']:.0f} minutes)
Number of Activities: {summary['activity_count']}
Average Activity Length: {summary['average_activity_duration']:.1f} minutes

CATEGORY BREAKDOWN
{'−'*60}
"""

        # Add category breakdown
        for category, data in sorted(breakdown['categories'].items(),
                                    key=lambda x: x[1]['minutes'],
                                    reverse=True):
            report += f"{category.upper():20s} {data['hours']:6.2f}h ({data['percentage']:5.1f}%)\n"

            # Add subcategories if available
            if data.get('subcategories'):
                for subcat, subdata in data['subcategories'].items():
                    report += f"  ├─ {subcat:16s} {subdata['hours']:6.2f}h ({subdata['percentage']:5.1f}%)\n"

        report += f"""
FOCUS METRICS
{'−'*60}
Deep Work Sessions: {focus_metrics['deep_work_sessions']}
Deep Work Time: {focus_metrics['deep_work_minutes'] / 60:.2f} hours
Focus Score: {focus_metrics['focus_score']:.1f}%
Context Switches: {focus_metrics['context_switches']}
Average Session Length: {focus_metrics['average_session_length']:.1f} minutes

TOP ACTIVITIES
{'−'*60}
"""

        for i, (activity, minutes) in enumerate(summary['top_activities'], 1):
            report += f"{i}. {activity:40s} {minutes / 60:6.2f}h\n"

        if summary.get('most_productive_hour') is not None:
            report += f"""
INSIGHTS
{'−'*60}
Most Productive Hour: {summary['most_productive_hour']:02d}:00
"""

        report += f"\n{'='*60}\n"

        return report

    async def generate_weekly_report(self, week_start: Optional[datetime] = None) -> str:
        """
        Generate a weekly summary report.

        Args:
            week_start: Start of week (defaults to current week)

        Returns:
            Formatted text report
        """
        trends = await self.analytics.get_weekly_trends(week_start)

        report = f"""
{'='*60}
WEEKLY TIME TRACKING REPORT
Week: {trends['week_start']} to {trends['week_end']}
{'='*60}

WEEKLY OVERVIEW
{'−'*60}
Total Time Tracked: {trends['total_tracked_hours']:.2f} hours
Average Daily Time: {trends['average_daily_hours']:.2f} hours
Most Productive Day: {trends['most_productive_day']}

CATEGORY TOTALS
{'−'*60}
"""

        for category, minutes in sorted(trends['category_totals'].items(),
                                       key=lambda x: x[1],
                                       reverse=True):
            hours = minutes / 60
            report += f"{category.upper():20s} {hours:6.2f}h\n"

        report += f"""
DAILY BREAKDOWN
{'−'*60}
"""

        for day in trends['daily_breakdown']:
            report += f"\n{day['date']} - {day['total_tracked_hours']:.1f}h tracked\n"
            for cat, mins in sorted(day['category_breakdown'].items(),
                                  key=lambda x: x[1],
                                  reverse=True)[:3]:
                report += f"  • {cat}: {mins / 60:.1f}h\n"

        report += f"\n{'='*60}\n"

        return report

    async def generate_productivity_report(self, days: int = 7) -> str:
        """
        Generate a productivity-focused report.

        Args:
            days: Number of days to analyze

        Returns:
            Formatted text report
        """
        end = datetime.now()
        start = end - timedelta(days=days)

        productivity = await self.categorizer.get_productivity_score(start, end)
        time_wasters = await self.analytics.identify_time_wasters(days)
        suggestions = await self.analytics.suggest_improvements(days)

        report = f"""
{'='*60}
PRODUCTIVITY REPORT
Period: Last {days} days
{'='*60}

PRODUCTIVITY SCORE: {productivity['productivity_score']:.1f}/100
{'−'*60}
Total Tracked Time: {productivity['total_tracked_time'] / 60:.2f} hours
Productive Time: {productivity['productive_time_hours']:.2f} hours

Breakdown:
  Highly Productive:     {productivity['breakdown_by_productivity']['highly_productive'] / 60:.2f}h
  Moderately Productive: {productivity['breakdown_by_productivity']['moderately_productive'] / 60:.2f}h
  Low Productivity:      {productivity['breakdown_by_productivity']['low_productivity'] / 60:.2f}h

TIME WASTERS IDENTIFIED
{'−'*60}
"""

        if time_wasters:
            for i, waster in enumerate(time_wasters[:5], 1):
                severity_icon = "🔴" if waster['severity'] == 'high' else "🟡"
                report += f"{severity_icon} {waster['activity']}\n"
                if waster.get('total_minutes'):
                    report += f"   Time spent: {waster['total_minutes'] / 60:.1f}h\n"
                report += f"   💡 {waster['recommendation']}\n\n"
        else:
            report += "No major time wasters identified! Great job! 🎉\n"

        report += f"""
IMPROVEMENT SUGGESTIONS
{'−'*60}
"""

        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                priority_icon = "🔴" if suggestion['priority'] == 'high' else "🟡"
                report += f"{priority_icon} {suggestion['suggestion']}\n"
                report += f"   Reason: {suggestion['reason']}\n"
                report += f"   Action: {suggestion['action']}\n\n"
        else:
            report += "Keep up the great work! No major improvements needed.\n"

        report += f"\n{'='*60}\n"

        return report

    async def export_to_json(self, start: datetime, end: datetime,
                           file_path: str) -> Dict[str, Any]:
        """
        Export time tracking data to JSON file.

        Args:
            start: Start of export period
            end: End of export period
            file_path: Path to save JSON file

        Returns:
            Export summary
        """
        activities = await self.storage.get_activities_by_period(start, end)
        breakdown = await self.categorizer.get_category_breakdown(start, end)

        export_data = {
            'export_info': {
                'generated_at': datetime.now().isoformat(),
                'period_start': start.isoformat(),
                'period_end': end.isoformat()
            },
            'summary': breakdown,
            'activities': activities
        }

        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        return {
            'status': 'success',
            'file_path': file_path,
            'activities_exported': len(activities),
            'total_time_hours': breakdown['total_tracked_hours']
        }

    async def export_to_csv(self, start: datetime, end: datetime,
                          file_path: str) -> Dict[str, Any]:
        """
        Export time tracking data to CSV file.

        Args:
            start: Start of export period
            end: End of export period
            file_path: Path to save CSV file

        Returns:
            Export summary
        """
        activities = await self.storage.get_activities_by_period(start, end)

        # Create CSV content
        csv_lines = ['Activity,Category,Subcategory,Start Time,End Time,Duration (minutes)']

        for activity in activities:
            csv_lines.append(
                f'"{activity["activity"]}",'
                f'{activity.get("category", "uncategorized")},'
                f'{activity.get("subcategory", "")},'
                f'{activity["start_time"]},'
                f'{activity.get("end_time", "")},'
                f'{activity.get("duration_minutes", 0)}'
            )

        with open(file_path, 'w') as f:
            f.write('\n'.join(csv_lines))

        return {
            'status': 'success',
            'file_path': file_path,
            'activities_exported': len(activities)
        }

    async def get_time_allocation_chart(self, start: datetime, end: datetime) -> str:
        """
        Generate a simple ASCII chart of time allocation.

        Args:
            start: Start of period
            end: End of period

        Returns:
            ASCII chart string
        """
        breakdown = await self.categorizer.get_category_breakdown(start, end)

        chart = f"""
TIME ALLOCATION CHART
Period: {start.date()} to {end.date()}
{'−'*60}
"""

        max_percentage = max(
            (data['percentage'] for data in breakdown['categories'].values()),
            default=0
        )

        for category, data in sorted(breakdown['categories'].items(),
                                    key=lambda x: x[1]['percentage'],
                                    reverse=True):
            bar_length = int(data['percentage'] / 2)  # Scale to 50 chars max
            bar = '█' * bar_length

            chart += f"{category:15s} {bar} {data['percentage']:5.1f}% ({data['hours']:.1f}h)\n"

        return chart

    async def generate_comparison_report(self, period1_start: datetime, period1_end: datetime,
                                        period2_start: datetime, period2_end: datetime) -> str:
        """
        Generate a comparison report between two periods.

        Args:
            period1_start: Start of first period
            period1_end: End of first period
            period2_start: Start of second period
            period2_end: End of second period

        Returns:
            Formatted comparison report
        """
        comparison = await self.analytics.compare_periods(
            period1_start, period1_end,
            period2_start, period2_end
        )

        report = f"""
{'='*60}
PERIOD COMPARISON REPORT
{'='*60}

PERIOD 1: {period1_start.date()} to {period1_end.date()}
Total Time: {comparison['period1']['total_minutes'] / 60:.2f}h
Activities: {comparison['period1']['activity_count']}

PERIOD 2: {period2_start.date()} to {period2_end.date()}
Total Time: {comparison['period2']['total_minutes'] / 60:.2f}h
Activities: {comparison['period2']['activity_count']}

OVERALL CHANGE
{'−'*60}
Time Tracked: {comparison['total_time_change']['minutes'] / 60:+.2f}h ({comparison['total_time_change']['percentage']:+.1f}%)

CATEGORY CHANGES
{'−'*60}
"""

        for category, changes in sorted(comparison['category_changes'].items(),
                                       key=lambda x: abs(x[1]['change_minutes']),
                                       reverse=True):
            change_icon = "↑" if changes['change_minutes'] > 0 else "↓" if changes['change_minutes'] < 0 else "→"
            report += f"{category:15s} {change_icon} {changes['change_minutes'] / 60:+.2f}h ({changes['change_percentage']:+.1f}%)\n"
            report += f"  Period 1: {changes['period1_minutes'] / 60:.2f}h → Period 2: {changes['period2_minutes'] / 60:.2f}h\n\n"

        report += f"{'='*60}\n"

        return report
