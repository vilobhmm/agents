#!/usr/bin/env python3
"""
Feedback Management System Demo

Demonstrates the complete feedback management workflow:
1. Collecting user feedback
2. Clustering by theme
3. Enriching with logs
4. Creating bugs
5. Generating solutions
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agency.tools.feedback_tools import (
    # Collection
    submit_feedback,
    get_feedback_reports,

    # Clustering
    create_cluster,
    get_clusters,
    add_feedback_to_cluster,

    # Enrichment
    enrich_feedback,
    save_user_logs,

    # Bug Tracking
    create_bug,
    post_bug_update,
    update_bug_status,
    get_bugs,

    # Solutioning
    create_solution,
    get_solutions,

    # Analytics
    get_feedback_analytics,
)


def demo():
    print("=" * 70)
    print("FEEDBACK MANAGEMENT SYSTEM DEMO")
    print("=" * 70)
    print()

    # ─── Step 1: Collect Feedback ─────────────────────────────────
    print("📥 Step 1: Collecting user feedback...")
    print("-" * 70)

    feedback1 = submit_feedback(
        user_id="user123",
        feedback_text="Page takes 10+ seconds to load, completely unusable",
        category="bug",
        severity="high",
        metadata={"browser": "Chrome", "version": "1.2.3"}
    )
    print(f"✓ Submitted feedback: {feedback1['id'][:8]}... - {feedback1['feedback_text'][:50]}...")

    feedback2 = submit_feedback(
        user_id="user456",
        feedback_text="Dashboard is very slow, times out often",
        category="bug",
        severity="high",
        metadata={"browser": "Firefox", "version": "1.2.3"}
    )
    print(f"✓ Submitted feedback: {feedback2['id'][:8]}... - {feedback2['feedback_text'][:50]}...")

    feedback3 = submit_feedback(
        user_id="user789",
        feedback_text="Load time is terrible, can't get any work done",
        category="bug",
        severity="critical",
        metadata={"browser": "Safari", "version": "1.2.3"}
    )
    print(f"✓ Submitted feedback: {feedback3['id'][:8]}... - {feedback3['feedback_text'][:50]}...")

    print(f"\n📊 Total feedback: {len(get_feedback_reports())}")
    print()

    # ─── Step 2: Clustering ────────────────────────────────────────
    print("🎯 Step 2: Clustering feedback by theme...")
    print("-" * 70)

    cluster = create_cluster(
        theme="Performance - Slow Load Times",
        description="Users experiencing slow page load times across all browsers. Load times range from 10+ seconds to complete timeouts. Critical impact on usability.",
        feedback_ids=[feedback1['id'], feedback2['id'], feedback3['id']],
        root_cause="Potential causes: Database query optimization, frontend bundle size, API response times, or infrastructure scaling issues."
    )
    print(f"✓ Created cluster: {cluster['theme']}")
    print(f"  - Grouped {len(cluster['feedback_ids'])} related feedback reports")
    print(f"  - Root cause: {cluster['root_cause'][:80]}...")
    print()

    # ─── Step 3: Enrichment ────────────────────────────────────────
    print("🔍 Step 3: Enriching feedback with logs and context...")
    print("-" * 70)

    # Save some example logs
    logs = """
2024-02-19 10:15:32 [INFO] User user123 accessed /dashboard
2024-02-19 10:15:33 [WARN] Database query took 8.5s: SELECT * FROM analytics...
2024-02-19 10:15:41 [ERROR] Request timeout after 10s
2024-02-19 10:15:41 [ERROR] Frontend render blocked, waiting for API response
    """
    save_user_logs("user123", "session_abc", logs)
    print("✓ Saved user logs for analysis")

    # Enrich the feedback
    enriched = enrich_feedback(
        feedback_id=feedback1['id'],
        logs=logs,
        conversation_history="User mentioned slow dashboard multiple times over past week",
        reproduction_steps=[
            "1. Login to dashboard",
            "2. Navigate to /dashboard",
            "3. Wait for page to load",
            "4. Observe 10+ second load time or timeout"
        ],
        root_cause="Database query on analytics table is not optimized. Full table scan on 10M+ rows causing 8.5s query time.",
        additional_context={
            "affected_users": 150,
            "first_reported": "2024-02-12",
            "browser_independent": True
        }
    )
    print(f"✓ Enriched feedback with logs and root cause analysis")
    print(f"  - Root cause: {enriched['enrichment']['root_cause'][:80]}...")
    print(f"  - Affected users: {enriched['enrichment']['affected_users']}")
    print()

    # ─── Step 4: Bug Tracking ──────────────────────────────────────
    print("🐛 Step 4: Creating bug and tracking updates...")
    print("-" * 70)

    bug = create_bug(
        title="Dashboard load timeout - Database query optimization needed",
        description="Users experiencing 10+ second load times or complete timeouts on dashboard. Root cause: unoptimized analytics query scanning 10M+ rows.",
        severity="critical",
        cluster_id=cluster['id'],
        feedback_ids=[feedback1['id'], feedback2['id'], feedback3['id']],
        assignee="backend-team"
    )
    print(f"✓ Created bug: {bug['title']}")
    print(f"  - Severity: {bug['severity']}")
    print(f"  - Linked to {len(bug['feedback_ids'])} feedback reports")
    print()

    # Simulate new related feedback coming in
    feedback4 = submit_feedback(
        user_id="user999",
        feedback_text="Still seeing slow dashboard loads after latest update",
        category="bug",
        severity="high"
    )

    # Post update to bug
    bug_update = post_bug_update(
        bug_id=bug['id'],
        update_text="New report indicates issue still occurring after v1.2.4 deploy. Issue remains unresolved.",
        new_feedback_ids=[feedback4['id']]
    )
    print(f"✓ Posted update: Issue still occurring (new feedback linked)")
    print(f"  - Total feedback on this bug: {len(bug_update['feedback_ids'])}")
    print()

    # ─── Step 5: Solutioning ───────────────────────────────────────
    print("💡 Step 5: Generating solutions with PRDs and coding prompts...")
    print("-" * 70)

    solution = create_solution(
        bug_id=bug['id'],
        title="Optimize analytics query with database indexing",
        approach="Add composite index on analytics table and implement query caching",
        prd="""
# PRD: Dashboard Performance Optimization

## Problem
Dashboard load times exceed 10 seconds due to unoptimized analytics query scanning 10M+ rows.

## Solution
1. Add composite index on analytics table (user_id, timestamp, event_type)
2. Implement Redis caching layer for frequently accessed analytics
3. Add pagination to limit query results

## Success Metrics
- Load time < 2 seconds for 95th percentile
- Zero timeouts
- Cache hit rate > 80%

## Timeline
- Week 1: Database indexing
- Week 2: Redis caching implementation
- Week 3: Testing and rollout
        """,
        prototype="Figma mockup: https://figma.com/dashboard-perf-v2",
        coding_prompt="""
You are a backend engineer. Implement the following optimizations:

1. Create database migration for composite index:
   - Table: analytics
   - Columns: (user_id, timestamp, event_type)
   - Type: B-tree index

2. Implement Redis caching:
   - Cache key: analytics:{user_id}:{date}
   - TTL: 1 hour
   - Invalidation: on new analytics events

3. Add pagination:
   - Default page size: 50
   - Max page size: 200
   - Return total count for UI

4. Update API endpoint:
   - /api/dashboard/analytics
   - Add query parameters: page, page_size
   - Return: { data: [...], total: N, page: M }

Use Django ORM and django-redis. Write unit tests for caching logic.
        """,
        trade_offs="""
**Pros:**
- Fast implementation (1-2 weeks)
- Proven approach
- Minimal code changes

**Cons:**
- Requires database migration (brief downtime)
- Redis adds infrastructure complexity
- Cache invalidation can be tricky

**Alternative:**
- Move analytics to separate service with optimized storage (longer timeline)
        """,
        effort_estimate="2 weeks (1 engineer)"
    )
    print(f"✓ Created solution: {solution['title']}")
    print(f"  - Approach: {solution['approach']}")
    print(f"  - Effort: {solution['effort_estimate']}")
    print(f"  - Includes: PRD, prototype link, and detailed coding prompt")
    print()

    # ─── Step 6: Analytics ─────────────────────────────────────────
    print("📊 Step 6: System analytics...")
    print("-" * 70)

    analytics = get_feedback_analytics()
    print(f"Total feedback reports: {analytics['total_feedback']}")
    print(f"  - New: {analytics['by_status']['new']}")
    print(f"  - Clustered: {analytics['by_status']['clustered']}")
    print(f"  - Enriched: {analytics['by_status']['enriched']}")
    print()
    print(f"Total clusters: {analytics['total_clusters']}")
    print(f"Total bugs: {analytics['total_bugs']}")
    print(f"  - Open: {analytics['bugs_by_status']['open']}")
    print(f"  - In Progress: {analytics['bugs_by_status']['in_progress']}")
    print()
    print(f"Total solutions: {analytics['total_solutions']}")
    print(f"  - Proposed: {analytics['solutions_by_status']['proposed']}")
    print(f"  - Approved: {analytics['solutions_by_status']['approved']}")
    print()

    # ─── Summary ───────────────────────────────────────────────────
    print("=" * 70)
    print("✨ DEMO COMPLETE!")
    print("=" * 70)
    print()
    print("Feedback workflow demonstrated:")
    print("  1. ✓ Collected 4 user feedback reports")
    print("  2. ✓ Clustered into 1 theme (Performance - Slow Load Times)")
    print("  3. ✓ Enriched with logs, root cause, and context")
    print("  4. ✓ Created bug and posted update on new report")
    print("  5. ✓ Generated solution with PRD, prototype, and coding prompt")
    print("  6. ✓ Analyzed system-wide metrics")
    print()
    print("Data stored in: ~/.agency/feedback/")
    print()
    print("To use with agents:")
    print('  @feedback_team "Analyze feedback and create solutions"')
    print()


if __name__ == "__main__":
    demo()
