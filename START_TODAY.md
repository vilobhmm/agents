# 🚀 START USING AVENGERS SYSTEM TODAY

**Complete setup in 15 minutes. No technical expertise required.**

*Multi-agent Agentic - Personal. Proactive. Powerful.*

---

## 📋 What You'll Have After This Guide

- ✅ Iron Man (Chief of Staff) accessible via Telegram
- ✅ 6 AI agents working for you 24/7
- ✅ Daily AI intelligence briefings
- ✅ Task delegation via chat
- ✅ Automated prototyping, tweeting, posting

**Time Required:** 15 minutes
**Cost:** Free (Anthropic API usage only)

---

## 🎯 Step 1: Get Your Anthropic API Key (3 minutes)

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Click "Get API Keys" or "API Keys" in the sidebar
4. Click "Create Key"
5. **Copy the key** (starts with `sk-ant-`)
6. Save it somewhere safe

**💰 Cost:** ~$3-5/month for personal use with this system

---

## 🤖 Step 2: Create Your Telegram Bot (5 minutes)

### A. Create the Bot

1. **Open Telegram** (on your phone or desktop)

2. **Search for:** `@BotFather`

3. **Send:** `/newbot`

4. **BotFather asks:** "Alright, a new bot. How are we going to call it?"
   - **You send:** `My Avengers AI` (or any name you like)

5. **BotFather asks:** "Good. Now let's choose a username for your bot."
   - **You send:** `my_avengers_ai_bot` (must end in 'bot' and be unique)
   - Try variations if taken: `my_ai_team_bot`, `personal_ai_assistant_bot`, etc.

6. **BotFather responds** with your bot token:
   ```
   Done! Congratulations on your new bot.
   ...
   Use this token to access the HTTP API:
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

7. **COPY THIS TOKEN** - you'll need it in a moment

### B. Get Your Chat ID

1. **Send a message to your bot:**
   - Search for your bot's username in Telegram
   - Send it any message (like "hello")

2. **Get your chat ID** (choose ONE method):

   **Method A - Using a bot (easiest):**
   - Search for `@userinfobot` in Telegram
   - Send it any message
   - It will show your chat ID (a number like `123456789`)

   **Method B - Using a web request:**
   - Open this URL in your browser (replace YOUR_BOT_TOKEN):
     ```
     https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
     ```
   - Look for `"chat":{"id":123456789` in the response
   - The number is your chat ID

3. **SAVE YOUR CHAT ID**

---

## 💻 Step 3: Install OpenClaw (5 minutes)

### A. Clone the Repository

```bash
# Clone the repo
git clone https://github.com/vilobhmm/agents.git openclaw
cd openclaw

# Or if you already have it
cd /path/to/openclaw
git pull origin claude/openclaw-weekend-projects-st5pW
```

### B. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### C. Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- anthropic (Claude AI)
- python-telegram-bot (Telegram interface)
- apscheduler (Task scheduling)
- All other dependencies

---

## ⚙️ Step 4: Configure Environment (2 minutes)

### A. Create .env File

```bash
# Copy the example
cp .env.example .env

# Edit it
nano .env
# Or use any text editor: code .env, vim .env, etc.
```

### B. Add Your Credentials

**REQUIRED (minimum setup):**

```bash
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=your_chat_id_here
```

**OPTIONAL (for full functionality):**

```bash
# GitHub (for Hulk to create repos)
GITHUB_TOKEN=ghp_your_github_token
GITHUB_USERNAME=your_github_username

# Twitter (for Thor to post)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_secret

# LinkedIn (for Black Widow to post)
LINKEDIN_ACCESS_TOKEN=your_token
```

**Save and close** (in nano: Ctrl+X, then Y, then Enter)

---

## 🎬 Step 5: Start Your AI Team! (NOW!)

### Option A: Telegram Only (Recommended for First Run)

**Just start the Telegram interface:**

```bash
python -m projects.11_avengers_system.telegram_manager
```

You should see:

```
🛡⚡ AVENGERS AI OPERATING SYSTEM - TELEGRAM INTERFACE

*Multi-agent Agentic - Personal. Proactive. Powerful.*

Initializing agents...

✅ Iron Man ready
✅ All agents coordinated

🚀 SYSTEM READY

Interact with Iron Man via Telegram!
```

**That's it!** 🎉

### Option B: Full System (Background Agents + Telegram)

**Terminal 1 - Start the background agent system:**

```bash
python -m projects.11_avengers_system.main
```

**Terminal 2 - Start Telegram interface:**

```bash
python -m projects.11_avengers_system.telegram_manager
```

---

## 💬 Step 6: Talk to Iron Man!

### Open Telegram

1. Find your bot (search for the username you created)
2. Send: `/start`

You'll see:

```
🛡⚡ AVENGERS AI OPERATING SYSTEM

Welcome! I'm Iron Man, your Chief of Staff.

I coordinate your AI team of 6 specialized agents:
🛡 Captain America - Research & Intelligence
⚡ Thor - X/Twitter Content
🕷 Black Widow - LinkedIn Authority
🔨 Hulk - GitHub Prototypes
🎯 Hawkeye - Newsletter Curation
```

### Try These Commands

```
/status
```
See what all agents are doing

```
/assign Build a tiny RAG demo
```
Iron Man will assign it to Hulk and track progress

```
What's the most important AI news today?
```
Natural conversation - Iron Man will ask Captain America and respond

```
/morning
```
Get your morning briefing

```
/help
```
See all available commands

---

## 🎯 First Day Checklist

Do these to verify everything works:

1. **✅ Send `/start`** to your bot
   - Confirms: Telegram connection works

2. **✅ Send `/status`**
   - Confirms: Iron Man can coordinate agents

3. **✅ Send "What is RAG?"**
   - Confirms: Natural conversation works

4. **✅ Send `/assign Build a hello world Python script`**
   - Confirms: Task assignment works
   - (Hulk will create it if you have GitHub configured)

5. **✅ Send `/morning`**
   - Confirms: Briefing generation works

---

## 🔧 Troubleshooting

### "ANTHROPIC_API_KEY not found"

**Fix:**
- Make sure .env file is in the root directory
- Check the key starts with `sk-ant-`
- No quotes needed: `ANTHROPIC_API_KEY=sk-ant-xxx` (not `"sk-ant-xxx"`)

### "TELEGRAM_BOT_TOKEN not found"

**Fix:**
- Copy token exactly from BotFather
- Format: `TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI`
- No spaces, no quotes

### Bot doesn't respond

**Fix:**
1. Check bot is running (should see "SYSTEM READY")
2. Make sure you sent `/start` first
3. Check TELEGRAM_CHAT_ID matches your chat ID
4. Restart: Ctrl+C, then run again

### "Module not found" errors

**Fix:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Agent says "No API credentials"

**This is OK for first run!**
- Captain America, Thor, etc. need their specific API keys
- Iron Man works without them
- Add credentials later as you need them

---

## 🎓 What to Do Next

### Day 1: Get Familiar

- Talk to Iron Man naturally
- Try `/assign` with simple tasks
- Check `/status` to see agent activity
- Read the commands with `/help`

### Day 2: Add Integrations

**Priority order:**

1. **GitHub** (so Hulk can create repos)
   - Settings → Developer Settings → Personal Access Tokens
   - Create token with `repo` scope
   - Add to .env

2. **Twitter** (so Thor can post)
   - https://developer.twitter.com
   - Create app, get API keys
   - Add to .env

3. **LinkedIn** (so Black Widow can post)
   - More complex - see LinkedIn API docs
   - Optional for now

### Week 1: Build Your Workflow

- **Morning:** Send `/morning` for your briefing
- **During Day:** Assign tasks as you think of them
- **Evening:** Send `/evening` for summary
- **Weekly:** Review `/sprint` to see what was built

### Ongoing: Customize

- Edit schedules in `projects/11_avengers_system/config.py`
- Add your own agents
- Customize Iron Man's behavior
- Share your setup!

---

## 📚 Advanced Features

Once you're comfortable, explore:

### Run Background Agents

Start the full system to enable:
- Automatic research sweeps (Captain America)
- Scheduled tweeting (Thor)
- Weekly newsletters (Hawkeye)

```bash
# Terminal 1
python -m projects.11_avengers_system.main

# Terminal 2
python -m projects.11_avengers_system.telegram_manager
```

### Add Custom Agents

Create your own in `projects/11_avengers_system/`
- Follow the pattern of existing agents
- Iron Man will coordinate automatically

### API Webhooks

Set up webhooks to trigger agents:
- Research update? → Notify Captain America
- New GitHub star? → Tell Iron Man
- Email received? → Triage it

---

## 💡 Pro Tips

1. **Use Natural Language**
   - "Build a demo" works better than "/assign Build a demo"
   - Iron Man understands context

2. **Check Status Regularly**
   - `/status` shows what everyone's doing
   - Great for debugging

3. **Start Simple**
   - Don't try to configure everything day 1
   - Add integrations as you need them

4. **Review Logs**
   - Check `avengers.log` for details
   - Helpful for debugging

5. **Keep It Running**
   - Use `screen` or `tmux` for persistent sessions
   - Or run on a server/Raspberry Pi

---

## 🎯 Success Criteria

You've successfully set up the system when:

- ✅ Iron Man responds to `/start`
- ✅ `/status` shows agent statuses
- ✅ You can have natural conversations
- ✅ `/assign` creates tasks
- ✅ Morning briefings work

**Everything else is optional enhancement!**

---

## 🆘 Getting Help

If you're stuck:

1. **Check the logs:** `tail -f avengers.log`
2. **Read error messages** - they're usually clear
3. **Re-read this guide** - did you miss a step?
4. **Check .env format** - most issues are here
5. **Try minimal config** - just API key + Telegram

---

## 🎉 You're Ready!

Open Telegram. Send `/start` to your bot.

**Welcome to your AI workforce.**

*Multi-agent Agentic - Personal. Proactive. Powerful.*

---

## 📖 Further Reading

- **Full System Docs:** `projects/11_avengers_system/README.md`
- **Agent Details:** Individual agent files
- **Configuration:** `projects/11_avengers_system/config.py`
- **Examples:** Chat logs in the README

---

**Questions? Issues? Improvements?**

Open an issue or contribute to the project!

**Now go build something. Your AI team is waiting.** 🚀
