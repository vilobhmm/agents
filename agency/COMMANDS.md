# 🎯 Agency Commands Quick Reference

**Comprehensive CLI command reference (inspired by tinyclaw)**

---

## 📋 Command Overview

| Command | Description | tinyclaw equivalent |
|---------|-------------|---------------------|
| `start` | Start full system (processor + Telegram) | `pnpm dev` |
| `process` | Run queue processor only | `pnpm dev:processor` |
| `telegram` | Run Telegram bot only | `pnpm dev:telegram` |
| `send` | Send test message to agent | `pnpm send` |
| `status` | Show system status | _(new)_ |
| `reset` | Reset conversation state | `pnpm db:reset` |
| `clear` | Clear all persistent data | `pnpm db:clear` |
| `init` | Initialize workspace | _(new)_ |

---

## 🚀 Development Commands

### Start Full System

```bash
python -m agency start
```

Starts:
- ✅ Queue processor (handles agent invocations)
- ✅ Telegram bot (receives messages from Telegram)

**Use when:** You want the complete system running

**Equivalent to:** `pnpm dev` in tinyclaw

---

### Start Processor Only

```bash
python -m agency process
```

Starts:
- ✅ Queue processor only
- ❌ No Telegram bot

**Use when:**
- Testing without Telegram
- Running processor separately from channels
- Debugging agent logic

**Equivalent to:** `pnpm dev:processor` in tinyclaw

---

### Start Telegram Bot Only

```bash
python -m agency telegram
```

Starts:
- ✅ Telegram bot only
- ❌ No processor

**Use when:**
- Testing Telegram integration
- Running bot separately from processor
- Debugging channel logic

**Equivalent to:** `pnpm dev:telegram` in tinyclaw

---

## 🧪 Testing & Debugging

### Send Test Message

```bash
# Send to default agent (researcher)
python -m agency send "What's new in AI?"

# Send to specific agent
python -m agency send "Post a tweet about AI" social

# Send to a team
python -m agency send "Create content" content
```

Features:
- Enqueues message to incoming queue
- Waits for response (up to 2 minutes)
- Displays response when ready
- Works even without Telegram

**Use when:**
- Testing agents locally
- Debugging agent responses
- CI/CD testing

**Equivalent to:** `pnpm send <message> [agent]` in tinyclaw

---

### Show System Status

```bash
python -m agency status
```

Displays:
- 📦 Queue sizes (incoming, processing, outgoing)
- 💬 Active conversation count
- 🤖 Configured agents
- 👥 Configured teams
- 📍 Workspace and queue paths

**Example output:**
```
📊 AGENCY SYSTEM STATUS
====================================================

📦 Queue Status:
  Incoming:   3 messages
  Processing: 1 messages
  Outgoing:   0 messages

💬 Conversations:
  Active: 2

🤖 Configured Agents:
  @researcher     - Research Assistant
  @social         - Social Media Manager
  @writer         - Content Writer
  @curator        - Content Curator
  @coordinator    - Team Coordinator

👥 Configured Teams:
  @content        - Content Creation Team
                   Members: @coordinator, @researcher, @writer

📍 Paths:
  Workspace: /home/user/agency-workspace
  Queue:     /home/user/.agency/queue
====================================================
```

**Use when:**
- Checking system health
- Debugging stuck messages
- Viewing configuration

---

## 🗄️ Database Management

### Reset Conversation State

```bash
python -m agency reset
```

Clears:
- ✅ Active conversations
- ❌ Keeps queue messages
- ❌ Keeps agent workspaces
- ❌ Keeps chat history

**Use when:**
- Clearing stuck conversations
- Starting fresh conversations
- Testing from clean state

**Equivalent to:** `pnpm db:reset` in tinyclaw

---

### Clear All Persistent Data

```bash
# With confirmation prompt
python -m agency clear

# Skip confirmation
python -m agency clear --force
```

Clears:
- ✅ Queue (incoming, processing, outgoing)
- ✅ Conversations
- ✅ Agent workspaces
- ✅ Chat history

**Use when:**
- Complete reset needed
- Clearing test data
- Starting completely fresh

**Equivalent to:** `pnpm db:clear` in tinyclaw

⚠️ **WARNING:** This is destructive! Use with caution.

---

## 🔧 Initialization

### Initialize Workspace

```bash
# Default workspace
python -m agency init

# Custom workspace
python -m agency init --workspace ~/my-agency-workspace
```

Creates:
- ✅ Workspace directory structure
- ✅ Queue directories
- ✅ Example `agents.json` config
- ✅ `.env.example` template

**Use when:**
- Setting up agency for first time
- Creating example configuration
- Generating environment template

---

## ⚙️ Advanced Options

### Custom Config File

```bash
python -m agency start --config ./my-agents.json
python -m agency process --config ./config.json
python -m agency status --config ./agents.json
```

Use custom agent/team configuration file instead of default.

**Default:** `agency/templates/agents.json`

---

### Custom Workspace

```bash
python -m agency start --workspace ~/my-workspace
python -m agency process --workspace /path/to/workspace
python -m agency reset --workspace ~/workspace
```

Use custom workspace directory instead of default.

**Default:** `~/agency-workspace`

---

### Combine Options

```bash
python -m agency start \
  --config ./agents.json \
  --workspace ~/my-workspace
```

---

## 📖 Getting Help

```bash
# General help
python -m agency --help

# Command-specific help
python -m agency start --help
python -m agency send --help
python -m agency clear --help
```

---

## 💡 Common Workflows

### Development Workflow

```bash
# 1. Initialize workspace
python -m agency init

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Test an agent
python -m agency send "What's new in AI?" researcher

# 4. Start processor (in one terminal)
python -m agency process

# 5. Start Telegram (in another terminal)
python -m agency telegram

# Or start both together
python -m agency start
```

---

### Testing Workflow

```bash
# 1. Send test message
python -m agency send "test message" researcher

# 2. Check status
python -m agency status

# 3. Reset if needed
python -m agency reset

# 4. Clear everything for fresh start
python -m agency clear --force
```

---

### Debugging Workflow

```bash
# 1. Check system status
python -m agency status

# 2. If queue is stuck, check for orphaned messages
ls ~/.agency/queue/processing/

# 3. Reset conversations
python -m agency reset

# 4. Test specific agent
python -m agency send "test" agent_id

# 5. Check logs
# (processor outputs to stdout)
```

---

## 🔍 Observability

### Check Queue Files

```bash
# See incoming messages
ls -la ~/.agency/queue/incoming/

# See processing messages
ls -la ~/.agency/queue/processing/

# See outgoing messages
ls -la ~/.agency/queue/outgoing/

# Read a message
cat ~/.agency/queue/incoming/1234567890_abc123.json
```

### Check Conversations

```bash
# See active conversations
ls -la ~/.agency/queue/conversations/

# Read conversation state
cat ~/.agency/queue/conversations/<conversation-id>.json
```

### Check Agent Workspaces

```bash
# List agent workspaces
ls -la ~/agency-workspace/

# Check agent's identity
cat ~/agency-workspace/researcher/IDENTITY.md

# Check conversation history
cat ~/agency-workspace/researcher/conversation.json
```

---

## 🆚 tinyclaw Command Mapping

| tinyclaw | agency | Notes |
|----------|--------|-------|
| `pnpm dev` | `python -m agency start` | Full system |
| `pnpm dev:processor` | `python -m agency process` | Processor only |
| `pnpm dev:telegram` | `python -m agency telegram` | Telegram only |
| `pnpm send <msg> [agent]` | `python -m agency send <msg> [agent]` | Test message |
| `pnpm db:reset` | `python -m agency reset` | Reset conversations |
| `pnpm db:clear` | `python -m agency clear` | Clear all data |
| _(none)_ | `python -m agency status` | System status |
| _(none)_ | `python -m agency init` | Initialize workspace |

---

## 📚 See Also

- **AGENCY_README.md** - Complete system overview
- **EXAMPLES.md** - Real-world use cases
- **QUICK_INTEGRATION_GUIDE.md** - External service setup

---

**Built with inspiration from [tinyclaw](https://github.com/jlia0/tinyclaw) 🙏**
