# 🤖 Proactive Automation Setup Guide

**Never miss an important email, meeting, or deadline again!**

This guide shows you how to set up fully automated proactive notifications that keep you ahead of your day.

---

## 🎯 What You Get

### Automatic Notifications For:
- ✅ **Meeting Prep** - 15 minutes before meetings, get full prep with context
- ✅ **Urgent Emails** - Instant alerts for important/urgent emails
- ✅ **Deadlines** - Reminders for approaching deadlines
- ✅ **Action Items** - Track pending tasks from emails
- ✅ **Calendar Conflicts** - Alerts for overlapping events
- ✅ **Daily Briefings** - Morning, midday, and EOD summaries

### Delivery Methods:
- 📱 **Telegram** - Get notifications on your phone
- 🖥️ **CLI** - Run manually when needed
- ⏰ **Automated** - Background service or cron jobs

---

## 📋 New Skills Available

### 1. `proactive-monitor` - Intelligent Monitoring

```bash
# Run once - check everything
.claude/skills/proactive-monitor

# Run continuously in background (daemon mode)
.claude/skills/proactive-monitor --daemon

# Only meeting prep
.claude/skills/proactive-monitor --meeting-prep

# Only urgent items
.claude/skills/proactive-monitor --urgent
```

**What it monitors:**
- Upcoming meetings (15-30 min window)
- Urgent/important emails
- Approaching deadlines
- Calendar conflicts
- Pending action items

**Sends Telegram alerts** when items found!

---

### 2. `meeting-prep` - Auto Meeting Preparation

```bash
# Prep for next meeting
.claude/skills/meeting-prep

# Prep for specific meeting
.claude/skills/meeting-prep "Project Review"

# Auto-run mode (sends to Telegram)
.claude/skills/meeting-prep --auto
```

**Provides:**
- Meeting details (time, location, attendees)
- Recent emails from attendees (last 3 days)
- Related Drive documents
- Previous meeting notes
- Suggested talking points
- Pending action items

---

### 3. `daily-digest` - Smart Daily Summaries

```bash
# Morning briefing (8 AM)
.claude/skills/daily-digest --morning

# Midday check-in (12 PM)
.claude/skills/daily-digest --midday

# End of day summary (6 PM)
.claude/skills/daily-digest --eod

# Full digest anytime
.claude/skills/daily-digest
```

**Morning Briefing:**
- Priority emails (urgent/important)
- Today's schedule
- Next meeting prep
- Deadlines this week
- Action items
- Recent files
- Smart suggestions

**Midday Check-in:**
- Time status
- New urgent items
- Afternoon prep
- Quick wins

**EOD Summary:**
- Today's accomplishments
- Inbox status
- Tomorrow's preview
- Pending items
- Evening suggestions
- Top priority tomorrow

---

## 🚀 Quick Start

### Step 1: Test the Skills

```bash
cd ~/claude-code/github/agents  # or wherever your repo is
source agents-venv/bin/activate

# Test meeting prep
.claude/skills/meeting-prep

# Test proactive monitor
.claude/skills/proactive-monitor

# Test morning digest
.claude/skills/daily-digest --morning
```

### Step 2: Set Up Telegram (if not done)

See `TELEGRAM_CC_INTEGRATION_GUIDE.md` for full setup.

Quick version:
1. Create bot with @BotFather
2. Get chat ID from @userinfobot
3. Add to `.env`:
   ```bash
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

### Step 3: Choose Automation Method

**Option A: Cron Jobs** (recommended for Mac/Linux)
**Option B: Background Daemon** (continuous monitoring)
**Option C: Manual** (run when needed)

---

## ⏰ Option A: Cron Jobs (Recommended)

### Set Up Automated Schedule

```bash
# Edit crontab
crontab -e

# Add these lines:
```

```cron
# Morning briefing at 8 AM (Mon-Fri)
0 8 * * 1-5 cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/daily-digest --morning

# Midday check at 12 PM (Mon-Fri)
0 12 * * 1-5 cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/daily-digest --midday

# Meeting prep every 15 minutes during work hours (9 AM - 6 PM)
*/15 9-18 * * 1-5 cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/meeting-prep --auto

# Urgent email check every 10 minutes during work hours
*/10 9-18 * * 1-5 cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/proactive-monitor --urgent

# Full proactive check every hour
0 * * * * cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/proactive-monitor

# EOD summary at 6 PM (Mon-Fri)
0 18 * * 1-5 cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/daily-digest --eod
```

**Save and exit** (in vim: `:wq`, in nano: Ctrl+X, Y, Enter)

### Verify Cron Jobs

```bash
# List your cron jobs
crontab -l

# Check cron is running
ps aux | grep cron
```

### Adjust Paths

Replace `~/claude-code/github/agents` with your actual path:

```bash
# Find your agents directory
pwd  # while in agents directory
# Copy the output and use it in crontab
```

---

## 🔄 Option B: Background Daemon

### Run Continuous Monitoring

```bash
cd ~/claude-code/github/agents
source agents-venv/bin/activate

# Run in background with nohup
nohup .claude/skills/proactive-monitor --daemon > ~/proactive-monitor.log 2>&1 &

# Check it's running
ps aux | grep proactive-monitor
tail -f ~/proactive-monitor.log
```

**What the daemon does:**
- Checks for meetings every **10 minutes**
- Checks urgent emails every **15 minutes**
- Full check every **hour**
- Sends Telegram alerts automatically

### Stop the Daemon

```bash
# Find the process
ps aux | grep proactive-monitor

# Kill it
pkill -f proactive-monitor

# Or by PID
kill <PID>
```

### Auto-start on Boot (macOS)

Create a launchd plist:

```bash
cat > ~/Library/LaunchAgents/com.user.proactive-monitor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.proactive-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/proactive-monitor --daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/proactive-monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/proactive-monitor.err</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.user.proactive-monitor.plist

# Unload it (to stop)
launchctl unload ~/Library/LaunchAgents/com.user.proactive-monitor.plist
```

---

## 🎯 Option C: Manual Use

### Run When Needed

```bash
# Before important meeting
.claude/skills/meeting-prep "Board Meeting"

# Check what needs attention
.claude/skills/proactive-monitor

# Morning routine
.claude/skills/daily-digest --morning

# End of day wrap-up
.claude/skills/daily-digest --eod
```

### Create Aliases for Quick Access

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Proactive aliases
alias pm='~/claude-code/github/agents/.claude/skills/proactive-monitor'
alias mp='~/claude-code/github/agents/.claude/skills/meeting-prep'
alias morning='~/claude-code/github/agents/.claude/skills/daily-digest --morning'
alias midday='~/claude-code/github/agents/.claude/skills/daily-digest --midday'
alias eod='~/claude-code/github/agents/.claude/skills/daily-digest --eod'
```

Reload: `source ~/.bashrc` or `source ~/.zshrc`

Now use:
```bash
pm          # Proactive monitor
mp          # Meeting prep
morning     # Morning briefing
eod         # End of day
```

---

## 📱 Telegram Integration

### All proactive features send to Telegram automatically!

**What you'll receive:**

```
🔜 MEETING PREP
Your Project Review meeting is in 15 minutes!
[Full context and talking points]

🚨 URGENT EMAILS
2 urgent emails need attention:
1. Boss: Q4 Budget (action required by EOD)
2. Client: Timeline change (meeting moved to tomorrow)

⏰ UPCOMING DEADLINES
Property tax - Feb 20 (3 days)
UW Application - March 1 (12 days)

✅ ACTION ITEMS
- Send budget proposal to Sarah
- Follow up with John on API issue
- Review design mockups from Alice

☀️ MORNING BRIEFING
Your digest is ready! [Full details]
```

### Enable Telegram Notifications

Make sure your `.env` has:
```bash
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

Test Telegram sending:
```bash
.claude/skills/telegram-send "Test notification"
```

---

## 🎛️ Customization

### Adjust Timing

**Meeting Prep Window:**
Edit `.claude/skills/proactive-monitor`:
```python
# Line: "Check if I have any meetings in the next 30 minutes"
# Change 30 to: 15, 45, 60, etc.
```

**Urgent Email Criteria:**
Edit the urgent check message to include/exclude keywords:
```python
# Add keywords: "invoice", "payment", "legal"
# Remove keywords: adjust the word list
```

**Check Frequency (Cron):**
```cron
*/10 9-18 * * 1-5  # Every 10 min
*/30 9-18 * * 1-5  # Every 30 min
0 */2 * * 1-5      # Every 2 hours
```

**Check Frequency (Daemon):**
Edit `.claude/skills/proactive-monitor`:
```python
# Line: if (now - last_meeting_check).seconds >= 600:  # 10 min
# Change 600 to: 300 (5 min), 900 (15 min), etc.
```

### Customize Content

**Add/Remove Sections:**
Edit `.claude/skills/daily-digest`:
- Modify `get_morning_digest()`
- Modify `get_eod_digest()`
- Add custom sections

**Change Notification Format:**
Edit `.claude/skills/proactive-monitor`:
- Modify `send_telegram()` message formats
- Add emojis, structure, etc.

---

## 🧪 Testing Your Setup

### Test Each Component

```bash
# 1. Test meeting prep
.claude/skills/meeting-prep
# Should show next meeting or "no meetings"

# 2. Test proactive monitor
.claude/skills/proactive-monitor
# Should check all items

# 3. Test daily digest
.claude/skills/daily-digest --morning
# Should show full briefing

# 4. Test Telegram send
.claude/skills/telegram-send "Test from proactive system"
# Should appear on your phone

# 5. Test automation (cron simulation)
cd ~/claude-code/github/agents && \
source agents-venv/bin/activate && \
.claude/skills/daily-digest --morning
# Should work exactly as cron will run it
```

### Verify Notifications

**Expected timeline (with cron setup):**

```
8:00 AM  → Morning briefing to Telegram
9:00 AM  → First proactive check
9:15 AM  → Meeting prep check
9:30 AM  → Meeting prep check
10:00 AM → Hourly proactive check
12:00 PM → Midday check-in
6:00 PM  → EOD summary
```

**Check logs:**
```bash
# Cron logs (macOS)
grep CRON /var/log/system.log

# Your custom logs
tail -f ~/proactive-monitor.log
```

---

## 📊 Example Automation Setup

### Conservative (Light Automation)

```cron
# Just morning and EOD
0 8 * * 1-5 ~/agents/.claude/skills/daily-digest --morning
0 18 * * 1-5 ~/agents/.claude/skills/daily-digest --eod

# Meeting prep once an hour
0 * * * * ~/agents/.claude/skills/meeting-prep --auto
```

### Moderate (Recommended)

```cron
# Daily digests
0 8 * * 1-5 ~/agents/.claude/skills/daily-digest --morning
0 12 * * 1-5 ~/agents/.claude/skills/daily-digest --midday
0 18 * * 1-5 ~/agents/.claude/skills/daily-digest --eod

# Meeting prep every 30 min
*/30 9-18 * * 1-5 ~/agents/.claude/skills/meeting-prep --auto

# Urgent checks every 15 min
*/15 9-18 * * 1-5 ~/agents/.claude/skills/proactive-monitor --urgent
```

### Aggressive (Full Automation)

```cron
# Daily digests
0 8 * * 1-5 ~/agents/.claude/skills/daily-digest --morning
0 12 * * 1-5 ~/agents/.claude/skills/daily-digest --midday
0 18 * * 1-5 ~/agents/.claude/skills/daily-digest --eod

# Meeting prep every 15 min
*/15 9-18 * * 1-5 ~/agents/.claude/skills/meeting-prep --auto

# Urgent checks every 10 min
*/10 9-18 * * 1-5 ~/agents/.claude/skills/proactive-monitor --urgent

# Full check every hour
0 * * * * ~/agents/.claude/skills/proactive-monitor
```

### Daemon (Continuous)

```bash
# Run once, monitors continuously
nohup .claude/skills/proactive-monitor --daemon > ~/pm.log 2>&1 &
```

---

## 🔧 Troubleshooting

### Cron Jobs Not Running

```bash
# Check cron service is running
ps aux | grep cron

# Check your crontab
crontab -l

# Test command manually
cd ~/claude-code/github/agents && source agents-venv/bin/activate && .claude/skills/daily-digest --morning

# Check cron logs
grep CRON /var/log/system.log  # macOS
grep CRON /var/log/syslog      # Linux
```

### Telegram Not Sending

```bash
# Test Telegram skill
.claude/skills/telegram-send "Test"

# Check .env
cat .env | grep TELEGRAM

# Verify bot token
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

### Skills Not Running

```bash
# Check permissions
ls -l .claude/skills/proactive-monitor
# Should show: -rwxr-xr-x

# Make executable
chmod +x .claude/skills/proactive-monitor
chmod +x .claude/skills/meeting-prep
chmod +x .claude/skills/daily-digest

# Check Python path
which python
# Should show your venv Python
```

### API Errors

```bash
# Check Google auth
ls -la google_token.pickle

# Re-authenticate
python -m openclaw.integrations.unified_auth

# Check Anthropic key
cat .env | grep ANTHROPIC_API_KEY
```

---

## 💡 Pro Tips

### 1. Start Simple
```bash
# Week 1: Just morning briefing
crontab -e
# Add: 0 8 * * 1-5 ~/agents/.claude/skills/daily-digest --morning

# Week 2: Add EOD
# Add: 0 18 * * 1-5 ~/agents/.claude/skills/daily-digest --eod

# Week 3: Add meeting prep
# Add: */30 9-18 * * 1-5 ~/agents/.claude/skills/meeting-prep --auto

# Week 4: Add full automation
```

### 2. Adjust to Your Schedule
```bash
# Early riser? Change to 6 AM
0 6 * * 1-5 ...

# Night owl? Change to 10 AM
0 10 * * 1-5 ...

# Custom work hours
*/15 10-19 * * 1-5 ...  # 10 AM - 7 PM
```

### 3. Weekend Mode
```bash
# No weekend notifications
* * * * 1-5 ...  # Mon-Fri only

# Weekend notifications too
* * * * * ...    # All days

# Weekend mornings only
0 9 * * 6-7 ~/agents/.claude/skills/daily-digest --morning
```

### 4. Quiet Hours
```cron
# Only during work hours (9 AM - 6 PM)
* 9-18 * * 1-5 ...

# Extended hours (7 AM - 9 PM)
* 7-21 * * 1-5 ...
```

### 5. Monitor Resource Usage
```bash
# Check CPU/memory
top | grep python

# Check network usage
nettop | grep python

# Limit frequency if needed
```

---

## 🎉 You're All Set!

**You now have:**
- ✅ Proactive meeting prep
- ✅ Urgent email alerts
- ✅ Deadline tracking
- ✅ Action item monitoring
- ✅ Daily briefings
- ✅ Telegram notifications

**Never miss an important email, meeting, or deadline again!** 🚀

---

## 📚 Related Guides

- `CC_AGENT_E2E_GUIDE.md` - Complete CC agent tutorial
- `TELEGRAM_CC_INTEGRATION_GUIDE.md` - Telegram setup
- `PRODUCTIVITY_SKILLS_GUIDE.md` - All productivity features
- `.claude/skills/README.md` - Skills reference

---

**Questions or issues?** Check the troubleshooting section or see the related guides above.

**Happy automating!** 🤖
