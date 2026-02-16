# 🔔 Proactive Notifications Guide

## Never Miss What Matters!

Get **instant notifications** on Telegram or Email without manually checking. The system monitors and alerts you automatically!

---

## ✨ Features

### ⏰ **Scheduled Notifications**

| Time | Notification | What You Get |
|------|--------------|-------------|
| **8:00 AM** | Morning Briefing | Emails, calendar, priorities |
| **6:00 PM** | Job Alerts | New job matches, deadlines |

### 🚨 **Event-Based Alerts** (Coming Soon)

| Trigger | Notification | When |
|---------|--------------|------|
| **Urgent Email** | Instant alert | High-priority sender or keywords |
| **Meeting Soon** | 30-min reminder | Before calendar events |
| **New Job Match** | Instant alert | Job matching your preferences |
| **Application Deadline** | 3-day warning | Application closing soon |

### 📱 **Delivery Methods**

1. **Telegram** (Primary) - Instant push notifications
2. **Email** (Fallback) - Sent if Telegram fails

---

## 🚀 Quick Setup

### Step 1: Get Your Telegram Chat ID

When you send a message to your bot, you need to get the chat ID.

**Method 1: Using getUpdates API**

1. Send any message to your bot on Telegram
2. Open this URL in browser (replace `<YOUR_BOT_TOKEN>`):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id":123456789}`
4. Copy the number (e.g., `123456789`)

**Method 2: Using @userinfobot**

1. Search `@userinfobot` on Telegram
2. Send `/start`
3. Copy your ID

### Step 2: Configure `.env`

Add these to your `.env` file:

```bash
# Telegram Configuration (already have these)
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_ALLOWED_USERS="your-user-id"

# NEW: Add these for proactive notifications
TELEGRAM_CHAT_ID="your-chat-id"  # Same as your user ID usually
PROACTIVE_EMAIL="vilobh.meshram@gmail.com"  # Your email

# Optional: Gmail for email notifications
GMAIL_USER="your-gmail@gmail.com"
GMAIL_APP_PASSWORD="your-app-password"  # Generate from Google Account settings
```

### Step 3: Generate Gmail App Password (Optional - For Email Notifications)

If you want email fallback:

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (required)
3. Go to **App passwords**: https://myaccount.google.com/apppasswords
4. Generate app password for "Mail"
5. Copy the 16-character password
6. Add to `.env` as `GMAIL_APP_PASSWORD`

### Step 4: Start the System

```bash
cd ~/claude-code/github/agents
./start-telegram.sh
```

**You should see:**
```
========================================
✅ Agency System Running!
========================================

Processes:
  Message Processor: PID 12345
  Telegram Bot: PID 12346
  Proactive Notifications: PID 12347

Proactive Notifications:
  ☀️  Morning briefing at 8:00 AM daily
  💼 Job alerts at 6:00 PM daily
  📧 Email fallback: vilobh.meshram@gmail.com
```

---

## 📅 Notification Schedule

### Morning Briefing (8:00 AM Daily)

**What:** Complete daily briefing

**Includes:**
- 📧 Unread emails (prioritized by importance)
- 📅 Today's calendar events
- 🎯 Top priorities and action items
- 📁 Recent files from Drive

**Sent to:** Telegram (with email fallback)

**Example:**
```
☀️ Good Morning!

📧 UNREAD EMAILS (3 urgent):
• Sarah - Q4 Budget Review (urgent)
• Client - Meeting time change
• HR - Benefits deadline Friday

📅 TODAY'S CALENDAR:
• 10:00am - Team Standup
• 2:00pm - Client Meeting
• 4:00pm - 1:1 with Manager

🎯 PRIORITIES:
1. Review Q4 budget before 10am
2. Prepare client meeting materials
3. Submit benefits by Friday

Ready for your day! 🚀
```

### Job Alerts (6:00 PM Daily)

**What:** New job opportunities matching your preferences

**Includes:**
- 💼 New job postings since yesterday
- 📊 Jobs matching your saved preferences
- ⏰ Application deadlines approaching
- 🎯 Recommended actions

**Sent to:** Telegram (with email fallback)

**Example:**
```
💼 Daily Job Alert

NEW MATCHES (3):
1. Senior Java Developer - TCS (Bangalore)
   Posted: Today
   🔗 Apply now

2. Software Engineer - Wipro (Mumbai)
   Posted: Today
   Match: 95%
   🔗 Apply now

3. ML Engineer - Infosys (Hyderabad)
   Posted: 1 day ago
   🔗 Apply now

⏰ DEADLINES:
• Google PM role closes in 3 days

Use /trackjobs to see all tracked positions
```

---

## 🚨 Event-Based Alerts (Coming Soon)

### Urgent Email Alert

**Trigger:** Email from important sender or with urgent keywords

**Example:**
```
🚨 Urgent Email

From: Sarah Chen (CEO)
Subject: Q4 Budget - Need input by EOD

Check your inbox immediately!
```

### Meeting Reminder

**Trigger:** 30 minutes before calendar event

**Example:**
```
🔔 Meeting Reminder

Client Meeting - Acme Corp
Starts in 30 minutes (2:00 PM)

Use /meeting for prep details
```

### New Job Match

**Trigger:** Job matching your saved preferences is posted

**Example:**
```
💼 New Job Match!

Senior Java Developer at TCS
Location: Bangalore, India
Salary: ₹15-20 LPA
Skills: Java, Spring Boot, Microservices

This matches your saved preferences!

🔗 https://www.naukri.com/...
```

### Application Deadline

**Trigger:** 3 days before application closes

**Example:**
```
⏰ Application Deadline

Product Manager at Google
Closes in 3 days

Don't miss out! Apply now.
```

---

## 🛠️ Customization

### Change Notification Times

Edit `agency/proactive_notifications.py`:

```python
# Default: 8:00 AM and 6:00 PM
morning_briefing_time = dtime(8, 0)  # Change to your preferred time
job_alerts_time = dtime(18, 0)       # Change to your preferred time
```

### Enable/Disable Specific Notifications

Comment out notifications you don't want in the scheduler loop.

### Add Custom Notifications

Add your own notification methods to the `ProactiveNotifier` class:

```python
async def custom_alert(self, message: str):
    """Your custom alert"""
    await self.notify(
        f"🔔 **Custom Alert**\n\n{message}",
        subject="Custom Alert"
    )
```

---

## 📊 Monitoring

### Check Logs

```bash
# Proactive notification logs
tail -f logs/proactive.log

# All logs at once
tail -f logs/*.log
```

### Test Notifications Manually

```python
# Test Telegram notification
python3 << EOF
import asyncio
from agency.proactive_notifications import ProactiveNotifier

async def test():
    notifier = ProactiveNotifier()
    await notifier.send_telegram("🧪 Test notification from proactive system!")

asyncio.run(test())
EOF
```

### Test Email Notification

```python
# Test email notification
python3 << EOF
from agency.proactive_notifications import ProactiveNotifier

notifier = ProactiveNotifier()
notifier.send_email(
    "Test Notification",
    "This is a test email from the proactive notification system!"
)
EOF
```

---

## 🔒 Security

### Telegram Security

- ✅ Bot token kept in `.env` (not in git)
- ✅ Only your chat ID receives notifications
- ✅ No public access to your bot

### Email Security

- ✅ Gmail App Password (not your real password)
- ✅ App password can be revoked anytime
- ✅ Limited to mail sending only

---

## 🐛 Troubleshooting

### Notifications Not Received

1. **Check if proactive service is running:**
   ```bash
   ps aux | grep proactive_notifications
   ```

2. **Check logs:**
   ```bash
   tail -f logs/proactive.log
   ```

3. **Verify environment variables:**
   ```bash
   echo $TELEGRAM_CHAT_ID
   echo $PROACTIVE_EMAIL
   ```

4. **Test manually:**
   ```bash
   python -m agency.proactive_notifications
   ```

### Email Not Working

1. **Check Gmail credentials:**
   ```bash
   echo $GMAIL_USER
   echo $GMAIL_APP_PASSWORD
   ```

2. **Verify app password:**
   - Go to https://myaccount.google.com/apppasswords
   - Regenerate if needed

3. **Check 2-Step Verification:**
   - Must be enabled for app passwords

### Wrong Notification Time

Check your system timezone:
```bash
date
timedatectl  # Linux
```

Adjust times in `proactive_notifications.py` based on your timezone.

---

## 🎯 Usage Examples

### Example 1: Morning Routine

**8:00 AM - Automatic Briefing**
```
☀️ Good Morning!

Your daily briefing is ready...
[Complete briefing from CC agent]
```

**Your response:**
- Review briefing while getting coffee ☕
- Know what's urgent before opening laptop 💻
- Already prepared for first meeting 📋

### Example 2: Job Hunting

**6:00 PM - Daily Job Alert**
```
💼 Daily Job Alert

3 new matches found!
[Job listings]
```

**Your response:**
```
You on Telegram: /jobsearch Java Developer at TCS

[Get updated search results]

You: @job_hunter Track the TCS Senior Java role

[Job tracked for later]
```

### Example 3: Urgent Notification

**Anytime - Urgent Email**
```
🚨 Urgent Email

From: CEO
Subject: Emergency meeting in 10 minutes

Check inbox immediately!
```

**Your response:**
- Instant awareness even if away from desk
- Quick action on time-sensitive items
- No missed critical emails

---

## 📈 Advanced: Running 24/7

To run as a background service that survives reboots:

### Create systemd Service

```bash
sudo nano /etc/systemd/system/agency-proactive.service
```

```ini
[Unit]
Description=Agency Proactive Notifications
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/claude-code/github/agents
EnvironmentFile=/home/your-username/claude-code/github/agents/.env
ExecStart=/home/your-username/claude-code/github/agents/agents-venv/bin/python -m agency.proactive_notifications
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable agency-proactive
sudo systemctl start agency-proactive

# Check status
sudo systemctl status agency-proactive

# View logs
sudo journalctl -u agency-proactive -f
```

---

## ✅ Benefits

### Before (Manual)
- ❌ Manually check email every hour
- ❌ Manually check calendar before meetings
- ❌ Manually search for jobs daily
- ❌ Miss urgent items when away from desk
- ❌ Forget application deadlines
- ❌ Reactive instead of proactive

### After (Proactive)
- ✅ Automatic morning briefing
- ✅ Instant urgent email alerts
- ✅ Meeting reminders 30 min before
- ✅ Daily job opportunities delivered
- ✅ Deadline warnings 3 days ahead
- ✅ Stay informed even when busy
- ✅ Truly proactive system

---

## 🎉 Summary

| Feature | Status | Schedule |
|---------|--------|----------|
| **Morning Briefing** | ✅ Active | 8:00 AM daily |
| **Job Alerts** | ✅ Active | 6:00 PM daily |
| **Email Fallback** | ✅ Active | If Telegram fails |
| **Urgent Emails** | 🔜 Coming | Real-time |
| **Meeting Reminders** | 🔜 Coming | 30 min before |
| **Job Matches** | 🔜 Coming | Real-time |
| **Deadline Warnings** | 🔜 Coming | 3 days before |

---

## 📞 Need Help?

### Quick Fixes

**Not receiving notifications?**
```bash
# Check if running
ps aux | grep proactive_notifications

# Restart
./start-telegram.sh
```

**Wrong time?**
```bash
# Check system time
date

# Edit notification times
nano agency/proactive_notifications.py
```

**Want to test?**
```bash
# Send test notification
python -m agency.proactive_notifications
```

---

**Never miss what matters! Your AI agents keep you informed proactively! 🚀**

---

## 🔜 Coming Soon

- Real-time urgent email detection
- Smart meeting preparation reminders
- Intelligent job matching alerts
- Custom notification rules
- Weekend/vacation mode
- Notification preferences per category
- SMS fallback option

Stay tuned! 🎯
