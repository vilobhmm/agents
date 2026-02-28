# 📱 Telegram + CC Agent Integration Guide

**Complete guide to using CC productivity features via Telegram and CLI**

---

## 🎯 Overview

This guide shows you how to use the **same CC agent** from **both Telegram and CLI**, giving you:

- **📱 Mobile Access** - Use CC from anywhere via Telegram
- **🖥️ Desktop Power** - Use CLI skills for automation
- **🔄 Seamless Integration** - Same backend, different interfaces
- **🔔 Notifications** - Get alerts on your phone

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Telegram Bot Setup](#telegram-bot-setup)
3. [Using CC via Telegram](#using-cc-via-telegram)
4. [Using CC via CLI](#using-cc-via-cli)
5. [Bidirectional Integration](#bidirectional-integration)
6. [Automation Examples](#automation-examples)
7. [Advanced Workflows](#advanced-workflows)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### What You'll Get:

**Via Telegram:**
```
/morning        → Daily briefing
/emails         → Check inbox
/calendar       → Today's schedule
/meeting        → Next meeting
@cc [question]  → Natural language queries
```

**Via CLI:**
```bash
.claude/skills/morning-brief     → Same daily briefing
.claude/skills/email-check       → Same inbox check
.claude/skills/cal-today         → Same schedule
.claude/skills/next-meeting      → Same meeting info
.claude/skills/telegram-send     → Send TO Telegram
```

**The Magic:**
- Same CC agent
- Same Google account data
- Different interfaces!

---

## Telegram Bot Setup

### Step 1: Create Your Telegram Bot

**On Telegram:**

```
1. Open Telegram app
2. Search for: @BotFather
3. Start a chat
4. Send: /newbot
5. Choose a name (e.g., "My CC Assistant")
6. Choose a username (e.g., "my_cc_bot")
7. Copy the bot token
```

**Expected Response:**
```
Done! Congratulations on your new bot!

Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

Keep your token secure and store it safely.
```

### Step 2: Get Your Chat ID

**Method 1: Using curl**

```bash
# Replace YOUR_BOT_TOKEN with your actual token
curl -s "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates"

# Send a message to your bot first, then run the command
# Look for "chat":{"id":123456789}
# That number is your chat ID
```

**Method 2: Using Telegram**

```
1. Search for: @userinfobot
2. Start a chat
3. It will tell you your user ID
4. That's your chat ID
```

### Step 3: Configure Environment

**Add to `.env` file:**

```bash
cd ~/claude-code/github/agents

# Create or edit .env
cat >> .env << 'EOF'

# Telegram Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
TELEGRAM_CHAT_ID=123456789
EOF
```

**Verify:**

```bash
cat .env | grep TELEGRAM
# Should show:
# TELEGRAM_BOT_TOKEN=...
# TELEGRAM_CHAT_ID=...
```

### Step 4: Start the Bot

**Option 1: Using start script (recommended)**

```bash
cd ~/claude-code/github/agents
./start_agency.sh
```

**Expected Output:**
```
🚀 Starting Agency System...

1️⃣ Starting message processor...
   ✅ Processor started (PID: 12345)
   📋 Logs: ~/.agency/logs/processor.log

2️⃣ Starting Telegram bot...
   Bot will poll for messages and send responses
   Press Ctrl+C to stop

✅ Telegram bot started
📱 Ready to receive messages!
```

**Option 2: Manual start**

```bash
cd ~/claude-code/github/agents
python -m agency.channels.telegram_bot
```

### Step 5: Test Your Bot

**On Telegram:**

```
1. Find your bot (search for the username you created)
2. Click "Start"
3. Send: /start
```

**Expected Response:**
```
👋 Hi [Your Name]!

🤖 Your Proactive AI Multi-Agent Team

I coordinate powerful AI agents to keep you ahead of your day!

**🌟 CC Agent (Productivity):**
• /morning - Daily briefing 📋
• /emails - Check inbox 📧
• /calendar - Today's schedule 📅
• /meeting - Next meeting prep 🔜

**💼 Job Hunter (Career):**
• /jobs - Quick job search 🔍
• /jobsearch [query] - Custom search 🎯
• /trackjobs - Tracked jobs 📊
• /applications - Your applications 📝

**🔧 System:**
• /help - Full command list
• /agents - Available agents
• /status - System status

**💬 Or just chat naturally:**
`@cc What's on my calendar?`
`@job_hunter Find Java jobs at TCS`

Type /help for more details! 🚀
```

---

## Using CC via Telegram

### Basic Commands

#### `/morning` or `/briefing` - Daily Briefing

**Send:**
```
/morning
```

**Response:**
```
☀️ Good Morning!

📧 INBOX: 5 unread emails
   • boss@company.com: "Project Update"
   • client@example.com: "Meeting Reschedule"
   • ...

📅 TODAY'S SCHEDULE: 3 events
   9:00 AM - Team Standup
   2:00 PM - Client Call
   4:00 PM - 1-on-1 with Manager

🔜 NEXT MEETING: Team Standup (in 30 min)
   Conference Room A

📁 RECENT FILES:
   • Project Proposal.docx (10 min ago)
   • Budget 2026.xlsx (1 hour ago)

✅ You're all set for the day!
```

#### `/emails` - Check Inbox

**Send:**
```
/emails
```

**Response:**
```
📧 You have 5 unread emails:

1. From: boss@company.com
   Subject: Project Update
   Time: 30 minutes ago
   Preview: Hi team, here's the latest...

2. From: client@example.com
   Subject: Meeting Tomorrow
   Time: 1 hour ago
   Preview: Can we reschedule to...

[...]
```

#### `/calendar` - Today's Schedule

**Send:**
```
/calendar
```

**Response:**
```
📅 Tuesday, February 17, 2026

Morning:
  9:00 AM - Team Standup
    Location: Conference Room A

  10:30 AM - Client Call
    Location: Zoom
    Link: https://zoom.us/...

Afternoon:
  2:00 PM - Project Review
    Location: Conference Room B

  4:00 PM - 1-on-1
    Location: Manager's Office

✅ 4 events today
```

#### `/meeting` - Next Meeting

**Send:**
```
/meeting
```

**Response:**
```
🔜 Next Meeting

📅 Team Standup
   Today at 9:00 AM (in 15 minutes)
   Duration: 1 hour
   Location: Conference Room A

👥 Attendees:
   • Alice Johnson
   • Bob Smith
   • You

💡 Prepare:
   - Sprint updates
   - Blockers
   - Next week planning

✅ You're ready!
```

### Natural Language Queries

#### Email Queries

```
@cc Check my emails
@cc Search emails from boss
@cc Show emails from yesterday
@cc Send email to john@example.com about the meeting
```

**Example:**
```
You: @cc Search emails from boss

Bot: 🔍 Found 3 emails from boss@company.com:

1. "Project Update" - 30 min ago
   Preview: Hi team, the project is...

2. "Budget Approval" - 2 hours ago
   Preview: I've approved the budget...

3. "Team Meeting" - Yesterday
   Preview: Don't forget the team...
```

#### Calendar Queries

```
@cc What's on my calendar today?
@cc Show me this week's meetings
@cc Create meeting tomorrow at 2pm
@cc When is my next meeting?
```

**Example:**
```
You: @cc Create meeting tomorrow at 2pm with Alice

Bot: ✅ Event created!

📅 Meeting with Alice
   Date: Wednesday, Feb 18
   Time: 2:00 PM - 3:00 PM

Added to your calendar!
```

#### Drive Queries

```
@cc Find project proposal
@cc Show recent files
@cc Search for budget spreadsheet
```

**Example:**
```
You: @cc Find project proposal

Bot: 📁 Found 3 files:

1. Project Proposal Q1 2026.docx
   Modified: Feb 15
   Link: https://drive.google.com/...

2. Budget Proposal.xlsx
   Modified: Feb 10
   Link: https://drive.google.com/...

3. Proposal Draft.pdf
   Modified: Jan 30
   Link: https://drive.google.com/...
```

---

## Using CC via CLI

### Basic Skills

All Telegram commands have CLI equivalents:

```bash
# Morning briefing
.claude/skills/morning-brief

# Check emails
.claude/skills/email-check

# Today's calendar
.claude/skills/cal-today

# Next meeting
.claude/skills/next-meeting --prep

# Search Drive
.claude/skills/drive-search "project proposal"
```

### Advanced CLI Features

#### Email Management

```bash
# Check inbox with count
.claude/skills/email-check --count 10

# Search emails
.claude/skills/email-search "from:boss@company.com"

# Send email
.claude/skills/email-send "john@example.com" "Meeting" "Tomorrow 2pm?"
```

#### Calendar Management

```bash
# Today's calendar
.claude/skills/cal-today

# Week's calendar
.claude/skills/cal-week

# Next week
.claude/skills/cal-week --next-week

# Create event
.claude/skills/cal-create "Team meeting tomorrow at 2pm"
```

#### Drive Management

```bash
# Search files
.claude/skills/drive-search "project proposal"

# Recent files
.claude/skills/drive-recent

# Today's files only
.claude/skills/drive-recent --today
```

---

## Bidirectional Integration

### CLI → Telegram Notifications

**Send notifications from CLI to Telegram:**

```bash
# Basic notification
.claude/skills/telegram-send "Hello from CLI!"

# Build notification
.claude/skills/telegram-send "✅ Build completed"

# Status update
.claude/skills/telegram-send "📊 Backup completed successfully"
```

**Use in scripts:**

```bash
#!/bin/bash
# backup.sh

if backup_database; then
  .claude/skills/telegram-send "✅ Database backup complete"
else
  .claude/skills/telegram-send "❌ Backup failed! Check logs"
fi
```

### Telegram → CLI Automation

**Trigger CLI actions from Telegram:**

While the bot is running, Telegram messages trigger the same agent that CLI uses, so:

```
Telegram: @cc Check emails
           ↓
        CC Agent
           ↓
      Gmail API
           ↓
    Response to Telegram
```

Same as:

```bash
CLI: .claude/skills/email-check
           ↓
        CC Agent
           ↓
      Gmail API
           ↓
    Response to CLI
```

---

## Automation Examples

### Example 1: Morning Routine with Telegram Notification

**Create script:**

```bash
cat > ~/morning-routine.sh << 'EOF'
#!/bin/bash

# Run morning briefing
BRIEFING=$(~/.claude/skills/morning-brief 2>&1)

# Send to Telegram
~/.claude/skills/telegram-send "☀️ Morning Briefing:\n\n$BRIEFING"

# Check urgent emails
URGENT=$(~/.claude/skills/email-search "is:important is:unread" 2>&1)

if echo "$URGENT" | grep -q "Found"; then
  ~/.claude/skills/telegram-send "🚨 URGENT EMAILS:\n\n$URGENT"
fi
EOF

chmod +x ~/morning-routine.sh
```

**Automate with cron:**

```bash
crontab -e

# Add:
0 8 * * 1-5 /Users/yourusername/morning-routine.sh
```

**What happens:**
- Every weekday at 8am
- Runs morning briefing
- Sends to Telegram
- Checks for urgent emails
- Alerts if found

### Example 2: Meeting Reminders via Telegram

**Create script:**

```bash
cat > ~/meeting-reminder.sh << 'EOF'
#!/bin/bash

# Get next meeting
MEETING=$(~/.claude/skills/next-meeting 2>&1)

# Check if meeting is within 10 minutes
if echo "$MEETING" | grep -q "in 10 minutes\|in 9 minutes\|in 8 minutes"; then
  ~/.claude/skills/telegram-send "⏰ MEETING SOON!\n\n$MEETING"
fi
EOF

chmod +x ~/meeting-reminder.sh
```

**Automate:**

```bash
crontab -e

# Run every 5 minutes during work hours
*/5 9-18 * * 1-5 /Users/yourusername/meeting-reminder.sh
```

### Example 3: Build Notifications

**In your CI/CD or build script:**

```bash
#!/bin/bash
# build.sh

echo "🔨 Starting build..."

if npm run build; then
  # Send success to Telegram
  ~/.claude/skills/telegram-send "✅ Build #$BUILD_NUMBER succeeded!"

  # Also send artifacts info
  SIZE=$(du -sh dist/ | cut -f1)
  ~/.claude/skills/telegram-send "📦 Build size: $SIZE"
else
  # Send failure to Telegram
  ~/.claude/skills/telegram-send "❌ Build #$BUILD_NUMBER FAILED!"
  ~/.claude/skills/telegram-send "Check logs: $BUILD_URL"
fi
```

### Example 4: Email Monitoring with Alerts

**Create monitor script:**

```bash
cat > ~/email-monitor.sh << 'EOF'
#!/bin/bash

# Check for emails from VIPs
VIPS="boss@company.com ceo@company.com"

for VIP in $VIPS; do
  RESULT=$(~/.claude/skills/email-search "from:$VIP is:unread" 2>&1)

  if echo "$RESULT" | grep -q "Found"; then
    ~/.claude/skills/telegram-send "📧 NEW EMAIL from $VIP:\n\n$RESULT"
  fi
done
EOF

chmod +x ~/email-monitor.sh
```

**Automate:**

```bash
crontab -e

# Every 10 minutes during work hours
*/10 9-18 * * 1-5 /Users/yourusername/email-monitor.sh
```

### Example 5: End-of-Day Report via Telegram

**Create script:**

```bash
cat > ~/eod-report.sh << 'EOF'
#!/bin/bash

# Generate productivity report
REPORT=$(~/.claude/skills/productivity 2>&1)

# Get tomorrow's calendar
TOMORROW=$(~/.claude/skills/cal-week 2>&1 | grep -A 10 "$(date -v+1d '+%A')")

# Send combined report
~/.claude/skills/telegram-send "📊 END OF DAY REPORT\n\n$REPORT\n\n📅 TOMORROW:\n$TOMORROW"

# Mark as sent
echo "Report sent at $(date)" >> ~/eod-reports.log
EOF

chmod +x ~/eod-report.sh
```

**Automate:**

```bash
crontab -e

# Every weekday at 6pm
0 18 * * 1-5 /Users/yourusername/eod-report.sh
```

---

## Advanced Workflows

### Workflow 1: Complete Mobile Productivity Suite

**What it does:**
- Use Telegram for on-the-go productivity
- Get notifications on phone
- Never miss important updates

**Setup:**

```bash
# 1. Start Telegram bot
./start_agency.sh

# 2. Set up morning routine
# (See Example 1 above)

# 3. Set up meeting reminders
# (See Example 2 above)

# 4. Set up email alerts
# (See Example 4 above)

# 5. Set up EOD report
# (See Example 5 above)
```

**Daily Usage:**

```
Morning:
- Get briefing on Telegram (automated)
- Check calendar: /calendar
- Check emails: /emails

During Day:
- Get meeting reminders (automated)
- Quick queries: @cc [question]
- Create events: @cc Create meeting...

Evening:
- Get EOD report (automated)
- Review tomorrow: @cc What's tomorrow's schedule?
```

### Workflow 2: Developer Automation

**What it does:**
- Get build notifications
- Monitor deployments
- Track issues
- Stay updated via Telegram

**Setup:**

```bash
# Add to CI/CD pipeline
cat >> .github/workflows/build.yml << 'EOF'
- name: Notify on Telegram
  if: always()
  run: |
    if [ "${{ job.status }}" == "success" ]; then
      ~/.claude/skills/telegram-send "✅ Build succeeded: ${{ github.sha }}"
    else
      ~/.claude/skills/telegram-send "❌ Build failed: ${{ github.sha }}"
    fi
EOF

# Add deployment notifications
cat > ~/deploy-notify.sh << 'EOF'
#!/bin/bash
ENV=$1
~/.claude/skills/telegram-send "🚀 Deploying to $ENV..."

if deploy_to_env $ENV; then
  ~/.claude/skills/telegram-send "✅ Deployed to $ENV successfully!"
else
  ~/.claude/skills/telegram-send "❌ Deployment to $ENV failed!"
fi
EOF
```

### Workflow 3: Executive Assistant Mode

**What it does:**
- Comprehensive daily management
- Proactive notifications
- Complete automation

**Setup:**

```bash
# Create master automation script
cat > ~/executive-assistant.sh << 'EOF'
#!/bin/bash

HOUR=$(date +%H)

# 7 AM: Morning briefing
if [ "$HOUR" == "07" ]; then
  ~/.claude/skills/morning-brief | \
  ~/.claude/skills/telegram-send
fi

# 8 AM: Detailed schedule
if [ "$HOUR" == "08" ]; then
  ~/.claude/skills/cal-today --detailed | \
  ~/.claude/skills/telegram-send
fi

# Every hour 9-6: Meeting check
if [ "$HOUR" -ge "09" ] && [ "$HOUR" -le "18" ]; then
  NEXT=$(~/.claude/skills/next-meeting)
  if echo "$NEXT" | grep -q "in.*minutes"; then
    echo "$NEXT" | ~/.claude/skills/telegram-send
  fi
fi

# 12 PM: Email summary
if [ "$HOUR" == "12" ]; then
  ~/.claude/skills/email-check | \
  ~/.claude/skills/telegram-send
fi

# 6 PM: EOD report
if [ "$HOUR" == "18" ]; then
  ~/.claude/skills/productivity | \
  ~/.claude/skills/telegram-send

  ~/.claude/skills/cal-week --next-week | \
  head -20 | \
  ~/.claude/skills/telegram-send
fi
EOF

chmod +x ~/executive-assistant.sh
```

**Automate:**

```bash
crontab -e

# Run every hour
0 * * * * /Users/yourusername/executive-assistant.sh
```

---

## Comparison: Telegram vs CLI

| Feature | Telegram | CLI Skills |
|---------|----------|------------|
| **Access** | 📱 Mobile anywhere | 🖥️ Desktop only |
| **Speed** | ⚡ Instant | ⚡ Instant |
| **Notifications** | ✅ Push notifications | ❌ No notifications |
| **Automation** | ⚙️ Limited | ✅ Full automation |
| **Convenience** | ✅ Very convenient | ⚙️ Requires terminal |
| **Commands** | 💬 Chat-like | 📝 Shell commands |
| **History** | ✅ Chat history | ❌ No history |
| **Rich Format** | ✨ Markdown | 📝 Plain text |
| **Scripting** | ❌ Not scriptable | ✅ Fully scriptable |

**Best Practice:**
- Use **Telegram** for mobile, on-the-go access
- Use **CLI** for automation and batch operations
- Use **both** together for complete coverage

---

## Troubleshooting

### Issue 1: Bot Not Responding

**Symptoms:**
- Send message to bot
- No response

**Solutions:**

```bash
# 1. Check if bot is running
ps aux | grep telegram_bot

# 2. Restart bot
pkill -f telegram_bot
./start_agency.sh

# 3. Check bot token
cat .env | grep TELEGRAM_BOT_TOKEN

# 4. Verify token with Telegram
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

### Issue 2: telegram-send Not Working

**Symptoms:**
```
❌ Error: TELEGRAM_CHAT_ID not set
```

**Solutions:**

```bash
# 1. Check environment
echo $TELEGRAM_CHAT_ID

# 2. Set in .env
echo "TELEGRAM_CHAT_ID=your_chat_id" >> .env

# 3. Export directly
export TELEGRAM_CHAT_ID="your_chat_id"

# 4. Test
.claude/skills/telegram-send "Test"
```

### Issue 3: Bot Commands Not Working

**Symptoms:**
- Commands like /morning work
- But @cc queries don't

**Solutions:**

```bash
# 1. Check agent is running
ps aux | grep agency

# 2. Check logs
tail -f ~/.agency/logs/processor.log

# 3. Restart system
./start_agency.sh
```

### Issue 4: Notifications Not Arriving

**Symptoms:**
- Script runs
- But no Telegram message

**Solutions:**

```bash
# 1. Test telegram-send directly
.claude/skills/telegram-send "Test notification"

# 2. Check if bot is running
ps aux | grep telegram

# 3. Check network
ping api.telegram.org

# 4. Check rate limits
# (Telegram has limits on messages per second)
```

### Issue 5: Wrong Chat Receiving Messages

**Symptoms:**
- Messages go to wrong chat

**Solutions:**

```bash
# 1. Verify chat ID
echo $TELEGRAM_CHAT_ID

# 2. Get correct chat ID
# Send message to your bot
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
# Find your chat ID in response

# 3. Update .env
nano .env
# Set correct TELEGRAM_CHAT_ID
```

---

## Quick Reference

### Telegram Commands

```
# Basic Commands
/start          - Welcome message
/help           - Full command list
/status         - System status

# CC Agent Commands
/morning        - Daily briefing
/briefing       - Daily briefing (alias)
/emails         - Check inbox
/calendar       - Today's schedule
/meeting        - Next meeting

# Natural Language
@cc [question]  - Ask CC agent anything
```

### CLI Skills

```bash
# Email
.claude/skills/email-check
.claude/skills/email-search "query"
.claude/skills/email-send "to" "subject" "body"

# Calendar
.claude/skills/cal-today
.claude/skills/cal-week
.claude/skills/next-meeting --prep
.claude/skills/cal-create "event details"

# Drive
.claude/skills/drive-search "query"
.claude/skills/drive-recent

# Dashboard
.claude/skills/productivity
.claude/skills/morning-brief

# Telegram
.claude/skills/telegram-send "message"
```

---

## Best Practices

### 1. Use Telegram for Mobile, CLI for Automation

```
Mobile/On-the-go:
- Use Telegram app
- Quick queries
- Notifications

Desktop/Automation:
- Use CLI skills
- Scripts and cron jobs
- Batch operations
```

### 2. Set Up Essential Notifications

**Recommended automated notifications:**
- Morning briefing (8 AM)
- Urgent email alerts (every 15 min)
- Meeting reminders (10 min before)
- EOD report (6 PM)

### 3. Start Small, Scale Up

```
Week 1: Just Telegram bot + basic commands
Week 2: Add morning briefing automation
Week 3: Add email monitoring
Week 4: Add full automation suite
```

### 4. Monitor Your Automation

```bash
# Keep logs
~/.claude/skills/telegram-send "Message" >> ~/telegram.log 2>&1

# Review regularly
tail -f ~/telegram.log
```

### 5. Respect Rate Limits

**Telegram limits:**
- 30 messages/second to same chat
- 20 messages/minute to same chat

**Don't spam:**
```bash
# Bad: Send 100 messages at once
for i in {1..100}; do
  .claude/skills/telegram-send "Message $i"
done

# Good: Rate limit your scripts
for i in {1..100}; do
  .claude/skills/telegram-send "Message $i"
  sleep 2  # Wait 2 seconds between messages
done
```

---

## Conclusion

You now have complete Telegram + CC agent integration!

**What you can do:**
- ✅ Use CC from anywhere via Telegram
- ✅ Get notifications on your phone
- ✅ Automate workflows with CLI
- ✅ Seamless bidirectional integration

**Your complete setup:**
- 📱 Telegram for mobile access
- 🖥️ CLI for automation
- 🔔 Notifications for everything
- 🤖 Same CC agent powering both

**Next Steps:**
1. Set up your automation suite
2. Create custom workflows
3. Monitor and refine
4. Enjoy your AI-powered productivity system!

---

**Happy automating! 🚀**

*Your productivity is now accessible from anywhere!*
