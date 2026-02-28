# 📖 Agency CLI Commands

Complete command reference for the `agency` CLI tool.

Inspired by [tinyclaw](https://github.com/jlia0/tinyclaw) 💜

---

## 📋 Table of Contents

- [Core Commands](#-core-commands) - System control
- [Agent Commands](#-agent-commands) - Manage agents
- [Team Commands](#-team-commands) - Manage teams
- [Configuration Commands](#️-configuration-commands) - Settings
- [Pairing Commands](#-pairing-commands) - Connect channels
- [Update Commands](#-update-commands) - Update Agency
- [Messaging Commands](#-messaging-commands) - Send messages
- [In-Chat Commands](#-in-chat-commands) - Chat interface

---

## 🚀 Core Commands

### `agency start`
Start the Agency system (processor + channels).

```bash
# Start full system (processor + Telegram)
agency start

# Start processor only
agency start --processor-only

# Start Telegram only
agency start --telegram-only

# Start in background (detached)
agency start --detach
```

**Options:**
- `--processor-only` - Only start message processor
- `--telegram-only` - Only start Telegram channel
- `--detach` - Run in background

**Example:**
```bash
$ agency start
🚀 Starting Agency...
Starting processor in background...
✅ Processor started (PID: 12345)
Starting Telegram in foreground...
✅ Telegram channel started
Press Ctrl+C to stop
```

---

### `agency stop`
Stop the Agency system.

```bash
agency stop
```

**Example:**
```bash
$ agency stop
⏹️  Stopping Agency...
✅ Stopped processor (PID: 12345)
✅ Stopped telegram (PID: 12346)
✅ Agency stopped
```

---

### `agency status`
Show system status.

```bash
# Human-readable status
agency status

# JSON output
agency status --json
```

**Options:**
- `--json` - Output as JSON

**Example:**
```bash
$ agency status
📊 Agency Status
==================================================
Status: ✅ Running
  processor: PID 12345
  telegram: PID 12346

Config dir: /home/user/.agency
Workspace:  /home/user/agency-workspace
Agents:     11
Teams:      5
```

---

### `agency logs`
View system logs.

```bash
# Show last 50 lines
agency logs

# Show last 100 lines
agency logs --lines 100
agency logs -n 100

# Follow logs (like tail -f)
agency logs --follow
agency logs -f
```

**Options:**
- `--lines, -n` - Number of lines to show (default: 50)
- `--follow, -f` - Follow log output

**Example:**
```bash
$ agency logs -f
[2025-01-15 10:30:15] INFO: Message received from user_123
[2025-01-15 10:30:16] INFO: Routing to agent: cc
[2025-01-15 10:30:18] INFO: Response generated
```

---

### `agency version`
Show version information.

```bash
agency version
```

**Example:**
```bash
$ agency version
Agency v0.1.0
Multi-agent AI system

Inspired by:
  - tinyclaw (https://github.com/jlia0/tinyclaw)
  - Google Labs CC (https://labs.google/cc)
```

---

### `agency init`
Initialize Agency workspace.

```bash
# Initialize with default settings
agency init

# Force overwrite existing config
agency init --force
```

**Options:**
- `--force` - Overwrite existing configuration

**Example:**
```bash
$ agency init
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

---

## 🤖 Agent Commands

### `agency agent list`
List all agents.

```bash
# Human-readable list
agency agent list

# JSON output
agency agent list --json
```

**Options:**
- `--json` - Output as JSON

**Example:**
```bash
$ agency agent list
🤖 Available Agents
======================================================================
✅ @cc              CC - Chief Coordinator          [opus]
✅ @assistant       Personal Assistant              [sonnet]
✅ @action_taker    Action Execution Specialist     [sonnet]
✅ @job_hunter      Job Search Specialist           [sonnet]
✅ @researcher      Research Assistant              [sonnet]
✅ @writer          Content Writer                  [sonnet]
✅ @social          Social Media Manager            [sonnet]
✅ @coordinator     Team Coordinator                [sonnet]
✅ @resume_optimizer Resume & Application Specialist [opus]
✅ @networker       Professional Networking Specialist [sonnet]
✅ @curator         Content Curator                 [sonnet]

Total: 11 agents
```

---

### `agency agent info <agent_id>`
Show agent details.

```bash
# Human-readable info
agency agent info cc

# JSON output
agency agent info cc --json
```

**Options:**
- `--json` - Output as JSON

**Example:**
```bash
$ agency agent info cc
🤖 Agent: @cc
======================================================================
Name:     CC - Chief Coordinator
Model:    opus
Provider: anthropic
Enabled:  True

Personality:
  You are CC (Chief Coordinator), an AI productivity agent inspired
  by Google Labs CC. You deliver personalized daily briefings...

Skills:
  • Access and analyze Gmail for important emails and context
  • Review Calendar for upcoming meetings and schedule
  • Search Drive for relevant documents and files
  • Deliver personalized morning briefings
  • Identify priorities and urgent items
  ...
```

---

### `agency agent create <agent_id>`
Create a new agent.

```bash
agency agent create my_agent \
  --name "My Custom Agent" \
  --model sonnet \
  --personality "You are a helpful assistant..."
```

**Arguments:**
- `agent_id` - Unique agent identifier

**Options:**
- `--name` - Agent display name (required)
- `--model` - Model to use: opus, sonnet, haiku (default: sonnet)
- `--personality` - Agent personality/system prompt

**Example:**
```bash
$ agency agent create task_master \
  --name "Task Master" \
  --model sonnet \
  --personality "You are a task management specialist"
✅ Created agent: @task_master
```

---

### `agency agent delete <agent_id>`
Delete an agent.

```bash
# With confirmation
agency agent delete my_agent

# Skip confirmation
agency agent delete my_agent --force
```

**Options:**
- `--force` - Skip confirmation

**Example:**
```bash
$ agency agent delete my_agent
Delete agent @my_agent? [y/N] y
✅ Deleted agent: @my_agent
```

---

### `agency agent enable <agent_id>`
Enable an agent.

```bash
agency agent enable my_agent
```

---

### `agency agent disable <agent_id>`
Disable an agent.

```bash
agency agent disable my_agent
```

---

## 👥 Team Commands

### `agency team list`
List all teams.

```bash
# Human-readable list
agency team list

# JSON output
agency team list --json
```

**Example:**
```bash
$ agency team list
👥 Available Teams
======================================================================
@cc_team        CC Productivity Team            (4 agents, led by @cc)
@job_search     Job Search Team                 (4 agents, led by @coordinator)
@content        Content Creation Team           (3 agents, led by @coordinator)
@intelligence   Intelligence Team               (3 agents, led by @coordinator)
@social_team    Social Media Team               (3 agents, led by @coordinator)

Total: 5 teams
```

---

### `agency team info <team_id>`
Show team details.

```bash
# Human-readable info
agency team info cc_team

# JSON output
agency team info cc_team --json
```

**Example:**
```bash
$ agency team info cc_team
👥 Team: @cc_team
======================================================================
Name:        CC Productivity Team
Leader:      @cc
Description: Personal productivity team led by CC. Delivers daily
             briefings, takes actions, and keeps you ahead of your day.

Team Members:
  👑 @cc
     @assistant
     @action_taker
     @researcher
```

---

### `agency team create <team_id>`
Create a new team.

```bash
agency team create my_team \
  --name "My Team" \
  --leader coordinator \
  --agents coordinator researcher writer
```

**Arguments:**
- `team_id` - Unique team identifier

**Options:**
- `--name` - Team display name (required)
- `--leader` - Leader agent ID (required)
- `--agents` - Agent IDs (space-separated)

**Example:**
```bash
$ agency team create analytics_team \
  --name "Analytics Team" \
  --leader coordinator \
  --agents coordinator researcher
✅ Created team: @analytics_team
```

---

### `agency team delete <team_id>`
Delete a team.

```bash
agency team delete my_team
```

---

### `agency team add-agent <team_id> <agent_id>`
Add agent to team.

```bash
agency team add-agent cc_team writer
```

**Example:**
```bash
$ agency team add-agent cc_team writer
✅ Added @writer to team @cc_team
```

---

### `agency team remove-agent <team_id> <agent_id>`
Remove agent from team.

```bash
agency team remove-agent cc_team writer
```

---

## ⚙️ Configuration Commands

### `agency config get <key>`
Get configuration value.

```bash
# Get nested value with dot notation
agency config get telegram.bot_token
agency config get anthropic.api_key
```

**Example:**
```bash
$ agency config get telegram.bot_token
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz...
```

---

### `agency config set <key> <value>`
Set configuration value.

```bash
agency config set telegram.bot_token "YOUR_TOKEN"
agency config set anthropic.api_key "sk-ant-..."
```

**Example:**
```bash
$ agency config set telegram.bot_token "1234567890:ABC..."
✅ Set telegram.bot_token = 1234567890:ABC...
```

---

### `agency config show`
Show all configuration.

```bash
# Human-readable (sensitive values masked)
agency config show

# JSON output
agency config show --json
```

**Example:**
```bash
$ agency config show
⚙️  Agency Configuration
==================================================
telegram:
  enabled: True
  bot_token: 1234567890...xyz
  allowed_users: [123456789]
anthropic:
  api_key: sk-ant-...abc
workspace_dir: /home/user/agency-workspace
log_level: INFO
```

---

### `agency config reset`
Reset configuration to defaults.

```bash
# With confirmation
agency config reset

# Skip confirmation
agency config reset --force
```

---

## 🔗 Pairing Commands

Pair external channels (Telegram, WhatsApp, etc.) with Agency.

### `agency pair <channel>`
Pair a channel.

```bash
# Pair Telegram (interactive)
agency pair telegram

# Pair with token directly
agency pair telegram --token "YOUR_BOT_TOKEN"
```

**Supported channels:**
- `telegram`
- `whatsapp` (coming soon)
- `slack` (coming soon)

**Example:**
```bash
$ agency pair telegram
🔗 Pairing telegram...
Enter Telegram bot token: 1234567890:ABCdef...
Testing token...
✅ Connected to @my_agency_bot
✅ Telegram paired!

Next steps:
  1. Start Agency: agency start
  2. Message your bot on Telegram
  3. Your user ID will be logged
  4. Add it to config: agency config set telegram.allowed_users '[123456789]'
```

---

### `agency unpair <channel>`
Unpair a channel.

```bash
agency unpair telegram
```

---

### `agency list-pairings`
List all paired channels.

```bash
# Human-readable list
agency list-pairings

# JSON output
agency list-pairings --json
```

**Example:**
```bash
$ agency list-pairings
🔗 Paired Channels
==================================================
✅ telegram
```

---

## 🔄 Update Commands

### `agency update`
Update Agency to latest version.

```bash
# Update to latest
agency update

# Check for updates only
agency update --check-only

# Update to specific version
agency update --version 0.2.0
```

**Options:**
- `--check-only` - Only check for updates
- `--version` - Update to specific version

---

### `agency check-updates`
Check for available updates.

```bash
agency check-updates
```

---

## 💬 Messaging Commands

### `agency send <message> <agent_id>`
Send message to an agent.

```bash
agency send "Hello!" cc
agency send "Find ML Engineer jobs" job_hunter
agency send "Create newsletter" writer
```

**Arguments:**
- `message` - Message text
- `agent_id` - Target agent ID

**Options:**
- `--user` - User ID (default: cli)

**Example:**
```bash
$ agency send "Good morning briefing" cc
✅ Message sent to @cc
Message ID: msg_1234567890

Response will be processed by the message processor.
Start it with: agency start --processor-only
```

---

### `agency broadcast <message>`
Broadcast message to multiple agents.

```bash
# Broadcast to specific agents
agency broadcast "Status update" --agents cc assistant researcher

# Broadcast to entire team
agency broadcast "Team meeting in 10 min" --team cc_team
```

**Options:**
- `--agents` - Agent IDs (space-separated)
- `--team` - Team ID

**Example:**
```bash
$ agency broadcast "Important update" --team cc_team
✅ Broadcast sent to 4 agents
```

---

### `agency history <agent_id>`
View conversation history.

```bash
# Show last 10 messages
agency history cc

# Show last 50 messages
agency history cc --limit 50

# JSON output
agency history cc --json
```

**Options:**
- `--user` - User ID (default: cli)
- `--limit` - Number of messages (default: 10)
- `--json` - Output as JSON

**Example:**
```bash
$ agency history cc --limit 5
💬 Conversation: cli ↔️ @cc
======================================================================
👤 [2025-01-15 10:30:15] user
   Good morning briefing

🤖 [2025-01-15 10:30:18] assistant
   Good morning! Here's your daily briefing:
   📧 Emails: 12 unread (3 urgent)
   📅 Calendar: 4 events today
   ...
```

---

## 💭 In-Chat Commands

Commands used within Telegram (or other chat interfaces).

### `@<agent_id> <message>`
Message a specific agent.

```
@cc Good morning briefing
@job_hunter Find ML Engineer roles at Anthropic
@writer Create blog post about AI agents
@researcher What's new in AI today?
```

**Example conversation:**
```
You: @cc Good morning briefing

CC: Good morning! Here's your daily briefing:

📧 Emails:
  • 12 unread
  • 🔴 3 urgent
  ...
```

---

### `@<team_id> <message>`
Message an entire team.

```
@cc_team Help me prepare for my day
@job_search Find and apply for roles
@content Create weekly newsletter
```

**Example:**
```
You: @cc_team Help me prepare for today

CC (Team Leader): I'll coordinate the team.
  [@assistant: Checking calendar...]
  [@researcher: Getting AI news...]
  [@action_taker: Drafting summary...]

[All agents work in parallel]

CC: Here's your day preparation:
  • 4 meetings today, first at 10 AM
  • 3 urgent tasks
  • Latest AI news: [summary]
  • Draft email ready
```

---

### Quick Replies

```
/help - Show help
/status - System status
/agents - List agents
/teams - List teams
```

---

## 📝 Examples

### Example 1: Complete Setup

```bash
# 1. Initialize
agency init

# 2. Pair Telegram
agency pair telegram --token "YOUR_TOKEN"

# 3. Configure allowed users
agency config set telegram.allowed_users '[123456789]'

# 4. Start
agency start

# 5. Test via CLI
agency send "Good morning briefing" cc
```

---

### Example 2: Create Custom Agent

```bash
# Create custom agent
agency agent create email_expert \
  --name "Email Expert" \
  --model opus \
  --personality "You are an email writing expert"

# Test it
agency send "Draft email to Sarah" email_expert
```

---

### Example 3: Create Custom Team

```bash
# Create team
agency team create email_team \
  --name "Email Team" \
  --leader coordinator \
  --agents coordinator email_expert writer

# Test it
agency send "Create professional email campaign" email_team
```

---

### Example 4: View Logs

```bash
# Start in one terminal
agency start

# In another terminal, follow logs
agency logs -f
```

---

### Example 5: Background Operation

```bash
# Start in background
agency start --detach

# Check status
agency status

# View logs
agency logs -f

# Stop
agency stop
```

---

## 🎓 Tips

### Tip 1: Add to PATH

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/home/user/agents:$PATH"
alias agency="/home/user/agents/agency_bin"

# Then use from anywhere
agency start
```

---

### Tip 2: Auto-start on Boot

```bash
# Add to crontab
@reboot /home/user/agents/agency_bin start --detach
```

---

### Tip 3: Morning Briefing Automation

```bash
# Add to crontab (every day at 8 AM)
0 8 * * * /home/user/agents/agency_bin send "Good morning briefing" cc
```

---

### Tip 4: Quick Status Check

```bash
# Create alias
alias as='agency status'

# Use it
as
```

---

## 📚 See Also

- [Agency README](../README.md) - Main documentation
- [Using Agents Guide](USING_AGENTS.md) - How to use agents
- [CC Agent Guide](CC_GUIDE.md) - CC-specific guide
- [Job Search Guide](JOB_SEARCH_GUIDE.md) - Job search automation

---

**Build amazing agentic systems!** 🚀
