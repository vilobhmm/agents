# 🚀 End-to-End Guide: Using CC Agent with Claude Code Skills

**Complete step-by-step guide from setup to advanced automation**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Testing Your First Skill](#testing-your-first-skill)
4. [Email Management Tutorial](#email-management-tutorial)
5. [Calendar Management Tutorial](#calendar-management-tutorial)
6. [Drive Management Tutorial](#drive-management-tutorial)
7. [Telegram Integration Tutorial](#telegram-integration-tutorial)
8. [Automation Workflows](#automation-workflows)
9. [Advanced Usage](#advanced-usage)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Need:

✅ **Google Account** with:
- Gmail enabled
- Google Calendar access
- Google Drive access

✅ **System Requirements:**
- Python 3.10+
- Git
- Terminal/Command line access

✅ **Optional (for Telegram):**
- Telegram account
- Telegram bot token

### Check Your Environment:

```bash
# Verify Python version
python --version  # Should be 3.10 or higher

# Verify Git
git --version

# Check if you're in the agents directory
pwd  # Should end with /agents
```

---

## Initial Setup

### Step 1: Clone and Navigate to Repository

```bash
# If not already cloned
git clone https://github.com/vilobhmm/agents.git
cd agents

# Switch to the skills branch
git checkout claude/openclaw-weekend-projects-st5pW
git pull
```

### Step 2: Verify Skills Installation

```bash
# List all available skills
ls -la .claude/skills/

# You should see 20+ executable skills:
# email-check, email-send, email-search
# cal-today, cal-week, next-meeting, cal-create
# drive-search, drive-recent
# productivity, morning-brief
# telegram-send
# (plus job hunting skills)
```

### Step 3: Make Skills Executable

```bash
# Ensure all skills are executable
chmod +x .claude/skills/*

# Verify permissions
ls -l .claude/skills/ | grep -v "^d"
# All files should start with -rwxr-xr-x
```

### Step 4: Set Up Environment Variables

```bash
# Check if .env file exists
ls -la .env

# If not, create it:
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
EOF

# Edit with your actual credentials
nano .env  # or vim .env, or code .env
```

### Step 5: Google OAuth Setup

**First Time Setup:**

```bash
# Run the Google authentication setup
cd ~/claude-code/github/agents  # or wherever your agents directory is

# Activate virtual environment if needed
source agents-venv/bin/activate

# Run authentication
python -m openclaw.integrations.unified_auth

# This will:
# 1. Open browser for Google OAuth
# 2. Ask you to authorize Gmail, Calendar, Drive access
# 3. Save credentials to google_token.pickle
```

**Verify Authentication:**

```bash
# Check if token file exists
ls -la google_token.pickle

# Should see a file with recent timestamp
```

---

## Testing Your First Skill

### Quick Test: Morning Brief

Let's start with the simplest skill:

```bash
# Test morning brief skill
.claude/skills/morning-brief
```

**What should happen:**

```
☀️ Good Morning! Preparing your daily briefing...
======================================================================

[Agent starts processing...]
[Shows unread email count]
[Shows today's calendar]
[Shows priorities]

✅ Done!
```

**If you see errors:**

```bash
# Common issues:

# 1. Permission denied
chmod +x .claude/skills/morning-brief

# 2. Google auth not set up
python -m openclaw.integrations.unified_auth

# 3. Agent not found
cd ~/claude-code/github/agents  # Make sure you're in the right directory
```

---

## Email Management Tutorial

### Lesson 1: Check Your Inbox

**Objective:** Check unread emails

```bash
# Basic inbox check
.claude/skills/email-check
```

**Expected Output:**
```
📧 Checking your inbox...
======================================================================

📬 You have 5 unread emails:

1. From: john@example.com
   Subject: Project Update
   Preview: Hi, here's the latest on...
   Time: 2 hours ago

2. From: boss@company.com
   Subject: Meeting Tomorrow
   Preview: Don't forget about...
   Time: 30 minutes ago

[...]
```

**Advanced Options:**

```bash
# Show only 10 emails
.claude/skills/email-check --count 10

# Show detailed view
.claude/skills/email-check --detailed
```

### Lesson 2: Search for Specific Emails

**Objective:** Find emails from a specific person

```bash
# Search by sender
.claude/skills/email-search "from:john@example.com"

# Search by subject
.claude/skills/email-search "subject:meeting"

# Search by date
.claude/skills/email-search "after:2026-02-01"

# Combine filters
.claude/skills/email-search "from:boss@company.com subject:urgent"
```

**Expected Output:**
```
🔍 Searching emails: from:john@example.com
======================================================================

Found 12 emails:

1. John Doe <john@example.com>
   Subject: Project Update
   Date: Feb 17, 2026
   [Preview of email content]

2. John Doe <john@example.com>
   Subject: Question about deadline
   Date: Feb 15, 2026
   [Preview of email content]

[...]
```

### Lesson 3: Send an Email

**Objective:** Send a quick email

```bash
# Method 1: Simple format
.claude/skills/email-send "recipient@example.com" "Subject Line" "Email body text"

# Method 2: Natural language
.claude/skills/email-send "Send email to john@example.com about project deadline saying we need 2 more days"

# Method 3: Draft an email
.claude/skills/email-send "Draft professional email to boss about vacation request for next week"
```

**What happens:**
```
📧 Sending email: Draft email to john@example.com...
======================================================================

📝 Composing email:
   To: john@example.com
   Subject: Project Deadline Extension Request
   Body: [AI-generated professional email]

✅ Email sent successfully!
```

**Practice Exercise:**

Try this complete email workflow:

```bash
# 1. Check inbox
.claude/skills/email-check

# 2. Search for emails from your boss
.claude/skills/email-search "from:boss@company.com"

# 3. Send a reply
.claude/skills/email-send "boss@company.com" "Re: Project Update" "Project is on track, will deliver by Friday"
```

---

## Calendar Management Tutorial

### Lesson 1: View Today's Calendar

**Objective:** See what's on your schedule today

```bash
# Basic view
.claude/skills/cal-today
```

**Expected Output:**
```
📅 Today's Calendar
======================================================================

Tuesday, February 17, 2026

Morning:
  9:00 AM - 10:00 AM: Team Standup
    Location: Conference Room A
    Attendees: Team Members

  10:30 AM - 11:30 AM: Client Call
    Location: Zoom (link: https://...)
    Attendees: Client Team, Sales

Afternoon:
  2:00 PM - 3:00 PM: 1-on-1 with Manager
    Location: Manager's Office

  4:00 PM - 5:00 PM: Project Review
    Location: Conference Room B

✅ 4 events today
```

**Advanced Options:**

```bash
# Detailed view with full descriptions
.claude/skills/cal-today --detailed
```

### Lesson 2: View Week's Calendar

**Objective:** See your entire week

```bash
# Current week
.claude/skills/cal-week

# Next week
.claude/skills/cal-week --next-week

# Detailed view
.claude/skills/cal-week --detailed
```

**Expected Output:**
```
📅 Week's Calendar
======================================================================

Week of February 17-23, 2026

Monday, Feb 17:
  - 9:00 AM: Team Standup
  - 2:00 PM: Client Meeting

Tuesday, Feb 18:
  - 10:00 AM: Project Review
  - 3:00 PM: 1-on-1

Wednesday, Feb 19:
  - All day: Focus Day (no meetings)

[...]
```

### Lesson 3: Get Next Meeting Details

**Objective:** Prepare for your next meeting

```bash
# Basic next meeting info
.claude/skills/next-meeting

# Full preparation mode
.claude/skills/next-meeting --prep
```

**Expected Output (with --prep):**
```
🔜 Next Meeting
======================================================================

📅 Team Standup
   Time: Today at 9:00 AM (in 15 minutes)
   Duration: 1 hour
   Location: Conference Room A

👥 Attendees:
   - Alice Johnson (alice@company.com)
   - Bob Smith (bob@company.com)
   - You

📋 Agenda:
   - Sprint updates
   - Blockers discussion
   - Next week planning

💡 Preparation Suggestions:
   - Review your sprint progress
   - Prepare blocker list
   - Have status update ready

🔍 Recent related emails:
   - "Sprint planning notes" from Alice (yesterday)
   - "Blocker: API issue" from Bob (this morning)

✅ You're ready for the meeting!
```

### Lesson 4: Create a Calendar Event

**Objective:** Schedule a new meeting

```bash
# Natural language event creation
.claude/skills/cal-create "Team meeting tomorrow at 2pm for 1 hour"

# With more details
.claude/skills/cal-create "Lunch with John on Friday at noon at Cafe Milano"

# Recurring event
.claude/skills/cal-create "Weekly standup every Monday at 9am for 30 minutes"
```

**Expected Output:**
```
📅 Creating calendar event: Team meeting tomorrow at 2pm for 1 hour
======================================================================

✅ Event created successfully!

📅 Team Meeting
   Date: Wednesday, February 18, 2026
   Time: 2:00 PM - 3:00 PM
   Duration: 1 hour

🔗 View in Calendar: [link]
```

**Practice Exercise:**

Try this complete calendar workflow:

```bash
# 1. Check today's schedule
.claude/skills/cal-today

# 2. Prepare for next meeting
.claude/skills/next-meeting --prep

# 3. Create a follow-up meeting
.claude/skills/cal-create "Follow-up meeting tomorrow at 3pm for 30 minutes"

# 4. View updated week
.claude/skills/cal-week
```

---

## Drive Management Tutorial

### Lesson 1: Search for Files

**Objective:** Find documents in your Google Drive

```bash
# Search by filename
.claude/skills/drive-search "project proposal"

# Search by type
.claude/skills/drive-search "type:pdf budget"

# Search by date
.claude/skills/drive-search "modified:2026"

# Combine filters
.claude/skills/drive-search "project type:spreadsheet modified:2026"
```

**Expected Output:**
```
🔍 Searching Google Drive: project proposal
======================================================================

Found 8 files:

📄 Project Proposal - Q1 2026.docx
   Modified: Feb 15, 2026
   Owner: You
   Link: https://drive.google.com/file/d/...

📊 Budget Proposal.xlsx
   Modified: Feb 10, 2026
   Owner: John Doe
   Shared with you
   Link: https://drive.google.com/file/d/...

[...]
```

### Lesson 2: View Recent Files

**Objective:** See what you've been working on

```bash
# Recent files (last 10)
.claude/skills/drive-recent

# More files
.claude/skills/drive-recent --count 20

# Only today's files
.claude/skills/drive-recent --today
```

**Expected Output:**
```
📁 Recent Google Drive Files
======================================================================

📄 Meeting Notes - Feb 17.docx
   Modified: 10 minutes ago
   Link: https://drive.google.com/file/d/...

📊 Q1 Budget Analysis.xlsx
   Modified: 1 hour ago
   Link: https://drive.google.com/file/d/...

📝 Project Status Report.pdf
   Modified: 2 hours ago
   Link: https://drive.google.com/file/d/...

[...]
```

**Practice Exercise:**

Try this Drive workflow:

```bash
# 1. Search for project files
.claude/skills/drive-search "project"

# 2. See what you worked on today
.claude/skills/drive-recent --today

# 3. Find all PDFs
.claude/skills/drive-search "type:pdf"
```

---

## Telegram Integration Tutorial

### Lesson 1: Set Up Telegram Bot

**Prerequisites:**

1. **Create Telegram Bot:**
```
1. Open Telegram
2. Search for @BotFather
3. Send: /newbot
4. Follow prompts to create bot
5. Copy the bot token (looks like: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)
```

2. **Get Your Chat ID:**
```
1. Start a chat with your new bot
2. Send any message
3. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
4. Find "chat":{"id":123456789} in the response
5. Copy the chat ID
```

3. **Update .env file:**
```bash
echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" >> .env
echo "TELEGRAM_CHAT_ID=your_chat_id_here" >> .env
```

### Lesson 2: Start Telegram Bot

```bash
# Start the bot
./start_agency.sh

# Or manually:
python -m agency.channels.telegram_bot
```

**Expected Output:**
```
🚀 Starting Agency System...

1️⃣ Starting message processor...
   ✅ Processor started

2️⃣ Starting Telegram bot...
   ✅ Bot started
   📱 Ready to receive messages
```

### Lesson 3: Use Telegram Commands

**On your phone/Telegram:**

```
# Send to your bot:
/start          # Get welcome message
/morning        # Daily briefing
/emails         # Check inbox
/calendar       # Today's schedule
/meeting        # Next meeting

# Or use natural language:
@cc Check my emails
@cc What's on my calendar today?
@cc Show me my next meeting
```

### Lesson 4: Send Messages from CLI to Telegram

**Objective:** Get notifications on your phone

```bash
# Basic notification
.claude/skills/telegram-send "Test notification"

# Build notification
.claude/skills/telegram-send "✅ Build completed successfully!"

# Status update
.claude/skills/telegram-send "📊 Daily report: All systems operational"
```

**What happens:**
- Message appears instantly on your phone in Telegram
- Can be used in scripts for notifications
- Perfect for automation alerts

**Practice Exercise:**

Create a simple notification script:

```bash
# Create notification script
cat > ~/notify-me.sh << 'EOF'
#!/bin/bash
MESSAGE="$1"
~/claude-code/github/agents/.claude/skills/telegram-send "$MESSAGE"
EOF

chmod +x ~/notify-me.sh

# Test it
~/notify-me.sh "Hello from my Mac!"
```

---

## Automation Workflows

### Workflow 1: Morning Startup Routine

**Objective:** Automate your morning routine

**Create the script:**

```bash
# Create morning routine
cat > ~/.claude/skills/my-morning << 'EOF'
#!/bin/bash
echo "☀️ Good morning! Starting your daily routine..."
echo ""

# 1. Daily briefing
echo "📋 Getting daily briefing..."
~/.claude/skills/morning-brief
echo ""

# 2. Check emails
echo "📧 Checking inbox..."
~/.claude/skills/email-check --count 10
echo ""

# 3. Today's calendar
echo "📅 Today's calendar..."
~/.claude/skills/cal-today
echo ""

# 4. Next meeting prep
echo "🔜 Next meeting preparation..."
~/.claude/skills/next-meeting --prep
echo ""

# 5. Recent files
echo "📁 Recent files..."
~/.claude/skills/drive-recent --count 5
echo ""

# 6. Send completion to Telegram
~/.claude/skills/telegram-send "✅ Morning routine complete!"

echo "✨ All done! Have a productive day!"
EOF

chmod +x ~/.claude/skills/my-morning
```

**Run it:**

```bash
~/.claude/skills/my-morning
```

**Automate it with cron:**

```bash
# Edit crontab
crontab -e

# Add this line to run every weekday at 8am:
0 8 * * 1-5 /Users/yourusername/.claude/skills/my-morning
```

### Workflow 2: Meeting Reminder System

**Objective:** Get reminded 10 minutes before meetings

**Create the script:**

```bash
cat > ~/.claude/skills/meeting-reminder << 'EOF'
#!/bin/bash

# Get next meeting details
MEETING_INFO=$(~/.claude/skills/next-meeting 2>&1)

# Send to Telegram
~/.claude/skills/telegram-send "⏰ Meeting in 10 minutes!\n\n$MEETING_INFO"
EOF

chmod +x ~/.claude/skills/meeting-reminder
```

**Set up cron to run every hour at :50:**

```bash
crontab -e

# Add:
50 * * * * /Users/yourusername/.claude/skills/meeting-reminder
```

### Workflow 3: Build Notification System

**Objective:** Get notified when builds complete

**In your build script:**

```bash
#!/bin/bash
# build.sh

echo "Starting build..."

if npm run build; then
  ~/.claude/skills/telegram-send "✅ Build succeeded!"
  ~/.claude/skills/telegram-send "Build completed at $(date)"
else
  ~/.claude/skills/telegram-send "❌ Build failed!"
  ~/.claude/skills/telegram-send "Check logs at ~/build.log"
fi
```

### Workflow 4: End-of-Day Summary

**Objective:** Get daily summary

```bash
cat > ~/.claude/skills/eod-summary << 'EOF'
#!/bin/bash

echo "📊 Generating end-of-day summary..."

# Get productivity dashboard
SUMMARY=$(~/.claude/skills/productivity 2>&1)

# Send to Telegram
~/.claude/skills/telegram-send "📊 End of Day Summary:\n\n$SUMMARY"

# Also save to file
echo "$SUMMARY" > ~/eod-summary-$(date +%Y-%m-%d).txt
EOF

chmod +x ~/.claude/skills/eod-summary

# Run daily at 6pm
crontab -e
# Add:
0 18 * * 1-5 /Users/yourusername/.claude/skills/eod-summary
```

### Workflow 5: Email Monitoring

**Objective:** Monitor for urgent emails

```bash
cat > ~/.claude/skills/urgent-email-monitor << 'EOF'
#!/bin/bash

# Search for urgent emails
URGENT=$(~/.claude/skills/email-search "is:unread is:important" 2>&1)

# If found, alert via Telegram
if echo "$URGENT" | grep -q "Found"; then
  ~/.claude/skills/telegram-send "🚨 URGENT EMAIL ALERT:\n\n$URGENT"
fi
EOF

chmod +x ~/.claude/skills/urgent-email-monitor

# Run every 15 minutes during work hours
crontab -e
# Add:
*/15 9-18 * * 1-5 /Users/yourusername/.claude/skills/urgent-email-monitor
```

---

## Advanced Usage

### Create Custom Skills

**Example: Custom weekly report skill**

```bash
cat > ~/.claude/skills/weekly-report << 'EOF'
#!/usr/bin/env python3
"""Generate weekly report"""

import subprocess
import sys

message = """
Generate a comprehensive weekly report with:

1. Emails sent and received this week
2. Meetings attended (count and list)
3. Files created or modified
4. Calendar for next week
5. Action items and priorities

Format as a professional summary.
"""

subprocess.run([
    "python", "-m", "agency", "debug", "test", "cc",
    "--message", message
], cwd="/home/user/agents")
EOF

chmod +x ~/.claude/skills/weekly-report

# Run it
~/.claude/skills/weekly-report
```

### Create Aliases for Faster Access

**Add to ~/.bashrc or ~/.zshrc:**

```bash
# Email aliases
alias ec='~/.claude/skills/email-check'
alias es='~/.claude/skills/email-search'
alias em='~/.claude/skills/email-send'

# Calendar aliases
alias ct='~/.claude/skills/cal-today'
alias cw='~/.claude/skills/cal-week'
alias nm='~/.claude/skills/next-meeting'
alias cc='~/.claude/skills/cal-create'

# Drive aliases
alias ds='~/.claude/skills/drive-search'
alias dr='~/.claude/skills/drive-recent'

# Dashboard aliases
alias pd='~/.claude/skills/productivity'
alias mb='~/.claude/skills/morning-brief'

# Telegram alias
alias tg='~/.claude/skills/telegram-send'

# Custom workflows
alias morning='~/.claude/skills/my-morning'
alias eod='~/.claude/skills/eod-summary'
```

**Reload shell:**

```bash
source ~/.bashrc  # or source ~/.zshrc
```

**Now use short commands:**

```bash
ec              # Check emails
ct              # Today's calendar
nm --prep       # Next meeting
tg "Hello!"     # Send to Telegram
morning         # Morning routine
```

### Integration with Other Tools

**Example: Integrate with tmux**

```bash
# Add to tmux status bar
# In ~/.tmux.conf:

set -g status-right '#(~/.claude/skills/next-meeting | head -1)'
```

**Example: Alfred/Spotlight Integration**

Create Quick Actions that run skills:

```bash
# Create Alfred workflow
# Command: ~/.claude/skills/email-check
# Keyword: emails
```

---

## Troubleshooting

### Issue 1: "Permission Denied"

**Error:**
```
-bash: .claude/skills/email-check: Permission denied
```

**Solution:**
```bash
chmod +x .claude/skills/*
```

### Issue 2: "Google Auth Failed"

**Error:**
```
❌ Error: Could not authenticate with Google
```

**Solution:**
```bash
# Re-run authentication
cd ~/claude-code/github/agents
python -m openclaw.integrations.unified_auth

# Follow browser prompts
# Make sure to authorize all requested permissions
```

### Issue 3: "Agent Not Found"

**Error:**
```
❌ Error: Could not find agency module
```

**Solution:**
```bash
# Make sure you're in the right directory
cd ~/claude-code/github/agents

# Or update the skill to use absolute path
# Edit the skill file and change:
cwd="/home/user/agents"
# To your actual agents directory
```

### Issue 4: "Telegram Not Sending"

**Error:**
```
❌ Error: TELEGRAM_CHAT_ID not set
```

**Solution:**
```bash
# Check environment variable
echo $TELEGRAM_CHAT_ID

# If empty, add to .env:
echo "TELEGRAM_CHAT_ID=your_chat_id" >> .env

# Or export directly:
export TELEGRAM_CHAT_ID="your_chat_id"
```

### Issue 5: "No Emails Found" (but you have emails)

**Solution:**
```bash
# Check if token is valid
ls -la google_token.pickle

# Re-authenticate
python -m openclaw.integrations.unified_auth

# Test with Gmail API directly
python -c "
from openclaw.integrations.email import GmailAPI
gmail = GmailAPI()
print(gmail.get_unread_emails(max_results=5))
"
```

### Issue 6: Skills Work but Telegram Bot Doesn't

**Solution:**
```bash
# Check if bot is running
ps aux | grep telegram

# Restart the bot
./start_agency.sh

# Or manually:
python -m agency.channels.telegram_bot
```

### Issue 7: "Rate Limit Exceeded"

**Error:**
```
❌ Error: Gmail API rate limit exceeded
```

**Solution:**
```bash
# Wait a few minutes and try again
# Gmail API has quotas:
# - 250 queries per second
# - 1 billion quota units per day

# Reduce frequency of automated checks
# Edit crontab to run less often
```

---

## Best Practices

### 1. Start Simple

```bash
# Day 1: Just try basic skills
.claude/skills/email-check
.claude/skills/cal-today

# Day 2: Add morning routine
~/.claude/skills/my-morning

# Day 3: Add Telegram integration
~/.claude/skills/telegram-send "Test"

# Day 4: Create custom workflows
```

### 2. Use Aliases

```bash
# Makes daily usage much faster
ec          # vs .claude/skills/email-check
ct          # vs .claude/skills/cal-today
nm --prep   # vs .claude/skills/next-meeting --prep
```

### 3. Automate Gradually

```bash
# Don't automate everything at once
# Start with one workflow (e.g., morning routine)
# Add more as you get comfortable
```

### 4. Monitor Your Automation

```bash
# Keep logs of automated runs
~/.claude/skills/my-morning >> ~/automation.log 2>&1

# Review periodically
tail -f ~/automation.log
```

### 5. Respect API Limits

```bash
# Don't run skills too frequently
# Recommended intervals:
# - Email check: Every 15-30 minutes
# - Calendar: Every hour
# - Drive: On demand
```

---

## Quick Reference Card

```bash
# ══════════════════════════════════════════════════════════
# PRODUCTIVITY SKILLS QUICK REFERENCE
# ══════════════════════════════════════════════════════════

# EMAIL
ec                              # Check inbox
es "from:boss"                  # Search emails
em "to@example.com" "Hi" "Msg"  # Send email

# CALENDAR
ct                              # Today's events
cw                              # Week's events
nm --prep                       # Next meeting + prep
cc "Meeting tomorrow 2pm"       # Create event

# DRIVE
ds "project proposal"           # Search files
dr --today                      # Today's files

# DASHBOARD
pd                              # Productivity overview
mb                              # Morning briefing

# TELEGRAM
tg "Message"                    # Send to Telegram

# CUSTOM WORKFLOWS
morning                         # Morning routine
eod                            # End of day summary

# ══════════════════════════════════════════════════════════
```

---

## Conclusion

You now have a complete productivity system powered by Claude Code skills!

**What you learned:**
- ✅ Email management (check, search, send)
- ✅ Calendar management (view, create, prepare)
- ✅ Drive management (search, recent files)
- ✅ Telegram integration (notifications, mobile access)
- ✅ Automation workflows (morning routine, reminders)
- ✅ Advanced customization (aliases, custom skills)

**Next Steps:**
1. Create your own custom skills
2. Build personalized workflows
3. Share your automations with the team
4. Explore job hunting skills (see CLAUDE_SKILLS_GUIDE.md)

**Need Help?**
- 📖 [Productivity Guide](PRODUCTIVITY_SKILLS_GUIDE.md)
- 📖 [Skills README](.claude/skills/README.md)
- 📖 [Quick Start](.claude/skills/QUICKSTART.md)
- 🐛 [Report Issues](https://github.com/vilobhmm/agents/issues)

---

**Happy automating! 🚀**

*Your productivity is now powered by AI!*
