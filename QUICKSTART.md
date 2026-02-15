# OpenClaw Quick Start Guide

Get your AI workforce running in under 10 minutes.

## What You're Building

By the end of this guide, you'll have:
- ✅ A Telegram bot that controls all your AI agents
- ✅ At least 2 agents running and working for you
- ✅ Automated daily briefings delivered to your phone
- ✅ A personal AI workforce you control via chat

## Prerequisites

- Python 3.9+ installed
- A Telegram account
- An Anthropic API key ([get one here](https://console.anthropic.com/))

## 5-Minute Setup

### Step 1: Clone & Install (2 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/openclaw.git
cd openclaw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Telegram Bot (2 minutes)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Name your bot: `My AI Manager`
4. Username: `my_ai_manager_bot` (must be unique)
5. **Save the token** BotFather gives you!

### Step 3: Get Your Chat ID (1 minute)

1. Search for `@userinfobot` in Telegram
2. Start a chat - it shows your chat ID
3. **Save this number!**

### Step 4: Configure Environment (1 minute)

```bash
# Copy example config
cp .env.example .env

# Edit .env
nano .env  # or use any text editor
```

Add these three essential values:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=your_chat_id_here
```

Save and exit.

### Step 5: Start Your AI Manager (30 seconds)

```bash
python telegram_manager.py
```

You should see:
```
🚀 OpenClaw Telegram Manager Started!
Bot is running and ready to receive commands
```

### Step 6: Activate Your First Agents (1 minute)

Open Telegram, find your bot, and send:

```
/start
```

The bot will greet you! Now activate your first agents:

```
/activate research
/activate email
```

Success! You now have 2 AI agents working for you.

## What To Do Next

### Test Your Agents

```
/ask research What should I read today?
/ask email Do I have any urgent emails?
```

### Check Status

```
/status
```

See which agents are running and their schedules.

### Morning Routine

```
/morning
```

Get a comprehensive morning briefing from all your agents.

### View All Commands

```
/help
```

## Common First-Time Issues

### "Bot not responding"
- Check if `telegram_manager.py` is still running
- Verify bot token in `.env`
- Make sure you messaged the correct bot

### "Agent activation failed"
- Missing API keys (check `.env`)
- Invalid credentials
- Run `/logs <agent>` to see error details

### "No agents listed"
- Restart: `python telegram_manager.py`
- Check logs: `tail -f openclaw.log`

## What Each Agent Does

**Research Assistant** (`research`)
- Monitors your reading lists
- Sends morning article summaries
- Creates reading blocks on calendar

**Email Triage** (`email`)
- Categorizes incoming emails
- Drafts responses
- Alerts you to urgent messages

**Meeting Prep** (`meeting`)
- Scans calendar 24 hours ahead
- Gathers context from emails/Slack
- Sends meeting briefings

**Expense Tracker** (`expense`)
- Processes receipt emails
- Categorizes spending
- Sends weekly reports

**Code Review** (`code`)
- Monitors GitHub PRs
- Analyzes code changes
- Drafts review comments

## Next Steps

1. **Read the detailed Telegram Guide**: [TELEGRAM_GUIDE.md](TELEGRAM_GUIDE.md)
2. **Explore all use cases**: [PROJECTS.md](PROJECTS.md)
3. **Set up more integrations**: Check `.env.example`
4. **Create custom agents**: See `examples/` directory
5. **Join the community**: Share your setup!

## Success Checklist

- [ ] Telegram bot created and responding
- [ ] At least 2 agents activated
- [ ] Successfully asked an agent a question
- [ ] Received `/morning` briefing
- [ ] Understood how to `/activate` and `/deactivate` agents

**All checked?** Congratulations! You now have a personal AI workforce. 🎉

---

**Ready to go deeper?** Check out the [Complete Telegram Guide](TELEGRAM_GUIDE.md) for advanced features, troubleshooting, and real-world usage examples.

Happy automating! 🚀
