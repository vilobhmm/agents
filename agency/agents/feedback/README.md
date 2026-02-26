# 📋 Feedback Management Multi-Agent Team

A complete system for managing user feedback at scale, from collection to solution.

---

## 🎯 **What It Does**

Based on your handwritten design, this system provides **4 core capabilities**:

### 1. **Clustering** 🎯
- Takes all user feedback reports
- Groups them into high-level themes
- Links granular bugs to broader categories
- Performs root cause analysis

### 2. **Feedback Enrichment** 🔍
- Analyzes user logs & conversation history
- Identifies root cause of each report
- Adds technical context and reproduction steps
- Correlates user actions with system behavior

### 3. **Updates** 🐛
- Posts updates on existing bugs when new related reports arrive
- Tracks if issues are still occurring or resolved
- Monitors bug lifecycle and status
- Alerts stakeholders on changes

### 4. **Solutioning** 💡
- Generates all possible solution options
- Creates Product Requirement Documents (PRDs)
- Designs prototypes
- Writes detailed coding agent prompts

---

## 🤖 **The Team**

### **feedback_coordinator** (Leader)
Orchestrates the entire feedback lifecycle and delegates to specialists.

**Skills:**
- Coordinate multi-agent workflows
- Prioritize feedback for action
- Synthesize insights from clustering and enrichment
- Track feedback resolution metrics

### **feedback_analyst**
Clusters feedback reports into themes.

**Skills:**
- Cluster by similarity and theme
- Identify patterns across feedback
- Link granular bugs to broader categories
- Perform root cause analysis

### **log_investigator**
Enriches feedback with technical context.

**Skills:**
- Analyze user logs
- Parse conversation history
- Correlate feedback with system traces
- Find reproduction steps from logs

### **bug_tracker**
Manages bug lifecycle and updates.

**Skills:**
- Track bugs across lifecycle
- Post updates when new related reports arrive
- Monitor if issues are resolved or recurring
- Link related bug reports automatically

### **solution_architect**
Generates comprehensive solutions.

**Skills:**
- Generate solution options
- Write PRDs (Product Requirement Documents)
- Create design prototypes
- Draft coding agent prompts
- Evaluate trade-offs

---

## 🛠️ **Tools Available**

### **Feedback Collection**
```python
submit_feedback(user_id, feedback_text, category, severity)
get_feedback_reports(status, category, severity)
update_feedback_status(feedback_id, status)
```

### **Clustering**
```python
create_cluster(theme, description, feedback_ids, root_cause)
get_clusters(status)
add_feedback_to_cluster(cluster_id, feedback_ids)
```

### **Enrichment**
```python
enrich_feedback(feedback_id, logs, conversation_history, reproduction_steps, root_cause)
save_user_logs(user_id, session_id, logs)
get_user_logs(user_id, session_id)
```

### **Bug Tracking**
```python
create_bug(title, description, severity, cluster_id, feedback_ids)
post_bug_update(bug_id, update_text, new_feedback_ids)
update_bug_status(bug_id, status)
get_bugs(status, severity)
```

### **Solutioning**
```python
create_solution(bug_id, title, approach, prd, prototype, coding_prompt)
get_solutions(bug_id, status)
update_solution_status(solution_id, status)
```

### **Analytics**
```python
get_feedback_analytics()  # System-wide metrics
```

---

## 📁 **Data Storage**

All feedback data is stored in:

```
~/.agency/feedback/
├── feedback_reports.json  ← All user feedback
├── clusters.json          ← Themes and groupings
├── bugs.json              ← Bug tracking database
├── solutions.json         ← PRDs and solution options
└── logs/                  ← User logs by session
    ├── user123_session_abc.log
    └── user456_session_xyz.log
```

---

## 🚀 **How to Use**

### **Via Telegram/Web UI:**

```
@feedback_team We have 50 user reports about slow load times.
Cluster them into themes, find root causes in logs,
track as bugs, and generate solution options with PRDs.
```

The coordinator will:
1. Ask **feedback_analyst** to cluster reports by theme
2. Ask **log_investigator** to enrich with logs and root cause
3. Ask **bug_tracker** to create/update bugs
4. Ask **solution_architect** to generate solutions with PRDs

---

## 📊 **Example Workflow**

### **Step 1: Users Submit Feedback**
```
User A: "Page takes 10+ seconds to load"
User B: "Dashboard is very slow, times out"
User C: "Load time is terrible"
```

### **Step 2: Analyst Clusters**
```
Cluster: "Performance - Slow Load Times"
Theme: Users experiencing 10+ second load times
Linked feedback: 3 reports
Root cause hypothesis: Database query or bundle size
```

### **Step 3: Investigator Enriches**
```
Analyzed logs for User A:
- Database query took 8.5s
- Full table scan on 10M+ rows
- Request timeout after 10s

Root cause: Unoptimized analytics query
```

### **Step 4: Tracker Creates Bug**
```
Bug: "Dashboard timeout - Database optimization needed"
Severity: Critical
Linked feedback: 3 reports
Status: Open
Assignee: backend-team
```

### **Step 5: Architect Generates Solutions**

```
Solution 1: Database Indexing + Caching
PRD:
  - Add composite index on analytics table
  - Implement Redis caching
  - Add pagination

Timeline: 2 weeks
Effort: 1 engineer

Coding Prompt:
  "Create database migration for composite index.
   Implement Redis caching with 1-hour TTL.
   Add pagination to API endpoint..."

Trade-offs:
  Pros: Fast, proven approach
  Cons: Redis adds complexity

Alternative: Move to separate analytics service (longer timeline)
```

### **Step 6: New Report Arrives**
```
User D: "Still seeing slow loads after latest update"

→ Tracker posts update:
  "New report indicates issue still occurring.
   Linked to existing bug #123.
   Total feedback: 4 reports"
```

---

## 🎨 **Web UI Integration**

The feedback team shows up in:

- **Team Gallery** (`/team.html`)
- **Control Center** (`/`)

Click the **feedback_team** card to:
- View team members
- Start a conversation
- See agent capabilities

---

## 📈 **Analytics Dashboard**

Get system-wide metrics:

```python
from agency.tools.feedback_tools import get_feedback_analytics

analytics = get_feedback_analytics()
# Returns:
{
  "total_feedback": 50,
  "by_status": {
    "new": 10,
    "clustered": 20,
    "enriched": 15,
    "resolved": 5
  },
  "total_clusters": 8,
  "total_bugs": 5,
  "total_solutions": 3,
  ...
}
```

---

## 💡 **Use Cases**

### **Product Teams**
- Manage user feedback at scale
- Identify patterns and trends
- Prioritize bug fixes
- Track resolution progress

### **Engineering Teams**
- Get detailed reproduction steps
- Access user logs and context
- Receive coding prompts for fixes
- Evaluate solution trade-offs

### **Support Teams**
- Track duplicate reports
- Post updates to users
- Monitor bug status
- See which issues are resolved

### **Leadership**
- View feedback analytics
- Understand user pain points
- Track team velocity on fixes
- Make data-driven decisions

---

## 🔄 **Complete Lifecycle**

```
Feedback Submitted
       ↓
   Clustered (by theme)
       ↓
   Enriched (with logs/root cause)
       ↓
   Bug Created
       ↓
   Solution Generated (PRD + coding prompt)
       ↓
   Implemented
       ↓
   Verified & Closed
       ↓
   (New reports trigger updates)
```

---

## 🧪 **Demo Script**

Run the included demo to see the full workflow:

```bash
cd ~/claude-code/github/agents

# The demo creates:
# - 4 feedback reports
# - 1 cluster (Performance theme)
# - Enrichment with logs
# - 1 bug with update
# - 1 solution with PRD

python examples/feedback_management_demo.py
```

---

## 🎯 **Key Features**

✅ **Automatic Clustering** - AI groups similar feedback
✅ **Log Analysis** - Enriches with technical context
✅ **Root Cause** - Identifies underlying issues
✅ **Bug Tracking** - Lifecycle management
✅ **Solution Generation** - PRDs, prototypes, code prompts
✅ **Update Notifications** - Alerts on new related reports
✅ **Analytics** - System-wide metrics
✅ **Storage** - Persistent JSON database
✅ **Multi-Agent** - Specialized agents for each phase
✅ **Scalable** - Handles thousands of reports

---

## 📞 **Quick Start**

### **1. Pull Latest Code**
```bash
cd ~/claude-code/github/agents
git pull origin claude/openclaw-weekend-projects-st5pW
```

### **2. Submit Feedback**
```python
from agency.tools.feedback_tools import submit_feedback

feedback = submit_feedback(
    user_id="john@example.com",
    feedback_text="Login button doesn't work on mobile",
    category="bug",
    severity="high"
)
```

### **3. Or Use Via Agent**
```
@feedback_team Analyze all feedback from the past week and
generate solutions for the top 3 issues
```

---

## 🎊 **What You Get**

- ✅ **5 specialized agents** for feedback management
- ✅ **Complete tool library** (15+ functions)
- ✅ **Persistent storage** (~/.agency/feedback/)
- ✅ **Analytics dashboard**
- ✅ **Demo script** with examples
- ✅ **Web UI integration**
- ✅ **Production-ready** code

---

## 🚀 **Ready to Use!**

The feedback team is now available in your agency. Just send:

```
@feedback_team Help me manage user feedback
```

And watch the magic happen! 🎉
