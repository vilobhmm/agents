# 🤖 Agency - For Agentic AI

**Proactive. Personal. Powerful.**

A multi-agent, multi-channel, multi-team system for autonomous AI that works 24/7.

---

## 🚀 **[👉 START HERE: Complete Setup Guide](GETTING_STARTED.md)** 👈

**The definitive step-by-step guide to get ALL agents working with Telegram!**

Includes:
- ✅ 15-minute setup
- ✅ Telegram configuration
- ✅ Google services setup (for CC)
- ✅ Complete examples for ALL agents
- ✅ 5 multi-agent team workflows
- ✅ Troubleshooting
- ✅ Advanced features

**[📖 Read GETTING_STARTED.md](GETTING_STARTED.md)**

---

## ⚡ Quick Start (Already Setup?)

```bash
# 1. Setup
python -m agency init

# 2. Configure (.env)
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=...

# 3. Start
python -m agency start

# 4. Talk to agents via Telegram
@cc Good morning briefing
@job_search Find ML Engineer roles
@feedback Submit feedback report
```

---

## 📁 Project Structure

```
agents/
├── agency/                    # Core agency system
│   ├── agents/               # AI agents with specialized skills
│   │   ├── README.md        # Agent overview
│   │   ├── cc/              # Chief Coordinator agent
│   │   │   ├── README.md   # CC complete guide
│   │   │   └── cc_skills.py
│   │   ├── job_search/      # Job search agent
│   │   │   ├── README.md   # Job search guide
│   │   │   └── job_search_skills.py
│   │   ├── feedback/        # Feedback management
│   │   │   ├── README.md   # Feedback guide
│   │   │   └── feedback_skills.py
│   │   └── base/            # Base framework
│   │       └── skills.py
│   ├── tools/               # Agent tools & utilities
│   ├── channels/            # Telegram, CLI, Web
│   ├── core/                # Core system logic
│   └── templates/           # Agent templates
├── examples/                 # Working examples & demos
│   ├── README.md            # Examples overview
│   ├── feedback/            # Feedback examples
│   │   ├── README.md       # Feedback examples guide
│   │   ├── e2e_feedback_github_demo.py
│   │   └── feedback_management_demo.py
│   └── basic/               # Basic agent examples
│       ├── simple_agent.py
│       ├── proactive_agent.py
│       └── multi_agent.py
├── projects/                 # 11 pre-built agent projects
└── docs/                    # Documentation (all guides)
```

---

## 🤖 Your AI Agents

### **@cc - Chief Coordinator** (Like Google Labs CC) 🎯
Daily briefings from Gmail, Calendar, Drive + takes actions

**📖 [Complete CC Agent Guide →](agency/agents/cc/README.md)**

**Quick features:**
- ☀️ Morning briefings with priorities
- 📧 Email management and drafting
- 📅 Meeting scheduling and prep
- ✅ Actions: send emails, block time
- 🤝 Coordinates other agents

---

### **@job_search** - Job hunting automation 💼
Finds jobs, tailors resume, gets referrals

**📖 [Complete Job Search Guide →](agency/agents/job_search/README.md)**

**Quick features:**
- 🔍 Find relevant job openings
- 📝 Tailor resumes automatically
- 📨 Automate applications
- 📊 Track application status
- 🤝 Network outreach

---

### **@feedback** - Feedback Management 📋
Collect feedback → Cluster by theme → Track bugs → Generate solutions

**📖 [Complete Feedback Guide →](agency/agents/feedback/README.md)**

**Quick features:**
- 📝 Collect user feedback
- 🎯 Cluster by theme with Claude AI
- 🐛 Track bugs and issues
- 💡 Generate solutions & PRDs
- 📊 Analytics dashboard

**🚀 [Try the E2E Demo →](examples/feedback/e2e_feedback_github_demo.py)**

---

## 📚 Documentation Structure

### Core Guides
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup (START HERE!)
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start
- **[AGENCY_README.md](AGENCY_README.md)** - Full agency guide

### Agent Guides
- **[CC Agent Guide](agency/agents/cc/README.md)** - Gmail, Calendar, Drive
- **[Job Search Guide](agency/agents/job_search/README.md)** - Job hunting
- **[Feedback Guide](agency/agents/feedback/README.md)** - Feedback management
- **[All Agents Overview](agency/agents/README.md)** - Agent framework

### Examples & Demos
- **[Examples Overview](examples/README.md)** - All examples
- **[Feedback Examples](examples/feedback/README.md)** - E2E demos
- **[Basic Examples](examples/basic/)** - Simple agent examples

### Integration & Setup
- **[Telegram Guide](TELEGRAM_GUIDE.md)** - Telegram bot setup
- **[Quick Integration Guide](QUICK_INTEGRATION_GUIDE.md)** - Service setup
- **[External Services Setup](EXTERNAL_SERVICES_SETUP.md)** - Google, etc.

### Reference
- **[CLI Commands](agency/CLI_COMMANDS.md)** - Command reference
- **[Agent Templates](agency/templates/)** - Customize agents
- **[Tools Reference](agency/tools/)** - Available tools

---

## 💻 CLI Commands

```bash
# Start the system
python -m agency start

# Check status
python -m agency status

# Send message to agent
python -m agency send "message" agent_id

# View logs
python -m agency logs -f

# Stop the system
python -m agency stop
```

See **[agency/CLI_COMMANDS.md](agency/CLI_COMMANDS.md)** for full reference.

---

## 🎯 Quick Examples

### CC Agent - Morning Briefing

```bash
# Via Telegram
@cc Good morning briefing

# Via CLI
python -m agency send "Good morning briefing" cc
```

**Result:**
- 📧 Email summary (urgent, important)
- 📅 Today's calendar
- 📁 Recent Drive files
- 🎯 Priorities
- 💡 Suggestions

---

### Job Search - Find Roles

```bash
@job_search Find ML Engineer roles at AI companies in SF
```

**Result:**
- 🔍 Searches job boards
- 📋 Lists relevant openings
- 💰 Shows salary ranges
- 🔗 Provides application links

---

### Feedback Management - E2E Demo

```bash
# Run the full E2E demo with real GitHub issues
ANTHROPIC_API_KEY=sk-ant-... python examples/feedback/e2e_feedback_github_demo.py
```

**Result:**
- Fetches real GitHub issues
- Claude AI clusters by theme
- Tracks bugs automatically
- Generates comprehensive solutions with PRDs

**[📖 See Feedback Examples Guide →](examples/feedback/README.md)**

---

## 🚀 Running Examples

### Basic Agent Examples

```bash
# Simple agent
python examples/basic/simple_agent.py

# Proactive agent with notifications
python examples/basic/proactive_agent.py

# Multi-agent coordination
python examples/basic/multi_agent.py
```

### Feedback Management Examples

```bash
# E2E GitHub feedback demo (recommended!)
python examples/feedback/e2e_feedback_github_demo.py

# Basic feedback workflow
python examples/feedback/feedback_management_demo.py
```

**[📖 See all examples →](examples/README.md)**

---

## 🛠️ Development

### Adding New Agents

1. Create agent directory:
   ```bash
   mkdir -p agency/agents/my_agent
   ```

2. Create skills file:
   ```python
   # agency/agents/my_agent/my_skills.py
   from agency.agents.base.skills import Skill, AgentSkill

   class MyAgentSkills(AgentSkill):
       @Skill(name="my_skill", description="...")
       def my_skill(self, param: str) -> dict:
           return {"result": "..."}
   ```

3. Create README documenting your agent

4. Add examples in `agency/agents/my_agent/examples/`

**[📖 See Agent Development Guide →](agency/agents/README.md#adding-new-agents)**

---

### Project Structure Benefits

✅ **Easy to find** - Each agent has its own folder with README
✅ **Self-contained** - Agent code, docs, and examples together
✅ **Discoverable** - Clear hierarchy and documentation
✅ **Maintainable** - Changes isolated to agent folders
✅ **Extensible** - Add new agents easily

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=...

# Optional (for CC agent)
GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
GOOGLE_TOKEN_FILE=google_token.pickle

# Optional (for job search)
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...
```

### Agent Templates

Customize agent behavior in `agency/templates/agents.json`:

```json
{
  "cc": {
    "personality": "You are CC, a personal AI productivity agent...",
    "preferences": {
      "briefing_time": "08:00",
      "focus_time_duration": 120
    }
  }
}
```

---

## 📖 Learning Path

1. **Start here:** [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Pick an agent:**
   - [CC Agent](agency/agents/cc/README.md) - for productivity
   - [Job Search](agency/agents/job_search/README.md) - for job hunting
   - [Feedback](agency/agents/feedback/README.md) - for feedback management
3. **Run examples:** [examples/](examples/)
4. **Build your own:** [Agent Development](agency/agents/README.md#adding-new-agents)

---

## 🐛 Troubleshooting

### Agent not responding?

```bash
# Check status
python -m agency status

# View logs
python -m agency logs -f

# Restart
python -m agency stop
python -m agency start
```

### Import errors?

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import agency; print(agency.__file__)"
```

### Can't find documentation?

All documentation is now organized by agent:
- Agent guides: `agency/agents/<agent_name>/README.md`
- Examples: `examples/<category>/README.md`
- Main guides: root directory

---

## 🌟 Features

- ✅ **Multi-agent system** - Specialized agents work together
- ✅ **Multi-channel** - Telegram, CLI, Web interface
- ✅ **Proactive** - Agents work 24/7 in the background
- ✅ **Personal** - Customize agent behavior and personality
- ✅ **Powerful** - Real integrations (Gmail, Calendar, Drive, etc.)
- ✅ **Extensible** - Easy to add new agents and skills
- ✅ **Production-ready** - Battle-tested tools and workflows

---

## 💡 Use Cases

### Personal Productivity (CC Agent)
- Morning briefings
- Email management
- Meeting scheduling
- Focus time blocking

### Job Hunting (Job Search Agent)
- Find relevant openings
- Tailor resumes
- Track applications
- Network outreach

### Product Management (Feedback Agent)
- Collect user feedback
- Cluster by theme
- Track bugs
- Generate solutions

---

## 📦 What's Included

- **3 Production Agents**: CC, Job Search, Feedback
- **11 Project Templates**: Ready-to-use agent projects
- **Working Examples**: E2E demos and tutorials
- **Complete Documentation**: Guides for every agent
- **Real Integrations**: Gmail, Calendar, Drive, GitHub
- **CLI & Telegram**: Multiple interaction modes

---

## 🎓 Next Steps

1. **[Complete Setup →](GETTING_STARTED.md)** - Get everything running
2. **[Try CC Agent →](agency/agents/cc/README.md)** - Morning briefings
3. **[Run Feedback Demo →](examples/feedback/e2e_feedback_github_demo.py)** - See E2E workflow
4. **[Build Your Agent →](agency/agents/README.md#adding-new-agents)** - Create custom agents

---

**Build agentic AI - Proactive, Personal, Powerful!** ✨

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

## 🔗 Links

- **Documentation**: See `agency/agents/` for agent guides
- **Examples**: See `examples/` for working demos
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions on GitHub Discussions

---

**Ready to get started?** 👉 [GETTING_STARTED.md](GETTING_STARTED.md)
