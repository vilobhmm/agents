# Time Tracker Multi-Agent System

> **Track every minute of your day with intelligent, multi-agent time tracking**

A comprehensive multi-agent system that helps you understand exactly how you spend your time. Get minute-level insights, automatic categorization, productivity analytics, and actionable recommendations.

## 🌟 Features

### **📊 Minute-Level Activity Tracking**
- Start/stop activities with one command
- Quick-log past activities
- Automatic gap detection
- Real-time activity monitoring

### **🏷️ Intelligent Categorization**
- Automatic category detection using AI
- Hierarchical categories (work, learning, health, etc.)
- Subcategory breakdown (meetings, deep work, exercise, etc.)
- Custom category support

### **📈 Advanced Analytics**
- Daily, weekly, and monthly reports
- Productivity scores (0-100)
- Peak productivity hour identification
- Time waste detection
- Focus metrics and deep work tracking
- Week-over-week comparisons

### **💡 Actionable Insights**
- Personalized improvement suggestions
- Time waster identification
- Productivity pattern analysis
- Focus and concentration metrics

### **📋 Comprehensive Reporting**
- Beautiful ASCII charts
- Daily summaries
- Weekly trends
- Productivity reports
- Export to JSON/CSV

## 🏗️ Architecture

The Time Tracker uses a **multi-agent architecture** with specialized agents:

1. **Activity Monitor Agent** - Tracks activities with minute-level granularity
2. **Categorizer Agent** - Organizes time into meaningful categories
3. **Analytics Agent** - Identifies patterns, trends, and insights
4. **Reporter Agent** - Generates reports and visualizations
5. **Time Tracker Coordinator** - Orchestrates all agents with a unified interface

## 🚀 Quick Start

### Basic Usage

```python
from agents.time_tracker import TimeTrackerCoordinator

# Initialize the tracker
tracker = TimeTrackerCoordinator()

# Start tracking an activity
await tracker.start_activity("Writing documentation")

# ... do your work ...

# Stop when done
await tracker.stop_activity()

# Get today's summary
print(await tracker.daily_report())
```

### Quick Logging

Log activities that you already completed:

```python
# Log a coffee break you took 30 minutes ago that lasted 15 minutes
await tracker.quick_log("Coffee break", minutes=15, minutes_ago=30)

# Log lunch
await tracker.quick_log("Lunch", minutes=45, minutes_ago=60)
```

### Check Current Activity

```python
# What am I currently working on?
current = await tracker.what_am_i_doing()
print(f"You're currently: {current['activity']}")
print(f"Duration so far: {current['current_duration_minutes']:.1f} minutes")
```

## 📖 Common Use Cases

### 1. Track Your Workday

```python
# Morning
await tracker.start_activity("Email triage", "work")
# ... 20 minutes later ...

await tracker.start_activity("Team standup meeting", "work")
# ... 15 minutes later ...

await tracker.start_activity("Deep work: Feature development", "work")
# ... 2 hours later ...

await tracker.start_activity("Lunch break", "breaks")
# ... and so on ...

# End of day - get your report
print(await tracker.daily_report())
```

### 2. Weekly Productivity Review

```python
# Get your productivity score for the week
score = await tracker.productivity_score(days=7)
print(f"Productivity Score: {score['productivity_score']}/100")

# See full weekly report
print(await tracker.weekly_report())

# Get insights and suggestions
insights = await tracker.get_insights(days=7)
for insight in insights:
    print(f"💡 {insight['suggestion']}")
    print(f"   Action: {insight['action']}")
```

### 3. Identify Time Wasters

```python
# Find activities that might be wasting your time
wasters = await tracker.time_wasters(days=7)

for waster in wasters:
    print(f"⚠️ {waster['activity']}")
    print(f"   Time spent: {waster['total_minutes'] / 60:.1f}h")
    print(f"   💡 {waster['recommendation']}")
```

### 4. Fill In Missing Time

```python
# Identify gaps in your tracking
gaps = await tracker.fill_gaps()

for gap in gaps:
    print(f"Gap: {gap['gap_start']} to {gap['gap_end']}")
    print(f"Duration: {gap['duration_minutes']:.0f} minutes")
    print(f"Suggestion: {gap['suggestion']}")
```

### 5. Analyze Productivity Patterns

```python
# When are you most productive?
patterns = await tracker.productivity_patterns(days=30)

print("Your peak productivity hours:")
for hour, minutes in patterns['peak_productivity_hours']:
    print(f"  {hour:02d}:00 - {minutes / 60:.1f}h of productive work")

print("\nMost productive days:")
for day, minutes in patterns['most_productive_days']:
    print(f"  {day}: {minutes / 60:.1f}h")
```

### 6. Export Your Data

```python
# Export to JSON
await tracker.export_json(days=90, file_path="my_time_data.json")

# Export to CSV for spreadsheet analysis
await tracker.export_csv(days=90, file_path="my_time_data.csv")

# Create a backup
await tracker.backup()
```

## 📊 Categories & Subcategories

The system uses hierarchical categories:

### **Work**
- `deep_work` - Focused, uninterrupted work
- `meetings` - Meetings, calls, collaborations
- `emails` - Email and communication
- `admin` - Administrative tasks, planning

### **Learning**
- `reading` - Books, articles, documentation
- `courses` - Online courses, tutorials
- `practice` - Hands-on practice
- `research` - Research and exploration

### **Health**
- `exercise` - Physical activity, workouts
- `meals` - Eating and meal preparation
- `sleep` - Rest and sleep
- `self_care` - Personal grooming, meditation

### **Personal**
- `errands` - Shopping, appointments
- `chores` - Cleaning, household tasks
- `social` - Time with friends and family

### **Entertainment**
- `leisure` - TV, movies, games
- `hobbies` - Creative hobbies
- `social_media` - Social media browsing

### **Breaks**
- `short_break` - Short breaks (< 15 min)
- `long_break` - Extended breaks
- `transition` - Context switching

## 🎯 API Reference

### Activity Logging

| Method | Description |
|--------|-------------|
| `start_activity(activity, category=None)` | Start tracking a new activity |
| `stop_activity()` | Stop the current activity |
| `quick_log(activity, minutes, minutes_ago=0)` | Log a past activity |
| `what_am_i_doing()` | Get current active activity |
| `get_today()` | Get all of today's activities |
| `fill_gaps()` | Find time gaps to fill in |

### Reports

| Method | Description |
|--------|-------------|
| `daily_report(date=None)` | Comprehensive daily report |
| `weekly_report(week_start=None)` | Weekly summary report |
| `productivity_report(days=7)` | Productivity-focused report |
| `chart(days=7)` | ASCII chart of time allocation |

### Analytics

| Method | Description |
|--------|-------------|
| `productivity_score(days=7)` | Get productivity score (0-100) |
| `time_wasters(days=7)` | Identify time-wasting activities |
| `get_insights(days=7)` | Get improvement suggestions |
| `productivity_patterns(days=30)` | Analyze productivity patterns |
| `focus_metrics(date=None)` | Focus and concentration metrics |
| `compare_weeks()` | Compare two weeks |

### Categorization

| Method | Description |
|--------|-------------|
| `breakdown(days=1)` | Category breakdown |
| `top_activities(days=7, limit=10)` | Top activities by time |
| `categories()` | Get available categories |

### Export

| Method | Description |
|--------|-------------|
| `export_json(days=30, file_path=None)` | Export to JSON |
| `export_csv(days=30, file_path=None)` | Export to CSV |
| `backup(backup_path=None)` | Create backup |
| `restore(backup_path)` | Restore from backup |
| `stats()` | Get storage statistics |

## 💾 Data Storage

Data is stored locally in `~/.time_tracker/` by default:
- `activities.json` - All activity records
- `metadata.json` - Tracking metadata

You can specify a custom directory:

```python
tracker = TimeTrackerCoordinator(data_dir="/path/to/data")
```

## 📈 Example Reports

### Daily Report

```
============================================================
DAILY TIME TRACKING REPORT
Date: 2026-03-02
============================================================

OVERVIEW
────────────────────────────────────────────────────────────
Total Time Tracked: 9.25 hours (555 minutes)
Number of Activities: 12
Average Activity Length: 46.3 minutes

CATEGORY BREAKDOWN
────────────────────────────────────────────────────────────
WORK                   5.50h (59.5%)
  ├─ deep_work          3.25h (59.1%)
  ├─ meetings           1.50h (27.3%)
  └─ emails             0.75h (13.6%)
BREAKS                 1.25h (13.5%)
LEARNING               1.00h (10.8%)
HEALTH                 0.75h ( 8.1%)
PERSONAL               0.75h ( 8.1%)

FOCUS METRICS
────────────────────────────────────────────────────────────
Deep Work Sessions: 3
Deep Work Time: 3.25 hours
Focus Score: 59.1%
Context Switches: 11
Average Session Length: 46.3 minutes

TOP ACTIVITIES
────────────────────────────────────────────────────────────
1. Feature development                            2.00h
2. Team standup meeting                           1.00h
3. Code review                                    1.25h
4. Documentation writing                          1.00h
5. Email triage                                   0.75h
============================================================
```

### Productivity Report

```
============================================================
PRODUCTIVITY REPORT
Period: Last 7 days
============================================================

PRODUCTIVITY SCORE: 78.5/100
────────────────────────────────────────────────────────────
Total Tracked Time: 52.50 hours
Productive Time: 41.21 hours

Breakdown:
  Highly Productive:     32.50h
  Moderately Productive: 12.25h
  Low Productivity:       7.75h

TIME WASTERS IDENTIFIED
────────────────────────────────────────────────────────────
🔴 Social media browsing
   Time spent: 5.2h
   💡 Consider reducing social media browsing time

🟡 Fragmented work sessions
   Time spent: 2.5h
   💡 Try to batch work into longer, focused sessions

IMPROVEMENT SUGGESTIONS
────────────────────────────────────────────────────────────
🔴 Increase deep work sessions (25+ minutes)
   Reason: Only 45.0% of work sessions are focused deep work
   Action: Try time-blocking 2-hour deep work sessions

🟡 Take more regular breaks
   Reason: Only 2.1 breaks per day on average
   Action: Use Pomodoro technique: 25min work + 5min break
============================================================
```

## 🔄 Integration Ideas

### Calendar Integration
```python
# Automatically import calendar events as activities
await tracker.activity_monitor.import_calendar_events()
```

### Pomodoro Timer
```python
# 25-minute focused work session
await tracker.start_activity("Deep work: Feature X", "work")
# ... work for 25 minutes ...
await tracker.stop_activity()

# 5-minute break
await tracker.start_activity("Pomodoro break", "breaks")
# ... break for 5 minutes ...
```

### End-of-Day Review
```python
# Automated end-of-day summary
daily = await tracker.daily_report()
focus = await tracker.focus_metrics()

# Send to yourself via email/Slack/etc.
print(daily)
print(f"\nFocus Score: {focus['focus_score']}/100")
```

## 🎓 Best Practices

1. **Track Consistently** - Log activities throughout the day, not just at the end
2. **Be Specific** - "Writing blog post" is better than "Writing"
3. **Use Categories** - Help the system learn your patterns
4. **Fill Gaps Daily** - Use `fill_gaps()` at end of day
5. **Review Weekly** - Check `weekly_report()` every Monday
6. **Act on Insights** - Review and act on `get_insights()`
7. **Backup Regularly** - Use `backup()` weekly

## 🤝 Tips for Success

- **Start small**: Just track for one day to get familiar
- **Be honest**: Track everything, including breaks and distractions
- **Review regularly**: Weekly reviews help identify patterns
- **Set goals**: Use insights to set productivity goals
- **Iterate**: Adjust categories and tracking based on what works for you

## 🔮 Advanced Features

### Compare Your Performance

```python
# Compare this week vs last week
print(await tracker.compare_weeks())
```

### Deep Productivity Analysis

```python
# 30-day analysis of when you're most productive
patterns = await tracker.productivity_patterns(days=30)

# Adjust your schedule based on peak hours
peak_hours = patterns['peak_productivity_hours']
print(f"Schedule deep work during: {peak_hours}")
```

### Focus Score Tracking

```python
# Track your focus score over time
for i in range(7):
    date = datetime.now() - timedelta(days=i)
    metrics = await tracker.focus_metrics(date)
    print(f"{date.date()}: Focus Score = {metrics['focus_score']}/100")
```

## 📱 Integration with Other Tools

The Time Tracker can integrate with:
- **Calendar** - Import events automatically
- **Task Managers** - Track time per task
- **Note Apps** - Log activities from notes
- **Slack/Teams** - Get daily summaries
- **Automation** - Trigger reports on schedule

## 🛠️ Troubleshooting

**Q: I forgot to log activities. What should I do?**
A: Use `quick_log()` to fill in past activities, then use `fill_gaps()` to find any remaining gaps.

**Q: How do I change a category?**
A: The system auto-categorizes, but you can manually categorize when starting an activity.

**Q: Can I track activities automatically?**
A: Currently manual tracking is required, but you can import calendar events.

**Q: How do I see my data?**
A: Use `export_json()` or `export_csv()` to export all your data.

## 📊 Sample Workflow

```python
# Morning routine
tracker = TimeTrackerCoordinator()

# Start your day
await tracker.start_activity("Morning email check", "work")

# Throughout the day
await tracker.start_activity("Feature development", "work")
await tracker.start_activity("Lunch", "breaks")
await tracker.start_activity("Code review", "work")
await tracker.start_activity("Learning: New framework", "learning")

# End of day review
print(await tracker.daily_report())
gaps = await tracker.fill_gaps()
if gaps:
    for gap in gaps:
        # Fill in missing time
        await tracker.quick_log("??", gap['duration_minutes'],
                               minutes_ago=gap['minutes_ago'])

# Weekly review (Mondays)
if datetime.now().weekday() == 0:
    print(await tracker.weekly_report())
    insights = await tracker.get_insights(days=7)
    # Review and act on insights
```

## 🎉 Get Started Now!

```python
from agents.time_tracker import TimeTrackerCoordinator

# Initialize
tracker = TimeTrackerCoordinator()

# Start tracking!
await tracker.start_activity("Building something awesome!")
```

## 📄 License

Part of the Multi-Agent System framework.

---

**Track your time. Understand your patterns. Optimize your productivity.** 🚀
