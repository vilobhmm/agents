# OpenClaw - AI Agent Framework

OpenClaw is a powerful, chat-first AI agent framework for building proactive automation systems. It enables you to create intelligent agents that monitor, analyze, and act on your behalf across multiple platforms and services.

## Features

- **Chat-First Interface**: Interact with your agents naturally through messaging platforms
- **Multi-Agent Orchestration**: Coordinate multiple specialized agents working together
- **Proactive Automation**: Agents that reach out to you, not just respond to queries
- **Rich Integrations**: Email, Calendar, Slack, WhatsApp, Telegram, Notion, GitHub, and more
- **Extensible Architecture**: Easy to add new tools and capabilities

## 10 Weekend Projects Included

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

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your integrations
cp .env.example .env
# Edit .env with your API keys

# Run a project
python -m projects.01_research_assistant.main
```

## Architecture

OpenClaw is built on three core concepts:

1. **Agents** - Autonomous entities that perform specific tasks
2. **Tools** - Capabilities agents can use (web scraping, summarization, OCR, etc.)
3. **Integrations** - Connections to external services (email, calendar, chat, etc.)

## Configuration

Each project has its own configuration file. See individual project READMEs for details.

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Format code
black openclaw/ projects/
```

## License

MIT

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.
