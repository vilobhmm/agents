# 🤖 Agency Agents

**Specialized AI agents with unique skills and capabilities**

This directory contains all the specialized agents that power the Agency system.

---

## 📁 Directory Structure

```
agents/
├── README.md (this file)
├── cc/                    # Chief Coordinator Agent
│   ├── README.md         # Complete CC agent guide
│   ├── cc_skills.py      # Gmail, Calendar, Drive skills
│   └── examples/         # CC usage examples
├── job_search/           # Job Search Agent
│   ├── README.md         # Job hunting guide
│   ├── job_search_skills.py  # Job search skills
│   └── examples/         # Job search examples
├── feedback/             # Feedback Management Team
│   ├── README.md         # Feedback system guide
│   ├── feedback_skills.py    # Feedback tools
│   └── examples/         # Feedback examples
├── voice/                # Voice Multi-Agent System
│   ├── README.md         # Voice agents guide
│   ├── dictation/        # Speech-to-text transcription
│   ├── productivity/     # Voice productivity assistant
│   ├── ideas_capture/    # Voice-to-notes
│   └── dev_copilot/      # Voice coding partner
├── co_scientist/         # Research & Startup Co-Founder
│   ├── README.md         # Co-scientist guide
│   ├── co_scientist_agent.py     # General science research
│   └── ai_agents_co_scientist.py # AI agents research
├── time_tracker/         # Time Tracking Multi-Agent System
│   ├── README.md         # Time tracker guide
│   ├── activity_monitor/ # Activity tracking agent
│   ├── categorizer/      # Time categorization agent
│   ├── analytics/        # Analytics & insights agent
│   ├── reporter/         # Report generation agent
│   ├── coordinator.py    # Multi-agent coordinator
│   └── storage.py        # Data storage manager
└── base/                 # Base Agent Framework
    └── skills.py         # Core skill definitions
```

---

## 🤖 Available Agents

### 1. **CC (Chief Coordinator)** 🎯
> *Your Personal AI Chief of Staff*

**Location:** [`cc/`](./cc/)

**What it does:**
- Morning briefings from Gmail, Calendar, Drive
- Email management and drafting
- Meeting scheduling and preparation
- Focus time blocking
- Proactive notifications

**Skills:**
- `get_gmail_summary` - Fetch and summarize emails
- `get_calendar_summary` - Review today's schedule
- `get_drive_summary` - Track document changes
- `send_email` - Send or draft emails
- `create_calendar_event` - Schedule meetings
- `block_focus_time` - Block calendar slots

**Quick start:**
```bash
# View full guide
cat agency/agents/cc/README.md

# Use via Telegram
@cc Good morning briefing
```

---

### 2. **Job Search** 💼
> *Automated Job Hunting*

**Location:** [`job_search/`](./job_search/)

**What it does:**
- Find relevant job openings
- Tailor resumes for each role
- Automate applications
- Track application status
- Manage networking and follow-ups

**Skills:**
- `search_jobs` - Find jobs across platforms
- `tailor_resume` - Customize resume for role
- `apply_to_job` - Submit application
- `track_application` - Monitor status
- `network_outreach` - Connect with recruiters

**Quick start:**
```bash
# View full guide
cat agency/agents/job_search/README.md

# Use via Telegram
@job_search Find ML Engineer roles at AI companies
```

---

### 3. **Feedback Management** 📋
> *User Feedback → Solutions Pipeline*

**Location:** [`feedback/`](./feedback/)

**What it does:**
- Collect and categorize user feedback
- Cluster feedback by theme
- Track bugs and issues
- Generate solutions and PRDs
- Analytics and reporting

**Skills:**
- `submit_feedback` - Submit new feedback
- `cluster_feedback` - Group by theme
- `enrich_feedback` - Add technical context
- `create_bug` - Track bugs
- `generate_solution` - Create PRD + prompts
- `feedback_analytics` - View reports

**Quick start:**
```bash
# View full guide
cat agency/agents/feedback/README.md

# Run E2E demo
python examples/feedback/e2e_feedback_github_demo.py
```

---

### 4. **Voice Multi-Agent System** 🎤
> *Voice-Powered Productivity*

**Location:** [`voice/`](./voice/)

**What it does:**
- Speech-to-text transcription (dictation)
- Voice productivity assistant
- Voice-to-notes idea capture
- Voice coding co-pilot

**Agents:**
- Dictation Agent - Replace typing with voice
- Productivity Agent - Daily updates via voice
- Ideas Capture - Speak ideas to Google Docs/Notes
- Dev Copilot - Voice-based code discussion

**Quick start:**
```bash
# View full guide
cat agents/voice/README.md

# Run demo
python examples/voice/e2e_voice_demo.py
```

---

### 5. **Co-Scientist** 🔬
> *Research & Startup Co-Founder*

**Location:** [`co_scientist/`](./co_scientist/)

**What it does:**
- Scientific literature review
- Hypothesis generation
- Experiment design
- Business strategy for AI startups
- Pitch deck creation
- Fundraising guidance

**Skills:**
- Literature review and research
- Agent architecture design
- Evaluation frameworks
- Product strategy
- Market analysis

**Quick start:**
```bash
# View full guide
cat agents/co_scientist/README.md

# Run demo
python examples/co_scientist/e2e_co_scientist_demo.py
```

---

### 6. **Time Tracker** ⏱️
> *Track Every Minute of Your Day*

**Location:** [`time_tracker/`](./time_tracker/)

**What it does:**
- Minute-level activity tracking
- Automatic categorization
- Productivity analytics & scoring
- Time waste identification
- Focus metrics & deep work tracking
- Comprehensive reporting

**Multi-Agent System:**
- **Activity Monitor** - Track activities with minute-level granularity
- **Categorizer** - Auto-categorize into work, learning, health, etc.
- **Analytics** - Identify patterns, trends, and productivity insights
- **Reporter** - Generate daily/weekly reports and charts

**Key Features:**
- 📊 Productivity score (0-100)
- 🎯 Focus metrics and deep work tracking
- ⚠️ Time waster identification
- 💡 Personalized improvement suggestions
- 📈 Weekly trends and patterns
- 📤 Export to JSON/CSV

**Quick start:**
```bash
# View full guide
cat agents/time_tracker/README.md

# Run interactive demo
python examples/time_tracker/e2e_time_tracker_demo.py

# Quick demo
python examples/time_tracker/e2e_time_tracker_demo.py --quick
```

**Example Usage:**
```python
from agents.time_tracker import TimeTrackerCoordinator

# Initialize
tracker = TimeTrackerCoordinator()

# Track activities
await tracker.start_activity("Writing documentation")
# ... do work ...
await tracker.stop_activity()

# Get insights
print(await tracker.daily_report())
score = await tracker.productivity_score()
print(f"Productivity: {score['productivity_score']}/100")
```

---

## 🛠️ Adding New Agents

### Step 1: Create Agent Directory

```bash
mkdir -p agency/agents/my_agent
cd agency/agents/my_agent
```

### Step 2: Create Skills File

```python
# my_agent_skills.py
from agency.agents.base.skills import Skill, AgentSkill

class MyAgentSkills(AgentSkill):
    """My custom agent skills."""

    @Skill(
        name="my_skill",
        description="What this skill does",
        parameters={
            "param1": "Description of param1"
        }
    )
    def my_skill(self, param1: str) -> dict:
        """Implementation of skill."""
        # Your logic here
        return {"status": "success", "result": "..."}
```

### Step 3: Create README

Document your agent's:
- Purpose and capabilities
- Available skills
- Usage examples
- Configuration options
- Troubleshooting tips

### Step 4: Add Examples

Create example scripts in `examples/` subdirectory.

---

## 📚 Common Patterns

### Accessing Agent Skills

```python
from agency.agents.cc.cc_skills import CCSkills
from agency.agents.job_search.job_search_skills import JobSearchSkills
from agency.agents.feedback.feedback_skills import FeedbackSkills

# Initialize
cc = CCSkills()
job_search = JobSearchSkills()
feedback = FeedbackSkills()

# Use skills
result = cc.get_gmail_summary(max_emails=10)
jobs = job_search.search_jobs(query="ML Engineer", location="SF")
report = feedback.submit_feedback(user_id="user123", text="Bug report")
```

### Multi-Agent Coordination

```python
from agency.core.coordinator import Coordinator

# Create coordinator
coord = Coordinator()

# Coordinate multiple agents
result = coord.execute_workflow([
    ("cc", "get_gmail_summary"),
    ("feedback", "submit_feedback", {"user_id": "...", "text": "..."}),
    ("cc", "send_email", {"to": "...", "subject": "...", "body": "..."})
])
```

---

## 🔧 Configuration

Each agent can be configured via:

1. **Environment variables** (`.env` file)
2. **Agent templates** (`agency/templates/agents.json`)
3. **Runtime parameters** (passed to skills)

Example configuration:

```env
# CC Agent
GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
GOOGLE_TOKEN_FILE=google_token.pickle

# Job Search Agent
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Feedback Agent
FEEDBACK_DB_PATH=feedback.db
```

---

## 📖 Learn More

- **[Getting Started](../../GETTING_STARTED.md)** - Complete setup guide
- **[CLI Commands](../CLI_COMMANDS.md)** - Command reference
- **[Examples](../../examples/)** - Working examples

---

## 💡 Tips

1. **Start with examples** - Run the example scripts in each agent's folder
2. **Read the READMEs** - Each agent has detailed documentation
3. **Combine agents** - Agents work better together
4. **Customize skills** - Extend agents with your own skills
5. **Use templates** - Agent templates define personality and behavior

---

**Build your AI agent team!** 🚀
