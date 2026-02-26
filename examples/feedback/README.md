# 📋 Feedback Management Examples

**End-to-end demos of feedback collection, clustering, and solution generation**

---

## 📁 Contents

1. **[e2e_feedback_github_demo.py](./e2e_feedback_github_demo.py)** - Full E2E demo with real GitHub issues
2. **[feedback_management_demo.py](./feedback_management_demo.py)** - Basic feedback workflow

---

## 🚀 E2E GitHub Feedback Demo

### Overview

**File:** `e2e_feedback_github_demo.py`

A complete end-to-end demonstration that:
- Fetches **real issues** from `vercel/next.js` GitHub repository
- Uses **Claude AI** to analyze and cluster feedback
- Tracks bugs and generates comprehensive solutions
- Produces analytics and insights

This mirrors the real Telegram workflow (`/submitfeedback`, `/clusterfeedback`, etc.) but runs standalone.

---

### Features

✅ **Real data** - Uses actual GitHub issues (no mocks)
✅ **Claude AI powered** - Every step uses Claude for intelligent analysis
✅ **Complete workflow** - From feedback submission to solution generation
✅ **Production-ready** - Same tools used in production Telegram agents
✅ **Analytics** - Comprehensive reporting and insights

---

### Workflow

```
1. Submit Feedback
   ↓
   Fetches 15 real GitHub issues
   Stores as feedback in database

2. Cluster Feedback (Claude AI)
   ↓
   Claude analyzes all feedback
   Creates 3-5 thematic clusters
   Performs root cause analysis

3. Track Bugs
   ↓
   Creates tracked bugs from clusters
   Links related feedback items
   Sets priority and severity

4. Generate Solutions (Claude AI)
   ↓
   Claude generates comprehensive solutions
   Creates PRDs and design docs
   Writes coding agent prompts

5. Analytics Dashboard
   ↓
   Shows metrics and insights
   Cluster distribution
   Bug lifecycle tracking
```

---

### Quick Start

```bash
# From project root
cd /home/user/agents

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run the demo
python examples/feedback/e2e_feedback_github_demo.py
```

**No GitHub token needed!** Uses public API.

---

### Configuration

Edit the config section in the file:

```python
# examples/feedback/e2e_feedback_github_demo.py

GITHUB_REPO   = "vercel/next.js"  # Change repo here
ISSUES_LIMIT  = 15                # Number of issues to fetch
CLAUDE_MODEL  = "claude-haiku-4-5-20251001"  # Claude model
```

Try other repos:
- `"facebook/react"`
- `"microsoft/vscode"`
- `"python/cpython"`
- Any public GitHub repo!

---

### Expected Output

```
═══════════════════════════════════════════════════════════════════
  🚀  E2E Feedback Management Demo — Real GitHub Issues + Claude AI
═══════════════════════════════════════════════════════════════════

▶ Step 1: Fetch real GitHub issues as feedback

  → Fetching 15 issues from vercel/next.js...
  ✓ Fetched 15 issues from GitHub API
  ✓ Submitted 15 feedback reports to database

  Top feedback items:
    • Build performance degradation in dev mode
    • TypeScript types not working with App Router
    • Image component causing layout shift
    ...

═══════════════════════════════════════════════════════════════════
  🎯  STEP 2: CLUSTER FEEDBACK
═══════════════════════════════════════════════════════════════════

▶ Claude is analyzing feedback and creating clusters...

  → Analyzing 15 feedback items with Claude AI...
  → Identifying themes and patterns...
  → Performing root cause analysis...
  ✓ Created 4 thematic clusters

  📊 Clusters Summary
  ──────────────────────────────────────────────────────────────

  Cluster 1: Build Performance Issues (5 items)
    Theme: Build process is slow and consuming excessive resources
    Root Cause: Webpack configuration not optimized for dev mode
    Severity: High

  Cluster 2: TypeScript Integration Problems (6 items)
    Theme: Type errors and inference issues with App Router
    Root Cause: Type definitions out of sync with runtime behavior
    Severity: Medium

  Cluster 3: Image Component Bugs (2 items)
    Theme: Layout shifts and loading issues
    Root Cause: Lazy loading race condition
    Severity: High

  Cluster 4: Routing Edge Cases (2 items)
    Theme: Unexpected behavior with dynamic routes
    Root Cause: Route matching algorithm edge cases
    Severity: Low

═══════════════════════════════════════════════════════════════════
  🐛  STEP 3: TRACK BUGS
═══════════════════════════════════════════════════════════════════

▶ Creating tracked bugs from clusters...

  ✓ Created 4 tracked bugs

  Bug #1: Build Performance Issues
    Priority: High | Status: open
    Related Feedback: 5 items
    Created: 2026-02-26 10:30:15

  Bug #2: TypeScript Integration Problems
    Priority: Medium | Status: open
    Related Feedback: 6 items
    Created: 2026-02-26 10:30:16

  ...

═══════════════════════════════════════════════════════════════════
  💡  STEP 4: GENERATE SOLUTIONS
═══════════════════════════════════════════════════════════════════

▶ Claude is generating comprehensive solutions...

  → Generating solution for Bug #1: Build Performance Issues
  ✓ Solution created (with PRD + coding prompt)

  Solution Summary:
  ──────────────────────────────────────────────────────────────

  **Proposed Solutions:**

  Option 1: Optimize Webpack Configuration (Recommended)
    - Update webpack config for dev mode
    - Enable caching and incremental builds
    - Estimated effort: 2-3 days
    - Impact: 50-70% build time reduction

  Option 2: Switch to Turbopack
    - Migrate build pipeline to Turbopack
    - Requires beta testing
    - Estimated effort: 1-2 weeks
    - Impact: 90% build time reduction

  Option 3: Implement Build Workers
    - Parallelize build tasks
    - Add worker pool management
    - Estimated effort: 1 week
    - Impact: 30-40% build time reduction

  **PRD:**
  [Generated 2-page Product Requirements Document]

  **Coding Prompt:**
  [Detailed step-by-step prompt for coding agent]

═══════════════════════════════════════════════════════════════════
  📊  STEP 5: ANALYTICS DASHBOARD
═══════════════════════════════════════════════════════════════════

  Overall Statistics
  ──────────────────────────────────────────────────────────────

  Total Feedback: 15
  Total Clusters: 4
  Total Bugs: 4
  Solutions Generated: 4

  Feedback by Category:
    • bug: 12 (80%)
    • feature: 2 (13%)
    • question: 1 (7%)

  Feedback by Severity:
    • high: 7 (47%)
    • medium: 6 (40%)
    • low: 2 (13%)

  Cluster Distribution:
    • Build Performance: 5 items (33%)
    • TypeScript Issues: 6 items (40%)
    • Image Component: 2 items (13%)
    • Routing: 2 items (13%)

  Bug Status:
    • open: 4 (100%)
    • in_progress: 0
    • resolved: 0

═══════════════════════════════════════════════════════════════════
  ✅  DEMO COMPLETE
═══════════════════════════════════════════════════════════════════

  📁 Data saved to:
    • feedback.db - All feedback items
    • clusters.db - Feedback clusters
    • bugs.db - Tracked bugs
    • solutions.db - Generated solutions

  🎯 Next steps:
    1. Review the generated solutions
    2. Implement fixes using coding prompts
    3. Run /feedbackreport for updated analytics
    4. Try with your own GitHub repo!

  🚀 Try the Telegram bot for interactive workflow:
    /submitfeedback - Submit new feedback
    /clusterfeedback - Re-cluster all feedback
    /trackbugs - Track new bugs
    /generatesolutions - Generate new solutions
    /feedbackreport - View analytics
```

---

## 🛠️ Feedback Management Demo

### Overview

**File:** `feedback_management_demo.py`

A simpler demo showing basic feedback operations:
- Direct tool usage
- Manual clustering
- Basic bug tracking

---

### Quick Start

```bash
python examples/feedback/feedback_management_demo.py
```

---

### What It Shows

- How to use feedback tools directly
- Submitting and retrieving feedback
- Creating clusters manually
- Tracking bugs
- Generating reports

---

## 🔧 Customization

### Use Your Own Data

#### Option 1: Different GitHub Repo

```python
# Edit e2e_feedback_github_demo.py
GITHUB_REPO = "facebook/react"  # Your repo here
```

#### Option 2: Custom Feedback

```python
# In feedback_management_demo.py
from agency.tools.feedback_tools import submit_feedback

feedback_items = [
    {"user_id": "user1", "text": "Login button not working", "category": "bug"},
    {"user_id": "user2", "text": "Need dark mode", "category": "feature"},
    # ... your feedback
]

for item in feedback_items:
    submit_feedback(**item)
```

---

### Adjust Claude Behavior

Edit prompts in `agency/tools/feedback_tools.py`:

```python
# Clustering prompt
CLUSTER_PROMPT = """
Analyze feedback and group into themes.
Focus on: [your focus areas]
Consider: [your criteria]
"""

# Solution generation prompt
SOLUTION_PROMPT = """
Generate solutions that prioritize: [your priorities]
Format: [your format]
"""
```

---

## 📊 Data Storage

All data is stored in SQLite databases:

```
feedback.db    - Raw feedback items
clusters.db    - Feedback clusters
bugs.db        - Tracked bugs
solutions.db   - Generated solutions
```

### Inspect Data

```bash
# View feedback
sqlite3 feedback.db "SELECT * FROM feedback;"

# View clusters
sqlite3 clusters.db "SELECT * FROM clusters;"

# View bugs
sqlite3 bugs.db "SELECT * FROM bugs;"
```

---

## 🐛 Troubleshooting

### Claude API Errors

```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Try with explicit key
ANTHROPIC_API_KEY=sk-ant-... python examples/feedback/e2e_feedback_github_demo.py
```

### GitHub Rate Limits

```bash
# Use personal access token for higher limits
export GITHUB_TOKEN=ghp_...

# Or reduce ISSUES_LIMIT
ISSUES_LIMIT = 5  # Fetch fewer issues
```

### Import Errors

```bash
# Run from project root
cd /home/user/agents
python examples/feedback/e2e_feedback_github_demo.py
```

---

## 📚 Learn More

- **[Feedback Agent Guide](../../agency/agents/feedback/README.md)** - Complete documentation
- **[Feedback Tools](../../agency/tools/feedback_tools.py)** - Tool implementation
- **[Telegram Integration](../../TELEGRAM_FEEDBACK_GUIDE.md)** - Use via Telegram

---

## 💡 Use Cases

### Product Teams
- Analyze user feedback at scale
- Identify common pain points
- Prioritize feature requests
- Track bug lifecycle

### Customer Support
- Cluster support tickets
- Identify recurring issues
- Generate solution templates
- Track resolution metrics

### Engineering Teams
- Automate bug tracking
- Generate technical specs from user reports
- Link related issues
- Monitor bug trends

---

**Transform feedback into actionable insights!** 🚀
