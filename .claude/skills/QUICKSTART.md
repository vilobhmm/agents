# 🚀 Job Hunter Skills - Quick Start Guide

**Get started with Claude Code skills for job hunting in 5 minutes!**

## ⚡ Instant Setup

All skills are ready to use! No configuration needed.

```bash
# List all available skills
ls .claude/skills/

# Make sure they're executable (already done!)
chmod +x .claude/skills/*
```

---

## 🎯 Try These Now

### 1. Quick Job Search (Instant Links)

```bash
# Get instant job board links
.claude/skills/job-quick google ml engineer
.claude/skills/job-quick tcs java india
.claude/skills/job-quick anthropic research
```

**Result:** Instant links to LinkedIn, Indeed, Glassdoor, Naukri

---

### 2. Advanced Job Search (Natural Language)

```bash
# Search with natural language
.claude/skills/job-search "Find Java Developer at TCS in India with 2-3 years"
.claude/skills/job-search "Find remote ML Engineer with Python and PyTorch"
.claude/skills/job-search "Find Software Engineer at Wipro in Bangalore"
```

**Result:** Customized search links with your exact filters

---

### 3. Track Jobs

```bash
# View tracked jobs
.claude/skills/job-track

# Track a specific job
.claude/skills/job-track "Track the Google ML Engineer role"

# Update status
.claude/skills/job-track "Update TCS status to applied"
```

---

### 4. View Dashboard

```bash
# See your job search overview
.claude/skills/job-dashboard

# Detailed view
.claude/skills/job-dashboard --detailed
```

---

### 5. Application Help

```bash
# Get help with applications
.claude/skills/job-apply "Help me apply to Google ML Engineer"
.claude/skills/job-apply "Generate cover letter for TCS Java Developer"
.claude/skills/job-apply "Tailor resume for Product Manager at Microsoft"
```

---

### 6. Company Research

```bash
# Research companies and roles
.claude/skills/job-research "Google ML Engineer interview process"
.claude/skills/job-research "TCS Java Developer salary in India"
.claude/skills/job-research "Anthropic company culture"
```

---

### 7. Interview Prep

```bash
# Prepare for interviews
.claude/skills/interview-prep "Google ML Engineer technical"
.claude/skills/interview-prep "Java coding questions for TCS"
.claude/skills/interview-prep "Behavioral for Product Manager"
```

---

### 8. Job Matching

```bash
# Find jobs matching your profile
.claude/skills/job-match

# Update preferences
.claude/skills/job-match "Update preferences: India, 2-3 years, Java"
```

---

### 9. Morning Briefing

```bash
# Daily briefing (emails + calendar)
.claude/skills/morning-brief

# Detailed briefing
.claude/skills/morning-brief --detailed
```

---

## 📋 Complete Workflow Example

```bash
# ========================================
# MORNING ROUTINE
# ========================================

# 1. Start your day
.claude/skills/morning-brief

# ========================================
# JOB SEARCH
# ========================================

# 2. Quick search for multiple companies
.claude/skills/job-quick google ml
.claude/skills/job-quick anthropic engineer
.claude/skills/job-quick tcs java india

# 3. Advanced search with filters
.claude/skills/job-search "Find Java Developer at TCS with 2-3 years in Bangalore"

# ========================================
# RESEARCH & TRACKING
# ========================================

# 4. Research interesting companies
.claude/skills/job-research "TCS company culture and Java Developer salary"

# 5. Track interesting jobs
.claude/skills/job-track "Track TCS Java Developer in Bangalore"
.claude/skills/job-track "Track Google ML Engineer remote"

# ========================================
# APPLICATION PREP
# ========================================

# 6. Prepare application materials
.claude/skills/job-apply "Tailor resume for TCS Java Developer"
.claude/skills/job-apply "Generate cover letter for TCS"

# 7. Update tracking after applying
.claude/skills/job-track "Update TCS status to applied"

# ========================================
# INTERVIEW PREP
# ========================================

# 8. Prepare for interview
.claude/skills/interview-prep "TCS Java technical interview"

# ========================================
# DASHBOARD CHECK
# ========================================

# 9. Check your overall progress
.claude/skills/job-dashboard
```

---

## 🔥 Power User Tips

### Tip 1: Alias for Faster Access

Add to your `~/.bashrc` or `~/.zshrc`:

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

# Now use them:
# jq google ml
# js "Find Java at TCS in India"
# jt
# jd
```

### Tip 2: Use in Scripts

```bash
#!/bin/bash
# Daily job search routine

echo "Starting daily job search..."

# Morning briefing
~/.claude/skills/morning-brief

# Search for new jobs
~/.claude/skills/job-search "Find ML Engineer with Python remote"

# Check dashboard
~/.claude/skills/job-dashboard

echo "Done!"
```

### Tip 3: Combine with Other Tools

```bash
# Search and save results
.claude/skills/job-quick google ml | tee google_jobs.txt

# Track all applications
.claude/skills/job-track > applications.txt
```

---

## 🎯 Common Use Cases

### Use Case 1: Indian IT Company Search

```bash
.claude/skills/job-quick tcs java india
.claude/skills/job-quick wipro java bangalore
.claude/skills/job-quick infosys full-stack
.claude/skills/job-quick accenture cloud india
```

### Use Case 2: Global Tech Company Search

```bash
.claude/skills/job-search "Find ML Engineer at Google with PyTorch"
.claude/skills/job-search "Find Research Scientist at Anthropic"
.claude/skills/job-search "Find Product Manager at Microsoft remote"
```

### Use Case 3: Skill-Based Search

```bash
.claude/skills/job-search "Find Backend Developer with Java and Spring Boot"
.claude/skills/job-search "Find DevOps Engineer with Kubernetes and AWS"
.claude/skills/job-search "Find Data Scientist with Python and TensorFlow"
```

### Use Case 4: Complete Application Process

```bash
# 1. Find job
.claude/skills/job-search "Find Java Developer at TCS in Bangalore"

# 2. Research
.claude/skills/job-research "TCS Java Developer salary and culture"

# 3. Track
.claude/skills/job-track "Track TCS Java Developer"

# 4. Apply
.claude/skills/job-apply "Tailor resume for TCS Java Developer"
.claude/skills/job-apply "Generate cover letter for TCS"

# 5. Update
.claude/skills/job-track "Update TCS status to applied"

# 6. Prepare
.claude/skills/interview-prep "TCS Java technical interview"
```

---

## 📊 Skill Comparison

| Skill | Speed | Detail | Best For |
|-------|-------|--------|----------|
| `/job-quick` | ⚡⚡⚡ | ⭐ | Instant links, quick searches |
| `/job-search` | ⚡⚡ | ⭐⭐⭐ | Advanced filters, specific requirements |
| `/job-track` | ⚡⚡ | ⭐⭐ | Managing applications |
| `/job-dashboard` | ⚡ | ⭐⭐⭐ | Complete overview |
| `/job-apply` | ⚡⚡ | ⭐⭐⭐ | Application materials |
| `/job-research` | ⚡ | ⭐⭐⭐ | Company insights |
| `/interview-prep` | ⚡ | ⭐⭐⭐ | Interview practice |
| `/job-match` | ⚡⚡ | ⭐⭐ | Preference matching |
| `/morning-brief` | ⚡⚡ | ⭐⭐⭐ | Daily overview |

---

## ❓ FAQ

### Q: Where are my tracked jobs stored?

A: `~/.agency/job_search/tracked_jobs.json`

### Q: Can I edit my preferences?

A: Yes! Use `.claude/skills/job-match "Update preferences: ..."`

### Q: How do I see all my applications?

A: `.claude/skills/job-dashboard` or `.claude/skills/job-track`

### Q: Can I search international jobs?

A: Yes! Just specify the country: "Find Software Engineer in France"

### Q: Which skill should I use for quick searches?

A: Use `/job-quick` for instant links, `/job-search` for filtered results

---

## 🆘 Troubleshooting

### Permission denied?

```bash
chmod +x ~/.claude/skills/*
```

### Skill not found?

```bash
# Check they exist
ls -la ~/.claude/skills/

# Run with full path
~/.claude/skills/job-search "Find jobs"
```

### No output?

```bash
# Test directly
.claude/skills/job-quick test
```

---

## 🎓 Next Steps

1. **Try each skill** - Run through all examples above
2. **Create aliases** - Add shortcuts to your shell config
3. **Set preferences** - Use `/job-match` to save your profile
4. **Build a routine** - Use `/morning-brief` daily
5. **Track everything** - Use `/job-track` for all applications

---

## 📖 Full Documentation

- [Complete Skills Guide](README.md)
- [Multi-Agent System](../README.md)
- [Job Search Tools](../agency/tools/job_search_tools.py)

---

**Start your job search with Claude Code skills today! 🚀**

*Any questions? Check the [README](README.md) or create an issue!*
