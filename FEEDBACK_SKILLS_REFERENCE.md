# 🎯 Feedback Management Skills - Quick Reference

Executable skill commands for feedback management.

---

## 📋 **Available Skills**

### 1. `/cluster-feedback` 🎯
**Groups feedback into themes**

```python
from agency.agents.feedback_skills import FeedbackSkills

skills = FeedbackSkills()
result = await skills.cluster_feedback(
    status="new",           # Feedback status to cluster
    min_cluster_size=2      # Minimum items per cluster
)

# Returns:
{
    "status": "success",
    "clusters_created": 3,
    "total_feedback": 15,
    "clusters": [
        {
            "theme": "Performance Issues",
            "feedback_ids": ["id1", "id2", "id3"],
            "root_cause": "..."
        }
    ]
}
```

**What it does:**
- Analyzes feedback with specified status
- Groups by similarity and theme
- Creates clusters with root cause analysis
- Links granular bugs to broader categories

---

### 2. `/enrich-feedback` 🔍
**Enriches feedback with logs and context**

```python
result = await skills.enrich_feedback_batch(
    feedback_ids=None,      # Specific IDs or None for all
    auto_analyze=True       # Auto root cause analysis
)

# Returns:
{
    "status": "success",
    "enriched_count": 10,
    "feedback_ids": ["id1", "id2", ...],
    "message": "Enriched 10 feedback items with logs and root cause"
}
```

**What it does:**
- Analyzes user logs for each feedback
- Extracts conversation history
- Identifies root causes
- Adds reproduction steps

---

### 3. `/track-bugs` 🐛
**Creates and updates bugs**

```python
result = await skills.track_bugs(
    auto_create=True,            # Auto-create bugs from clusters
    min_feedback_per_bug=2       # Minimum feedback to create bug
)

# Returns:
{
    "status": "success",
    "bugs_created": 5,
    "bugs_updated": 3,
    "created_bug_ids": ["bug1", "bug2", ...],
    "updated_bug_ids": ["bug3", "bug4", ...]
}
```

**What it does:**
- Creates bugs from feedback clusters
- Posts updates when new related feedback arrives
- Tracks bug lifecycle (open → in_progress → resolved)
- Calculates severity based on feedback count

---

### 4. `/generate-solutions` 💡
**Generates PRDs, prototypes, and coding prompts**

```python
result = await skills.generate_solutions(
    bug_ids=None,               # Specific bugs or None for all open
    include_prd=True,           # Generate PRD
    include_prototype=False,    # Generate prototype
    include_coding_prompt=True  # Generate coding prompt
)

# Returns:
{
    "status": "success",
    "solutions_created": 5,
    "solution_ids": ["sol1", "sol2", ...],
    "components": {
        "prd": True,
        "prototype": False,
        "coding_prompt": True
    }
}
```

**What it does:**
- Generates Product Requirement Documents (PRDs)
- Creates design prototypes (if requested)
- Writes detailed coding agent prompts
- Analyzes trade-offs and estimates effort

---

### 5. `/feedback-report` 📊
**Generates analytics report**

```python
result = await skills.feedback_report(
    include_trends=True,        # Include trend analysis
    include_top_issues=True,    # Include top issues
    top_n=5                     # Number of top issues
)

# Returns:
{
    "status": "success",
    "analytics": {
        "total_feedback": 50,
        "by_status": {...},
        "total_clusters": 8,
        "total_bugs": 5
    },
    "top_issues": [
        {
            "theme": "Performance Issues",
            "feedback_count": 15,
            "description": "..."
        }
    ],
    "trends": {...}
}
```

**What it does:**
- System-wide analytics
- Top issues by feedback count
- Trend analysis
- Resolution metrics

---

## 🚀 **Usage Examples**

### **Example 1: Full Workflow**

```python
from agency.agents.feedback_skills import FeedbackSkills
import asyncio

async def process_feedback():
    skills = FeedbackSkills()

    # Step 1: Cluster new feedback
    print("Clustering feedback...")
    clusters = await skills.cluster_feedback(status="new")
    print(f"✓ Created {clusters['clusters_created']} clusters")

    # Step 2: Enrich with logs
    print("Enriching feedback...")
    enriched = await skills.enrich_feedback_batch(auto_analyze=True)
    print(f"✓ Enriched {enriched['enriched_count']} items")

    # Step 3: Track bugs
    print("Tracking bugs...")
    bugs = await skills.track_bugs(auto_create=True)
    print(f"✓ Created {bugs['bugs_created']} bugs, updated {bugs['bugs_updated']}")

    # Step 4: Generate solutions
    print("Generating solutions...")
    solutions = await skills.generate_solutions(
        include_prd=True,
        include_coding_prompt=True
    )
    print(f"✓ Generated {solutions['solutions_created']} solutions")

    # Step 5: Get report
    print("Generating report...")
    report = await skills.feedback_report()
    print(f"✓ Report: {report['analytics']['total_feedback']} total feedback")

asyncio.run(process_feedback())
```

### **Example 2: Quick Clustering**

```python
async def quick_cluster():
    skills = FeedbackSkills()
    result = await skills.cluster_feedback()

    for cluster in result.get('clusters', []):
        print(f"Theme: {cluster['theme']}")
        print(f"  Items: {len(cluster['feedback_ids'])}")
        print(f"  Root cause: {cluster['root_cause']}\n")

asyncio.run(quick_cluster())
```

### **Example 3: Generate Solutions for Critical Bugs**

```python
async def solve_critical_bugs():
    skills = FeedbackSkills()

    # Get critical bugs
    from agency.tools.feedback_tools import get_bugs
    critical_bugs = get_bugs(severity="critical")
    critical_ids = [b['id'] for b in critical_bugs]

    # Generate solutions
    result = await skills.generate_solutions(
        bug_ids=critical_ids,
        include_prd=True,
        include_prototype=True,
        include_coding_prompt=True
    )

    print(f"Generated {result['solutions_created']} solutions for critical bugs")

asyncio.run(solve_critical_bugs())
```

---

## 🎨 **Integration with Agents**

### **Via Telegram/Web:**

```
@feedback_team Run cluster-feedback skill
```

### **Via Code:**

```python
from agency.agents.feedback_skills import FeedbackSkills

skills = FeedbackSkills()

# Use skills
await skills.cluster_feedback()
await skills.enrich_feedback_batch()
await skills.track_bugs()
await skills.generate_solutions()
await skills.feedback_report()
```

---

## 📊 **Skill Results**

All skills return a standardized result format:

```python
{
    "status": "success" | "error" | "insufficient_data",
    "timestamp": "2024-02-19T10:30:00Z",
    "message": "Human-readable message",
    # ... skill-specific data ...
}
```

**Status codes:**
- `"success"` - Skill executed successfully
- `"error"` - Error occurred (see `error` field)
- `"insufficient_data"` - Not enough data to execute

---

## 🔧 **Customization**

### **Custom Clustering Logic:**

```python
class CustomFeedbackSkills(FeedbackSkills):
    def _identify_themes(self, feedback):
        # Your custom clustering logic
        # Could use embeddings, LLM, or ML models
        pass
```

### **Custom Root Cause Analysis:**

```python
class CustomFeedbackSkills(FeedbackSkills):
    def _analyze_root_cause(self, feedback):
        # Use LLM to analyze root cause
        # Or integrate with your log analysis system
        pass
```

---

## 🎯 **When to Use Each Skill**

| Skill | When to Use |
|-------|-------------|
| **cluster-feedback** | Have new feedback that needs grouping |
| **enrich-feedback** | Need technical context and root cause |
| **track-bugs** | Ready to create/update bug reports |
| **generate-solutions** | Need PRDs or coding prompts for fixes |
| **feedback-report** | Want analytics and top issues |

---

## 💡 **Tips**

1. **Run cluster-feedback regularly** (e.g., daily) to group new feedback
2. **Enrich before creating bugs** to have full context
3. **Use auto_create=True** for automatic bug creation
4. **Generate solutions early** to start planning fixes
5. **Check feedback-report** for trends and priorities

---

## ⚡ **Quick Commands**

```bash
# Run full workflow
python -c "from agency.agents.feedback_skills import FeedbackSkills; import asyncio; skills = FeedbackSkills(); asyncio.run(skills.cluster_feedback())"

# Get analytics
python -c "from agency.agents.feedback_skills import FeedbackSkills; import asyncio; skills = FeedbackSkills(); print(asyncio.run(skills.feedback_report()))"
```

---

## 🎊 **All Skills Available!**

✅ `/cluster-feedback` - Group by theme
✅ `/enrich-feedback` - Add logs & root cause
✅ `/track-bugs` - Create/update bugs
✅ `/generate-solutions` - PRDs & coding prompts
✅ `/feedback-report` - Analytics & trends

**Ready to use!** 🚀
