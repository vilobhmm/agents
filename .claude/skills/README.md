# Claude Skills for Job Hunter & CC Multi-Agent

Custom Claude Code skills for enhanced job hunting and productivity.

## 📁 Available Skills

### 1. `/job-search` - Universal Job Search

**Search for ANY job at ANY company in natural language!**

#### Usage:
```bash
# Format: /job-search "YOUR NATURAL LANGUAGE QUERY"

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

#### What You Get:
- ✅ LinkedIn Jobs (pre-filtered)
- ✅ Indeed (global + country-specific)
- ✅ Naukri.com (India)
- ✅ Glassdoor (with ratings)

All with **one-click apply** links!

---

## 🎯 How Skills Work

Claude Code skills are executable scripts in `.claude/skills/` that:
1. Parse your natural language input
2. Call the appropriate multi-agent
3. Return formatted results

### Skill Structure:
```
.claude/
  skills/
    job-search         # Job hunting skill
    README.md          # This file
```

---

## 🚀 Creating Your Own Skills

### Example: Custom Job Search Skill

```python
#!/usr/bin/env python3
"""Custom job search skill"""

import sys
import subprocess

query = " ".join(sys.argv[1:])
print(f"🔍 Searching: {query}")

# Call job_hunter agent
subprocess.run([
    "python", "-m", "agency", "debug", "test", "job_hunter",
    "--message", query
])
```

### Make it executable:
```bash
chmod +x .claude/skills/your-skill-name
```

### Use it:
```bash
/your-skill-name "your query here"
```

---

## 📚 Skill Ideas

### Job Hunting Skills:
- `/job-search` - Universal job search (✅ Implemented)
- `/job-track` - Track interesting jobs
- `/job-apply` - Help with applications
- `/resume-optimize` - Optimize resume for job
- `/cover-letter` - Generate cover letter

### Productivity Skills:
- `/morning-brief` - Get daily briefing (email + calendar)
- `/schedule-meeting` - Create calendar event
- `/send-email` - Quick email composition
- `/find-files` - Search Google Drive
- `/summarize-emails` - Summarize unread emails

### Research Skills:
- `/tech-news` - Latest tech news
- `/paper-summary` - Summarize research papers
- `/company-research` - Research company info

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
chmod +x .claude/skills/job-search
```

### Skill runs but no output?
```bash
# Run directly to debug
.claude/skills/job-search "test query"
```

---

## 🎓 Example Session

```bash
# Morning routine
/morning-brief

# Job hunting
/job-search "Find Java Developer at TCS in India with 2-3 years"

# Check results on LinkedIn, Indeed, Naukri, Glassdoor

# Track interesting job
/job-track "Save this TCS Java Developer role"

# Optimize resume
/resume-optimize "Tailor resume for Java Developer at TCS"

# Generate cover letter
/cover-letter "Create cover letter for TCS Java Developer role"

# Send application
/job-apply "Submit application with resume and cover letter"
```

---

## 📖 Learn More

- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Job Hunter Guide](../JOB_HUNTER_FLEXIBLE_GUIDE.md)
- [CC User Guide](../CC_USER_GUIDE.md)

---

**Your job search is now powered by Claude Code skills! 🚀**
