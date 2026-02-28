# 📱 Feedback Management via Telegram

Complete guide to managing user feedback through Telegram commands.

---

## 🎯 **Available Commands**

### **1. `/submitfeedback` 📝**
**Submit user feedback**

```
/submitfeedback The dashboard loads very slowly
/submitfeedback Login button doesn't work on mobile
/submitfeedback Love the new search feature!
```

**What happens:**
- Feedback is stored in the database
- Categorized as "user_report"
- Severity set to "medium" by default
- Feedback team will cluster with similar reports

**Response:**
```
✅ Feedback Submitted!

📝 The dashboard loads very slowly

The feedback team will analyze and cluster this
with similar reports. Thank you for helping us improve!
```

---

### **2. `/clusterfeedback` 🎯**
**Cluster feedback into themes**

```
/clusterfeedback
```

**What happens:**
- Analyzes all "new" feedback reports at one place
- Groups by similarity (Performance, Crashes, Memory Leaks, UI/UX, etc.)
- Creates clusters with themes
- Performs root cause analysis
- Links granular bugs to broader categories

**Response:**
```
🎯 Clustering Feedback...

Analyzing feedback reports and grouping by theme...
This may take a moment.

[Then shows clusters created with themes]
```

**Example Result:**
```
Created 3 clusters:

1. Performance Issues (15 reports)
   - Root cause: Database query optimization needed

2. Mobile UI Problems (8 reports)
   - Root cause: Responsive design issues

3. Login Errors (5 reports)
   - Root cause: Session timeout handling
```

---

### **3. `/trackbugs` 🐛**
**Create and track bugs**

```
/trackbugs
```

**What happens:**
- Creates bugs from feedback clusters
- Posts updates on existing bugs when new reports arrive
- Calculates severity automatically (based on feedback count)
- Links bugs to clusters

**Response:**
```
🐛 Tracking Bugs...

Creating and updating bug reports from feedback clusters...

Created 3 new bugs:
- Bug #1: Dashboard Performance (Critical)
- Bug #2: Mobile UI Issues (High)
- Bug #3: Login Timeout (Medium)

Updated 2 existing bugs with new reports.
```

---

### **4. `/generatesolutions` 💡**
**Generate PRDs and solutions**

```
/generatesolutions
```

**What happens:**
- Analyzes all open bugs
- Generates Product Requirement Documents (PRDs)
- Creates coding agent prompts
- Analyzes trade-offs
- Estimates effort

**Response:**
```
💡 Generating Solutions...

Creating PRDs, prototypes, and coding prompts for bugs...
This will include trade-offs and effort estimates.

Generated 3 solutions:

Solution #1: Database Query Optimization
- PRD: Add composite index, implement caching
- Coding prompt: "Create migration for index..."
- Effort: 2 weeks, 1 engineer
- Trade-offs: Fast fix vs. full refactor

[... more solutions ...]
```

---

### **5. `/feedbackreport` 📊**
**Analytics report**

```
/feedbackreport
```

**What happens:**
- System-wide metrics
- Top issues by feedback count
- Trend analysis
- Bug and solution statistics

**Response:**
```
📊 Feedback Report

Total Feedback: 50 reports
- New: 10
- Clustered: 20
- Enriched: 15
- Resolved: 5

Active Clusters: 8
Open Bugs: 5
Proposed Solutions: 3

Top Issues:
1. Performance (15 reports) - Critical
2. Mobile UI (8 reports) - High
3. Login Errors (5 reports) - Medium

Trends:
- 5 new reports per day (avg)
- 3 bugs resolved per day
- Avg time to cluster: 2 hours
```

---

## 🚀 **Complete Workflow**

### **For End Users (Submitting Feedback):**

```
1. Open Telegram
2. Message your Agency bot
3. Type: /submitfeedback [your feedback]
4. Get confirmation
```

**Example:**
```
You: /submitfeedback App crashes when I upload photos
Bot: ✅ Feedback Submitted! The feedback team will analyze...
```

---

### **For Product/Engineering Teams (Managing Feedback):**

#### **Morning Routine:**

```
1. /feedbackreport
   → See overnight feedback

2. /clusterfeedback
   → Group new feedback

3. /trackbugs
   → Create/update bugs
```

#### **Sprint Planning:**

```
1. /feedbackreport
   → Review top issues

2. /generatesolutions
   → Get PRDs for bugs

3. Review solutions
   → Prioritize for sprint
```

#### **Weekly Review:**

```
1. /feedbackreport
   → See trends

2. /clusterfeedback
   → Re-cluster if needed

3. /trackbugs
   → Update bug status
```

---

## 💡 **Usage Scenarios**

### **Scenario 1: User Reports Bug**

```
User: /submitfeedback Can't save my profile, keeps erroring

Bot: ✅ Feedback Submitted!
```

**Behind the scenes:**
- Stored in `~/.agency/feedback/feedback_reports.json`
- Status: "new"
- Ready to be clustered

---

### **Scenario 2: Daily Feedback Processing**

```
PM: /clusterfeedback

Bot: 🎯 Clustering Feedback...
     Created 2 clusters from 12 reports

PM: /trackbugs

Bot: 🐛 Tracking Bugs...
     Created 2 bugs, updated 1

PM: /generatesolutions

Bot: 💡 Generating Solutions...
     Generated 2 solutions with PRDs
```

---

### **Scenario 3: Sprint Planning**

```
PM: /feedbackreport

Bot: 📊 Top Issues:
     1. Profile Save Error (10 reports) - Critical
     2. Slow Dashboard (8 reports) - High
     3. UI Glitch (3 reports) - Low

PM: Reviews PRDs from /generatesolutions
Team: Prioritizes Critical bug for sprint
```

---

## 🎨 **Telegram Menu**

All commands appear in the Telegram command menu:

```
📋 Feedback Management
  📝 /submitfeedback - Submit user feedback
  🎯 /clusterfeedback - Cluster by theme
  🐛 /trackbugs - Track bugs
  💡 /generatesolutions - Generate solutions
  📊 /feedbackreport - Analytics report
```

---

## 🔧 **Advanced Usage**

### **Detailed Feedback Submission:**

```
/submitfeedback [Category: bug] [Severity: critical] The app crashes on login every time. I've tried 5 times. Using Chrome on Mac.
```

**More context = better analysis!**

---

### **Combining with Agent Mentions:**

```
@feedback_team Cluster all feedback from the past week,
create bugs for critical issues, and generate solutions
for the top 3 bugs. Format as a sprint planning report.
```

---

### **Quick Status Check:**

```
/feedbackreport
```

**Get instant overview of:**
- Total feedback count
- Pending vs. resolved
- Top issues
- Trends

---

## 📊 **Dashboard View**

After running commands, you can see results in:

1. **Telegram** - Immediate responses
2. **Web UI** - `http://localhost:3000/team.html`
3. **Files** - `~/.agency/feedback/*.json`

---

## 🎯 **Best Practices**

### **For Users:**

✅ **Be specific** - "Dashboard loads slowly" is better than "App is slow"
✅ **Include context** - Browser, device, when it happens
✅ **One issue per submission** - Don't combine multiple bugs

### **For Admins:**

✅ **Run /clusterfeedback daily** - Keep feedback organized
✅ **Use /trackbugs regularly** - Stay on top of issues
✅ **Review /feedbackreport weekly** - Monitor trends
✅ **Generate solutions early** - Plan fixes proactively

---

## 🚦 **Workflow Timing**

| Command | Frequency | When |
|---------|-----------|------|
| `/submitfeedback` | As needed | Users submit anytime |
| `/clusterfeedback` | Daily | Morning routine |
| `/trackbugs` | Daily | After clustering |
| `/generatesolutions` | Weekly | Sprint planning |
| `/feedbackreport` | Daily/Weekly | Morning or review |

---

## 🎁 **What You Get**

✅ **5 Telegram commands** - Easy access
✅ **Instant feedback** - Bot confirms actions
✅ **Automatic processing** - Skills run in background
✅ **Real results** - Clusters, bugs, PRDs created
✅ **Analytics** - Track metrics and trends
✅ **Team coordination** - Multi-agent workflows
✅ **Persistent storage** - All data saved

---

## 🚀 **Quick Start**

### **Step 1: Start Your Bot**

```bash
cd ~/claude-code/github/agents
git pull
./start_agency.sh
```

### **Step 2: Open Telegram**

Find your Agency bot

### **Step 3: Try Commands**

```
/help                                 ← See all commands
/submitfeedback Test feedback        ← Submit test
/feedbackreport                       ← See stats
```

---

## 📱 **Command Cheat Sheet**

```
Quick Submit:
/submitfeedback App is slow

Morning Routine:
/feedbackreport
/clusterfeedback
/trackbugs

Sprint Planning:
/feedbackreport
/generatesolutions

Anytime Status:
/feedbackreport
```

---

## 🎊 **All Set!**

Your Telegram bot now has complete feedback management:

✅ **Submit** - `/submitfeedback`
✅ **Cluster** - `/clusterfeedback`
✅ **Track** - `/trackbugs`
✅ **Solve** - `/generatesolutions`
✅ **Report** - `/feedbackreport`

**Try it now on Telegram!** 📱

---

## 💬 **Example Conversation**

```
You: /submitfeedback Login button not working

Bot: ✅ Feedback Submitted!
     📝 Login button not working
     The feedback team will analyze and cluster this
     with similar reports. Thank you!

---

You: /clusterfeedback

Bot: 🎯 Clustering Feedback...
     Analyzing feedback reports and grouping by theme...

     Created 1 cluster:
     • Authentication Issues (3 reports)
       Root cause: Session validation logic

---

You: /trackbugs

Bot: 🐛 Tracking Bugs...
     Created 1 bug:
     • Bug #42: Login Authentication Fix (High)
       Linked to 3 feedback reports

---

You: /generatesolutions

Bot: 💡 Generating Solutions...

     Solution for Bug #42:
     PRD: Fix session validation, add retry logic
     Coding Prompt: "Update auth middleware to..."
     Effort: 3-5 days

---

You: /feedbackreport

Bot: 📊 Feedback Report
     Total: 15 reports
     Open Bugs: 3
     Top Issue: Authentication (3 reports)
```

**Perfect workflow!** 🎉
