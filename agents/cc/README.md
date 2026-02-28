# 🎯 CC Agent - Complete E2E Guide

**Your Personal AI Productivity Agent** (Inspired by Google Labs CC)

Get ahead of your day with personalized briefings, automated actions, and intelligent assistance.

---

## 🌟 What is CC?

**CC (Chief Coordinator)** is your personal AI productivity agent that:

- ☀️ Delivers **personalized morning briefings**
- 📧 Analyzes your **Gmail** for urgent emails
- 📅 Reviews your **Calendar** for today's schedule
- 📁 Tracks your **Drive** documents
- ✅ **Takes actions** (send emails, schedule meetings, block time)
- 🤝 **Coordinates other agents** for complex tasks

Think of CC as your AI Chief of Staff!

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Google Services

CC needs access to your Gmail, Calendar, and Drive.

```bash
# Follow the integration guide
cat QUICK_INTEGRATION_GUIDE.md

# Install dependencies
pip install google-auth-oauthlib google-api-python-client

# Configure OAuth credentials
export GOOGLE_OAUTH_CREDENTIALS_FILE="google_oauth_credentials.json"
export GOOGLE_TOKEN_FILE="google_token.pickle"
```

### Step 2: Start Agency

```bash
agency start
```

### Step 3: Get Your First Briefing

**Via Telegram:**
```
@cc Good morning briefing
```

**Via CLI:**
```bash
agency send "Good morning briefing" cc
```

---

## 📊 Morning Briefing

### What's Included

**📧 Email Summary**
- Total unread count
- Urgent emails (ASAP, deadline, action required)
- Important emails (meetings, reviews, approvals)
- Top 5 emails highlighted

**📅 Calendar Summary**
- Events today
- Next meeting with time
- Tomorrow's schedule
- Meeting conflicts

**📁 Drive Summary**
- Recently modified files
- Shared documents
- Documents by type (docs, sheets, slides)

**🎯 Priorities**
- Automatically identified from email + calendar
- Urgent items highlighted
- Deadlines flagged

**💡 Suggestions**
- Actionable next steps
- Time management tips
- Meeting preparation suggestions

---

## 💬 Using CC

### Get Morning Briefing

```
You: @cc Good morning briefing

CC: Good morning! Here's your daily briefing:

📧 Emails:
  • 12 unread
  • 🔴 3 urgent
  • ⭐ 5 important

📅 Calendar:
  • 4 events today
  • Next: Team Sync at 10:00 AM

📁 Drive:
  • 8 recently modified files

🎯 Priorities:
  • 🔴 3 urgent emails need immediate attention
  • 📅 Next meeting: Team Sync

💡 Suggestions:
  • Review urgent emails first
  • Prepare for Team Sync meeting
  • Block focus time between meetings
```

---

### Schedule Meetings

```
You: @cc Schedule meeting with Sarah tomorrow at 2pm

CC: I'll schedule that meeting.

Creating calendar event...
✅ Meeting scheduled: "Meeting with Sarah"
  📅 Tomorrow (Jan 16) at 2:00 PM
  ⏱️ Duration: 30 minutes
  📧 Calendar invite sent to Sarah

Want me to prepare a meeting brief?
```

**Advanced scheduling:**
```
@cc Schedule 1-hour meeting with John and Mike next Wednesday at 10am
@cc Reschedule tomorrow's 2pm meeting to Friday 3pm
@cc Find time for 30min meeting with team next week
```

---

### Send Emails

```
You: @cc Draft email to John about project update

CC: I'll draft that email.

[Reads recent context from Calendar and Drive]

Here's the draft:

---
To: John <john@company.com>
Subject: Project Update - Q1 Status

Hi John,

Hope you're well! Quick update on our Q1 project:

✅ Completed:
  - Phase 1 implementation
  - Initial testing

🚧 In Progress:
  - Performance optimization
  - Documentation

📅 Next:
  - Team review (scheduled Jan 18)
  - Launch prep

Let me know if you need any details!

Best,
[Your name]
---

Want me to:
1. Send it now
2. Save as draft
3. Revise something
```

**Quick sends:**
```
@cc Send thank you email to Sarah
@cc Reply to Mike's email - I approve
@cc Email team about meeting reschedule
```

---

### Block Focus Time

```
You: @cc Block 2 hours of focus time

CC: I'll block focus time on your calendar.

Looking for best time slot today...
✅ Blocked "Focus Time"
  📅 Today 2:00 PM - 4:00 PM
  📝 Calendar set to "Busy"
  🔕 Notifications will be muted

Enjoy your focused work!
```

---

### Ask Questions

```
# Calendar
@cc What's on my calendar today?
@cc When is my next meeting?
@cc Do I have any conflicts this week?

# Email
@cc Any urgent emails?
@cc Summarize emails from Sarah
@cc What needs my response?

# Drive
@cc Find the Q1 budget spreadsheet
@cc What documents were shared with me today?
@cc Show recent presentations
```

---

## 🤝 Team Coordination

CC can coordinate other agents for complex tasks!

### Example: Full Day Preparation

```
You: @cc_team Help me prepare for my day

CC: I'll coordinate the team.
  [@assistant: Check calendar and prioritize tasks]
  [@researcher: Get latest AI news for context]
  [@action_taker: Draft morning summary email]

[All agents work in parallel]

CC: Here's your day preparation:

📅 Calendar (from @assistant):
  • 4 meetings today
  • First: Team Sync at 10:00 AM
  • Gap: 2-4 PM (perfect for focus time)

🔍 Context (from @researcher):
  • Anthropic released Claude 4.5 yesterday
  • Your competitor launched new feature
  • Industry discussion about AI agents

✉️ Summary Email (from @action_taker):
  Draft ready to send to team

Want me to:
1. Send the summary email
2. Block that 2-4 PM focus time
3. Prepare brief for 10 AM meeting
```

---

## 🔄 Proactive Features

### Automatic Morning Briefings

Set up CC to automatically send briefings every morning!

**Using cron:**
```bash
# Edit crontab
crontab -e

# Add line (briefing at 8 AM every day)
0 8 * * * /home/user/agents/agency_bin send "Good morning briefing" cc
```

**Result:**
Every morning at 8 AM, you'll receive your personalized briefing via Telegram!

---

### Smart Alerts

CC can proactively alert you about:

- ⚠️ **Urgent emails** - New urgent email arrived
- ⏰ **Meeting reminders** - Meeting in 15 minutes
- 📅 **Schedule conflicts** - Double-booked meetings
- 📝 **Action items** - Deadline approaching
- 📊 **Daily summary** - End of day recap

---

## 📝 Real-World Examples

### Example 1: Complete Morning Routine

**8:00 AM - Automatic Briefing**
```
CC: Good morning! Here's your daily briefing:

📧 12 unread emails (3 urgent)
📅 4 meetings today
🎯 3 priorities identified

[Full briefing...]
```

**8:05 AM - Review Urgent**
```
You: @cc Show me the urgent emails

CC: Here are the 3 urgent emails:

1. 🔴 Sarah: "Budget approval needed by EOD"
2. 🔴 Mike: "Code review ASAP"
3. 🔴 HR: "Action required: Benefits deadline"

Want me to draft responses?
```

**8:10 AM - Quick Actions**
```
You: @cc Approve Sarah's budget and reply

CC: ✅ Email sent to Sarah approving budget
✅ Flagged for accounting review
✅ Added to calendar for follow-up
```

---

### Example 2: Meeting Preparation

**Before Meeting**
```
You: @cc Prepare me for the 10 AM Team Sync

CC: Here's your meeting brief:

📅 Team Sync - Today 10:00 AM
⏱️ Duration: 1 hour
👥 Attendees: Sarah, Mike, John

📋 Agenda (from invite):
  1. Q1 Progress Review
  2. Upcoming Milestones
  3. Blockers

📁 Relevant Documents:
  • Q1 Progress Report (you updated yesterday)
  • Project Timeline (shared by Sarah)
  • Sprint Notes (from last week)

📧 Recent Context:
  • Sarah asked about deadline extension
  • Mike flagged performance issue
  • John shared new mockups

💡 Suggested talking points:
  • Update on your tasks (3/5 complete)
  • Discuss Sarah's deadline concern
  • Address Mike's performance issue

Ready for your meeting!
```

---

### Example 3: Email Management

**Inbox Zero Flow**
```
You: @cc Help me get to inbox zero

CC: Let's tackle your inbox! 12 emails.

Urgent (3): Need immediate response
  [Shows list with quick action buttons]

Important (5): Need response today
  [Shows list]

FYI (4): No action needed, can archive

Want to:
1. Start with urgent
2. Bulk archive FYI
3. Schedule time for important
```

```
You: Start with urgent

CC: Email 1/3: Sarah's budget approval

[Shows email]

Quick actions:
1. Approve and reply
2. Decline with reason
3. Ask for more info
4. Defer to tomorrow
```

---

## ⚙️ Configuration

### Customize Briefing

Edit CC's personality in `agency/templates/agents.json`:

```json
{
  "cc": {
    "personality": "You are CC. Focus on: [customize here]",
    "preferences": {
      "briefing_time": "08:00",
      "email_priority": ["urgent", "important"],
      "calendar_lookahead_days": 2,
      "focus_time_duration": 120
    }
  }
}
```

### Privacy & Security

CC accesses your data locally:
- ✅ All processing happens on your machine
- ✅ No data sent to third parties
- ✅ You control all permissions
- ✅ Revoke access anytime

**Manage Google permissions:**
```bash
# View permissions
cat google_token.pickle

# Revoke access
rm google_token.pickle

# Re-authenticate
python -m openclaw.integrations.google_services
```

---

## 🎓 Tips & Best Practices

### Tip 1: Be Specific

❌ **Vague:** `@cc Help with emails`

✅ **Specific:** `@cc Draft response to Sarah's email about budget approval`

---

### Tip 2: Use Natural Language

CC understands natural requests:
- "Schedule meeting with Sarah next Tuesday afternoon"
- "Block focus time after lunch"
- "What's the most urgent thing right now?"
- "Draft thank you email to Mike"

---

### Tip 3: Set Expectations

Tell CC your preferences:
- "I prefer morning meetings"
- "Always ask before sending emails"
- "Prioritize emails from Sarah and Mike"
- "Keep responses concise"

---

### Tip 4: Combine Actions

```
@cc Schedule meeting with Sarah, draft agenda, and send invite
@cc Review urgent emails, draft responses, and ask before sending
@cc Block focus time and set reminder 5 minutes before
```

---

## 🐛 Troubleshooting

### CC Not Responding?

```bash
# Check if processor is running
agency status

# View logs
agency logs -f

# Restart
agency stop
agency start
```

### Google Authentication Issues?

```bash
# Re-authenticate
rm google_token.pickle
python -m openclaw.integrations.google_services

# Check credentials
cat google_oauth_credentials.json
```

### No Emails/Calendar Showing?

1. Check Google API permissions
2. Verify credentials file exists
3. Check API quotas (Google Cloud Console)
4. Review logs for errors

---

## 📚 See Also

- [CLI Commands](CLI_COMMANDS.md) - All commands
- [Integration Guide](../QUICK_INTEGRATION_GUIDE.md) - Google setup
- [Job Search Guide](JOB_SEARCH_GUIDE.md) - Job hunting with agents

---

## 💡 Feature Requests

Want new CC features?
- Daily/weekly summaries
- Smart scheduling suggestions
- Email templates
- Meeting notes automation
- Task tracking integration

Open an issue or build it yourself! CC is fully customizable.

---

**Get ahead of your day with CC!** ☀️✨