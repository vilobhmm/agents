# 🤖 Telegram Integration Guide - Manage Your AI Agents from Telegram

## Overview

Control your **CC (Chief Coordinator)** and **Job Hunter** agents directly from Telegram! Get proactive briefings, search for jobs, manage your calendar, check emails - all from your phone! 📱

---

## 🚀 Quick Start

### Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather
3. **Send** `/newbot`
4. **Choose a name** for your bot (e.g., "My AI Assistant")
5. **Choose a username** (must end with 'bot', e.g., "my_ai_assistant_bot")
6. **Copy the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure Environment Variables

Add your Telegram bot token to `.env`:

```bash
cd ~/claude-code/github/agents

# Edit .env file
nano .env
```

Add these lines:

```bash
# Telegram Configuration
TELEGRAM_BOT_TOKEN="your-bot-token-here"
TELEGRAM_ALLOWED_USERS="your-telegram-user-id"
```

**How to get your Telegram User ID:**
1. Search for `@userinfobot` on Telegram
2. Start chat and send `/start`
3. Copy your user ID (a number like `123456789`)
4. Add it to `TELEGRAM_ALLOWED_USERS` in `.env`

### Step 3: Start the Agency System

You need to run **TWO processes**:

#### Terminal 1: Message Processor
```bash
cd ~/claude-code/github/agents
source agents-venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)

# Start the message processor (processes agent requests)
python -m agency process
```

#### Terminal 2: Telegram Bot
```bash
cd ~/claude-code/github/agents
source agents-venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)

# Start the Telegram bot (receives/sends messages)
python -m agency.channels.telegram_channel
```

### Step 4: Start Using Your Bot!

1. **Open Telegram** on your phone or desktop
2. **Search for your bot** by username (e.g., `@my_ai_assistant_bot`)
3. **Send** `/start`
4. **You're ready!** 🎉

---

## 📱 Available Commands

### 🌟 CC Agent (Your Productivity Copilot)

#### `/morning` or `/briefing`
**Get your daily briefing**
```
/morning
```

**What you get:**
- ☀️ Unread emails (prioritized)
- 📅 Today's calendar events
- 🎯 Priorities and action items
- 📁 Recent files from Drive

#### `/emails`
**Check your inbox**
```
/emails
```

**What you get:**
- Unread email count
- Important messages flagged
- Quick email summaries
- Action items

#### `/calendar`
**View today's schedule**
```
/calendar
```

**What you get:**
- All meetings for today
- Meeting times and attendees
- Location/video links
- Preparation suggestions

#### `/meeting`
**Next meeting prep**
```
/meeting
```

**What you get:**
- Next meeting details
- Attendees and agenda
- Related emails
- Recent files/context

---

### 💼 Job Hunter Agent (Your Career Assistant)

#### `/jobs` - Quick Job Search
**Search for jobs with optional query**

```bash
# General search
/jobs

# With role
/jobs Software Engineer

# With company
/jobs Java Developer at TCS

# With location
/jobs ML Engineer in Bangalore

# Full query
/jobs Senior Java Developer at TCS in India 5+ years
```

**What you get:**
- ✅ LinkedIn Jobs (pre-filtered)
- ✅ Indeed (country-specific)
- ✅ Naukri.com (for India)
- ✅ Glassdoor (with ratings)

#### `/jobsearch` - Custom Job Search
**Detailed job search with full query**

```bash
# Search by role and company
/jobsearch Java Developer at TCS in India

# Search by company only
/jobsearch Software Engineer at Wipro

# Search by skills
/jobsearch ML Engineer with Python and PyTorch

# Search by experience
/jobsearch Senior Product Manager 5+ years

# Search remote
/jobsearch Product Manager remote

# Search by location
/jobsearch Software Engineer in Bangalore

# Full Stack with skills
/jobsearch Full Stack Developer with React and Node.js at Infosys
```

**Examples:**
```
/jobsearch Java Developer at TCS in India with 2-3 years
/jobsearch Software Engineer at Wipro in Bangalore
/jobsearch ML Engineer with Python, PyTorch, TensorFlow
/jobsearch Product Manager at Google, remote
/jobsearch Data Scientist in Mumbai with ML skills
/jobsearch DevOps Engineer with Kubernetes and AWS
```

#### `/trackjobs` - View Tracked Jobs
**See all jobs you're tracking**
```
/trackjobs
```

**What you get:**
- List of tracked jobs
- Current status (interested, applied, interviewing, etc.)
- Application deadlines
- Next actions

#### `/applications` - Your Applications
**View all job applications**
```
/applications
```

**What you get:**
- All submitted applications
- Application status
- Follow-up reminders
- Interview schedules

---

### 🔧 System Commands

#### `/agents` - List All Agents
```
/agents
```

Shows all available agents and their capabilities.

#### `/teams` - List All Teams
```
/teams
```

Shows all multi-agent teams.

#### `/status` - System Status
```
/status
```

Check if the agency system is running.

#### `/help` - Full Help
```
/help
```

Complete command reference.

---

## 💬 Natural Language (Advanced)

You can also talk to agents directly using `@mention`:

### CC Agent Examples:

```
@cc What's on my calendar today?

@cc Do I have any urgent emails?

@cc When is my next meeting?

@cc Block 30 minutes for focus time

@cc Send an email to sarah@company.com about the project update

@cc Find the Q4 budget spreadsheet in Drive

@cc What do I need to prepare for the 2pm meeting?
```

### Job Hunter Examples:

```
@job_hunter Find Java Developer jobs at TCS in India

@job_hunter Search for Software Engineer roles at Wipro

@job_hunter Find ML Engineer positions with Python and PyTorch skills

@job_hunter Show me Product Manager jobs at Google

@job_hunter Find remote Software Engineer jobs

@job_hunter Track the TCS Java Developer position I found earlier

@job_hunter Update the Wipro application status to "interviewing"

@job_hunter What jobs have I applied to?
```

---

## 🎯 Real-World Usage Examples

### Morning Routine (5 minutes)

```
You: /morning

Bot: ☀️ Good morning! Preparing your daily briefing...

Bot: 📋 Daily Briefing - Monday, Feb 17, 2025

📧 Unread Emails (5):
• Sarah - Q4 Budget Review (urgent)
• Team - Project Update
• HR - Benefits enrollment deadline Friday
• ...

📅 Today's Calendar:
• 10:00am - Team Standup (30 min)
• 2:00pm - Client Meeting with Acme Corp (1 hour)
  - Attendees: Sarah, John, Client team
  - Agenda: Project proposal review
• 4:00pm - 1:1 with Manager (30 min)

🎯 Priorities:
1. Review Q4 budget before 10am
2. Prepare client meeting materials
3. Submit benefits enrollment by EOD Friday

📁 Recent Files:
• Q4_Budget_Draft_v2.xlsx (updated yesterday)
• Client_Proposal_Acme.pdf (shared by Sarah)
```

### Job Hunting (Throughout the day)

```
You: /jobsearch Java Developer at TCS in India with 2-3 years

Bot: 🔍 Searching: Java Developer at TCS in India with 2-3 years
     Searching across all job boards...

Bot: 💼 Job Search Results

I searched LinkedIn, Indeed, Naukri.com, and Glassdoor for Java Developer roles at TCS in India with 2-3 years experience.

Here are your direct search links:

📍 LINKEDIN JOBS
🔗 https://www.linkedin.com/jobs/search?keywords=Java%20Developer%20TCS&location=India
→ 45+ matching positions
→ Use "Easy Apply" for quick applications

📍 INDEED (India)
🔗 https://in.indeed.com/jobs?q=Java%20Developer%20at%20TCS&l=India
→ 30+ matching positions
→ Filter by salary, benefits

📍 NAUKRI.COM
🔗 https://www.naukri.com/jobs-in-india?k=Java%20Developer&cmp=TCS
→ India's #1 job portal
→ 50+ TCS Java positions

📍 GLASSDOOR
🔗 https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Java%20Developer%20TCS
→ View with company ratings (★4.0)
→ Salary insights available

Click any link to view all matching jobs and apply! 🎯

---

You: @job_hunter Track the TCS Senior Java Developer role

Bot: 📊 Tracked! I'll monitor this position and notify you of any updates.

---

Later...

You: /trackjobs

Bot: 📊 Your Tracked Jobs (3)

1. **Senior Java Developer** - TCS
   Status: Interested
   Location: Bangalore, India
   Tracked: 2 days ago
   → Ready to apply?

2. **Software Engineer** - Wipro
   Status: Applied (5 days ago)
   Location: Mumbai, India
   → Waiting for response

3. **ML Engineer** - Infosys
   Status: Interviewing
   Location: Hyderabad, India
   Next: Phone screen on Feb 20
   → Prepare for interview?
```

### Quick Email Check

```
You: /emails

Bot: 📧 Checking your emails...

Bot: 📬 Unread Emails (3 urgent, 7 total)

🔴 URGENT:
1. Sarah Chen - "Q4 Budget - Need your input by EOD"
   Preview: "Hi, can you review the attached budget and provide..."
   📎 Q4_Budget.xlsx

2. Client (Acme Corp) - "Meeting time change"
   Preview: "Can we move tomorrow's meeting from 2pm to 3pm?"

3. HR - "Action Required: Benefits Deadline Friday"
   Preview: "Reminder: Health insurance enrollment closes..."

📧 OTHERS:
• Team Newsletter - Weekly Update
• LinkedIn - 3 new job matches
• Calendar - Meeting reminder: Team Standup
...

Need me to draft a response to any of these?
```

### Meeting Preparation

```
You: /meeting

Bot: 🔜 Checking your next meeting...

Bot: 🎯 Next Meeting

📅 Client Meeting - Acme Corp
⏰ Today at 2:00pm (in 3 hours)
⏱️ Duration: 1 hour
📍 Zoom: [link]

👥 ATTENDEES:
• Sarah Chen (your team)
• John Smith (your team)
• Jane Doe (Acme Corp - VP Engineering)
• Bob Wilson (Acme Corp - CTO)

📋 AGENDA:
• Project proposal review
• Timeline discussion
• Budget approval

📧 RELATED EMAILS:
• Sarah sent updated proposal yesterday
• Client asked about timeline on Friday
• Budget approved by finance last week

📁 RELEVANT FILES:
• Client_Proposal_Acme_v3.pdf (latest)
• Project_Timeline.xlsx
• Budget_Breakdown.xlsx

💡 PREP TIPS:
✓ Review latest proposal (v3)
✓ Be ready to discuss 6-month timeline
✓ Budget already approved - green light
✓ Client is eager to start - positive signals

Ready for your meeting! 🚀
```

---

## 🔄 Proactive Features

The agents can be **proactive** and send you updates without you asking!

### Daily Morning Briefing (Automatic)

Set up a scheduled briefing every morning at 8am:

```bash
# In your crontab (crontab -e)
0 8 * * * cd ~/claude-code/github/agents && source agents-venv/bin/activate && python -c "import agency.proactive; agency.proactive.send_morning_briefing()"
```

### Job Alerts (Automatic)

Get notified when new jobs matching your criteria are posted:

```
@job_hunter Set up daily job alerts for Java Developer roles at TCS, Wipro, and Infosys in India
```

**You'll receive:**
- Daily digest of new matching jobs
- Alerts for application deadlines
- Reminders to follow up on applications

### Calendar Alerts

Get notified 30 minutes before meetings:

```
@cc Remind me 30 minutes before my next meeting
```

---

## 🛠️ Advanced Setup

### Running as Background Services

Create systemd services to run the agency automatically.

#### 1. Create Processor Service

```bash
sudo nano /etc/systemd/system/agency-processor.service
```

```ini
[Unit]
Description=Agency Message Processor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/claude-code/github/agents
EnvironmentFile=/home/your-username/claude-code/github/agents/.env
ExecStart=/home/your-username/claude-code/github/agents/agents-venv/bin/python -m agency process
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Create Telegram Bot Service

```bash
sudo nano /etc/systemd/system/agency-telegram.service
```

```ini
[Unit]
Description=Agency Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/claude-code/github/agents
EnvironmentFile=/home/your-username/claude-code/github/agents/.env
ExecStart=/home/your-username/claude-code/github/agents/agents-venv/bin/python -m agency.channels.telegram_channel
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services (start on boot)
sudo systemctl enable agency-processor
sudo systemctl enable agency-telegram

# Start services now
sudo systemctl start agency-processor
sudo systemctl start agency-telegram

# Check status
sudo systemctl status agency-processor
sudo systemctl status agency-telegram
```

#### 4. View Logs

```bash
# Processor logs
sudo journalctl -u agency-processor -f

# Telegram bot logs
sudo journalctl -u agency-telegram -f
```

---

## 🔒 Security Best Practices

### 1. Restrict Bot Access

Always set `TELEGRAM_ALLOWED_USERS` in `.env`:

```bash
TELEGRAM_ALLOWED_USERS="123456789,987654321"  # Your user IDs only
```

This prevents unauthorized users from accessing your agents.

### 2. Keep Tokens Secret

Never commit your `.env` file to git:

```bash
# .gitignore
.env
*.env
```

### 3. Use Strong API Keys

Make sure your Google API credentials are secure and have limited scopes.

### 4. Monitor Access

Check logs regularly for unauthorized access attempts:

```bash
sudo journalctl -u agency-telegram | grep "Unauthorized"
```

---

## 📊 Monitoring & Debugging

### Check System Status

```bash
# From Telegram
/status

# From command line
python -m agency debug status
```

### View Queue Status

```bash
ls -la ~/.agency/queue/incoming/
ls -la ~/.agency/queue/outgoing/
```

### Tail Logs

```bash
# Processor logs
tail -f ~/.agency/logs/processor.log

# Telegram bot logs
tail -f ~/.agency/logs/telegram.log
```

### Test Agent Directly

```bash
# Test CC agent
python -m agency debug test cc --message "Give me a morning briefing"

# Test job_hunter agent
python -m agency debug test job_hunter --message "Find Java jobs at TCS"
```

---

## 🎓 Tips & Tricks

### 1. **Use Shortcuts for Frequent Tasks**

Set up aliases in your `.bashrc`:

```bash
alias morning='python -m agency debug test cc --message "morning briefing"'
alias jobs='python -m agency debug test job_hunter --message "find new jobs"'
```

### 2. **Batch Commands**

You can send multiple commands at once:

```
@cc Check my emails and calendar, then prepare context for my next meeting
```

### 3. **Save Preferences**

Tell the job hunter your preferences once:

```
@job_hunter Save my preferences: I'm interested in Java Developer and Software Engineer roles at TCS, Wipro, Infosys, and Accenture in India. I have 2-3 years experience with Java, Spring Boot, and Microservices.
```

Then just:

```
/jobs
```

Will automatically use your saved preferences!

### 4. **Set Up Keyboard Shortcuts**

On your phone, set up Telegram quick replies for common commands:

- `/morning` → Daily briefing
- `/jobs` → Find jobs
- `/emails` → Check inbox
- `/calendar` → Today's schedule

---

## 🐛 Troubleshooting

### Bot Not Responding

1. **Check if services are running:**
   ```bash
   sudo systemctl status agency-processor
   sudo systemctl status agency-telegram
   ```

2. **Check logs for errors:**
   ```bash
   sudo journalctl -u agency-processor -n 50
   sudo journalctl -u agency-telegram -n 50
   ```

3. **Verify environment variables:**
   ```bash
   echo $TELEGRAM_BOT_TOKEN
   echo $ANTHROPIC_API_KEY
   ```

### "Unauthorized User" Error

Make sure your Telegram user ID is in `TELEGRAM_ALLOWED_USERS`:

```bash
# Get your user ID from @userinfobot on Telegram
# Add to .env
TELEGRAM_ALLOWED_USERS="your-user-id-here"
```

### Commands Not Working

1. **Check agent configuration:**
   ```bash
   python -m agency debug test --list-agents
   ```

2. **Test agent directly:**
   ```bash
   python -m agency debug test job_hunter --message "test"
   ```

3. **Restart services:**
   ```bash
   sudo systemctl restart agency-processor
   sudo systemctl restart agency-telegram
   ```

### No Response from CC

1. **Verify Google credentials:**
   ```bash
   python -m agency.tools.google_tools test
   ```

2. **Check if OAuth flow completed:**
   ```bash
   ls ~/.agency/google_credentials/
   ```

3. **Re-authenticate if needed:**
   ```bash
   rm ~/.agency/google_credentials/*.json
   # Then run CC agent again - it will prompt for re-auth
   ```

---

## 🎉 You're All Set!

Your Telegram bot is now your **personal AI command center**!

### Quick Reference Card:

| Command | What It Does |
|---------|-------------|
| `/morning` | Daily briefing 📋 |
| `/emails` | Check inbox 📧 |
| `/calendar` | Today's schedule 📅 |
| `/meeting` | Next meeting prep 🔜 |
| `/jobs` | Search jobs 💼 |
| `/jobsearch <query>` | Custom job search 🔍 |
| `/trackjobs` | Tracked jobs 📊 |
| `/applications` | Your applications 📝 |

### Pro Tips:

✅ Send `/morning` every day to stay ahead
✅ Use `/jobsearch` for flexible job hunting
✅ Track interesting jobs with natural language
✅ Let CC prepare you for meetings automatically
✅ Set up services to run 24/7

**Enjoy your proactive, personal, powerful AI multi-agent system! 🚀**
