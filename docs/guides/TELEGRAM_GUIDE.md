# OpenClaw Telegram Integration Guide

Complete guide to running and managing your AI agents via Telegram like virtual employees.

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [Setting Up Your Telegram Bot](#setting-up-your-telegram-bot)
3. [Running the Agent Manager](#running-the-agent-manager)
4. [Managing Your Agents](#managing-your-agents)
5. [Agent Commands](#agent-commands)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

---

## Quick Setup

### 1. Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to create a new bot
3. Follow prompts to name your bot (e.g., "My OpenClaw Manager")
4. BotFather will give you a **bot token** - save this!
5. Send `/mybots`, select your bot, then "Edit Bot" → "Edit Commands"
6. Paste these commands:

```
start - Start the agent manager
status - View all agent statuses
agents - List all available agents
activate - Activate an agent
deactivate - Deactivate an agent
ask - Ask an agent a question
report - Get agent activity report
schedule - View agent schedules
help - Show all commands
```

### 2. Get Your Chat ID

Two ways to get your chat ID:

**Option A - Using userinfobot:**
1. Search for `@userinfobot` in Telegram
2. Start a chat - it will show your chat ID

**Option B - Using your bot:**
1. Start your bot (instructions below)
2. Send `/start` to your bot
3. Check the logs - your chat ID will be printed

### 3. Configure Environment Variables

Edit your `.env` file:

```bash
# Telegram Configuration
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional: Restrict to specific users
TELEGRAM_ALLOWED_USERS=user_id_1,user_id_2

# Anthropic API (required)
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Agent Manager

```bash
python telegram_manager.py
```

You should see:
```
OpenClaw Telegram Manager started!
Bot username: @YourBotName
Send /start to your bot to begin
```

### 6. Start Using Your Agents!

Open Telegram, find your bot, and send:
```
/start
```

You'll see a welcome message with available commands. You're ready to go!

---

## Setting Up Your Telegram Bot

### Detailed Setup

#### Step 1: Create Bot with BotFather

```
You: /newbot
BotFather: Alright, a new bot. How are we going to call it?

You: OpenClaw Manager
BotFather: Good. Now let's choose a username for your bot.

You: openclaw_manager_bot
BotFather: Done! Congratulations on your new bot.
```

**Save the token that BotFather gives you!**

#### Step 2: Configure Bot Settings

1. **Set bot description** (shows when users first interact):
```
/setdescription
```
Then send:
```
I manage your AI agents. Send /start to begin!
```

2. **Set about text**:
```
/setabouttext
```
Then send:
```
OpenClaw Agent Manager - Control your personal AI workforce via Telegram
```

3. **Set bot profile picture** (optional):
```
/setuserpic
```
Upload an image

#### Step 3: Security Settings

For personal use, you can restrict the bot to only respond to you:

In `.env`:
```bash
TELEGRAM_ALLOWED_USERS=your_user_id
```

To get your user ID, use `@userinfobot` or check logs when you first message your bot.

---

## Running the Agent Manager

### Start the Manager

```bash
# Basic start
python telegram_manager.py

# With custom config
python telegram_manager.py --config my_config.env

# In background (Linux/Mac)
nohup python telegram_manager.py > openclaw.log 2>&1 &

# Using screen (recommended for servers)
screen -S openclaw
python telegram_manager.py
# Press Ctrl+A then D to detach
# screen -r openclaw to reattach
```

### Verify It's Running

Send `/start` to your bot. You should receive:

```
👋 Welcome to OpenClaw Agent Manager!

I manage your personal AI workforce. Your agents are standing by and ready to assist.

Available agents:
📚 Research Assistant
📅 Meeting Prep
💻 Code Review
💰 Expense Tracker
🎓 Learning Path
✈️ Travel Autopilot
📄 Research Digest
🔄 Context Switcher
📧 Email Triage
🧠 Knowledge Graph

Use /help to see all commands
Use /agents to view detailed agent info
```

---

## Managing Your Agents

### Core Workflow

1. **Check status** → See what agents are running
2. **Activate agents** → Start the ones you need
3. **Monitor** → Get updates and reports
4. **Ask questions** → Interact directly with agents
5. **Review reports** → See what agents have done

### Example Session

```
You: /status

Bot: 📊 Agent Status:

✅ Active (3):
- Research Assistant (last run: 2 hours ago)
- Email Triage (last run: 30 min ago)
- Expense Tracker (last run: 1 day ago)

💤 Inactive (7):
- Meeting Prep
- Code Review
- Learning Path
- Travel Autopilot
- Research Digest
- Context Switcher
- Knowledge Graph

You: /activate meeting_prep

Bot: ✅ Meeting Prep Agent activated!

Schedule: Runs daily at 7:00 AM
Next run: Tomorrow at 7:00 AM

The agent will scan your calendar 24 hours ahead and send briefings automatically.

You: /ask research What did I learn about AI this week?

Bot: 🤔 Asking Research Assistant...

Research Assistant: Based on your reading list this week, you explored:

1. Transformer architecture improvements
2. Retrieval-augmented generation (RAG)
3. Agent frameworks and tool use

Key papers:
- "Attention Is All You Need" revisited
- Latest advances in context length

Would you like detailed summaries of any of these topics?

You: /report research

Bot: 📊 Research Assistant Report (Last 7 Days):

📚 Articles Processed: 23
⏱️ Total reading time saved: 4.5 hours
📝 Summaries created: 23
📅 Calendar blocks created: 5
💾 Notion pages: 23

Top categories:
- AI/ML: 15 articles
- Programming: 5 articles
- Productivity: 3 articles

Next scheduled run: Tonight at 2:00 AM
```

---

## Agent Commands

### Universal Commands

```
/start              - Start the agent manager
/help               - Show all available commands
/status             - View status of all agents
/agents             - List all agents with descriptions
```

### Agent Management

```
/activate <agent>   - Start an agent
/deactivate <agent> - Stop an agent
/schedule           - View all agent schedules
/restart <agent>    - Restart an agent
```

**Agent Names:**
- `research` - Research Assistant
- `meeting` - Meeting Prep
- `code` - Code Review
- `expense` - Expense Tracker
- `learning` - Learning Path
- `travel` - Travel Autopilot
- `papers` - Research Digest
- `context` - Context Switcher
- `email` - Email Triage
- `knowledge` - Knowledge Graph

### Interaction Commands

```
/ask <agent> <question>     - Ask an agent a question
/report <agent>             - Get agent's activity report
/config <agent>             - View agent configuration
/logs <agent>               - View recent agent logs
```

### Examples

```bash
# Activate agents
/activate research
/activate email
/activate expense

# Ask questions
/ask research What are the top papers this week?
/ask knowledge What did I learn about Python?
/ask email Do I have any urgent emails?

# Get reports
/report research
/report expense
/report email

# Check schedules
/schedule
/schedule research

# Deactivate when not needed
/deactivate travel
```

### Quick Actions

```
/today              - Get today's briefing from all active agents
/urgent             - Check for urgent items across all agents
/summary            - Get weekly summary
/morning            - Morning briefing (meetings, emails, tasks)
/evening            - Evening summary (what happened today)
```

---

## Advanced Usage

### Custom Schedules

You can customize when agents run:

```
You: /config research

Bot: Research Assistant Configuration:

Schedule: 2:00 AM daily (fetch articles)
         8:00 AM daily (send briefing)
Max articles: 10 per day
Summary style: bullet_points

To modify, use:
/set research schedule "0 3 * * *"
/set research max_articles 15

You: /set research schedule "0 3 * * *"

Bot: ✅ Research Assistant schedule updated!
New schedule: 3:00 AM daily
Next run: Tomorrow at 3:00 AM
```

### Agent Collaboration

Some agents work better together:

```bash
# Morning workflow
/activate meeting
/activate email
/activate context

# Research workflow
/activate research
/activate papers
/activate knowledge

# Travel workflow
/activate travel
/activate email
/activate meeting
```

### Direct Conversations

Start a conversation with a specific agent:

```
You: /chat research

Bot: 💬 Starting conversation with Research Assistant
Send 'exit' to end the conversation

Research Assistant: Hello! I can help you with your reading list. What would you like to know?

You: What should I read first?

Research Assistant: Based on your interests and current projects, I recommend starting with...

You: exit

Bot: ✅ Conversation ended
```

### Batch Operations

```bash
# Activate multiple agents
/batch activate research,email,expense

# Get multiple reports
/batch report research,email,knowledge

# Morning routine
/routine morning

# This activates: meeting, email, context
# And sends combined briefing
```

### Notifications

Configure when you want to be notified:

```bash
# Set quiet hours (no notifications)
/quiet 22:00-07:00

# Only notify for urgent items
/notify urgent

# Notify for everything
/notify all

# Daily digest only
/notify digest
```

---

## Real-World Usage Examples

### Morning Routine

```
6:30 AM - You wake up

You: /morning

Bot: ☀️ Good morning! Here's your briefing:

📅 MEETINGS TODAY (3):
9:00 AM - Team standup
11:00 AM - Product review (prep available)
3:00 PM - Client call (prep available)

📧 URGENT EMAILS (2):
- From: boss@company.com - "Q4 Planning"
- From: client@bigcorp.com - "Project timeline"

💰 EXPENSES (Yesterday):
Total: $87.45 (3 transactions)

📚 NEW ARTICLES (Last night):
5 articles summarized, Notion pages ready

💡 CONTEXT: You're working on the ML pipeline project
Relevant docs and tasks prepared

You: /ask meeting Tell me about the 11am product review

Bot: 🤔 Asking Meeting Prep Agent...

Meeting Prep: Product Review - 11:00 AM

Attendees: Sarah (PM), Mike (Eng), You
Context:
- Last discussed feature priorities 2 weeks ago
- 3 related Slack threads about performance issues
- Mike sent updated designs yesterday

Suggested Agenda:
1. Review current sprint progress
2. Discuss performance optimization approach
3. Finalize Q4 feature list
4. Set next review date

[Full briefing in Notion: link]
```

### Travel Day

```
Day before trip:

You: /activate travel

Bot: ✅ Travel Autopilot activated!
Monitoring your email for flight confirmations...

---

Next morning:

Bot: ✈️ FLIGHT DETECTED!

Flight: UA1234
SFO → NYC
Tomorrow, 2:00 PM

✅ Added to calendar
⏰ Set check-in reminder (24h before)
📧 Monitoring for updates

You: Thanks!

---

24 hours before:

Bot: ⏰ CHECK-IN REMINDER

Flight UA1234 - Check-in is now open!
Confirmation: ABC123

I'll monitor for delays and update you.

---

If delay occurs:

Bot: ⚠️ FLIGHT DELAY

Your flight UA1234 is delayed by 2 hours.
New departure: 4:00 PM

📅 Checking calendar for conflicts...
Found: 6:30 PM dinner in NYC

Options:
1. Cancel/reschedule dinner
2. Take later flight
3. Keep current flight (might be tight)

What would you like to do?
```

### Research Session

```
You: /chat research

Research Assistant: Hi! Ready to help with your reading and research.

You: I want to learn about RAG systems

Research Assistant: Great! I'll help you build a learning path.

🔍 Finding resources...

Found 12 high-quality resources:
- 3 foundational papers
- 2 implementation tutorials
- 4 real-world case studies
- 3 advanced topics

I'll:
1. ✅ Create learning schedule (next 2 weeks)
2. ✅ Add calendar blocks for reading
3. ✅ Generate quiz questions for each section
4. ✅ Track your progress

Starting with: "Retrieval-Augmented Generation for Large Language Models" (Lewis et al.)

Added to your reading queue. 1-hour block scheduled for tonight at 7 PM.

You: Perfect!

Research Assistant: I'll send a summary tonight and check-in in 2 days to see how you're progressing. Let me know if you need the schedule adjusted!
```

### Weekly Review

```
Friday evening:

You: /summary

Bot: 📊 WEEKLY SUMMARY

📚 Research Assistant:
- 34 articles processed
- 8 hours of reading condensed to 45 min
- 34 Notion pages created
- Top topics: AI agents, system design

📅 Meeting Prep:
- 12 meetings prepared
- 47 emails analyzed for context
- 83 Slack messages summarized
- Saved ~3 hours of prep time

💰 Expense Tracker:
- Total spent: $487.32
- 23 transactions categorized
- Top category: Food & Dining (42%)
- ⚠️ Above budget by $87

💻 Code Review:
- 8 PRs reviewed
- 47 suggestions made
- Average review time: 15 min
- 3 critical issues caught

📧 Email Triage:
- 156 emails processed
- 12 urgent (all notified)
- 43 responses drafted
- 89 archived
- 12 follow-ups sent

🧠 Knowledge Graph:
- 234 new nodes added
- 189 relationships mapped
- 3 insights surfaced
- Most connected: "AI agents"

🎯 Overall: Highly productive week!
   Time saved by agents: ~12 hours
   Tasks automated: 178
```

---

## Troubleshooting

### Bot Not Responding

1. **Check if manager is running:**
```bash
ps aux | grep telegram_manager
```

2. **Check logs:**
```bash
tail -f openclaw.log
```

3. **Verify bot token:**
```bash
# Test with curl
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

4. **Restart manager:**
```bash
pkill -f telegram_manager
python telegram_manager.py
```

### Agent Not Running

```
You: /logs research

Bot: 📋 Recent logs for Research Assistant:

ERROR: Failed to fetch Pocket articles
Reason: Invalid API credentials

Solution: Check POCKET_ACCESS_TOKEN in .env
```

Fix and restart:
```
You: /restart research

Bot: ✅ Research Assistant restarted
Status: Running
Next run: 2:00 AM
```

### Rate Limiting

If you're sending too many requests:

```
Bot: ⚠️ Rate limit reached
Please wait 30 seconds before sending more commands
```

### Permission Errors

```
Bot: ❌ Unauthorized
You are not in the allowed users list.

Contact the bot administrator.
```

Add your user ID to `.env`:
```bash
TELEGRAM_ALLOWED_USERS=123456789
```

### Common Issues

**Issue: "Agent already running"**
```
You: /activate research
Bot: ⚠️ Research Assistant is already active
     Last run: 5 minutes ago
     Next run: Tonight at 2:00 AM

     To restart: /restart research
```

**Issue: "Missing API key"**
```
You: /activate research
Bot: ❌ Cannot activate Research Assistant
     Missing: POCKET_ACCESS_TOKEN

     Please configure in .env and restart
```

**Issue: "No recent activity"**
```
You: /report research
Bot: Research Assistant has no recent activity

     Possible reasons:
     - Agent recently activated
     - No data sources configured
     - Errors during execution

     Check /logs research for details
```

---

## Tips & Best Practices

### 1. Start Small
Activate 2-3 agents first, learn how they work, then add more:
```bash
/activate email
/activate research
/activate expense
```

### 2. Set Up Integrations Gradually
Don't try to connect everything at once:
- Day 1: Telegram + basic agents
- Day 2: Add email integration
- Day 3: Add calendar
- Day 4: Add Notion
- etc.

### 3. Create Daily Routines
```bash
# Morning
/routine morning

# Lunch break
/status

# Evening
/routine evening
/summary
```

### 4. Use Agent Combinations
```bash
# Deep work session
/activate context
/activate research
/quiet 9:00-12:00

# Travel planning
/activate travel
/activate email
/activate meeting
```

### 5. Regular Check-ins
```bash
# Check status twice daily
Morning: /morning
Evening: /summary

# Weekly review
Friday: /summary
/report all
```

### 6. Customize Notifications
Find the right balance:
```bash
# Too noisy?
/notify urgent

# Missing important stuff?
/notify all

# Just want summaries?
/notify digest
```

---

## Next Steps

1. **Complete setup** following the Quick Start guide
2. **Start your first agent** with `/activate research`
3. **Experiment with commands** - ask questions, get reports
4. **Add more agents gradually** as you get comfortable
5. **Customize schedules** to match your workflow
6. **Set up integrations** (email, calendar, etc.)
7. **Create routines** for morning/evening
8. **Join the community** to share tips and learn from others

---

## Support

- **Check logs:** `/logs <agent>`
- **View configuration:** `/config <agent>`
- **Test connectivity:** `/status`
- **Restart if needed:** `/restart <agent>`

For more help, see:
- README.md - General documentation
- PROJECTS.md - Detailed project guides
- .env.example - Configuration reference

Happy automating! 🚀
