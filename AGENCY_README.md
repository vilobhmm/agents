# 🤖 Agency - Multi-Agent Multi-Channel Coordination System

**Simple. Powerful. 24/7.**

A lightweight multi-agent system inspired by [tinyclaw](https://github.com/jlia0/tinyclaw), built for AI-powered intelligence, content creation, and social media management.

---

## 🎯 What is Agency?

Agency is a **decentralized multi-agent coordination system** that uses:

✅ **File-based queues** - Atomic, crash-safe, observable
✅ **Actor model** - No central orchestrator, message-driven
✅ **Per-agent chains** - Sequential per agent, parallel across agents
✅ **Simple tracking** - Pending counters, not state machines
✅ **Multi-channel** - Telegram, Discord, Slack, WhatsApp (coming soon)
✅ **Team coordination** - Agents collaborate via mentions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Telegram / Discord / Slack                  │
└────────────────────┬────────────────────────────────────────┘
                     │ JSON message files
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              File-Based Queue System                         │
│         (incoming/ → processing/ → outgoing/)               │
└────────────────────┬────────────────────────────────────────┘
                     │ Agency Processor
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Per-Agent Processing (Parallel)                      │
│         - Researcher sequential queue                        │
│         - Social concurrent queue                            │
│         - Writer sequential queue                            │
└────────────────────┬────────────────────────────────────────┘
                     │ Anthropic Claude API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AI Responses & Actions                          │
│    (Research, Social Posts, Content Creation, etc.)         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites

```bash
# Install dependencies
pip install anthropic python-telegram-bot python-dotenv

# Set up environment
export ANTHROPIC_API_KEY="sk-ant-..."
export TELEGRAM_BOT_TOKEN="123456:ABC..."
export TELEGRAM_ALLOWED_USERS="your_telegram_user_id"
```

### 2. Start the System

```bash
# Start full system (processor + Telegram bot)
python -m agency start
```

### 3. Talk to Agents via Telegram

```
You: @researcher What's new in AI today?
Researcher: Here's what's happening in AI...

You: @social Post a tweet about Claude 4.5
Social: I'll create a tweet...

You: @content Create a newsletter about AI trends
Coordinator: I'll research and write that for you.
  [@researcher: Find latest AI trends]
  [@writer: Draft newsletter about these trends]
```

**That's it!** 🎉

---

## 📦 What's Included

### Pre-Built Agents

#### 🔍 **@researcher** - Research Assistant
- Monitors AI news, papers, trends
- Access to Twitter/X, ArXiv, Hacker News
- Summarizes complex research
- Identifies important breakthroughs

#### 📱 **@social** - Social Media Manager
- Creates tweets and threads
- Writes LinkedIn posts
- Optimizes for engagement
- Platform-specific best practices

#### ✍️ **@writer** - Content Writer
- Writes newsletters and articles
- Clear, engaging style
- Structures content effectively
- Compelling headlines

#### 📚 **@curator** - Content Curator
- Finds high-quality sources
- Evaluates relevance
- Organizes by topic
- Creates reading lists

#### 🎯 **@coordinator** - Team Coordinator
- Delegates to specialists
- Manages multi-agent workflows
- Ensures quality
- Synthesizes results

### Pre-Built Teams

#### 📝 **@content** - Content Creation Team
- Members: coordinator, researcher, writer
- Creates research-backed content
- Handles full content pipeline

#### 🧠 **@intelligence** - Intelligence Team
- Members: coordinator, researcher, curator
- Gathers and analyzes intelligence
- Delivers actionable insights

#### 🌐 **@social_team** - Social Media Team
- Members: coordinator, researcher, social
- Researches trends
- Creates engaging posts
- Manages social presence

---

## 💬 How to Use

### Single Agent

```
@researcher What are the latest Claude 4.5 capabilities?
@social Post a thread about AI safety
@writer Draft a newsletter introduction
```

### Team Collaboration

```
@content Write a blog post about AI agents

# Coordinator receives request
# → Mentions @researcher: "Research AI agents"
# → Researcher responds with findings
# → Mentions @writer: "Write blog post with this research"
# → Writer creates post
# → Coordinator aggregates and delivers
```

### Agent-to-Agent Communication

Agents can mention teammates:

```python
# Agent response format:
"I've researched AI trends. [@writer: Create a newsletter from these findings]"

# Results in:
# 1. Writer receives directed message
# 2. Writer processes and responds
# 3. Conversation completes
# 4. All responses aggregated and sent to user
```

---

## 🔧 Configuration

### Custom Agents

Edit `agency/templates/agents.json`:

```json
{
  "agents": {
    "my_agent": {
      "name": "My Custom Agent",
      "agent_id": "my_agent",
      "provider": "anthropic",
      "model": "sonnet",
      "personality": "You are a...",
      "skills": ["Skill 1", "Skill 2"]
    }
  }
}
```

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=123456:ABC...

# Optional
TELEGRAM_ALLOWED_USERS=user1,user2  # Comma-separated
OPENAI_API_KEY=sk-...               # For OpenAI models

# Integrations (from QUICK_INTEGRATION_GUIDE.md)
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
LINKEDIN_CLIENT_ID=...
GITHUB_TOKEN=...
```

---

## 🛠️ Commands

```bash
# Start full system (processor + Telegram)
python -m agency start

# Start only processor
python -m agency process

# Start only Telegram bot
python -m agency telegram

# Send test message
python -m agency send "Your message" researcher
```

---

## 📁 Directory Structure

```
~/agency-workspace/          # Agent workspaces
├── researcher/
│   ├── IDENTITY.md          # Agent personality
│   ├── TEAMMATES.md         # Team info
│   └── conversation.json    # Conversation history
├── social/
├── writer/
└── ...

~/.agency/                   # System state
├── queue/
│   ├── incoming/            # New messages
│   ├── processing/          # Being processed
│   └── outgoing/            # Ready to send
├── conversations/           # Active conversations
└── chats/                   # Team conversation archives
    └── content/
        └── 2026-02-15_....md
```

---

## 🎨 Key Features

### 1. Crash-Safe

File-based queues with automatic recovery:
- Atomic file operations
- Orphaned message detection
- No lost messages

### 2. Observable

Everything is visible in the filesystem:
```bash
ls ~/.agency/queue/incoming/    # See pending messages
ls ~/.agency/queue/processing/  # See what's processing
ls ~/.agency/queue/outgoing/    # See responses ready to send
```

### 3. Parallel Processing

- Same agent: Sequential (preserves context)
- Different agents: Parallel (no blocking)
- 3 agents × 30s each = ~30s total (not 90s)

### 4. Team Coordination

Agents collaborate naturally:
```
@coordinator Task X
  └→ [@researcher: subtask 1]
     └→ [@writer: subtask 2 using researcher's output]
        └→ All responses aggregated
```

### 5. Loop Protection

Built-in protection against infinite loops:
- Max 50 messages per conversation
- Automatic termination
- Warning logs

---

## 🔌 Integrations

Agency integrates with all services from `QUICK_INTEGRATION_GUIDE.md`:

✅ **Google Services** (Gmail, Calendar, Drive)
✅ **Twitter/X** (Post, search, monitor)
✅ **LinkedIn** (Professional content)
✅ **GitHub** (Repositories, trends)
✅ **ArXiv** (Research papers)
✅ **Hacker News** (Tech news)

Agents can use these services automatically!

---

## 📚 Use Cases

### 1. Daily Intelligence Briefing

```
@intelligence Give me a briefing on AI news today

# Coordinator gathers from:
# - Twitter AI hashtags
# - ArXiv papers
# - Hacker News
# - AI company blogs
# Delivers comprehensive briefing
```

### 2. Social Media Automation

```
@social_team Create content about [topic]

# Researcher finds trends
# Social creates optimized posts
# Posts to Twitter and LinkedIn
```

### 3. Newsletter Creation

```
@content Create this week's AI newsletter

# Researcher gathers news
# Curator selects best stories
# Writer crafts newsletter
# Coordinator delivers final version
```

### 4. 24/7 Autonomous Operation

Agents can work continuously:
- Monitor sources
- Create content
- Post updates
- Respond to mentions
- All without manual intervention

---

## 🆚 Why Agency vs. Alternatives?

| Feature | Agency | LangGraph | AutoGPT | CrewAI |
|---------|--------|-----------|---------|--------|
| **Simplicity** | ✅ File-based, no DB | ❌ Complex graphs | ❌ Heavy framework | ⚠️ Medium |
| **Crash-safe** | ✅ Automatic recovery | ⚠️ Depends on setup | ❌ No | ⚠️ Depends |
| **Observable** | ✅ Filesystem | ❌ Black box | ❌ Black box | ⚠️ Limited |
| **Multi-channel** | ✅ Telegram, Discord, etc. | ❌ No | ❌ No | ❌ No |
| **Team coordination** | ✅ Natural mentions | ⚠️ Manual graph | ❌ No | ✅ Yes |
| **Setup time** | ✅ 5 minutes | ❌ Hours | ❌ Hours | ⚠️ 30 min |

---

## 🤝 Inspiration

This project is inspired by [tinyclaw](https://github.com/jlia0/tinyclaw) by @jlia0.

Key insights borrowed from tinyclaw:
- File-based queues for crash safety
- Per-agent promise chains for parallel processing
- Actor model for decentralized coordination
- Simple conversation tracking (pending counter)
- Team coordination via mentions

Agency adapts these concepts to Python with:
- async/await instead of TypeScript promises
- Integration with external services (Google, Twitter, etc.)
- Pre-built agents for common use cases
- Simplified configuration

**Thank you to the tinyclaw team for the elegant architecture!** 🙏

---

## 📖 Documentation

- **Quick Integration Guide**: `QUICK_INTEGRATION_GUIDE.md`
- **External Services Setup**: `EXTERNAL_SERVICES_SETUP.md`
- **Verify Integrations**: `python verify_integrations.py`

---

## 🚧 Roadmap

- [ ] Discord channel support
- [ ] Slack channel support
- [ ] WhatsApp channel support
- [ ] Web dashboard
- [ ] Proactive agents (heartbeat-based)
- [ ] Advanced scheduling
- [ ] Multi-model support (OpenAI, local models)
- [ ] Agent skill marketplace

---

## 📝 License

MIT License - Feel free to use, modify, and distribute!

---

## 🎉 Get Started Now!

```bash
# 1. Install
pip install anthropic python-telegram-bot python-dotenv

# 2. Configure
export ANTHROPIC_API_KEY="sk-ant-..."
export TELEGRAM_BOT_TOKEN="..."

# 3. Run
python -m agency start

# 4. Chat with agents via Telegram!
@researcher What's new in AI?
```

**Build your AI agent empire today!** 🚀
