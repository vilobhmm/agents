# 🤖 Agency - Complete Setup & Usage Guide

**The Definitive Guide to Getting All Multi-Agents Working with Telegram**

Your personal AI agency - proactive, personal, powerful!

---

## 📋 Table of Contents

1. [What You'll Get](#-what-youll-get)
2. [Prerequisites](#-prerequisites)
3. [Installation (15 Minutes)](#-installation-15-minutes)
4. [Telegram Setup](#-telegram-setup)
5. [Google Services Setup (For CC Agent)](#-google-services-setup-for-cc-agent)
6. [Start Your Agency](#-start-your-agency)
7. [Try All Agents - Complete Examples](#-try-all-agents---complete-examples)
8. [Advanced Features](#-advanced-features)
9. [Troubleshooting](#-troubleshooting)

---

## 🎯 What You'll Get

After following this guide, you'll have:

✅ **11 AI Agents** working via Telegram:
- **@cc** - Your personal productivity assistant (like Google Labs CC)
- **@job_hunter** - Finds jobs at top AI companies
- **@resume_optimizer** - Tailors resumes & applications
- **@networker** - Manages referrals & outreach
- **@researcher** - Research assistant for AI/tech
- **@writer** - Content creation specialist
- **@social** - Social media manager
- **@curator** - Content curation
- **@coordinator** - Team coordination
- **@assistant** - Personal assistant
- **@action_taker** - Action execution

✅ **5 Multi-Agent Teams**:
- **@cc_team** - Personal productivity (CC + assistant + action_taker + researcher)
- **@job_search** - Complete job automation (job_hunter + resume_optimizer + networker)
- **@content** - Content creation (researcher + writer + coordinator)
- **@intelligence** - Intelligence gathering (researcher + curator)
- **@social_team** - Social media (researcher + social)

✅ **Fully Working Telegram Bot** that responds to:
```
@cc Good morning briefing
@job_search Find ML Engineer roles
@content Create newsletter
@researcher Latest AI news
```

---

## 🔧 Prerequisites

### Required:
- Python 3.8+ installed
- Anthropic API key ([get one here](https://console.anthropic.com))
- Telegram account

### Optional (for specific features):
- Google account (for CC agent: Gmail, Calendar, Drive)
- Twitter/X account (for social media features)
- LinkedIn account (for social media features)

---

## 📦 Installation (15 Minutes)

### Step 1: Install Python Dependencies

```bash
cd /home/user/agents

# Core dependencies
pip install anthropic python-telegram-bot python-dotenv aiofiles

# Optional: Google services (for CC agent)
pip install google-auth-oauthlib google-api-python-client

# Optional: Social media
pip install tweepy

# Optional: Web scraping (for job search)
pip install beautifulsoup4 requests playwright
```

### Step 2: Initialize Agency

```bash
# Make the CLI executable
chmod +x /home/user/agents/agency_bin

# Add to PATH (optional but recommended)
echo 'export PATH="/home/user/agents:$PATH"' >> ~/.bashrc
echo 'alias agency="/home/user/agents/agency_bin"' >> ~/.bashrc
source ~/.bashrc

# Initialize workspace
python -m agency init
```

**Output:**
```
🎬 Initializing Agency workspace...
✅ Created config file
✅ Created .env.example
✅ Workspace initialized!

Config:     /home/user/.agency/config.json
Workspace:  /home/user/agency-workspace
Queues:     /home/user/.agency/queue

Next steps:
  1. Configure .env with your API keys
  2. Run: agency pair telegram
  3. Run: agency start
```

### Step 3: Configure Environment

```bash
# Copy example env file
cd /home/user/agents
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Add to `.env`:**
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# For Telegram (we'll get this in next section)
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_ALLOWED_USERS=your-user-id-here

# Optional: Google Services (for CC agent)
GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
GOOGLE_TOKEN_FILE=google_token.pickle

# Optional: Social Media
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
```

---

## 📱 Telegram Setup

### Step 1: Create Bot

1. **Open Telegram** and search for `@BotFather`

2. **Start a chat** with BotFather and send:
   ```
   /newbot
   ```

3. **Choose a name** for your bot (e.g., "My AI Agency")

4. **Choose a username** (must end with 'bot', e.g., `my_agency_bot`)

5. **Copy the bot token** - looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Step 2: Configure Your Bot

Send these commands to BotFather:

```
/setcommands
```

Then paste:
```
help - Show help
status - System status
agents - List all agents
teams - List all teams
briefing - Get morning briefing from CC
jobs - Find jobs with job_search team
```

### Step 3: Get Your User ID

1. **Search for `@userinfobot`** on Telegram

2. **Start a chat** - it will tell you your user ID (e.g., `123456789`)

3. **Copy your user ID**

### Step 4: Pair Telegram with Agency

```bash
# Pair Telegram bot
python -m agency pair telegram --token "YOUR_BOT_TOKEN"
```

**Or interactively:**
```bash
python -m agency pair telegram
# Enter token when prompted
```

**Output:**
```
🔗 Pairing telegram...
Testing token...
✅ Connected to @my_agency_bot
✅ Telegram paired!

Next steps:
  1. Start Agency: agency start
  2. Message your bot on Telegram
  3. Your user ID will be logged
  4. Add it to config: agency config set telegram.allowed_users '[123456789]'
```

### Step 5: Add Your User ID

```bash
# Replace 123456789 with YOUR user ID
python -m agency config set telegram.allowed_users '[123456789]'
```

✅ **Telegram setup complete!**

---

## 🔐 Google Services Setup (For CC Agent)

CC agent needs access to Gmail, Calendar, and Drive for morning briefings.

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "Agency AI"
3. Note the project ID

### Step 2: Enable APIs

Enable these APIs for your project:
- Gmail API
- Google Calendar API
- Google Drive API

```
Go to: APIs & Services → Enable APIs and Services
Search for each and click "Enable"
```

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop app**
4. Download JSON file
5. Save as `/home/user/agents/google_oauth_credentials.json`

### Step 4: Authenticate

```bash
cd /home/user/agents

# Run authentication flow
python -c "
from openclaw.integrations.google_services import GoogleServices
gs = GoogleServices()
print('✅ Google services authenticated!')
"
```

This will:
1. Open browser
2. Ask you to sign in to Google
3. Grant permissions
4. Save token to `google_token.pickle`

✅ **Google services setup complete!**

**Skip this section if you only want basic agents without CC features.**

---

## 🚀 Start Your Agency

### Start the System

```bash
# Start everything (processor + Telegram bot)
python -m agency start
```

**Output:**
```
🚀 Starting Agency...
Starting processor in background...
✅ Processor started (PID: 12345)
Starting Telegram in foreground...
✅ Telegram channel started
Press Ctrl+C to stop

[INFO] Telegram bot started: @my_agency_bot
[INFO] Waiting for messages...
```

**Or start in background:**
```bash
python -m agency start --detach

# Check status
python -m agency status

# View logs
python -m agency logs -f
```

### Test the Connection

1. **Open Telegram**
2. **Find your bot** (search for `@my_agency_bot`)
3. **Send a test message:**
   ```
   /help
   ```

**Expected response:**
```
🤖 Agency - Your AI Assistant Team

Available Agents:
• @cc - Chief Coordinator (productivity)
• @job_hunter - Job search
• @researcher - Research
• @writer - Content creation
• @social - Social media
... and more!

Available Teams:
• @cc_team - Personal productivity
• @job_search - Job search automation
• @content - Content creation
• @intelligence - Research & analysis
• @social_team - Social media management

Try:
@cc Good morning briefing
@job_search Find ML Engineer roles
@researcher What's new in AI?
```

✅ **Your agency is running!**

---

## 🎯 Try All Agents - Complete Examples

### 1. **@cc - Chief Coordinator** (Personal Productivity)

**Morning Briefing:**
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
  • 🔴 3 urgent emails need attention
  • 📅 Next meeting: Team Sync

💡 Suggestions:
  • Review urgent emails first
  • Prepare for Team Sync
  • Block focus time between meetings
```

**Schedule Meeting:**
```
You: @cc Schedule meeting with Sarah tomorrow at 2pm

CC: I'll schedule that meeting.

✅ Meeting scheduled: "Meeting with Sarah"
  📅 Tomorrow at 2:00 PM
  ⏱️ Duration: 30 minutes
  📧 Calendar invite sent

Done!
```

**Draft Email:**
```
You: @cc Draft email to John about project update

CC: Here's a draft:

---
Subject: Project Update - Q1 Status

Hi John,

Hope you're well! Quick update on our Q1 project:

✅ Completed: Phase 1 implementation, initial testing
🚧 In Progress: Performance optimization
📅 Next: Team review (Jan 18), launch prep

Let me know if you need details!

Best,
[Your name]
---

Want me to:
1. Send it now
2. Save as draft
3. Revise something
```

**Block Focus Time:**
```
You: @cc Block 2 hours of focus time

CC: ✅ Blocked "Focus Time"
  📅 Today 2:00 PM - 4:00 PM
  🔕 Notifications muted

Enjoy your focused work!
```

---

### 2. **@job_hunter - Job Search**

**Find Jobs:**
```
You: @job_hunter Find ML Engineer roles at Anthropic and OpenAI

Job Hunter: Searching career pages...

Found 11 positions:

**Anthropic (5 roles)**
1. 🎯 Senior ML Engineer - Agents
   📍 San Francisco, CA
   💼 Senior level
   ⭐ 95% match
   📅 Posted 2 days ago
   🔗 https://anthropic.com/careers/123

2. ML Research Engineer
   📍 Remote
   💼 Mid-Senior
   ⭐ 92% match
   🔗 https://anthropic.com/careers/124

**OpenAI (6 roles)**
3. Research Engineer - Reasoning
   📍 San Francisco, CA
   💼 Senior level
   ⭐ 94% match
   🔗 https://openai.com/careers/456

... (showing top 5)

Want me to:
1. Show all details
2. Tailor resume for top match
3. Find referral contacts
```

**Track Companies:**
```
You: @job_hunter Monitor Anthropic, OpenAI, DeepMind daily

Job Hunter: ✅ Now monitoring:
  • Anthropic
  • OpenAI
  • DeepMind

I'll check daily and notify you of new postings!
```

---

### 3. **@resume_optimizer - Resume Tailoring**

```
You: @resume_optimizer Tailor my resume for Anthropic Senior ML Engineer

Resume Optimizer: Analyzing job description...

Key requirements:
✓ Deep learning (PyTorch/JAX)
✓ LLM training & fine-tuning
✓ Production ML systems
✓ Research background

Optimizing your resume...
✏️ Highlighted LLM work
✏️ Emphasized PyTorch expertise
✏️ Added production metrics
✏️ Featured research publications

✅ Resume optimized!
  Match score: 95% → 98%
  Saved as: resume_anthropic_senior_ml.pdf

Want me to create a cover letter?
```

---

### 4. **@networker - Referrals & Outreach**

**Find Referral Contacts:**
```
You: @networker Who can refer me to Anthropic?

Networker: Checking your network...

Found 3 potential referrals:

1. 👤 Sarah Chen
   💼 Senior ML Engineer at Anthropic
   🤝 Strong connection (worked together 2020)
   ⭐ Best option

2. Mike Johnson
   💼 Research Scientist at Anthropic
   🤝 Friend from Stanford
   ⭐ Good option

3. Emily Davis
   💼 Recruiter at Anthropic
   🤝 Met at AI conference
   ⭐ Medium option

Recommended: Start with Sarah

Want me to draft a referral request?
```

**Draft Referral Request:**
```
You: Yes, draft for Sarah

Networker: Here's a personalized request:

---
Subject: Catching up + Anthropic opportunity

Hi Sarah,

Hope you're doing well! It's been great seeing your
work at Anthropic - Claude releases have been incredible.

I noticed Anthropic is hiring for Senior ML Engineer
(Agents team). Given our work together at PreviousCo
on the recommendation system, I think my LLM deployment
experience could be a good fit.

Would you be open to a quick chat about the role?
If you think it's a match, I'd really appreciate a referral!

Best,
[Your name]
---

Send now?
```

---

### 5. **@researcher - Research Assistant**

```
You: @researcher What's new in AI today?

Researcher: Here's today's AI news:

📰 **Top Stories**
1. Anthropic releases Claude 4.5
   - Improved reasoning capabilities
   - Faster response times
   - Source: Anthropic blog

2. OpenAI announces GPT-5 training
   - 10x larger than GPT-4
   - Expected Q2 2025
   - Source: Sam Altman tweet

3. DeepMind's AlphaFold 3
   - Predicts protein-ligand binding
   - Nature publication
   - Source: DeepMind blog

📊 **Trending on Twitter**
- #AIAgents (10k tweets)
- Claude 4.5 reviews
- Discussions on AI safety

📄 **New Research Papers** (ArXiv)
1. "Constitutional AI: Training Helpful and Harmless AI"
2. "Scaling Laws for Large Language Models"
3. "RLHF at Scale"

Want details on any of these?
```

---

### 6. **@writer - Content Creation**

```
You: @writer Create newsletter about AI agents

Writer: I'll create a newsletter about AI agents.

[Working...]

✅ Newsletter ready!

---
Subject: 🤖 The Rise of AI Agents

Hi there,

AI agents are transforming how we work. Here's what
you need to know:

**What are AI Agents?**
AI agents are autonomous systems that can plan, execute,
and adapt to complete complex tasks...

**Key Developments**
1. Multi-agent collaboration
2. Tool use capabilities
3. Long-term memory

**Use Cases**
- Personal productivity (like CC)
- Job search automation
- Content creation
- Research assistance

**Getting Started**
[Step-by-step guide...]

**What's Next**
The future of AI agents looks...

---

Want me to:
1. Post to your blog
2. Send as email
3. Revise anything
```

---

### 7. **@social - Social Media Manager**

**Twitter Thread:**
```
You: @social Create Twitter thread about AI agents

Social: Here's a thread about AI agents:

---
🧵 Thread: The AI Agent Revolution

1/ AI agents are changing everything. Here's what
   makes them different from traditional AI 🤖👇

2/ Traditional AI: You ask, it answers
   AI Agents: They plan, act, and adapt autonomously

   Think personal assistant vs. chatbot

3/ Real examples of AI agents in action:
   • Personal productivity (schedule, email, tasks)
   • Job search (find, apply, network)
   • Content creation (research, write, publish)

4/ Key capabilities:
   ✅ Multi-step planning
   ✅ Tool use (API calls, web browsing)
   ✅ Memory & context
   ✅ Self-correction

5/ What's next?
   Multi-agent teams where specialized agents
   collaborate to solve complex problems.

   The future is agentic! 🚀

6/6 Want to build your own AI agency?
   Check out: [link]
---

Want me to:
1. Post now
2. Schedule for later
3. Revise anything
```

**LinkedIn Post:**
```
You: @social Write LinkedIn post about my AI project

Social: Here's a professional LinkedIn post:

---
🚀 Excited to share my latest project: Building an
   AI Agent System

After months of development, I've built a multi-agent
AI system that automates:

📧 Personal productivity (emails, calendar, tasks)
💼 Job search (finding roles, tailoring resumes)
✍️ Content creation (research, writing, publishing)
📱 Social media management

**Key learnings:**
1. Multi-agent coordination is powerful
2. Tool use is the future of AI
3. Autonomous systems need good constraints

**Tech stack:**
- Claude (Anthropic)
- Python async/await
- File-based queues (crash-safe!)
- Telegram integration

The system handles 100+ messages/day and has helped
me land 3 interviews at top AI labs!

Open to chatting about AI agents, system design, or
career opportunities in AI. DM me!

#AI #MachineLearning #Automation #Agents
---

Post now?
```

---

### 8. **@cc_team - Personal Productivity Team** (Multi-Agent!)

```
You: @cc_team Help me prepare for my day

CC (Team Leader): I'll coordinate the team to help you prepare.

[@assistant: Checking calendar and tasks...]
[@researcher: Getting latest AI news...]
[@action_taker: Preparing summary...]

[All agents work in parallel]

✅ Day preparation complete!

📅 **Calendar** (from @assistant):
  • 4 meetings today
  • First: Team Sync at 10:00 AM
  • Gap: 2-4 PM (perfect for focus time)
  • Last: 1-on-1 with manager at 4 PM

✅ **Tasks** (from @assistant):
  High Priority (3):
  • Code review for Sarah (due today)
  • Finish Q1 report (due tomorrow)
  • Respond to client email

🔍 **Context** (from @researcher):
  • Anthropic released Claude 4.5 yesterday
  • Your competitor launched new feature
  • Industry discussion about AI agents

✉️ **Summary Email** (from @action_taker):
  Draft ready to send to team:
  "Good morning team, here's today's focus..."

💡 **Recommendations**:
1. Block 2-4 PM for code review + report
2. Prepare Team Sync talking points
3. Send team summary before 10 AM

Want me to:
1. Send the summary email
2. Block that focus time
3. Prepare Team Sync brief
```

---

### 9. **@job_search Team - Complete Job Automation** (Multi-Agent!)

```
You: @job_search Find and apply for ML Engineer roles

Coordinator: Running complete job search workflow!

[@job_hunter: Searching career pages...]
[@resume_optimizer: Preparing tailored resumes...]
[@networker: Finding referral contacts...]

[All agents work in parallel]

✅ Complete! Here's your job search package:

📊 **Jobs Found: 15** (from @job_hunter)
  Top 5 recommendations (90%+ match):
  1. Anthropic - Senior ML Engineer (95%)
  2. OpenAI - Research Engineer (94%)
  3. DeepMind - ML Research Scientist (92%)
  4. Cohere - ML Engineer (91%)
  5. Anthropic - Applied AI Engineer (90%)

📝 **Resume Package: 5** (from @resume_optimizer)
  ✅ All optimized for ATS
  ✅ Custom cover letters
  ✅ Match scores: 95-98%

  Files:
  - resume_anthropic_senior_ml.pdf
  - resume_openai_research.pdf
  - resume_deepmind_scientist.pdf
  - resume_cohere_ml.pdf
  - resume_anthropic_applied.pdf

🤝 **Referrals: 8 contacts** (from @networker)
  Strong connections (3):
  • Sarah at Anthropic (ready to reach out)
  • Mike at OpenAI (can refer)
  • Emily at DeepMind (can introduce)

  Referral requests drafted and ready to send!

📧 **Next Steps**:
  Option 1: Apply to all 5 now (auto-submit)
  Option 2: Review applications first
  Option 3: Send referral requests first

What would you like to do?
```

---

### 10. **@content Team - Content Creation** (Multi-Agent!)

```
You: @content Create weekly AI newsletter

Coordinator: I'll coordinate the content team!

[@researcher: Gathering AI news and trends...]
[@writer: Drafting newsletter...]

[Agents work in sequence]

✅ Newsletter ready!

📰 **This Week in AI** (from @researcher)
  Research: 15 papers analyzed
  News: 25 articles reviewed
  Trends: 10 trending topics

  Top stories:
  1. Anthropic Claude 4.5 release
  2. OpenAI GPT-5 announcement
  3. DeepMind AlphaFold 3
  4. AI agent frameworks trending
  5. Constitutional AI discussion

✍️ **Newsletter Draft** (from @writer)

  [Shows complete newsletter with:
   - Catchy subject line
   - Executive summary
   - Top 5 stories with analysis
   - Deep dive on AI agents
   - What's next section
   - Call to action]

  Word count: 1,250
  Reading time: 5 minutes
  Links: 10 sources included

Want me to:
1. Send to your email list
2. Post to blog
3. Export as PDF
4. Revise anything
```

---

## 🎓 Advanced Features

### 1. Automatic Morning Briefings

Set CC to send briefings automatically every morning!

```bash
# Edit crontab
crontab -e

# Add this line (8 AM every day)
0 8 * * * /home/user/agents/agency_bin send "Good morning briefing" cc
```

Now you'll get a personalized briefing in Telegram at 8 AM daily! ☀️

---

### 2. Daily Job Alerts

Get notified of new jobs every morning:

```bash
# Add to crontab (9 AM every day)
0 9 * * * /home/user/agents/agency_bin send "Any new ML Engineer jobs?" job_hunter
```

---

### 3. Weekly Content Creation

Automate weekly newsletter:

```bash
# Every Monday at 10 AM
0 10 * * 1 /home/user/agents/agency_bin broadcast "Create weekly newsletter" --team content
```

---

### 4. Custom Agents

Create your own specialized agent:

```bash
python -m agency agent create email_expert \
  --name "Email Expert" \
  --model opus \
  --personality "You are an expert at writing professional emails"

# Test it
python -m agency send "Draft professional email" email_expert
```

---

### 5. Custom Teams

Build custom teams:

```bash
python -m agency team create my_team \
  --name "My Custom Team" \
  --leader coordinator \
  --agents coordinator researcher writer email_expert

# Use it
python -m agency broadcast "Complex task" --team my_team
```

---

### 6. Background Operation

Run Agency in the background:

```bash
# Start in background
python -m agency start --detach

# Check status
python -m agency status

# View logs
python -m agency logs -f

# Stop when needed
python -m agency stop
```

---

### 7. Auto-start on Boot

```bash
# Edit crontab
crontab -e

# Add line
@reboot /home/user/agents/agency_bin start --detach
```

Now Agency starts automatically when your computer boots!

---

## 🐛 Troubleshooting

### Issue: "Bot not responding"

**Check if running:**
```bash
python -m agency status
```

**Start if stopped:**
```bash
python -m agency start
```

**View logs:**
```bash
python -m agency logs -f
```

---

### Issue: "Agent not found"

**List all agents:**
```bash
python -m agency agent list
```

**Check agent status:**
```bash
python -m agency agent info cc
```

---

### Issue: "No permission" or "User not allowed"

**Check allowed users:**
```bash
python -m agency config get telegram.allowed_users
```

**Add your user ID:**
```bash
python -m agency config set telegram.allowed_users '[YOUR_USER_ID]'
```

**Restart:**
```bash
python -m agency stop
python -m agency start
```

---

### Issue: "Google authentication failed"

**Re-authenticate:**
```bash
rm google_token.pickle
python -c "
from openclaw.integrations.google_services import GoogleServices
GoogleServices()
"
```

---

### Issue: "API key invalid"

**Check API key:**
```bash
python -m agency config get anthropic.api_key
```

**Set API key:**
```bash
python -m agency config set anthropic.api_key "sk-ant-your-key"
```

**Restart:**
```bash
python -m agency stop
python -m agency start
```

---

### Issue: "Message not processed"

**Check queue:**
```bash
ls ~/.agency/queue/incoming/
ls ~/.agency/queue/processing/
```

**Check logs:**
```bash
python -m agency logs -f
```

**Reset if needed:**
```bash
python -m agency stop
rm -rf ~/.agency/queue/*
python -m agency start
```

---

## 📚 Next Steps

### Learn More

- **CLI Reference**: `agency/CLI_COMMANDS.md` - All 60+ commands
- **CC Guide**: `agency/CC_AGENT_GUIDE.md` - Complete CC walkthrough
- **Job Search**: `agency/JOB_SEARCH_E2E_GUIDE.md` - Job automation guide
- **Architecture**: `AGENCY_README.md` - System details

### Customize

```bash
# View all agents
python -m agency agent list

# View all teams
python -m agency team list

# View configuration
python -m agency config show

# Create custom agent
python -m agency agent create my_agent --name "My Agent" --model sonnet

# Create custom team
python -m agency team create my_team --name "My Team" --leader coordinator
```

### Get Help

```bash
# CLI help
python -m agency --help
python -m agency agent --help
python -m agency team --help

# In Telegram
/help
```

---

## 🎉 You're All Set!

Your AI Agency is now running! Try these commands in Telegram:

```
@cc Good morning briefing
@job_search Find ML Engineer roles at Anthropic
@researcher What's new in AI today?
@writer Create blog post about AI agents
@social Create Twitter thread about my project
@cc_team Help me prepare for my day
@content Create weekly newsletter
```

**Welcome to the world of agentic AI!** 🚀

---

## 📊 Quick Reference

### Most Used Commands

```bash
# System
python -m agency start              # Start everything
python -m agency status             # Check status
python -m agency logs -f            # View logs
python -m agency stop               # Stop system

# Messaging
python -m agency send "message" cc
python -m agency broadcast "message" --team cc_team

# Management
python -m agency agent list
python -m agency team list
python -m agency config show
```

### Most Used Telegram Commands

```
@cc Good morning briefing
@cc Schedule meeting with [name] [time]
@cc Draft email to [name] about [topic]
@job_hunter Find [role] at [company]
@resume_optimizer Tailor resume for [role]
@networker Who can refer me to [company]?
@researcher What's new in [topic]?
@writer Create [content type] about [topic]
@social Create [platform] post about [topic]
```

---

**Build amazing things with your AI agency!** ✨🤖💪
