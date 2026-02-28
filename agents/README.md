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
