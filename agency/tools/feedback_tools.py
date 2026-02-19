"""
Feedback Management Tools

Tools for the feedback management multi-agent team:
- Clustering feedback reports
- Enriching with logs and conversation history
- Tracking bugs and posting updates
- Generating solutions (PRDs, prototypes, coding prompts)
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

# ─── Storage Paths ────────────────────────────────────────────────────────────

FEEDBACK_DIR = Path.home() / ".agency" / "feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

FEEDBACK_DB = FEEDBACK_DIR / "feedback_reports.json"
CLUSTERS_DB = FEEDBACK_DIR / "clusters.json"
BUGS_DB = FEEDBACK_DIR / "bugs.json"
SOLUTIONS_DB = FEEDBACK_DIR / "solutions.json"
LOGS_DIR = FEEDBACK_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ─── Helper Functions ─────────────────────────────────────────────────────────

def _load_json(path: Path, default: Any = None) -> Any:
    """Load JSON from file."""
    if not path.exists():
        return default or {}
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load {path}: {e}")
        return default or {}


def _save_json(path: Path, data: Any):
    """Save JSON to file."""
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save {path}: {e}")


# ─── Feedback Collection ──────────────────────────────────────────────────────

def submit_feedback(
    user_id: str,
    feedback_text: str,
    category: str = "general",
    severity: str = "medium",
    metadata: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Submit a new feedback report.

    Args:
        user_id: User ID submitting feedback
        feedback_text: The feedback content
        category: Category (bug, feature, improvement, etc.)
        severity: Severity level (low, medium, high, critical)
        metadata: Additional metadata (browser, version, etc.)

    Returns:
        Created feedback report with ID
    """
    feedback_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    report = {
        "id": feedback_id,
        "user_id": user_id,
        "feedback_text": feedback_text,
        "category": category,
        "severity": severity,
        "status": "new",
        "created_at": timestamp,
        "updated_at": timestamp,
        "metadata": metadata or {},
        "cluster_id": None,
        "bug_ids": [],
        "enrichment": {},
    }

    # Load existing feedback
    db = _load_json(FEEDBACK_DB, {"reports": []})
    db.setdefault("reports", []).append(report)
    _save_json(FEEDBACK_DB, db)

    logger.info(f"Submitted feedback report: {feedback_id}")
    return report


def get_feedback_reports(
    status: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get feedback reports with optional filters.

    Args:
        status: Filter by status (new, clustered, enriched, resolved)
        category: Filter by category
        severity: Filter by severity
        limit: Max number of reports to return

    Returns:
        List of feedback reports
    """
    db = _load_json(FEEDBACK_DB, {"reports": []})
    reports = db.get("reports", [])

    # Apply filters
    if status:
        reports = [r for r in reports if r.get("status") == status]
    if category:
        reports = [r for r in reports if r.get("category") == category]
    if severity:
        reports = [r for r in reports if r.get("severity") == severity]

    # Sort by timestamp (newest first)
    reports = sorted(reports, key=lambda x: x.get("created_at", ""), reverse=True)

    return reports[:limit]


def update_feedback_status(feedback_id: str, status: str, notes: str = "") -> Dict[str, Any]:
    """Update feedback report status."""
    db = _load_json(FEEDBACK_DB, {"reports": []})
    reports = db.get("reports", [])

    for report in reports:
        if report["id"] == feedback_id:
            report["status"] = status
            report["updated_at"] = datetime.utcnow().isoformat()
            if notes:
                report.setdefault("notes", []).append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "note": notes
                })
            _save_json(FEEDBACK_DB, db)
            logger.info(f"Updated feedback {feedback_id} status to {status}")
            return report

    raise ValueError(f"Feedback report not found: {feedback_id}")


# ─── Clustering ───────────────────────────────────────────────────────────────

def create_cluster(
    theme: str,
    description: str,
    feedback_ids: List[str],
    root_cause: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new feedback cluster (theme).

    Args:
        theme: High-level theme name
        description: Cluster description
        feedback_ids: List of feedback IDs in this cluster
        root_cause: Root cause analysis

    Returns:
        Created cluster
    """
    cluster_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    cluster = {
        "id": cluster_id,
        "theme": theme,
        "description": description,
        "feedback_ids": feedback_ids,
        "root_cause": root_cause,
        "created_at": timestamp,
        "updated_at": timestamp,
        "bug_ids": [],
        "status": "active",
    }

    # Save cluster
    db = _load_json(CLUSTERS_DB, {"clusters": []})
    db.setdefault("clusters", []).append(cluster)
    _save_json(CLUSTERS_DB, db)

    # Update feedback reports with cluster_id
    feedback_db = _load_json(FEEDBACK_DB, {"reports": []})
    for report in feedback_db.get("reports", []):
        if report["id"] in feedback_ids:
            report["cluster_id"] = cluster_id
            report["status"] = "clustered"
    _save_json(FEEDBACK_DB, feedback_db)

    logger.info(f"Created cluster: {cluster_id} with theme '{theme}'")
    return cluster


def get_clusters(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all clusters, optionally filtered by status."""
    db = _load_json(CLUSTERS_DB, {"clusters": []})
    clusters = db.get("clusters", [])

    if status:
        clusters = [c for c in clusters if c.get("status") == status]

    return sorted(clusters, key=lambda x: x.get("created_at", ""), reverse=True)


def add_feedback_to_cluster(cluster_id: str, feedback_ids: List[str]) -> Dict[str, Any]:
    """Add feedback reports to an existing cluster."""
    db = _load_json(CLUSTERS_DB, {"clusters": []})
    clusters = db.get("clusters", [])

    for cluster in clusters:
        if cluster["id"] == cluster_id:
            cluster["feedback_ids"].extend(feedback_ids)
            cluster["feedback_ids"] = list(set(cluster["feedback_ids"]))  # Remove duplicates
            cluster["updated_at"] = datetime.utcnow().isoformat()
            _save_json(CLUSTERS_DB, db)

            # Update feedback reports
            feedback_db = _load_json(FEEDBACK_DB, {"reports": []})
            for report in feedback_db.get("reports", []):
                if report["id"] in feedback_ids:
                    report["cluster_id"] = cluster_id
                    report["status"] = "clustered"
            _save_json(FEEDBACK_DB, feedback_db)

            logger.info(f"Added {len(feedback_ids)} feedback items to cluster {cluster_id}")
            return cluster

    raise ValueError(f"Cluster not found: {cluster_id}")


# ─── Enrichment ───────────────────────────────────────────────────────────────

def enrich_feedback(
    feedback_id: str,
    logs: Optional[str] = None,
    conversation_history: Optional[str] = None,
    reproduction_steps: Optional[List[str]] = None,
    root_cause: Optional[str] = None,
    additional_context: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Enrich a feedback report with logs, conversation history, and analysis.

    Args:
        feedback_id: Feedback report ID
        logs: User logs related to the feedback
        conversation_history: Conversation history
        reproduction_steps: Steps to reproduce
        root_cause: Root cause analysis
        additional_context: Any additional context

    Returns:
        Updated feedback report
    """
    db = _load_json(FEEDBACK_DB, {"reports": []})
    reports = db.get("reports", [])

    for report in reports:
        if report["id"] == feedback_id:
            enrichment = report.setdefault("enrichment", {})

            if logs:
                enrichment["logs"] = logs
            if conversation_history:
                enrichment["conversation_history"] = conversation_history
            if reproduction_steps:
                enrichment["reproduction_steps"] = reproduction_steps
            if root_cause:
                enrichment["root_cause"] = root_cause
            if additional_context:
                enrichment.update(additional_context)

            report["status"] = "enriched"
            report["updated_at"] = datetime.utcnow().isoformat()
            _save_json(FEEDBACK_DB, db)

            logger.info(f"Enriched feedback {feedback_id}")
            return report

    raise ValueError(f"Feedback report not found: {feedback_id}")


def save_user_logs(user_id: str, session_id: str, logs: str) -> str:
    """Save user logs for later analysis."""
    log_file = LOGS_DIR / f"{user_id}_{session_id}.log"
    log_file.write_text(logs)
    logger.info(f"Saved logs for {user_id}/{session_id}")
    return str(log_file)


def get_user_logs(user_id: str, session_id: Optional[str] = None) -> str:
    """Retrieve user logs."""
    if session_id:
        log_file = LOGS_DIR / f"{user_id}_{session_id}.log"
        if log_file.exists():
            return log_file.read_text()
        return ""

    # Return all logs for user
    logs = []
    for log_file in LOGS_DIR.glob(f"{user_id}_*.log"):
        logs.append(f"=== {log_file.name} ===\n{log_file.read_text()}\n")
    return "\n".join(logs)


# ─── Bug Tracking ─────────────────────────────────────────────────────────────

def create_bug(
    title: str,
    description: str,
    severity: str,
    cluster_id: Optional[str] = None,
    feedback_ids: Optional[List[str]] = None,
    assignee: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new bug entry.

    Args:
        title: Bug title
        description: Bug description
        severity: Severity (low, medium, high, critical)
        cluster_id: Associated cluster
        feedback_ids: Associated feedback reports
        assignee: Person assigned to fix

    Returns:
        Created bug
    """
    bug_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    bug = {
        "id": bug_id,
        "title": title,
        "description": description,
        "severity": severity,
        "status": "open",
        "cluster_id": cluster_id,
        "feedback_ids": feedback_ids or [],
        "assignee": assignee,
        "created_at": timestamp,
        "updated_at": timestamp,
        "updates": [],
        "solution_ids": [],
    }

    # Save bug
    db = _load_json(BUGS_DB, {"bugs": []})
    db.setdefault("bugs", []).append(bug)
    _save_json(BUGS_DB, db)

    # Link to cluster if provided
    if cluster_id:
        clusters_db = _load_json(CLUSTERS_DB, {"clusters": []})
        for cluster in clusters_db.get("clusters", []):
            if cluster["id"] == cluster_id:
                cluster.setdefault("bug_ids", []).append(bug_id)
        _save_json(CLUSTERS_DB, clusters_db)

    logger.info(f"Created bug: {bug_id} - {title}")
    return bug


def post_bug_update(bug_id: str, update_text: str, new_feedback_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Post an update to an existing bug (e.g., new related reports).

    Args:
        bug_id: Bug ID
        update_text: Update message
        new_feedback_ids: New feedback reports related to this bug

    Returns:
        Updated bug
    """
    db = _load_json(BUGS_DB, {"bugs": []})
    bugs = db.get("bugs", [])

    for bug in bugs:
        if bug["id"] == bug_id:
            update = {
                "timestamp": datetime.utcnow().isoformat(),
                "update": update_text,
                "new_feedback_ids": new_feedback_ids or [],
            }
            bug.setdefault("updates", []).append(update)
            bug["updated_at"] = datetime.utcnow().isoformat()

            if new_feedback_ids:
                bug.setdefault("feedback_ids", []).extend(new_feedback_ids)
                bug["feedback_ids"] = list(set(bug["feedback_ids"]))  # Remove duplicates

            _save_json(BUGS_DB, db)
            logger.info(f"Posted update to bug {bug_id}")
            return bug

    raise ValueError(f"Bug not found: {bug_id}")


def update_bug_status(bug_id: str, status: str, notes: str = "") -> Dict[str, Any]:
    """Update bug status (open, in_progress, resolved, closed)."""
    db = _load_json(BUGS_DB, {"bugs": []})
    bugs = db.get("bugs", [])

    for bug in bugs:
        if bug["id"] == bug_id:
            bug["status"] = status
            bug["updated_at"] = datetime.utcnow().isoformat()
            if notes:
                bug.setdefault("updates", []).append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "update": f"Status changed to {status}: {notes}"
                })
            _save_json(BUGS_DB, db)
            logger.info(f"Updated bug {bug_id} status to {status}")
            return bug

    raise ValueError(f"Bug not found: {bug_id}")


def get_bugs(status: Optional[str] = None, severity: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get bugs with optional filters."""
    db = _load_json(BUGS_DB, {"bugs": []})
    bugs = db.get("bugs", [])

    if status:
        bugs = [b for b in bugs if b.get("status") == status]
    if severity:
        bugs = [b for b in bugs if b.get("severity") == severity]

    return sorted(bugs, key=lambda x: x.get("created_at", ""), reverse=True)


# ─── Solutioning ──────────────────────────────────────────────────────────────

def create_solution(
    bug_id: str,
    title: str,
    approach: str,
    prd: Optional[str] = None,
    prototype: Optional[str] = None,
    coding_prompt: Optional[str] = None,
    trade_offs: Optional[str] = None,
    effort_estimate: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a solution for a bug or feature.

    Args:
        bug_id: Associated bug ID
        title: Solution title
        approach: Solution approach description
        prd: Product Requirements Document
        prototype: Prototype description or link
        coding_prompt: Prompt for coding agent
        trade_offs: Trade-offs analysis
        effort_estimate: Effort estimate

    Returns:
        Created solution
    """
    solution_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    solution = {
        "id": solution_id,
        "bug_id": bug_id,
        "title": title,
        "approach": approach,
        "prd": prd,
        "prototype": prototype,
        "coding_prompt": coding_prompt,
        "trade_offs": trade_offs,
        "effort_estimate": effort_estimate,
        "status": "proposed",
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    # Save solution
    db = _load_json(SOLUTIONS_DB, {"solutions": []})
    db.setdefault("solutions", []).append(solution)
    _save_json(SOLUTIONS_DB, db)

    # Link to bug
    bugs_db = _load_json(BUGS_DB, {"bugs": []})
    for bug in bugs_db.get("bugs", []):
        if bug["id"] == bug_id:
            bug.setdefault("solution_ids", []).append(solution_id)
    _save_json(BUGS_DB, bugs_db)

    logger.info(f"Created solution: {solution_id} for bug {bug_id}")
    return solution


def get_solutions(bug_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get solutions with optional filters."""
    db = _load_json(SOLUTIONS_DB, {"solutions": []})
    solutions = db.get("solutions", [])

    if bug_id:
        solutions = [s for s in solutions if s.get("bug_id") == bug_id]
    if status:
        solutions = [s for s in solutions if s.get("status") == status]

    return sorted(solutions, key=lambda x: x.get("created_at", ""), reverse=True)


def update_solution_status(solution_id: str, status: str) -> Dict[str, Any]:
    """Update solution status (proposed, approved, implemented, rejected)."""
    db = _load_json(SOLUTIONS_DB, {"solutions": []})
    solutions = db.get("solutions", [])

    for solution in solutions:
        if solution["id"] == solution_id:
            solution["status"] = status
            solution["updated_at"] = datetime.utcnow().isoformat()
            _save_json(SOLUTIONS_DB, db)
            logger.info(f"Updated solution {solution_id} status to {status}")
            return solution

    raise ValueError(f"Solution not found: {solution_id}")


# ─── Analytics ────────────────────────────────────────────────────────────────

def get_feedback_analytics() -> Dict[str, Any]:
    """Get analytics on feedback system."""
    feedback_db = _load_json(FEEDBACK_DB, {"reports": []})
    clusters_db = _load_json(CLUSTERS_DB, {"clusters": []})
    bugs_db = _load_json(BUGS_DB, {"bugs": []})
    solutions_db = _load_json(SOLUTIONS_DB, {"solutions": []})

    reports = feedback_db.get("reports", [])
    clusters = clusters_db.get("clusters", [])
    bugs = bugs_db.get("bugs", [])
    solutions = solutions_db.get("solutions", [])

    return {
        "total_feedback": len(reports),
        "by_status": {
            "new": len([r for r in reports if r.get("status") == "new"]),
            "clustered": len([r for r in reports if r.get("status") == "clustered"]),
            "enriched": len([r for r in reports if r.get("status") == "enriched"]),
            "resolved": len([r for r in reports if r.get("status") == "resolved"]),
        },
        "by_severity": {
            "low": len([r for r in reports if r.get("severity") == "low"]),
            "medium": len([r for r in reports if r.get("severity") == "medium"]),
            "high": len([r for r in reports if r.get("severity") == "high"]),
            "critical": len([r for r in reports if r.get("severity") == "critical"]),
        },
        "total_clusters": len(clusters),
        "total_bugs": len(bugs),
        "bugs_by_status": {
            "open": len([b for b in bugs if b.get("status") == "open"]),
            "in_progress": len([b for b in bugs if b.get("status") == "in_progress"]),
            "resolved": len([b for b in bugs if b.get("status") == "resolved"]),
            "closed": len([b for b in bugs if b.get("status") == "closed"]),
        },
        "total_solutions": len(solutions),
        "solutions_by_status": {
            "proposed": len([s for s in solutions if s.get("status") == "proposed"]),
            "approved": len([s for s in solutions if s.get("status") == "approved"]),
            "implemented": len([s for s in solutions if s.get("status") == "implemented"]),
            "rejected": len([s for s in solutions if s.get("status") == "rejected"]),
        },
    }
