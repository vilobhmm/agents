# 🤖 AI Agents Repository

**Production-ready AI agents with voice, research, and integration capabilities**

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...

# 3. Try an agent
python -m agents.cc.cc_skills
```

**→ [Complete Setup Guide](docs/setup/GETTING_STARTED.md)**

---

## 📁 Repository Structure

```
/
├── agents/                # ALL AI AGENTS (main focus)
│   ├── cc/               # Chief Coordinator - productivity assistant
│   ├── job_search/       # Job hunting automation
│   ├── feedback/         # Feedback management
│   ├── voice/            # 4 voice agents (dictation, productivity, ideas, dev)
│   └── co_scientist/     # Research & startup co-founder
│
├── integrations/          # External integrations
│   ├── adk/              # Google ADK ecosystem
│   └── voice_core/       # Voice capabilities (STT/TTS)
│
├── core/                  # Core framework
│   ├── channels/         # Telegram, CLI, Web
│   ├── templates/        # Agent templates
│   └── processor.py      # Message processing
│
├── examples/              # Working examples
├── docs/                  # All documentation
└── tools/                 # Utilities and scripts
```

---

## 🤖 Available Agents

### **1. CC Agent** - Chief Coordinator 🎯
Your personal AI productivity assistant (like Google Labs CC)

- Morning briefings from Gmail, Calendar, Drive
- Email management and drafting
- Meeting scheduling
- Voice-activated commands

**→ [agents/cc/README.md](agents/cc/README.md)**

---

### **2. Job Search Agent** - Job Hunting Automation 💼
Automate your job search process

- Find relevant job openings
- Tailor resumes for each role
- Track applications
- Network outreach

**→ [agents/job_search/README.md](agents/job_search/README.md)**

---

### **3. Feedback Agent** - User Feedback Management 📋
Collect, cluster, and analyze feedback

- Feedback collection and categorization
- AI-powered clustering (Claude)
- Bug tracking
- Solution generation with PRDs

**→ [agents/feedback/README.md](agents/feedback/README.md)**

---

### **4. Voice Agents** - Complete Voice System 🎙️
4 specialized voice agents for hands-free productivity

- **Dictation**: Voice-to-text for any chat
- **Productivity**: Voice assistant for daily tasks
- **Ideas Capture**: Voice-to-Google Docs/Notes
- **Dev Copilot**: Voice-based pair programming

**→ [agents/voice/README.md](agents/voice/README.md)**

---

### **5. Co-Scientist Agent** - Research & Startup Partner 🔬
AI partner for building science/AI-based companies

- Literature reviews
- Hypothesis generation
- Experiment design
- Business strategy
- Pitch deck creation
- Fundraising planning

**→ [agents/co_scientist/README.md](agents/co_scientist/README.md)**

---

## 🔌 Integrations

### **ADK Ecosystem** - Google's Agent Development Kit
Complete integration with Google's ADK:

- **Observability**: AgentOps, Arize, Phoenix, W&B Weave
- **Platforms**: n8n (automation), StackOne (200+ SaaS apps)
- **AI/ML**: Hugging Face (200K+ models)

**→ [integrations/adk/README.md](integrations/adk/README.md)**

---

## 📚 Documentation

### Setup Guides
- **[Getting Started](docs/setup/GETTING_STARTED.md)** - Complete setup walkthrough
- **[External Services](docs/setup/EXTERNAL_SERVICES_SETUP.md)** - Google, Telegram, etc.
- **[Quick Integration](docs/setup/QUICK_INTEGRATION_GUIDE.md)** - Fast integration guide

### Agent Guides
- **[CC Agent E2E](docs/guides/CC_AGENT_E2E_GUIDE.md)** - Complete CC guide
- **[Job Hunter](docs/guides/JOB_HUNTER_FLEXIBLE_GUIDE.md)** - Job search automation
- **[Feedback Team](docs/guides/FEEDBACK_TEAM_GUIDE.md)** - Feedback management
- **[Telegram Integration](docs/guides/TELEGRAM_GUIDE.md)** - Use agents via Telegram

### Reference
- **[Agent Capabilities](docs/AGENT_CAPABILITIES.md)** - What agents can do
- **[Claude Skills Guide](docs/CLAUDE_SKILLS_GUIDE.md)** - Skill system
- **[All Documentation](docs/)** - Complete docs

---

## 💻 Usage Examples

### CC Agent - Morning Briefing

```python
from agents.cc.cc_skills import CCSkills

cc = CCSkills()
result = await cc.get_gmail_summary(max_emails=10)
result = await cc.get_calendar_summary()
```

### Voice Agent - Dictation

```bash
# Dictate to Claude (10 seconds)
python -m agents.voice.dictation.dictation_agent 10 claude
```

### Feedback Agent - E2E Demo

```bash
# Run complete feedback workflow with real GitHub issues
python examples/feedback/e2e_feedback_github_demo.py
```

### ADK Integration

```python
from integrations.adk import ADKAgent
from integrations.adk.integrations import create_observability_stack

agent = ADKAgent("my_agent", "task executor")

# Add full observability
for integration in create_observability_stack():
    agent.add_integration(integration)

result = await agent.execute_task("your task")
```

---

## 🛠️ Development

```bash
# Run tests
python tools/test_agency.py

# Start Telegram bot
./tools/start-telegram.sh

# Verify integrations
python tools/verify_integrations.py
```

---

## 🎯 Key Features

✅ **5 Production Agents** - CC, Job Search, Feedback, Voice (4), Co-Scientist
✅ **Voice-Enabled** - Complete voice system with 4 specialized agents
✅ **Google ADK** - Full integration ecosystem
✅ **Multi-Channel** - Telegram, CLI, Web
✅ **Observability** - AgentOps, Arize, Phoenix, W&B
✅ **200+ Integrations** - Via StackOne
✅ **Production-Ready** - Battle-tested tools and workflows

---

## 📦 Installation

```bash
# Clone repository
git clone <repo-url>
cd agents

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Quick test
python tools/test_agency.py
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Quick Links

- **[Getting Started](docs/setup/GETTING_STARTED.md)** - Start here!
- **[All Agents](agents/README.md)** - Agent overview
- **[Examples](examples/README.md)** - Working examples
- **[Documentation](docs/)** - Complete docs

---

**Build production AI agents - from voice to research to automation.** 🚀✨
