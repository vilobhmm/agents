# 🚀 Agency System - Quick Start Guide

## Prerequisites

1. **Python 3.10+** installed
2. **Anthropic API Key** ([get one here](https://console.anthropic.com/))
3. **Telegram Bot Token** (optional, for Telegram features)

## 1. Setup Environment

Create a `.env` file in the project root:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional - for Telegram bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ALLOWED_USERS=your_telegram_user_id

# Optional - for Google integrations (CC agent)
GOOGLE_OAUTH_CREDENTIALS=google_oauth_credentials.json
GOOGLE_TOKEN_PATH=google_token.pickle
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Start the Agency

### Option A: Start Everything (Recommended)

```bash
# Using the quick start script
./start_agency.sh

# Or using the CLI
python -m agency start
```

This starts:
- ✅ Message processor (routes messages to agents)
- ✅ Telegram bot (if configured)

### Option B: Start Components Separately

```bash
# Terminal 1: Start processor
python -m agency start --processor-only

# Terminal 2: Start Telegram bot
python -m agency start --telegram-only
```

### Option C: Background Mode

```bash
# Start in background
python -m agency start --detach

# View logs
python -m agency logs -f

# Stop
python -m agency stop
```

## 4. Test the System

### Test via CLI

```bash
# Send a message to an agent
python -m agency send "Hello! Give me a brief update." cc

# Or use the test script
python test_agency.py
```

### Test via Telegram

Open your Telegram bot and try:

**Quick Commands:**
- `/help` - See all agents and commands
- `/briefing` - Get daily briefing from CC
- `/jobs` - Search for job opportunities
- `/research` - Get latest AI research
- `/agents` - List all agents
- `/teams` - List all teams
- `/status` - System status

**Direct Agent Messages:**
```
@cc Good morning! Give me a daily briefing
@researcher What's new in AI today?
@job_hunter Find ML Engineer jobs at Anthropic and OpenAI
@writer Draft a newsletter about AI trends
```

## 5. Available Agents

All agents use **Claude Sonnet 4.5** (claude-sonnet-4-5-20250929):

### Personal Productivity
- `@cc` - Chief Coordinator (productivity, briefings)
- `@assistant` - Personal assistant (scheduling, organization)
- `@action_taker` - Action execution (emails, calendar, etc.)

### Job Search
- `@job_hunter` - Find job opportunities
- `@resume_optimizer` - Optimize resumes and applications
- `@networker` - Professional networking and outreach

### Content & Research
- `@researcher` - AI/tech research assistant
- `@writer` - Content writer (newsletters, articles)
- `@social` - Social media manager
- `@curator` - Content curation
- `@coordinator` - Team coordinator

## 6. Available Teams

Teams are coordinated groups of agents working together:

- `@cc_team` - Personal productivity (led by CC)
- `@job_search` - Complete job search automation
- `@content` - Full-service content creation
- `@intelligence` - Intelligence gathering and analysis
- `@social_team` - Social media management

## 7. Common Issues

### Messages not being processed

**Problem:** You send a message but get no response.

**Solution:**
1. Check if the agency is running: `python -m agency status`
2. Start it if not: `python -m agency start`
3. Check logs: `python -m agency logs -f`

### Telegram bot not responding

**Problem:** Telegram commands don't work.

**Solution:**
1. Check if both processor AND Telegram are running
2. Verify `TELEGRAM_BOT_TOKEN` is set in `.env`
3. Restart: `python -m agency stop && python -m agency start`

### "Agent not found" error

**Problem:** `agency send` says agent doesn't exist.

**Solution:**
1. List available agents: `python -m agency list agents`
2. Use exact agent ID (e.g., `cc`, `job_hunter`, not `CC` or `Job Hunter`)

## 8. System Architecture

```
┌─────────────────┐
│  Telegram Bot   │ ─┐
└─────────────────┘  │
                     ├─> ┌──────────────┐    ┌───────────────┐
┌─────────────────┐  │   │ File Queue   │───>│   Processor   │
│   CLI (send)    │ ─┘   │  (incoming)  │    │  (router)     │
└─────────────────┘      └──────────────┘    └───────┬───────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  Agent        │
                                              │  (Claude API) │
                                              └───────┬───────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  File Queue   │
                                              │  (outgoing)   │
                                              └───────┬───────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  Telegram     │
                                              │  (send reply) │
                                              └───────────────┘
```

## 9. Next Steps

1. **Configure Google Services** (for CC agent):
   - Follow `EXTERNAL_SERVICES_SETUP.md`
   - Enables email, calendar, drive access

2. **Customize Agents**:
   - Edit `agency/templates/agents.json`
   - Add skills, change personalities, adjust models

3. **Add Integrations**:
   - See `QUICK_INTEGRATION_GUIDE.md`
   - Add Slack, WhatsApp, Notion, GitHub, etc.

4. **Build Custom Agents**:
   - Use `python -m agency create` to scaffold new agents
   - Customize for your specific needs

## 10. Getting Help

- **View logs**: `python -m agency logs -f`
- **Check status**: `python -m agency status`
- **List agents**: `python -m agency list agents`
- **Test messaging**: `python test_agency.py`

## Quick Reference

```bash
# Start
python -m agency start              # Start everything
python -m agency start --detach     # Background mode

# Status
python -m agency status             # Check if running
python -m agency logs -f            # View live logs

# Messaging
python -m agency send "Hello" cc    # Send to agent
python test_agency.py               # Test system

# Stop
python -m agency stop               # Stop all

# Telegram (if configured)
/briefing    # Daily briefing
/jobs        # Job search
/research    # AI research
/agents      # List agents
```

---

**Ready to go!** Start the agency with `./start_agency.sh` or `python -m agency start` 🚀
