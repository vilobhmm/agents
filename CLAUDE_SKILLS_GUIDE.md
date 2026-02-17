# 🚀 Claude Code Skills for Job Hunting

**Alternative job hunting implementation using Claude Code skills instead of multi-agent architecture**

## 📚 Overview

This repository provides **TWO ways** to use job hunting capabilities:

### 1️⃣ Multi-Agent Architecture (Original)
- Complex multi-agent system with Telegram integration
- Full conversation management
- Team-based collaboration
- **Location:** `agency/` directory

### 2️⃣ Claude Code Skills (NEW! ⭐)
- Simple, lightweight Claude Code skills
- Direct command-line interface
- Natural language processing
- **Location:** `.claude/skills/` directory

---

## 🎯 Why Use Claude Skills?

### Advantages:
✅ **Simple** - No complex setup, just run commands
✅ **Fast** - Direct execution, no queue processing
✅ **Portable** - Works anywhere Claude Code is installed
✅ **Extensible** - Easy to add new skills
✅ **Natural** - Use conversational language

### When to Use Skills vs Multi-Agent:
- **Skills** - Quick searches, one-off tasks, CLI usage
- **Multi-Agent** - Complex workflows, Telegram integration, team collaboration

---

## 📋 Available Skills

### Job Hunting Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **job-quick** | `/job-quick google ml` | ⚡ Instant job board links |
| **job-search** | `/job-search "Find Java at TCS"` | 🔍 Advanced natural language search |
| **job-track** | `/job-track` | 📊 Track and manage applications |
| **job-dashboard** | `/job-dashboard` | 📈 Complete overview |
| **job-apply** | `/job-apply "Help with Google"` | 📝 Application assistance |
| **job-match** | `/job-match` | 🎯 Smart job matching |
| **job-research** | `/job-research "TCS culture"` | 🔬 Company research |
| **interview-prep** | `/interview-prep "Google ML"` | 🎯 Interview preparation |

### Productivity Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **morning-brief** | `/morning-brief` | ☀️ Daily email + calendar briefing |

---

## 🚀 Quick Start

### Installation

Skills are already installed in `.claude/skills/`!

```bash
# Verify installation
ls -la .claude/skills/

# Make executable (if needed)
chmod +x .claude/skills/*
```

### Basic Usage

```bash
# Quick job search (instant links)
.claude/skills/job-quick google ml engineer

# Advanced search (natural language)
.claude/skills/job-search "Find Java Developer at TCS in India with 2-3 years"

# Track jobs
.claude/skills/job-track "Track the Google ML Engineer role"

# View dashboard
.claude/skills/job-dashboard

# Morning briefing
.claude/skills/morning-brief
```

---

## 📖 Complete Examples

### Example 1: Quick Search for Indian IT Companies

```bash
# Get instant links for multiple companies
.claude/skills/job-quick tcs java india
.claude/skills/job-quick wipro software bangalore
.claude/skills/job-quick infosys full-stack mumbai
.claude/skills/job-quick accenture cloud engineer
```

**Output:** Instant links to LinkedIn, Indeed, Glassdoor, and Naukri

---

### Example 2: Advanced Natural Language Search

```bash
# Specific requirements
.claude/skills/job-search "Find Java Developer at TCS in India with 2-3 years experience"

# Skill-based search
.claude/skills/job-search "Find ML Engineer with Python, PyTorch, and TensorFlow"

# Location-based
.claude/skills/job-search "Find remote Product Manager jobs"

# Experience-based
.claude/skills/job-search "Find entry level Software Engineer in Bangalore"
```

**Output:** Customized search URLs with exact filters

---

### Example 3: Complete Application Workflow

```bash
# 1. Search for jobs
.claude/skills/job-search "Find Java Developer at TCS with Spring Boot in Bangalore"

# 2. Research company
.claude/skills/job-research "What's TCS company culture? Java Developer salary 2-3 years?"

# 3. Track the job
.claude/skills/job-track "Track TCS Java Developer role in Bangalore"

# 4. Prepare application
.claude/skills/job-apply "Tailor my resume for TCS Java Developer with Spring Boot"
.claude/skills/job-apply "Generate cover letter for TCS highlighting my 2 years experience"

# 5. Update status
.claude/skills/job-track "Update TCS Java Developer status to applied"

# 6. Prepare for interview
.claude/skills/interview-prep "TCS Java Developer technical interview questions"

# 7. Check progress
.claude/skills/job-dashboard
```

---

## 🎯 Power User Tips

### Create Shell Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Job hunting aliases
alias jq='~/.claude/skills/job-quick'
alias js='~/.claude/skills/job-search'
alias jt='~/.claude/skills/job-track'
alias jd='~/.claude/skills/job-dashboard'
alias ja='~/.claude/skills/job-apply'
alias jr='~/.claude/skills/job-research'
alias jp='~/.claude/skills/interview-prep'
alias mb='~/.claude/skills/morning-brief'
```

Now use them:
```bash
jq google ml
js "Find Java at TCS in India"
jt
jd
mb
```

### Daily Routine Script

```bash
#!/bin/bash
# daily-job-search.sh

echo "🌅 Starting daily job search routine..."

# Morning briefing
~/.claude/skills/morning-brief

# Search for new jobs
~/.claude/skills/job-search "Find ML Engineer with Python remote"

# Check dashboard
~/.claude/skills/job-dashboard

echo "✅ Done!"
```

---

## 🔧 Creating Custom Skills

### Example: LinkedIn Connection Request Skill

```python
#!/usr/bin/env python3
"""LinkedIn connection request helper"""

import sys
import subprocess

query = " ".join(sys.argv[1:])
message = f"Draft a professional LinkedIn connection request for: {query}"

subprocess.run([
    "python", "-m", "agency", "debug", "test", "job_hunter",
    "--message", message
], cwd="/home/user/agents")
```

Make it executable:
```bash
chmod +x .claude/skills/linkedin-connect
```

Use it:
```bash
.claude/skills/linkedin-connect "Google recruiter Sarah Chen about ML roles"
```

---

## 📊 Skills vs Multi-Agent Comparison

| Feature | Claude Skills | Multi-Agent System |
|---------|---------------|-------------------|
| **Setup** | None - ready to use | Complex (processor + Telegram) |
| **Speed** | Instant | Queue-based |
| **Interface** | CLI | Telegram + CLI |
| **Complexity** | Simple scripts | Full agent architecture |
| **Conversation** | One-off commands | Persistent conversations |
| **Team Collaboration** | No | Yes (multi-agent teams) |
| **Best For** | Quick tasks | Complex workflows |

**Recommendation:**
- Use **Skills** for daily job searching and quick tasks
- Use **Multi-Agent** for comprehensive job hunting campaigns with tracking

---

## 📂 Project Structure

```
agents/
├── .claude/
│   └── skills/              # ⭐ Claude Code Skills
│       ├── job-quick        # Instant job links
│       ├── job-search       # Natural language search
│       ├── job-track        # Job tracking
│       ├── job-dashboard    # Overview
│       ├── job-apply        # Application help
│       ├── job-match        # Smart matching
│       ├── job-research     # Company research
│       ├── interview-prep   # Interview prep
│       ├── morning-brief    # Daily briefing
│       ├── README.md        # Full documentation
│       └── QUICKSTART.md    # Quick start guide
│
├── agency/                  # Multi-agent system
│   ├── agents/             # Agent definitions
│   ├── tools/              # Job search tools
│   │   ├── job_search_tools.py
│   │   ├── universal_job_scraper.py
│   │   └── job_scraper.py
│   └── config.json         # Agent configuration
│
└── CLAUDE_SKILLS_GUIDE.md  # This file
```

---

## 🎓 Documentation

### For Users:
- [Quick Start Guide](.claude/skills/QUICKSTART.md) - Get started in 5 minutes
- [Skills README](.claude/skills/README.md) - Complete skill documentation
- [Multi-Agent Guide](README.md) - Multi-agent system documentation

### For Developers:
- [Job Search Tools](agency/tools/job_search_tools.py) - Tool implementation
- [Universal Scraper](agency/tools/universal_job_scraper.py) - Job board scraping
- [Agent Config](agency/config.json) - Agent configuration

---

## ✨ Examples by Use Case

### Use Case 1: Fresh Graduate Looking for Entry-Level Jobs

```bash
# Search for entry-level positions
.claude/skills/job-search "Find entry level Software Engineer in Bangalore"
.claude/skills/job-search "Find graduate trainee at TCS, Wipro, Infosys"

# Research companies
.claude/skills/job-research "Best entry-level companies for fresh graduates in India"

# Track opportunities
.claude/skills/job-track "Track TCS graduate trainee program"
```

### Use Case 2: Experienced Developer Looking for Senior Roles

```bash
# Search for senior positions
.claude/skills/job-search "Find Senior Java Engineer with 5+ years at TCS, Accenture"
.claude/skills/job-search "Find Staff Engineer remote with distributed systems"

# Research salary
.claude/skills/job-research "Senior Java Engineer salary in India with 5 years experience"

# Prepare for senior-level interviews
.claude/skills/interview-prep "System design interview for Senior Engineer"
```

### Use Case 3: ML Engineer Targeting AI Companies

```bash
# Search AI companies
.claude/skills/job-search "Find ML Engineer at Google, Anthropic, OpenAI with PyTorch"
.claude/skills/job-quick anthropic research scientist

# Research specific companies
.claude/skills/job-research "Anthropic ML Engineer interview process and requirements"

# Prepare for ML interviews
.claude/skills/interview-prep "Machine Learning technical interview at Google"
```

### Use Case 4: Career Change to Product Management

```bash
# Search for PM roles
.claude/skills/job-search "Find Product Manager entry to mid-level remote"

# Research PM requirements
.claude/skills/job-research "What skills needed for Product Manager at Google?"

# Prepare for PM interviews
.claude/skills/interview-prep "Product Management behavioral and case interviews"

# Tailor resume
.claude/skills/job-apply "Tailor my engineering resume for Product Manager role"
```

---

## 🔍 How It Works

### Architecture

```
User Command
    ↓
Claude Code Skill (Python script)
    ↓
Agency Multi-Agent System
    ↓
Job Search Tools
    ↓
Real Job Board APIs / Web Scraping
    ↓
Formatted Results
```

### Under the Hood

1. **User runs skill:** `.claude/skills/job-search "Find Java at TCS"`
2. **Skill parses input:** Extracts natural language query
3. **Calls agent:** Invokes `job_hunter` agent via agency system
4. **Agent processes:** Uses tools to search job boards
5. **Returns results:** Formatted job links and information

---

## 🆘 Troubleshooting

### Skill not found?
```bash
ls -la .claude/skills/
chmod +x .claude/skills/*
```

### Permission denied?
```bash
chmod +x .claude/skills/job-search
```

### No output?
```bash
# Test directly
.claude/skills/job-quick test
```

### Agent not responding?
```bash
# Check agency system
python -m agency debug test job_hunter --message "test"
```

---

## 🚀 Next Steps

1. **Try Quick Start** - Follow [QUICKSTART.md](.claude/skills/QUICKSTART.md)
2. **Create Aliases** - Add shell shortcuts for faster access
3. **Daily Routine** - Use `/morning-brief` and `/job-dashboard` daily
4. **Track Everything** - Use `/job-track` for all applications
5. **Build Custom Skills** - Create your own skills for specific needs

---

## 📖 Additional Resources

- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [Multi-Agent System README](README.md)
- [Job Search Tools Documentation](agency/tools/README.md)

---

## 🎉 Summary

**Claude Code Skills provide a simple, powerful alternative to the multi-agent system for job hunting:**

✅ **No setup** - Works out of the box
✅ **Natural language** - Search conversationally
✅ **Fast** - Instant results
✅ **Extensible** - Easy to customize
✅ **Comprehensive** - Full job search workflow

**Start job hunting with Claude Code skills today! 🚀**

---

*Built with ❤️ using Claude Code and Claude Agent SDK*
