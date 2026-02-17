# Claude Skills for Job Hunter & Productivity

**Supercharge your job search and daily productivity with Claude Code skills!**

## 🎯 Quick Start

```bash
# Morning routine
/morning-brief

# Job hunting
/job-search "Find Java Developer at TCS in India with 2-3 years"
/job-dashboard

# Quick search
/job-quick google ml engineer
```

---

## 📋 Job Hunting Skills

### 1. `/job-search` - Universal Job Search ⭐

**Search for ANY job at ANY company in natural language!**

```bash
# Indian IT Companies
/job-search "Find Java Developer at TCS in India with 2-3 years experience"
/job-search "Find Software Engineer at Wipro in Bangalore"
/job-search "Find Full Stack Developer at Infosys with React and Node.js"
/job-search "Find Senior Java Engineer at Accenture in Mumbai, 5+ years"

# Global Tech Companies
/job-search "Find Product Manager at Google, remote"
/job-search "Find ML Engineer at Microsoft with PyTorch"
/job-search "Find Research Scientist at Anthropic with NLP"
/job-search "Find Data Scientist at Meta in San Francisco"

# Skill-Based Search
/job-search "Find Backend Developer with Java and Spring Boot"
/job-search "Find ML Engineer with Python, TensorFlow, and PyTorch"
/job-search "Find DevOps Engineer with Kubernetes and AWS"
/job-search "Find Frontend Developer with React and TypeScript"

# Location-Based
/job-search "Find Software Engineer in Bangalore"
/job-search "Find Data Analyst in Mumbai"
/job-search "Find remote Product Manager jobs"
/job-search "Find Software Engineer in France"

# Experience-Based
/job-search "Find entry level Software Developer jobs"
/job-search "Find Senior ML Engineer with 5+ years experience"
/job-search "Find Mid-level Product Manager with 3-5 years"
```

**Returns:**
- ✅ LinkedIn Jobs (pre-filtered)
- ✅ Indeed (global + country-specific)
- ✅ Naukri.com (India)
- ✅ Glassdoor (with company ratings)

All with **one-click apply** links!

---

### 2. `/job-quick` - Instant Job Links ⚡

**Super fast! Get job board links instantly.**

```bash
/job-quick google ml
/job-quick anthropic engineer
/job-quick tcs java india
/job-quick microsoft product remote
```

Returns instant links to LinkedIn, Indeed, Glassdoor, and Naukri (for India searches).

---

### 3. `/job-track` - Track & Manage Jobs 📊

**Track interesting jobs and manage your applications.**

```bash
# View tracked jobs
/job-track

# Track a specific job
/job-track "Track the Google ML Engineer role"

# Update status
/job-track "Update TCS Java Developer status to applied"

# View applications
/job-track "Show jobs I've applied to"
```

---

### 4. `/job-dashboard` - Complete Overview 📈

**See your entire job search at a glance.**

```bash
# Quick dashboard
/job-dashboard

# Detailed dashboard
/job-dashboard --detailed
```

**Shows:**
- Jobs you've applied to (with status)
- Tracked jobs you're interested in
- Upcoming application deadlines
- Interview schedules
- Response rates and statistics

---

### 5. `/job-apply` - Application Helper 📝

**Get help with applications, resumes, and cover letters.**

```bash
/job-apply "Help me apply to Google ML Engineer role"
/job-apply "Generate cover letter for TCS Java Developer"
/job-apply "Tailor my resume for Product Manager at Microsoft"
/job-apply "What's the status of my Anthropic application?"
```

---

### 6. `/job-match` - Smart Job Matching 🎯

**Find jobs that match YOUR profile automatically.**

```bash
# Show matched jobs based on saved preferences
/job-match

# Update preferences
/job-match "Update my preferences: location India, experience 2-3 years"
/job-match "Set preferences: remote, ML roles, Python, 50k+ salary"
```

---

### 7. `/job-research` - Company Research 🔬

**Research companies, roles, and salary ranges.**

```bash
/job-research "Tell me about Google's ML Engineer interview process"
/job-research "What's the salary range for Java Developer at TCS?"
/job-research "Research Anthropic's company culture and values"
/job-research "What skills do I need for Product Manager at Microsoft?"
```

---

### 8. `/interview-prep` - Interview Preparation 🎯

**Prepare for interviews with practice questions and tips.**

```bash
/interview-prep "Google ML Engineer technical interview"
/interview-prep "Behavioral questions for Product Manager"
/interview-prep "System design questions for Senior Engineer"
/interview-prep "Java coding questions for TCS interview"
```

---

## 📆 Productivity Skills

### 9. `/morning-brief` - Daily Briefing ☀️

**Start your day with emails, calendar, and priorities.**

```bash
# Quick briefing
/morning-brief

# Detailed briefing
/morning-brief --detailed
```

**Includes:**
- Unread emails summary
- Today's calendar events
- Recent Drive files
- Action items and priorities

---

## 🎓 Example Job Search Workflow

```bash
# 1. Morning routine
/morning-brief

# 2. Search for jobs
/job-search "Find Java Developer at TCS in India with 2-3 years"

# 3. Quick search for more companies
/job-quick wipro java india
/job-quick infosys java bangalore

# 4. Track interesting jobs
/job-track "Track the TCS Java Developer role in Bangalore"

# 5. Research company
/job-research "What's TCS company culture like? Salary for 2-3 years Java?"

# 6. Prepare application
/job-apply "Tailor my resume for TCS Java Developer with Spring Boot"
/job-apply "Generate cover letter for TCS highlighting my 2 years experience"

# 7. Track application
/job-track "Update TCS Java Developer status to applied"

# 8. Prepare for interview
/interview-prep "TCS Java Developer technical interview"

# 9. Check dashboard
/job-dashboard
```

---

## 🚀 How Claude Skills Work

Claude Code skills are executable scripts in `.claude/skills/` that:
1. Parse your natural language input
2. Call the appropriate multi-agent (job_hunter, cc, etc.)
3. Return formatted results

### Skill Structure:

```
.claude/
  skills/
    job-search         # Universal job search
    job-quick          # Instant job links
    job-track          # Track jobs
    job-dashboard      # Complete overview
    job-apply          # Application helper
    job-match          # Smart matching
    job-research       # Company research
    interview-prep     # Interview prep
    morning-brief      # Daily briefing
    README.md          # This file
```

---

## 🛠️ Creating Your Own Skills

### Example: Custom Networking Skill

```python
#!/usr/bin/env python3
"""LinkedIn connection request helper"""

import sys
import subprocess

query = " ".join(sys.argv[1:])
message = f"Draft a LinkedIn connection request for: {query}"

subprocess.run([
    "python", "-m", "agency", "debug", "test", "job_hunter",
    "--message", message
], cwd="/home/user/agents")
```

### Make it executable:

```bash
chmod +x .claude/skills/linkedin-connect
```

### Use it:

```bash
/linkedin-connect "Google recruiter Sarah Chen about ML roles"
```

---

## 📚 More Skill Ideas

### Job Hunting:
- ✅ `/job-search` - Universal job search
- ✅ `/job-quick` - Instant job links
- ✅ `/job-track` - Track jobs
- ✅ `/job-dashboard` - Overview
- ✅ `/job-apply` - Application helper
- ✅ `/job-match` - Smart matching
- ✅ `/job-research` - Company research
- ✅ `/interview-prep` - Interview prep
- 💡 `/resume-optimize` - Resume optimization
- 💡 `/cover-letter` - Cover letter generator
- 💡 `/linkedin-outreach` - LinkedIn messages
- 💡 `/salary-negotiate` - Salary negotiation help
- 💡 `/referral-request` - Request referrals

### Productivity:
- ✅ `/morning-brief` - Daily briefing
- 💡 `/schedule-meeting` - Create calendar event
- 💡 `/send-email` - Quick email composition
- 💡 `/find-files` - Search Google Drive
- 💡 `/summarize-emails` - Summarize unread emails
- 💡 `/week-review` - Weekly summary

### Research:
- 💡 `/tech-news` - Latest tech news
- 💡 `/paper-summary` - Summarize research papers
- 💡 `/company-research` - Deep company research

---

## ✅ Best Practices

1. **Keep skills simple** - One skill, one purpose
2. **Use natural language** - Make it conversational
3. **Provide examples** - Show users how to use it
4. **Error handling** - Handle edge cases gracefully
5. **Clear output** - Format results for readability

---

## 🔧 Troubleshooting

### Skill not found?

```bash
# Check skill exists
ls -la .claude/skills/

# Make it executable
chmod +x .claude/skills/job-search
```

### Permission denied?

```bash
# Ensure script is executable
chmod +x .claude/skills/*
```

### Skill runs but no output?

```bash
# Run directly to debug
.claude/skills/job-search "test query"
```

---

## 💡 Tips

- **Use `/job-quick` for fast searches** - Get instant links
- **Use `/job-search` for advanced filters** - More control
- **Track jobs immediately** - Use `/job-track` right after finding interesting roles
- **Check `/job-dashboard` daily** - Stay on top of applications
- **Prepare early** - Use `/interview-prep` as soon as you apply

---

## 📖 Learn More

- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Multi-Agent System Guide](../README.md)
- [Job Hunter Configuration](../agency/config.json)

---

**Your job search is now powered by Claude Code skills! 🚀**

*Built with ❤️ using Claude Agent SDK*
