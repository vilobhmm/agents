# OpenClaw - Agentic AI Use Cases

**Personal. Proactive. Powerful.**

OpenClaw is a production-ready AI agent framework that transforms how you work. Build intelligent agents that monitor, analyze, and act on your behalf - like having a team of virtual employees working 24/7.

## Core Philosophy

**Personal** - Tailored to your unique workflow and preferences
**Proactive** - Agents that reach out to you, not just respond to queries
**Powerful** - Multi-agent orchestration with rich integrations

## Features

- 🎯 **Chat-First Control**: Manage your entire AI workforce via Telegram
- 🤝 **Multi-Agent Orchestration**: Coordinate specialized agents working together
- 🔄 **Proactive Automation**: Agents monitor and act automatically on schedules
- 🔌 **Rich Integrations**: Email, Calendar, Slack, WhatsApp, Telegram, Notion, GitHub
- 🛠️ **Extensible Architecture**: Easy to customize and add new capabilities

## Agentic AI Use Cases

1. **Personal Research Assistant** - Monitors reading lists, summarizes articles, sends briefings
2. **Proactive Meeting Prep Agent** - Scans calendar, pulls context, generates prep docs
3. **Code Review Companion** - Monitors PRs, analyzes code, drafts review comments
4. **Smart Expense Tracker** - Processes receipts, categorizes spending, sends reports
5. **Learning Path Orchestrator** - Curates content, schedules learning, generates quizzes
6. **Travel Autopilot System** - Handles check-ins, bookings, itinerary updates
7. **Research Paper Digest Pipeline** - Monitors feeds, analyzes papers, builds knowledge
8. **Proactive Context Switcher** - Detects work context changes, surfaces relevant info
9. **Email Triaging & Auto-Response** - Categorizes emails, drafts responses, follows up
10. **Personal Knowledge Graph Builder** - Extracts insights, builds queryable knowledge
11. **🛡⚡ Avengers System** - Multi-agent orchestration via WhatsApp (6 specialized agents working as a team)

## Quick Start Options

### Option 1: Avengers System (Multi-Agent via WhatsApp)

The most powerful setup - manage 6 specialized agents through WhatsApp:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up WhatsApp (Twilio)
# Get Twilio account and WhatsApp sandbox

# 3. Configure .env
cp .env.example .env
# Add TWILIO credentials and ANTHROPIC_API_KEY

# 4. Start the Avengers system
python -m projects.11_avengers_system.main

# 5. In separate terminal, start WhatsApp manager
python -m projects.11_avengers_system.whatsapp_manager

# 6. Message your Twilio WhatsApp number!
```

See [Avengers System README](projects/11_avengers_system/README.md) for details.

### Option 2: Telegram Control (Individual Agents)

Control individual agents via Telegram:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up Telegram bot (see TELEGRAM_GUIDE.md)
# Get bot token from @BotFather

# 3. Configure .env
cp .env.example .env
# Add TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY

# 4. Start the manager
python telegram_manager.py

# 5. Send /start to your bot in Telegram!
```

**First Time?** Read the comprehensive [Telegram Integration Guide](TELEGRAM_GUIDE.md)

**Super Quick?** See [Quick Start Guide](QUICKSTART.md) for 10-minute setup

### Alternative: Run Agents Directly

```bash
# Run individual agents
python -m projects.01_research_assistant.main
python -m projects.02_meeting_prep.main
```

## Architecture

OpenClaw is built on three core concepts:

1. **Agents** - Autonomous entities that perform specific tasks
2. **Tools** - Capabilities agents can use (web scraping, summarization, OCR, etc.)
3. **Integrations** - Connections to external services (email, calendar, chat, etc.)

## Configuration

Each project has its own configuration file. See individual project READMEs for details.

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 10 minutes
- **[Telegram Integration Guide](TELEGRAM_GUIDE.md)** - Complete Telegram setup and usage
- **[Use Cases](PROJECTS.md)** - Detailed guide for all 10 agents
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Examples](examples/)** - Code examples

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
make format

# Run linters
make lint
```

## The Vision

OpenClaw demonstrates the future of personal AI assistance:

**Not**: Ask AI a question → Get an answer
**But**: AI monitors your world → Acts proactively → Keeps you informed

**Not**: One-off AI interactions
**But**: Persistent agents that learn your patterns

**Not**: General-purpose chatbot
**But**: Specialized agents orchestrated for your workflow

## License

MIT - See LICENSE file

## Contributing

We'd love your contributions! Whether it's:
- New agent implementations
- Integration modules
- Bug fixes
- Documentation improvements
- Real-world usage examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Community

Share your agent setups, ask questions, and learn from others.

## Acknowledgments

Built with:
- Anthropic Claude for intelligent reasoning
- Python for the framework
- Telegram for the chat interface

---

**OpenClaw - Agentic AI Use Cases**
*Personal. Proactive. Powerful.*
