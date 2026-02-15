# OpenClaw Weekend Projects

This repository contains 10 complete weekend projects built with OpenClaw, demonstrating various AI agent capabilities.

## Quick Start Guide

### 1. Personal Research Assistant
**Location:** `projects/01_research_assistant/`
**Complexity:** ⭐ Easy (Single agent)
**Time to Build:** 1 weekend

Monitors your reading lists (Pocket, Instapaper) and automatically summarizes articles, sends morning briefings via WhatsApp, creates calendar blocks, and generates Notion pages.

**Run:**
```bash
python -m projects.01_research_assistant.main
```

### 2. Proactive Meeting Prep Agent
**Location:** `projects/02_meeting_prep/`
**Complexity:** ⭐⭐ Medium (Multi-agent)
**Time to Build:** 1 weekend

Scans your calendar 24 hours ahead, pulls relevant emails and Slack threads, generates briefing docs, and suggests agenda items.

**Run:**
```bash
python -m projects.02_meeting_prep.main
```

### 3. Code Review Companion
**Location:** `projects/03_code_review/`
**Complexity:** ⭐⭐ Medium (Coding agent)
**Time to Build:** 1 weekend

Monitors GitHub PRs, analyzes code changes, searches internal docs for patterns, and drafts constructive review comments.

**Key Features:**
- Automated PR analysis
- Pattern detection
- Daily digest of team activity

### 4. Smart Expense Tracker
**Location:** `projects/04_expense_tracker/`
**Complexity:** ⭐ Easy (Single agent)
**Time to Build:** 1 weekend

Processes receipts and invoices from email, extracts expense details using vision, categorizes spending, and sends weekly reports.

**Key Features:**
- OCR for receipt processing
- Automatic categorization
- Weekly spending reports
- Unusual transaction flagging

### 5. Learning Path Orchestrator
**Location:** `projects/05_learning_path/`
**Complexity:** ⭐⭐⭐ Advanced (Multi-agent system)
**Time to Build:** 2 weekends

A sophisticated multi-agent system with specialized agents:
- **Curator Agent:** Finds courses, papers, tutorials
- **Scheduler Agent:** Blocks learning time based on availability
- **Quiz Agent:** Generates practice questions
- **Progress Agent:** Sends reports and adjusts learning path

**Run:**
```python
from projects.05_learning_path.agent import LearningPathOrchestrator

orchestrator = LearningPathOrchestrator()
await orchestrator.start_learning_path("Machine Learning", hours_per_week=5)
```

### 6. Travel Autopilot System
**Location:** `projects/06_travel_autopilot/`
**Complexity:** ⭐⭐ Medium (Event-driven)
**Time to Build:** 1-2 weekends

End-to-end travel automation:
- Monitors flight confirmation emails
- Auto check-in 24 hours before departure
- Adds boarding passes to calendar
- Handles flight delays and reschedules meetings

**Key Features:**
- Proactive monitoring
- Automatic calendar management
- Delay detection and response

### 7. Research Paper Digest Pipeline
**Location:** `projects/07_research_digest/`
**Complexity:** ⭐⭐ Medium (Research agent)
**Time to Build:** 1 weekend

Monitors arXiv/research feeds, analyzes papers for relevance, generates structured summaries, maintains knowledge graph, and sends curated weekly digests.

**Key Features:**
- Semantic search and filtering
- Structured analysis (problem, method, results, implications)
- Knowledge graph integration

### 8. Proactive Context Switcher
**Location:** `projects/08_context_switcher/`
**Complexity:** ⭐⭐⭐ Advanced (Multi-agent)
**Time to Build:** 2 weekends

Multi-agent system that detects context changes:
- **Pattern Detector:** Recognizes project switches
- **Knowledge Retriever:** Surfaces relevant docs and tasks
- **Context Assembler:** Prepares "context packs" in Notion

**Key Features:**
- Automatic context detection
- Proactive information surfacing
- Slack status updates

### 9. Email Triaging & Auto-Response
**Location:** `projects/09_email_triage/`
**Complexity:** ⭐⭐ Medium (NLP classification)
**Time to Build:** 1 weekend

Intelligent email management:
- Analyzes emails for urgency/importance
- Categorizes into action needed, FYI, archive
- Drafts responses for routine requests
- Sends gentle follow-up reminders

**Key Features:**
- Smart categorization
- Auto-draft responses
- Follow-up tracking

### 10. Personal Knowledge Graph Builder
**Location:** `projects/10_knowledge_graph/`
**Complexity:** ⭐⭐⭐ Advanced (Multi-agent, graph DB)
**Time to Build:** 2-3 weekends

A comprehensive knowledge management system:
- **Extraction Agent:** Extracts entities and relationships
- **Graph Builder:** Maintains knowledge graph
- **Query Engine:** Answers questions
- **Insight Generator:** Surfaces connections

**Key Features:**
- Processes emails, messages, notes, articles
- Builds queryable knowledge graph
- Answers questions like "What did I learn about X last month?"
- Weekly knowledge reviews

**Run:**
```python
from projects.10_knowledge_graph.agent import KnowledgeGraphOrchestrator

kg = KnowledgeGraphOrchestrator()
await kg.process_all_sources()
answer = await kg.answer_question("What did I learn about transformers?")
```

## Implementation Tips

### For Beginners
Start with these projects:
- Project 1 (Research Assistant) - Simple single agent
- Project 4 (Expense Tracker) - Good for learning OCR and data extraction
- Project 9 (Email Triage) - Practical everyday use

### For Advanced Users
These projects offer deep value:
- Project 5 (Learning Path) - Multi-agent coordination
- Project 7 (Research Digest) - Knowledge management
- Project 10 (Knowledge Graph) - Graph databases and semantic search

### High Impact Projects
These solve daily friction points:
- Project 2 (Meeting Prep) - Saves hours of meeting prep
- Project 6 (Travel Autopilot) - Automates travel hassles
- Project 8 (Context Switcher) - Reduces context switching overhead

## Key Concepts Demonstrated

### Single Agent Pattern (Projects 1, 4)
Simple agent with clear inputs/outputs, good for straightforward automation.

### Multi-Agent Orchestration (Projects 2, 5, 8, 10)
Multiple specialized agents working together, coordinated by an orchestrator.

### Proactive Scheduling (All Projects)
Agents that run on schedules and reach out to you, not just respond to queries.

### Chat-First Interface (All Projects)
All agents communicate via messaging platforms (WhatsApp, Telegram, Slack).

### Tool Integration (All Projects)
Demonstrates integration with:
- Email (Gmail API)
- Calendar (Google Calendar)
- Chat (Slack, WhatsApp, Telegram)
- Knowledge Base (Notion)
- Code (GitHub)
- Web (RSS feeds, web scraping)

## Configuration

All projects use environment variables from `.env`:

```bash
# Copy example config
cp .env.example .env

# Edit with your API keys
nano .env
```

## Running Multiple Projects

You can run multiple projects simultaneously:

```bash
# Terminal 1
python -m projects.01_research_assistant.main

# Terminal 2
python -m projects.02_meeting_prep.main

# Terminal 3
python -m projects.09_email_triage.main
```

## Customization

Each project can be customized:
- Edit `config.py` in each project directory
- Modify schedules (cron expressions)
- Adjust notification preferences
- Change data sources

## Troubleshooting

### Common Issues

1. **API Keys Not Working**
   - Verify `.env` file is in root directory
   - Check API key format
   - Ensure no extra spaces

2. **Scheduler Not Running**
   - Check timezone settings
   - Verify cron expressions
   - Look at logs for errors

3. **Integration Failures**
   - Verify OAuth credentials
   - Check API rate limits
   - Ensure network connectivity

## Next Steps

After building these projects:
1. Combine agents for more complex workflows
2. Add custom tools and integrations
3. Build your own agents for specific needs
4. Share your creations with the community

## Community

Share your implementations, improvements, and new projects!

## License

MIT - See LICENSE file for details
