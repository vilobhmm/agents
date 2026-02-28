#!/usr/bin/env python3
"""
E2E Feedback Management Demo — Real GitHub Issues + Claude AI
=============================================================

Uses REAL issues from `vercel/next.js` as the feedback source.
Claude AI powers every intelligent step end-to-end.

Workflow (mirrors Telegram commands):
  /submitfeedback    → Fetch & store real GitHub issues as feedback
  /clusterfeedback   → Claude clusters by theme + root cause
  /trackbugs         → Create tracked bugs from each cluster
  /generatesolutions → Claude writes PRDs + coding prompts per bug
  /feedbackreport    → Analytics dashboard

Run:
  python examples/e2e_feedback_github_demo.py
  ANTHROPIC_API_KEY=sk-... python examples/e2e_feedback_github_demo.py
"""

import json
import os
import sys
import time
from pathlib import Path

import anthropic
import requests

# ── Project root on path ──────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent_tools.feedback_tools import (
    submit_feedback,
    get_feedback_reports,
    create_cluster,
    get_clusters,
    enrich_feedback,
    create_bug,
    post_bug_update,
    get_bugs,
    create_solution,
    get_solutions,
    get_feedback_analytics,
    FEEDBACK_DB,
    CLUSTERS_DB,
    BUGS_DB,
    SOLUTIONS_DB,
)

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_REPO   = "vercel/next.js"
ISSUES_LIMIT  = 15          # fetch N real issues (public API, no token needed)
CLAUDE_MODEL  = "claude-haiku-4-5-20251001"

BOLD  = "\033[1m"
GREEN = "\033[92m"
CYAN  = "\033[96m"
YELLOW= "\033[93m"
RED   = "\033[91m"
DIM   = "\033[2m"
RESET = "\033[0m"

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def banner(title: str, emoji: str = ""):
    width = 70
    print()
    print(f"{CYAN}{'═' * width}{RESET}")
    print(f"{BOLD}{CYAN}  {emoji}  {title}{RESET}")
    print(f"{CYAN}{'═' * width}{RESET}")


def step(msg: str):
    print(f"\n{BOLD}{GREEN}▶ {msg}{RESET}")


def info(msg: str):
    print(f"  {DIM}→{RESET} {msg}")


def ok(msg: str):
    print(f"  {GREEN}✓{RESET} {msg}")


def warn(msg: str):
    print(f"  {YELLOW}⚠{RESET}  {msg}")


def section(title: str):
    print(f"\n  {BOLD}{title}{RESET}")
    print(f"  {'─' * 60}")


def claude(prompt: str, system: str = "") -> str:
    """Call Claude and return text response."""
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": CLAUDE_MODEL, "max_tokens": 2048, "messages": messages}
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return resp.content[0].text.strip()


def clear_feedback_db():
    """Reset feedback DBs for a clean demo run."""
    for db in [FEEDBACK_DB, CLUSTERS_DB, BUGS_DB, SOLUTIONS_DB]:
        if db.exists():
            db.unlink()


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — /submitfeedback  (real GitHub issues → feedback DB)
# ─────────────────────────────────────────────────────────────────────────────

def step1_submit_feedback() -> list[dict]:
    banner("STEP 1 — /submitfeedback", "📥")
    step(f"Fetching real issues from GitHub: {GITHUB_REPO}")

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    params = {
        "state": "open",
        "labels": "bug",
        "per_page": ISSUES_LIMIT,
        "sort": "comments",
        "direction": "desc",
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    gh_token = os.getenv("GITHUB_TOKEN")
    if gh_token:
        headers["Authorization"] = f"token {gh_token}"

    r = requests.get(url, params=params, headers=headers, timeout=15)
    if r.status_code != 200:
        warn(f"GitHub API returned {r.status_code} — using fallback sample data")
        issues = _fallback_issues()
    else:
        issues = [i for i in r.json() if "pull_request" not in i][:ISSUES_LIMIT]
        info(f"Fetched {len(issues)} real bug issues from {GITHUB_REPO}")

    submitted = []
    for issue in issues:
        title = issue.get("title", "")
        body  = (issue.get("body") or "")[:400]
        labels = [lb["name"] for lb in issue.get("labels", [])]
        comments = issue.get("comments", 0)

        sev = "low"
        if comments > 20 or "critical" in " ".join(labels).lower():
            sev = "critical"
        elif comments > 10 or "high" in " ".join(labels).lower():
            sev = "high"
        elif comments > 4:
            sev = "medium"

        fb = submit_feedback(
            user_id=f"gh_user_{issue.get('number', 0)}",
            feedback_text=f"{title}. {body}".strip(),
            category="bug",
            severity=sev,
            metadata={
                "source": "github",
                "repo": GITHUB_REPO,
                "issue_number": issue.get("number"),
                "issue_url": issue.get("html_url", ""),
                "labels": labels,
                "comments": comments,
            },
        )
        submitted.append(fb)
        ok(f"#{issue.get('number')} [{sev:8s}] {title[:65]}")

    print()
    info(f"Total feedback stored: {len(submitted)}")
    return submitted


def _fallback_issues():
    """Fallback sample issues mimicking real Next.js bugs."""
    return [
        {"number": 1001, "title": "App Router: Static pages not invalidating after ISR revalidate", "body": "After setting revalidate=60 in fetch(), the pages are not revalidating on production. This worked in Pages Router but is broken in App Router.", "labels": [{"name": "bug"}, {"name": "area: app"}], "comments": 25},
        {"number": 1002, "title": "next/image causes CLS (cumulative layout shift) on Safari", "body": "The Image component doesn't reserve space correctly on Safari 16+, causing layout shift before image loads. Affects Lighthouse scores.", "labels": [{"name": "bug"}, {"name": "area: image"}], "comments": 18},
        {"number": 1003, "title": "Memory leak in dev server: RAM usage keeps growing", "body": "After running next dev for 1-2 hours, RAM usage grows from 200MB to 4GB+. Have to restart the server frequently.", "labels": [{"name": "bug"}, {"name": "dev-server"}], "comments": 42},
        {"number": 1004, "title": "Middleware: cookies() not working in edge runtime after Next.js 14.1", "body": "cookies() from next/headers throws 'cookies was called outside a request scope' in middleware after upgrading to 14.1.", "labels": [{"name": "bug"}, {"name": "area: middleware"}], "comments": 31},
        {"number": 1005, "title": "next/font: Flash of unstyled text (FOUT) on first render", "body": "When using next/font with local fonts, there's a noticeable FOUT on first page load even with preload set to true.", "labels": [{"name": "bug"}, {"name": "area: font"}], "comments": 15},
        {"number": 1006, "title": "Server Actions: 'use server' causes 500 error with file uploads", "body": "When using Server Actions to upload files, the FormData parsing throws an internal server error. Works fine with regular forms.", "labels": [{"name": "bug"}, {"name": "area: server actions"}], "comments": 22},
        {"number": 1007, "title": "Dev server memory leak: webpack HMR module cache not cleared", "body": "HMR module registry grows indefinitely. After many file changes, webpack compilation slows down significantly.", "labels": [{"name": "bug"}, {"name": "dev-server"}], "comments": 38},
        {"number": 1008, "title": "Static exports: dynamic routes with generateStaticParams fail on Vercel", "body": "Pages using generateStaticParams work locally but throw 404 on Vercel deployment when using output: 'export'.", "labels": [{"name": "bug"}, {"name": "area: static-export"}], "comments": 12},
        {"number": 1009, "title": "App Router: useSearchParams causes entire page to suspend", "body": "Wrapping a component with useSearchParams causes unexpected Suspense boundary activation on the entire page, not just the component.", "labels": [{"name": "bug"}, {"name": "area: app"}], "comments": 28},
        {"number": 1010, "title": "next/image: srcSet generated incorrectly for AVIF format", "body": "When using AVIF format, the srcSet attribute has duplicated entries and some sizes are missing, affecting responsive images.", "labels": [{"name": "bug"}, {"name": "area: image"}], "comments": 9},
        {"number": 1011, "title": "next dev extremely slow on monorepo with many packages", "body": "Initial compilation in a Turborepo monorepo with 30+ packages takes 3-5 minutes. Turbopack is faster but still has issues.", "labels": [{"name": "bug"}, {"name": "dev-server"}], "comments": 55},
        {"number": 1012, "title": "cookies() in Server Component randomly returns empty on CDN edge nodes", "body": "On Vercel Edge Network, cookies() intermittently returns an empty ReadonlyRequestCookies object on ~2% of requests.", "labels": [{"name": "bug"}, {"name": "area: middleware"}], "comments": 19},
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — /clusterfeedback  (Claude groups by theme)
# ─────────────────────────────────────────────────────────────────────────────

def step2_cluster_feedback(feedback_list: list[dict]) -> list[dict]:
    banner("STEP 2 — /clusterfeedback", "🎯")
    step("Asking Claude to cluster feedback into themes...")

    feedback_lines = "\n".join(
        f"ID:{fb['id'][:8]} SEV:{fb['severity']:8s} TEXT:{fb['feedback_text'][:100]}"
        for fb in feedback_list
    )

    prompt = f"""You are a senior product analyst. Cluster these {len(feedback_list)} bug reports from the Next.js GitHub repo into 3-5 meaningful themes.

FEEDBACK REPORTS:
{feedback_lines}

For each cluster output JSON exactly like this (no markdown, pure JSON array):
[
  {{
    "theme": "Short descriptive theme name",
    "description": "2-3 sentence description of the common pattern",
    "root_cause": "Technical root cause hypothesis (1-2 sentences)",
    "severity": "critical|high|medium|low",
    "feedback_short_ids": ["id1", "id2"]
  }}
]

Rules:
- short_ids = first 8 chars of feedback ID (exact match from input)
- Every feedback must be in exactly one cluster
- Order clusters by severity (critical first)
- Be precise about root causes, mention specific Next.js internals when possible"""

    raw = claude(prompt)

    # Parse JSON (handle if Claude wraps in ```json ``` blocks)
    raw_clean = raw.strip()
    if raw_clean.startswith("```"):
        raw_clean = raw_clean.split("```")[1]
        if raw_clean.startswith("json"):
            raw_clean = raw_clean[4:]
    try:
        cluster_specs = json.loads(raw_clean)
    except json.JSONDecodeError:
        warn("Claude response wasn't clean JSON — extracting manually")
        start = raw.find("[")
        end   = raw.rfind("]") + 1
        cluster_specs = json.loads(raw[start:end])

    # Build short_id → full_id map
    id_map = {fb["id"][:8]: fb["id"] for fb in feedback_list}

    created_clusters = []
    for spec in cluster_specs:
        full_ids = [id_map[sid] for sid in spec["feedback_short_ids"] if sid in id_map]
        if not full_ids:
            warn(f"Skipping empty cluster: {spec['theme']}")
            continue

        c = create_cluster(
            theme=spec["theme"],
            description=spec["description"],
            feedback_ids=full_ids,
            root_cause=spec["root_cause"],
        )
        created_clusters.append(c)

        ok(f"{spec['severity'].upper():8s}  {spec['theme']}")
        info(f"{spec['description'][:80]}...")
        info(f"Root cause: {spec['root_cause'][:80]}...")
        info(f"Reports grouped: {len(full_ids)}")

    print()
    info(f"Total clusters created: {len(created_clusters)}")
    return created_clusters


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — /trackbugs  (bug per cluster + enrichment + updates)
# ─────────────────────────────────────────────────────────────────────────────

def step3_track_bugs(clusters: list[dict], all_feedback: list[dict]) -> list[dict]:
    banner("STEP 3 — /trackbugs", "🐛")
    step("Creating bugs from clusters and enriching with context...")

    # Build feedback lookup
    fb_map = {fb["id"]: fb for fb in all_feedback}

    created_bugs = []
    for cluster in clusters:
        ids_in_cluster = cluster["feedback_ids"]

        # Determine severity from linked feedback
        severities = [fb_map.get(fid, {}).get("severity", "medium") for fid in ids_in_cluster]
        sev_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        max_sev = max(severities, key=lambda s: sev_order.get(s, 0))

        # Count total GitHub comments as proxy for user impact
        total_comments = sum(fb_map.get(fid, {}).get("metadata", {}).get("comments", 0) for fid in ids_in_cluster)

        bug_title = f"[{max_sev.upper()}] {cluster['theme']}"

        bug = create_bug(
            title=bug_title,
            description=(
                f"{cluster['description']}\n\n"
                f"Root Cause: {cluster['root_cause']}\n\n"
                f"Affects {len(ids_in_cluster)} feedback reports with {total_comments} total community comments."
            ),
            severity=max_sev,
            cluster_id=cluster["id"],
            feedback_ids=ids_in_cluster,
            assignee="engineering-team",
        )
        created_bugs.append(bug)
        ok(f"Created  BUG-{bug['id'][:6]}  {bug_title}")
        info(f"Linked to {len(ids_in_cluster)} feedback reports ({total_comments} GitHub comments)")

        # Enrich the highest-severity feedback in the cluster
        if ids_in_cluster:
            top_fb = max(ids_in_cluster, key=lambda fid: sev_order.get(fb_map.get(fid, {}).get("severity", "low"), 0))
            top_fb_data = fb_map.get(top_fb, {})
            issue_url = top_fb_data.get("metadata", {}).get("issue_url", "")

            enrich_feedback(
                feedback_id=top_fb,
                logs=(
                    f"[GitHub] Repo: {GITHUB_REPO}\n"
                    f"[GitHub] Issue: {issue_url}\n"
                    f"[GitHub] Comments: {top_fb_data.get('metadata', {}).get('comments', 0)}\n"
                    f"[GitHub] Labels: {top_fb_data.get('metadata', {}).get('labels', [])}"
                ),
                conversation_history=f"Linked to cluster '{cluster['theme']}'",
                reproduction_steps=[
                    "1. See original GitHub issue for repro steps",
                    f"2. Issue URL: {issue_url}",
                    "3. Root cause: " + cluster["root_cause"],
                ],
                root_cause=cluster["root_cause"],
                additional_context={"total_community_comments": total_comments, "cluster_id": cluster["id"]},
            )
            ok(f"Enriched  feedback {top_fb[:8]}  with GitHub context")

    # Simulate a new incoming report arriving after bugs were created
    section("Simulating new incoming feedback (post-bug-creation)")
    new_report = submit_feedback(
        user_id="gh_user_9999",
        feedback_text="Dev server still leaking memory after latest canary release. RAM hits 6GB now.",
        category="bug",
        severity="critical",
        metadata={"source": "github", "repo": GITHUB_REPO, "issue_number": 9999, "comments": 5},
    )
    ok(f"New feedback arrived: {new_report['id'][:8]}  (dev-server memory leak update)")

    # Post update to the dev-server bug if it exists
    dev_bug = next((b for b in created_bugs if "dev" in b["title"].lower() or "memory" in b["title"].lower()), None)
    if dev_bug:
        post_bug_update(
            bug_id=dev_bug["id"],
            update_text="New community report: Memory usage reaching 6GB in canary release. Issue still unresolved after latest patch.",
            new_feedback_ids=[new_report["id"]],
        )
        ok(f"Posted update to  BUG-{dev_bug['id'][:6]}  — linked new report")

    print()
    info(f"Total bugs tracked: {len(created_bugs)}")
    return created_bugs


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — /generatesolutions  (Claude writes PRDs + coding prompts)
# ─────────────────────────────────────────────────────────────────────────────

def step4_generate_solutions(bugs: list[dict]) -> list[dict]:
    banner("STEP 4 — /generatesolutions", "💡")
    step("Asking Claude to generate PRDs and coding prompts for each bug...")

    all_solutions = []
    for bug in bugs:
        print(f"\n  {BOLD}► BUG-{bug['id'][:6]}: {bug['title']}{RESET}")

        prompt = f"""You are a senior Next.js / React engineer and product manager.

BUG TITLE: {bug['title']}
DESCRIPTION: {bug['description']}

Generate a concise but complete solution. Return ONLY valid JSON (no markdown), exactly:
{{
  "title": "Solution title (≤ 10 words)",
  "approach": "1-2 sentence technical approach",
  "prd": "# PRD\\n## Problem\\n...\\n## Solution\\n...\\n## Success Metrics\\n...\\n## Timeline\\n...",
  "coding_prompt": "You are a Next.js core contributor. Implement the following fix:\\n\\n1. ...\\n2. ...\\n\\nInclude unit tests.",
  "trade_offs": "**Pros:**\\n- ...\\n\\n**Cons:**\\n- ...\\n\\n**Alternatives:**\\n- ...",
  "effort_estimate": "X days / Y engineers"
}}"""

        raw = claude(prompt, system="You are a technical product manager. Output only valid JSON, no extra text.")
        raw_clean = raw.strip()
        if raw_clean.startswith("```"):
            raw_clean = "\n".join(raw_clean.split("\n")[1:-1])
        try:
            spec = json.loads(raw_clean)
        except json.JSONDecodeError:
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            spec  = json.loads(raw[start:end])

        sol = create_solution(
            bug_id=bug["id"],
            title=spec["title"],
            approach=spec["approach"],
            prd=spec["prd"],
            coding_prompt=spec["coding_prompt"],
            trade_offs=spec["trade_offs"],
            effort_estimate=spec["effort_estimate"],
        )
        all_solutions.append(sol)

        ok(f"Solution: {spec['title']}")
        info(f"Approach: {spec['approach'][:90]}")
        info(f"Effort:   {spec['effort_estimate']}")

        # Print PRD excerpt
        prd_lines = spec["prd"].split("\n")
        print(f"\n    {BOLD}PRD Preview:{RESET}")
        for line in prd_lines[:10]:
            if line.strip():
                print(f"    {DIM}{line}{RESET}")

        # Print coding prompt excerpt
        print(f"\n    {BOLD}Coding Prompt Preview:{RESET}")
        for line in spec["coding_prompt"].split("\n")[:6]:
            if line.strip():
                print(f"    {DIM}{line}{RESET}")

    print()
    info(f"Total solutions generated: {len(all_solutions)}")
    return all_solutions


# ─────────────────────────────────────────────────────────────────────────────
# Step 5 — /feedbackreport  (analytics dashboard)
# ─────────────────────────────────────────────────────────────────────────────

def step5_feedback_report():
    banner("STEP 5 — /feedbackreport", "📊")
    step("Generating analytics report...")

    a   = get_feedback_analytics()
    fbs = get_feedback_reports()
    cls = get_clusters()
    bgs = get_bugs()
    sls = get_solutions()

    section("System Overview")
    print(f"    {'Total Feedback Reports':<30} {a['total_feedback']}")
    print(f"    {'Total Clusters':<30} {a['total_clusters']}")
    print(f"    {'Total Bugs':<30} {a['total_bugs']}")
    print(f"    {'Total Solutions':<30} {a['total_solutions']}")

    section("Feedback by Status")
    for status, count in a["by_status"].items():
        bar = "█" * count
        print(f"    {status:<12} {count:>3}  {GREEN}{bar}{RESET}")

    section("Feedback by Severity")
    sev_colors = {"critical": RED, "high": YELLOW, "medium": CYAN, "low": DIM}
    for sev, count in a["by_severity"].items():
        color = sev_colors.get(sev, RESET)
        bar = "█" * count
        print(f"    {sev:<12} {count:>3}  {color}{bar}{RESET}")

    section("Bugs by Status")
    for status, count in a["bugs_by_status"].items():
        bar = "█" * count
        print(f"    {status:<14} {count:>3}  {YELLOW}{bar}{RESET}")

    section("Open Bugs (sorted by severity)")
    open_bugs = [b for b in bgs if b["status"] == "open"]
    sev_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    open_bugs.sort(key=lambda b: sev_order.get(b["severity"], 0), reverse=True)
    for bug in open_bugs:
        color = sev_colors.get(bug["severity"], RESET)
        fb_count = len(bug.get("feedback_ids", []))
        sol_count = len(bug.get("solution_ids", []))
        updates = len(bug.get("updates", []))
        print(f"    {color}[{bug['severity'].upper():<8}]{RESET}  BUG-{bug['id'][:6]}  {bug['title'][:55]}")
        print(f"              {DIM}feedback:{fb_count}  solutions:{sol_count}  updates:{updates}{RESET}")

    section("Clusters & Themes")
    for cluster in cls:
        fb_count = len(cluster.get("feedback_ids", []))
        print(f"    {CYAN}●{RESET} {cluster['theme']}")
        print(f"      {DIM}{cluster['description'][:90]}{RESET}")
        print(f"      {DIM}Reports: {fb_count}  |  Root cause: {cluster['root_cause'][:70]}...{RESET}")

    section("Solution Proposals")
    for sol in sls:
        linked_bug = next((b for b in bgs if b["id"] == sol["bug_id"]), {})
        bug_title = linked_bug.get("title", "Unknown bug")[:50]
        print(f"    {GREEN}✓{RESET} {sol['title']}")
        print(f"      {DIM}For: {bug_title}{RESET}")
        print(f"      {DIM}Effort: {sol['effort_estimate']}  |  Status: {sol['status']}{RESET}")

    # Ask Claude for an executive summary
    section("AI Executive Summary")
    summary_prompt = f"""Summarize this Next.js feedback analysis in 3-4 concise bullet points for an engineering manager:

- {a['total_feedback']} feedback reports from GitHub issues
- {a['total_clusters']} clusters identified
- {a['total_bugs']} bugs tracked (open: {a['bugs_by_status']['open']})
- {a['total_solutions']} solutions proposed

Top clusters: {', '.join(c['theme'] for c in cls[:3])}
Critical bugs: {sum(1 for b in bgs if b['severity'] == 'critical')}
High severity: {sum(1 for b in bgs if b['severity'] == 'high')}

Write actionable, specific bullets."""

    summary = claude(summary_prompt)
    for line in summary.split("\n"):
        if line.strip():
            print(f"    {line}")


# ─────────────────────────────────────────────────────────────────────────────
# Final summary
# ─────────────────────────────────────────────────────────────────────────────

def final_summary(feedback: list, clusters: list, bugs: list, solutions: list):
    banner("E2E COMPLETE!", "✨")

    print(f"""
  {BOLD}GitHub Repo:{RESET}      {GITHUB_REPO}
  {BOLD}Claude Model:{RESET}     {CLAUDE_MODEL}
  {BOLD}Data stored in:{RESET}   ~/.agency/feedback/

  {BOLD}Workflow Completed:{RESET}
    {GREEN}✓{RESET}  /submitfeedback    — {len(feedback)} real GitHub issues ingested
    {GREEN}✓{RESET}  /clusterfeedback   — {len(clusters)} themes clustered by Claude AI
    {GREEN}✓{RESET}  /trackbugs         — {len(bugs)} bugs tracked with enrichment
    {GREEN}✓{RESET}  /generatesolutions — {len(solutions)} PRDs + coding prompts generated
    {GREEN}✓{RESET}  /feedbackreport    — Full analytics dashboard rendered

  {BOLD}Stored files:{RESET}
    {DIM}~/.agency/feedback/feedback_reports.json{RESET}
    {DIM}~/.agency/feedback/clusters.json{RESET}
    {DIM}~/.agency/feedback/bugs.json{RESET}
    {DIM}~/.agency/feedback/solutions.json{RESET}

  {BOLD}To replay on Telegram:{RESET}
    {CYAN}/submitfeedback App Router cache not invalidating after deploy{RESET}
    {CYAN}/clusterfeedback{RESET}
    {CYAN}/trackbugs{RESET}
    {CYAN}/generatesolutions{RESET}
    {CYAN}/feedbackreport{RESET}
""")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    banner("E2E FEEDBACK MANAGEMENT DEMO", "🚀")
    print(f"""
  {BOLD}Source:{RESET}  Real GitHub issues from {CYAN}{GITHUB_REPO}{RESET}
  {BOLD}AI:{RESET}      Claude ({CLAUDE_MODEL})
  {BOLD}Steps:{RESET}   submit → cluster → track bugs → generate solutions → report
""")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(f"  {RED}ERROR: ANTHROPIC_API_KEY not set{RESET}")
        print(f"  Export it:  {CYAN}export ANTHROPIC_API_KEY=sk-ant-...{RESET}")
        sys.exit(1)

    # Clear existing data for a clean demo
    step("Clearing previous demo data for fresh run...")
    clear_feedback_db()
    ok("Database cleared")

    t0 = time.time()

    feedback  = step1_submit_feedback()
    clusters  = step2_cluster_feedback(feedback)
    bugs      = step3_track_bugs(clusters, feedback)
    solutions = step4_generate_solutions(bugs)
    step5_feedback_report()

    elapsed = time.time() - t0
    final_summary(feedback, clusters, bugs, solutions)
    print(f"  {DIM}Total time: {elapsed:.1f}s{RESET}\n")


if __name__ == "__main__":
    main()
