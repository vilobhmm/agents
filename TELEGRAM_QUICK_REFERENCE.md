# 📱 Telegram Bot Quick Reference Card

## 🚀 Start the System

```bash
cd ~/claude-code/github/agents
./start-telegram.sh
```

**Or manually:**
```bash
# Terminal 1 - Processor
python -m agency process

# Terminal 2 - Telegram Bot
python -m agency.channels.telegram_channel
```

---

## ⚡ Quick Commands

### CC Agent (Productivity)

| Command | Description | Example |
|---------|-------------|---------|
| `/morning` | Daily briefing | `/morning` |
| `/briefing` | Same as /morning | `/briefing` |
| `/emails` | Check inbox | `/emails` |
| `/calendar` | Today's schedule | `/calendar` |
| `/meeting` | Next meeting prep | `/meeting` |

### Job Hunter (Career)

| Command | Description | Example |
|---------|-------------|---------|
| `/jobs` | Quick search | `/jobs` |
| `/jobs [query]` | Search with params | `/jobs Java Developer at TCS` |
| `/jobsearch <query>` | Full custom search | `/jobsearch ML Engineer with Python` |
| `/trackjobs` | View tracked jobs | `/trackjobs` |
| `/applications` | Your applications | `/applications` |

### System

| Command | Description |
|---------|-------------|
| `/help` | Full help |
| `/agents` | List agents |
| `/status` | System status |

---

## 💬 Natural Language Examples

### CC Examples

```
@cc What's on my calendar today?
@cc Do I have urgent emails?
@cc When is my next meeting?
@cc Block 30 minutes for lunch
@cc Send email to sarah@company.com
@cc Find Q4 budget in Drive
```

### Job Hunter Examples

```
@job_hunter Find Java jobs at TCS in India
@job_hunter Search for Software Engineer at Wipro
@job_hunter Find ML Engineer with Python and PyTorch
@job_hunter Track the TCS Java Developer role
@job_hunter Show my tracked jobs
@job_hunter What have I applied to?
```

---

## 🎯 Job Search Patterns

### By Role & Company
```
/jobsearch Java Developer at TCS
/jobsearch Software Engineer at Wipro
/jobsearch ML Engineer at Microsoft
```

### By Location
```
/jobsearch Software Engineer in Bangalore
/jobsearch Data Scientist in Mumbai
/jobsearch Product Manager remote
```

### By Skills
```
/jobsearch Java Developer with Spring Boot
/jobsearch ML Engineer with Python and PyTorch
/jobsearch DevOps with Kubernetes and AWS
```

### By Experience
```
/jobsearch Senior Java Developer 5+ years
/jobsearch Entry level Software Engineer
/jobsearch Mid-level Product Manager 3-5 years
```

### Full Query
```
/jobsearch Senior Java Developer at TCS in India with 5+ years experience and Spring Boot
```

---

## 📊 What You Get

### From /morning
- ✅ Unread emails (prioritized)
- ✅ Today's calendar
- ✅ Action items
- ✅ Recent files

### From /jobs
- ✅ LinkedIn Jobs
- ✅ Indeed (country-specific)
- ✅ Naukri.com (India)
- ✅ Glassdoor (ratings)

---

## 🔧 Troubleshooting

### Bot not responding?
```bash
# Check if running
ps aux | grep "agency process"
ps aux | grep "telegram_channel"

# Restart
./start-telegram.sh
```

### Check logs
```bash
tail -f logs/processor.log
tail -f logs/telegram.log
```

### Test directly
```bash
# Test CC
python -m agency debug test cc --message "test"

# Test job_hunter
python -m agency debug test job_hunter --message "test"
```

---

## 🎓 Pro Tips

✅ **Daily Routine**: Send `/morning` every day
✅ **Job Alerts**: Use `/jobsearch` for specific roles
✅ **Track Jobs**: Save interesting positions
✅ **Meeting Prep**: Use `/meeting` before calls
✅ **Stay Organized**: Check `/emails` regularly

---

## 📞 Support

**Full Guide**: `TELEGRAM_SETUP_GUIDE.md`
**Job Hunter Guide**: `JOB_HUNTER_FLEXIBLE_GUIDE.md`
**CC Guide**: `CC_USER_GUIDE.md`

---

**Your AI agents are always ready! 🤖✨**
