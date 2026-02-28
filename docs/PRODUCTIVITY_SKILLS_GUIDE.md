# 🚀 Claude Code Skills for Productivity & Telegram

**Complete productivity management using Claude Code skills with Telegram integration**

## 📚 Overview

This repository provides **productivity skills** that mirror and extend your **Telegram bot commands**, allowing you to manage emails, calendar, and files from both CLI and Telegram!

### Two Ways to Use Productivity Features:

### 1️⃣ Claude Code Skills (CLI) ⭐ NEW!
- Simple command-line interface
- Direct execution
- Natural language commands
- **Location:** `.claude/skills/` directory

### 2️⃣ Telegram Bot Commands
- Mobile-friendly
- Push notifications
- Conversation-based
- **Location:** `agency/channels/telegram_channel.py`

---

## 📋 Available Skills

### 📧 Email Management

| Skill | Command | Telegram Equivalent |
|-------|---------|-------------------|
| **email-check** | `/email-check` | `/emails` |
| **email-send** | `/email-send "to" "subject" "body"` | Chat: "Send email to..." |
| **email-search** | `/email-search "query"` | Chat: "Search emails for..." |

### 📅 Calendar Management

| Skill | Command | Telegram Equivalent |
|-------|---------|-------------------|
| **cal-today** | `/cal-today` | `/calendar` |
| **cal-week** | `/cal-week` | Chat: "Show week calendar" |
| **next-meeting** | `/next-meeting` | `/meeting` |
| **cal-create** | `/cal-create "event details"` | Chat: "Create meeting..." |

### 📁 Drive Management

| Skill | Command | Telegram Equivalent |
|-------|---------|-------------------|
| **drive-search** | `/drive-search "query"` | Chat: "Find file..." |
| **drive-recent** | `/drive-recent` | Chat: "Recent files" |

### 📊 Dashboard

| Skill | Command | Telegram Equivalent |
|-------|---------|-------------------|
| **productivity** | `/productivity` | Chat: "Show dashboard" |
| **morning-brief** | `/morning-brief` | `/morning` or `/briefing` |

### 📱 Telegram Integration

| Skill | Command | Description |
|-------|---------|-------------|
| **telegram-send** | `/telegram-send "message"` | Send message from CLI to Telegram |

---

## 🚀 Quick Start

### Installation

Skills are already installed in `.claude/skills/`!

```bash
# Verify installation
ls -la .claude/skills/

# Make executable (if needed)
chmod +x .claude/skills/*
```

### Basic Usage

```bash
# Email management
.claude/skills/email-check
.claude/skills/email-send "john@example.com" "Meeting" "Tomorrow at 2pm?"

# Calendar management
.claude/skills/cal-today
.claude/skills/next-meeting --prep
.claude/skills/cal-create "Team standup tomorrow at 9am for 30 minutes"

# Drive management
.claude/skills/drive-search "project proposal"
.claude/skills/drive-recent --today

# Dashboard
.claude/skills/productivity
.claude/skills/morning-brief

# Telegram integration
.claude/skills/telegram-send "Build completed successfully!"
```

---

## 📖 Complete Examples

### Example 1: Morning Routine

```bash
# Get morning briefing
.claude/skills/morning-brief

# Check inbox
.claude/skills/email-check

# View today's calendar
.claude/skills/cal-today

# Prepare for next meeting
.claude/skills/next-meeting --prep
```

**Telegram Equivalent:**
```
/morning
/emails
/calendar
/meeting
```

---

### Example 2: Email Workflow

```bash
# Check inbox
.claude/skills/email-check

# Search for specific emails
.claude/skills/email-search "from:boss@company.com"

# Send reply
.claude/skills/email-send "boss@company.com" "Re: Project Update" "Status report attached"
```

**Telegram Equivalent:**
```
/emails
@cc Search emails from boss@company.com
@cc Send email to boss about project update
```

---

### Example 3: Calendar Management

```bash
# View today's schedule
.claude/skills/cal-today

# View full week
.claude/skills/cal-week

# Create new meeting
.claude/skills/cal-create "Project review with team on Friday at 3pm for 1 hour"

# Prepare for next meeting
.claude/skills/next-meeting --prep
```

**Telegram Equivalent:**
```
/calendar
@cc Show me this week's calendar
@cc Create meeting: Project review Friday 3pm
/meeting
```

---

### Example 4: File Management

```bash
# Find specific file
.claude/skills/drive-search "Q1 budget spreadsheet"

# See recent files
.claude/skills/drive-recent --count 10

# See today's files
.claude/skills/drive-recent --today
```

**Telegram Equivalent:**
```
@cc Find file: Q1 budget spreadsheet
@cc Show recent files
@cc Show files modified today
```

---

### Example 5: CLI to Telegram Integration

```bash
# Send notification to Telegram
.claude/skills/telegram-send "Backup completed successfully"

# Send status update
.claude/skills/telegram-send "Build failed - check logs"

# Send reminder
.claude/skills/telegram-send "Meeting starts in 10 minutes!"
```

**Use Case:** Automate notifications from scripts!

```bash
#!/bin/bash
# backup.sh

if backup_database; then
  .claude/skills/telegram-send "✅ Database backup completed"
else
  .claude/skills/telegram-send "❌ Backup failed!"
fi
```

---

## 🎯 Power User Tips

### Create Shell Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Email aliases
alias ec='.claude/skills/email-check'
alias es='.claude/skills/email-search'

# Calendar aliases
alias ct='.claude/skills/cal-today'
alias cw='.claude/skills/cal-week'
alias nm='.claude/skills/next-meeting'
alias cc='.claude/skills/cal-create'

# Drive aliases
alias ds='.claude/skills/drive-search'
alias dr='.claude/skills/drive-recent'

# Dashboard aliases
alias pd='.claude/skills/productivity'
alias mb='.claude/skills/morning-brief'

# Telegram alias
alias tg='.claude/skills/telegram-send'
```

Now use:
```bash
ec              # Check emails
ct              # Today's calendar
nm --prep       # Next meeting
tg "Hello!"     # Send to Telegram
```

---

### Daily Routine Script

Create `~/morning-routine.sh`:

```bash
#!/bin/bash
# Morning productivity routine

echo "☀️ Good morning! Starting your daily routine..."

# Morning briefing
.claude/skills/morning-brief

# Check calendar
.claude/skills/cal-today

# Check emails
.claude/skills/email-check

# Recent files
.claude/skills/drive-recent --count 5

# Send completion to Telegram
.claude/skills/telegram-send "✅ Morning routine complete!"

echo "✨ Done! Have a productive day!"
```

Make executable and run:
```bash
chmod +x ~/morning-routine.sh
~/morning-routine.sh
```

---

### Automation Examples

#### 1. Build Notification

```bash
#!/bin/bash
# build-and-notify.sh

if npm run build; then
  .claude/skills/telegram-send "✅ Build succeeded!"
else
  .claude/skills/telegram-send "❌ Build failed - check logs"
fi
```

#### 2. Meeting Reminder

```bash
#!/bin/bash
# meeting-reminder.sh

# Get next meeting
.claude/skills/next-meeting > /tmp/meeting.txt

# Send to Telegram
.claude/skills/telegram-send "🔜 $(cat /tmp/meeting.txt)"
```

Add to crontab to run 10 minutes before meetings:
```bash
# Run at :50 past each hour (10 min before meetings)
50 * * * * /home/user/meeting-reminder.sh
```

#### 3. End-of-Day Summary

```bash
#!/bin/bash
# eod-summary.sh

echo "📊 Generating end-of-day summary..."

# Get productivity dashboard
.claude/skills/productivity > /tmp/summary.txt

# Send to Telegram
.claude/skills/telegram-send "📊 End of day summary:\n\n$(cat /tmp/summary.txt)"
```

---

## 📊 Skills vs Telegram Comparison

| Feature | Claude Skills (CLI) | Telegram Bot |
|---------|-------------------|--------------|
| **Interface** | 🖥️ Command line | 📱 Mobile app |
| **Speed** | ⚡ Instant | ⚡ Instant |
| **Automation** | ✅ Easy (scripts) | ⚙️ Limited |
| **Notifications** | ❌ No | ✅ Yes (push) |
| **Accessibility** | 🖥️ Desktop only | 📱 Anywhere |
| **Rich Formatting** | 📝 Plain text | ✨ Markdown |
| **Best For** | Scripts, automation | On-the-go, mobile |

**Recommendation:**
- Use **Skills** for automation, scripts, and desktop work
- Use **Telegram** for mobile access and push notifications
- Use **Both** for complete productivity coverage!

---

## 🔄 Telegram Integration Workflow

### CLI → Telegram

```bash
# Run CLI command
.claude/skills/email-check

# Get notification on Telegram
.claude/skills/telegram-send "Checked emails - 5 unread"
```

### Telegram → CLI

```
# Send on Telegram:
@cc Check emails

# Bot responds with email summary
# (Same backend as CLI skills!)
```

### Bidirectional Automation

```bash
#!/bin/bash
# sync-productivity.sh

# CLI: Check for updates
.claude/skills/email-check > /tmp/emails.txt
.claude/skills/cal-today > /tmp/calendar.txt

# Telegram: Send summary
.claude/skills/telegram-send "📧 Emails: $(wc -l < /tmp/emails.txt) unread"
.claude/skills/telegram-send "📅 Meetings: $(wc -l < /tmp/calendar.txt) today"
```

---

## 📂 Project Structure

```
agents/
├── .claude/
│   └── skills/                         ⭐ NEW: Productivity Skills
│       ├── email-check                 📧 Check inbox
│       ├── email-send                  ✉️ Send email
│       ├── email-search                🔍 Search emails
│       ├── cal-today                   📅 Today's calendar
│       ├── cal-week                    📆 Week's calendar
│       ├── next-meeting                🔜 Next meeting
│       ├── cal-create                  ➕ Create event
│       ├── drive-search                🔍 Search Drive
│       ├── drive-recent                📁 Recent files
│       ├── productivity                📊 Dashboard
│       ├── telegram-send               📱 Send to Telegram
│       ├── morning-brief               ☀️ Daily briefing
│       └── README.md                   📖 Documentation
│
├── agency/
│   ├── channels/
│   │   └── telegram_channel.py         📱 Telegram bot
│   ├── tools/
│   │   ├── google_tools.py             🔧 Gmail, Calendar, Drive
│   │   └── job_search_tools.py         💼 Job search
│   └── agents/
│       └── cc/                          🤖 CC agent
│
└── PRODUCTIVITY_SKILLS_GUIDE.md        📚 This file
```

---

## 🎓 Documentation

### For Users:
- [Productivity Skills Guide](PRODUCTIVITY_SKILLS_GUIDE.md) - This file
- [Quick Start](.claude/skills/QUICKSTART.md) - Get started in 5 minutes
- [Skills README](.claude/skills/README.md) - Complete skill reference
- [Main Guide](CLAUDE_SKILLS_GUIDE.md) - Overall system guide

### For Developers:
- [Telegram Channel](agency/channels/telegram_channel.py) - Bot implementation
- [Google Tools](agency/tools/google_tools.py) - Gmail, Calendar, Drive tools
- [Agent Config](agency/config.py) - Agent configuration

---

## ✨ Complete Workflow Examples

### Workflow 1: Morning Startup

**CLI Version:**
```bash
#!/bin/bash
# 1. Morning briefing
.claude/skills/morning-brief

# 2. Today's calendar
.claude/skills/cal-today

# 3. Check emails
.claude/skills/email-check --count 10

# 4. Recent files
.claude/skills/drive-recent --today

# 5. Notify completion
.claude/skills/telegram-send "✅ Morning routine complete!"
```

**Telegram Version:**
```
/morning
/calendar
/emails
@cc Show files modified today
```

---

### Workflow 2: Meeting Preparation

**CLI Version:**
```bash
# 1. Get next meeting details
.claude/skills/next-meeting --prep

# 2. Search related emails
.claude/skills/email-search "subject:project"

# 3. Find related files
.claude/skills/drive-search "project documents"

# 4. Send reminder to Telegram
.claude/skills/telegram-send "Meeting prep complete!"
```

**Telegram Version:**
```
/meeting
@cc Search emails about project
@cc Find project documents in Drive
```

---

### Workflow 3: Email Management

**CLI Version:**
```bash
# 1. Check unread
.claude/skills/email-check

# 2. Search for urgent
.claude/skills/email-search "is:important is:unread"

# 3. Send responses
.claude/skills/email-send "client@example.com" "Update" "Project on track"

# 4. Notify completion
.claude/skills/telegram-send "📧 Inbox cleared!"
```

**Telegram Version:**
```
/emails
@cc Search important unread emails
@cc Send email to client about project update
```

---

## 🔧 Customization

### Create Custom Skills

Example: Weekly Report Skill

```python
#!/usr/bin/env python3
"""Weekly report generator"""

import sys
import subprocess

# Generate report
message = """
Generate a weekly report with:
1. Emails sent/received this week
2. Meetings attended
3. Files created/modified
4. Tasks completed
"""

subprocess.run([
    "python", "-m", "agency", "debug", "test", "cc",
    "--message", message
], cwd="/home/user/agents")
```

Save as `.claude/skills/weekly-report`, make executable, and run:
```bash
.claude/skills/weekly-report
```

---

## 🆘 Troubleshooting

### Skill not found?
```bash
ls -la .claude/skills/
chmod +x .claude/skills/*
```

### Permission denied?
```bash
chmod +x .claude/skills/email-check
```

### Telegram not sending?
```bash
# Check environment variable
echo $TELEGRAM_CHAT_ID

# If not set, add to ~/.bashrc:
export TELEGRAM_CHAT_ID="your_chat_id"
```

### Agent not responding?
```bash
# Test agent directly
python -m agency debug test cc --message "test"
```

---

## 🚀 Next Steps

1. **Read Documentation:**
   - Start with this guide
   - Check [QUICKSTART.md](.claude/skills/QUICKSTART.md)

2. **Try Skills:**
   - `.claude/skills/email-check`
   - `.claude/skills/cal-today`
   - `.claude/skills/productivity`

3. **Create Aliases:**
   - Add shortcuts to ~/.bashrc
   - Test: `ec`, `ct`, `mb`

4. **Automate:**
   - Create morning routine script
   - Add cron jobs for reminders
   - Integrate with CI/CD

5. **Extend:**
   - Create custom skills
   - Add new workflows
   - Share with team

---

## 📈 Usage Statistics

Track your productivity skill usage:

```bash
# Count skill executions
ls ~/.claude/logs/*.log | xargs grep "email-check" | wc -l

# Most used skills
history | grep ".claude/skills" | awk '{print $2}' | sort | uniq -c | sort -rn

# Automation scripts
crontab -l | grep ".claude/skills"
```

---

## 🎉 Summary

**Claude Code Productivity Skills provide:**

✅ **Complete email management** (check, send, search)
✅ **Full calendar control** (view, create, next meeting)
✅ **Drive file access** (search, recent)
✅ **Integrated dashboards** (productivity, morning brief)
✅ **Telegram integration** (CLI ↔️ mobile)
✅ **Automation friendly** (scripts, cron jobs)
✅ **Mirrors Telegram commands** (same backend, different interface)

---

**Your productivity is now powered by Claude Code skills! 🚀**

Use CLI for automation, Telegram for mobile access, and enjoy seamless integration between both!

---

*Built with ❤️ using Claude Code, Claude Agent SDK, and Telegram*
