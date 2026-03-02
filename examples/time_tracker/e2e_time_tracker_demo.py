#!/usr/bin/env python3
"""
End-to-End Time Tracker Demo

This demo shows how to use the Time Tracker multi-agent system to:
1. Track activities throughout a day
2. Get insights and analytics
3. Generate reports
4. Identify productivity patterns
"""

import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.time_tracker import TimeTrackerCoordinator


async def simulate_workday(tracker):
    """Simulate tracking a full workday."""
    print("=" * 60)
    print("SIMULATING A WORKDAY")
    print("=" * 60)
    print()

    # Simulate activities from earlier in the day using quick_log
    print("📝 Logging morning activities...")

    # Morning routine (6 hours ago)
    await tracker.quick_log("Morning routine", minutes=30, minutes_ago=360)
    await tracker.quick_log("Email check", minutes=20, minutes_ago=330)
    await tracker.quick_log("Team standup meeting", minutes=15, minutes_ago=310)

    # Mid-morning work (4 hours ago)
    await tracker.quick_log("Feature development - Authentication", minutes=90, minutes_ago=295)
    await tracker.quick_log("Coffee break", minutes=10, minutes_ago=205)

    # Late morning (2 hours ago)
    await tracker.quick_log("Code review for PR #123", minutes=45, minutes_ago=195)
    await tracker.quick_log("Documentation writing", minutes=30, minutes_ago=150)
    await tracker.quick_log("Lunch break", minutes=45, minutes_ago=120)

    # Early afternoon (1 hour ago)
    await tracker.quick_log("Design discussion meeting", minutes=30, minutes_ago=75)
    await tracker.quick_log("Bug fixing", minutes=45, minutes_ago=45)

    print("✅ Morning and afternoon activities logged!")
    print()

    # Now simulate real-time tracking for current activity
    print("⏱️  Starting current activity...")
    await tracker.start_activity("Writing integration tests", "work")

    current = await tracker.what_am_i_doing()
    print(f"Current activity: {current['activity']}")
    print(f"Category: {current['category']}")
    print()

    # Check today's progress
    today_activities = await tracker.get_today()
    print(f"📊 Total activities tracked today: {len(today_activities)}")
    print()


async def demo_reports(tracker):
    """Demonstrate various report generation."""
    print("=" * 60)
    print("GENERATING REPORTS")
    print("=" * 60)
    print()

    # Daily report
    print("📋 DAILY REPORT")
    print("-" * 60)
    daily_report = await tracker.daily_report()
    print(daily_report)
    print()

    # Breakdown by category
    print("📊 CATEGORY BREAKDOWN")
    print("-" * 60)
    breakdown = await tracker.breakdown(days=1)
    for category, data in sorted(breakdown['categories'].items(),
                                 key=lambda x: x[1]['percentage'],
                                 reverse=True):
        print(f"{category:15s} {data['hours']:6.2f}h ({data['percentage']:5.1f}%)")
    print()

    # ASCII chart
    print("📈 TIME ALLOCATION CHART")
    print("-" * 60)
    chart = await tracker.chart(days=1)
    print(chart)
    print()


async def demo_analytics(tracker):
    """Demonstrate analytics and insights."""
    print("=" * 60)
    print("ANALYTICS & INSIGHTS")
    print("=" * 60)
    print()

    # Focus metrics
    print("🎯 FOCUS METRICS")
    print("-" * 60)
    focus = await tracker.focus_metrics()
    print(f"Deep Work Sessions: {focus['deep_work_sessions']}")
    print(f"Deep Work Time: {focus['deep_work_minutes'] / 60:.2f} hours")
    print(f"Focus Score: {focus['focus_score']:.1f}/100")
    print(f"Context Switches: {focus['context_switches']}")
    print(f"Average Session Length: {focus['average_session_length']:.1f} minutes")
    print()

    # Top activities
    print("🔝 TOP ACTIVITIES")
    print("-" * 60)
    top = await tracker.top_activities(days=1, limit=5)
    for i, activity in enumerate(top, 1):
        print(f"{i}. {activity['activity']:40s} {activity['total_hours']:.2f}h")
    print()

    # Productivity score
    print("📈 PRODUCTIVITY SCORE")
    print("-" * 60)
    score = await tracker.productivity_score(days=1)
    print(f"Score: {score['productivity_score']:.1f}/100")
    print(f"Productive Time: {score['productive_time_hours']:.2f}h")
    print()

    # Time wasters
    print("⚠️  TIME WASTERS")
    print("-" * 60)
    wasters = await tracker.time_wasters(days=1)
    if wasters:
        for waster in wasters:
            severity = "🔴" if waster['severity'] == 'high' else "🟡"
            print(f"{severity} {waster['activity']}")
            if waster.get('total_minutes'):
                print(f"   Time: {waster['total_minutes'] / 60:.1f}h")
            print(f"   💡 {waster['recommendation']}")
            print()
    else:
        print("No time wasters identified! 🎉")
    print()

    # Improvement suggestions
    print("💡 IMPROVEMENT SUGGESTIONS")
    print("-" * 60)
    insights = await tracker.get_insights(days=1)
    if insights:
        for i, insight in enumerate(insights, 1):
            priority = "🔴" if insight['priority'] == 'high' else "🟡"
            print(f"{priority} {insight['suggestion']}")
            print(f"   Reason: {insight['reason']}")
            print(f"   Action: {insight['action']}")
            print()
    else:
        print("Looking good! Keep up the great work! 🎉")
    print()


async def demo_gap_detection(tracker):
    """Demonstrate gap detection and filling."""
    print("=" * 60)
    print("GAP DETECTION")
    print("=" * 60)
    print()

    gaps = await tracker.fill_gaps()

    if gaps:
        print(f"Found {len(gaps)} time gaps to fill:")
        print()
        for i, gap in enumerate(gaps, 1):
            start = datetime.fromisoformat(gap['gap_start'])
            end = datetime.fromisoformat(gap['gap_end'])
            print(f"{i}. {start.strftime('%H:%M')} - {end.strftime('%H:%M')} "
                  f"({gap['duration_minutes']:.0f} minutes)")
            print(f"   💡 {gap['suggestion']}")
            print()
    else:
        print("No gaps found! All time is accounted for. 🎉")
        print()


async def demo_export(tracker):
    """Demonstrate data export."""
    print("=" * 60)
    print("DATA EXPORT")
    print("=" * 60)
    print()

    # Export to JSON
    print("📤 Exporting to JSON...")
    json_result = await tracker.export_json(days=1, file_path="time_tracker_demo_export.json")
    print(f"✅ Exported {json_result['activities_exported']} activities")
    print(f"   File: {json_result['file_path']}")
    print(f"   Total time: {json_result['total_time_hours']:.2f}h")
    print()

    # Export to CSV
    print("📤 Exporting to CSV...")
    csv_result = await tracker.export_csv(days=1, file_path="time_tracker_demo_export.csv")
    print(f"✅ Exported {csv_result['activities_exported']} activities")
    print(f"   File: {csv_result['file_path']}")
    print()

    # Create backup
    print("💾 Creating backup...")
    backup_result = await tracker.backup()
    print(f"✅ Backup created: {backup_result['backup_path']}")
    print(f"   Activities backed up: {backup_result['activities_backed_up']}")
    print()


async def demo_storage_stats(tracker):
    """Show storage statistics."""
    print("=" * 60)
    print("STORAGE STATISTICS")
    print("=" * 60)
    print()

    stats = await tracker.stats()

    print(f"Total Activities: {stats['total_activities']}")
    print(f"Total Time Tracked: {stats['total_time_tracked_hours']:.2f} hours")
    print(f"Data Directory: {stats['data_directory']}")
    print(f"Storage Created: {stats['storage_created']}")
    print(f"Last Updated: {stats['last_updated']}")

    if stats['earliest_activity']:
        earliest = datetime.fromisoformat(stats['earliest_activity'])
        latest = datetime.fromisoformat(stats['latest_activity'])
        print(f"Date Range: {earliest.date()} to {latest.date()}")

    print()


async def interactive_demo():
    """Run an interactive demo."""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "TIME TRACKER MULTI-AGENT DEMO" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Initialize tracker
    print("🚀 Initializing Time Tracker...")
    tracker = TimeTrackerCoordinator(data_dir="/tmp/time_tracker_demo")
    print("✅ Time Tracker initialized!")
    print()

    # Run demos
    await simulate_workday(tracker)

    input("Press Enter to see reports...")
    await demo_reports(tracker)

    input("Press Enter to see analytics...")
    await demo_analytics(tracker)

    input("Press Enter to check for time gaps...")
    await demo_gap_detection(tracker)

    input("Press Enter to export data...")
    await demo_export(tracker)

    input("Press Enter to see storage stats...")
    await demo_storage_stats(tracker)

    # Final summary
    print("=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print()
    print("✨ You've seen how to:")
    print("   • Track activities throughout the day")
    print("   • Generate comprehensive reports")
    print("   • Get productivity insights and analytics")
    print("   • Identify and fill time gaps")
    print("   • Export and backup your data")
    print()
    print("🚀 Start tracking your time with:")
    print("   from agents.time_tracker import TimeTrackerCoordinator")
    print("   tracker = TimeTrackerCoordinator()")
    print("   await tracker.start_activity('Your activity here')")
    print()


async def quick_demo():
    """Run a quick non-interactive demo."""
    print()
    print("🚀 TIME TRACKER QUICK DEMO")
    print("=" * 60)
    print()

    tracker = TimeTrackerCoordinator(data_dir="/tmp/time_tracker_demo")

    # Simulate a day
    await simulate_workday(tracker)
    await demo_reports(tracker)
    await demo_analytics(tracker)

    print("=" * 60)
    print("✨ Demo complete! Check the full README for more features.")
    print("=" * 60)
    print()


async def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        await quick_demo()
    else:
        await interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())
