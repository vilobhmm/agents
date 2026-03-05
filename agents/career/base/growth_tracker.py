"""
Growth Tracker — Persists and analyzes skill growth over time.

Stores snapshots of skill assessments and provides trend analysis,
progress reports, and growth velocity metrics.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from agents.career.base.career_types import (
    SkillLevel, SkillAssessment, CareerProfile,
)

logger = logging.getLogger(__name__)


class GrowthTracker:
    """
    Tracks skill growth over time with local file persistence.

    Data is stored as JSON snapshots in ~/.career_growth/
    """

    def __init__(self, data_dir: Optional[str] = None):
        """Initialize growth tracker."""
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / ".career_growth"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_snapshot(self, profile: CareerProfile) -> Dict:
        """
        Save a point-in-time snapshot of the career profile.

        Args:
            profile: Career profile to snapshot

        Returns:
            Snapshot metadata
        """
        timestamp = datetime.now()
        snapshot = {
            "name": profile.name,
            "role": profile.role,
            "seniority": profile.seniority,
            "overall_score": profile.overall_score(),
            "overall_level": profile.overall_level().value,
            "skills": {
                name: {
                    "score": a.score,
                    "level": a.level.value,
                }
                for name, a in profile.skills.items()
            },
            "timestamp": timestamp.isoformat(),
        }

        # Save to file
        filename = f"snapshot_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.data_dir / profile.name.replace(" ", "_").lower() / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(snapshot, f, indent=2)

        logger.info(f"Saved growth snapshot: {filepath}")
        return {"file": str(filepath), "timestamp": timestamp.isoformat()}

    def get_history(self, profile_name: str) -> List[Dict]:
        """
        Get all historical snapshots for a profile.

        Args:
            profile_name: Name of the profile

        Returns:
            List of snapshots sorted by timestamp
        """
        profile_dir = self.data_dir / profile_name.replace(" ", "_").lower()
        if not profile_dir.exists():
            return []

        snapshots = []
        for filepath in sorted(profile_dir.glob("snapshot_*.json")):
            with open(filepath) as f:
                snapshots.append(json.load(f))

        return snapshots

    def get_growth_delta(
        self, profile_name: str, last_n: int = 2
    ) -> Dict:
        """
        Compare the last N snapshots to show growth.

        Args:
            profile_name: Name of the profile
            last_n: Number of recent snapshots to compare

        Returns:
            Growth delta with per-skill changes
        """
        history = self.get_history(profile_name)
        if len(history) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 snapshots to compute growth",
                "snapshots_available": len(history),
            }

        recent = history[-last_n:]
        oldest = recent[0]
        newest = recent[-1]

        skill_deltas = {}
        all_skills = set(oldest.get("skills", {}).keys()) | set(newest.get("skills", {}).keys())

        for skill in all_skills:
            old_score = oldest.get("skills", {}).get(skill, {}).get("score", 0)
            new_score = newest.get("skills", {}).get(skill, {}).get("score", 0)
            delta = new_score - old_score
            skill_deltas[skill] = {
                "old_score": old_score,
                "new_score": new_score,
                "delta": delta,
                "direction": "↑" if delta > 0 else ("↓" if delta < 0 else "→"),
            }

        overall_delta = newest.get("overall_score", 0) - oldest.get("overall_score", 0)

        return {
            "period": {
                "from": oldest.get("timestamp"),
                "to": newest.get("timestamp"),
            },
            "overall_delta": overall_delta,
            "skill_deltas": skill_deltas,
            "fastest_growing": max(skill_deltas.items(), key=lambda x: x[1]["delta"])[0] if skill_deltas else None,
            "needs_attention": min(skill_deltas.items(), key=lambda x: x[1]["delta"])[0] if skill_deltas else None,
        }

    def progress_report(self, profile_name: str) -> str:
        """
        Generate a text progress report.

        Args:
            profile_name: Name of the profile

        Returns:
            Formatted progress report
        """
        history = self.get_history(profile_name)

        if not history:
            return f"No growth data available for {profile_name}."

        latest = history[-1]
        lines = [
            f"📊 Growth Report: {profile_name}",
            f"{'=' * 50}",
            f"Role: {latest.get('role', 'unknown').replace('_', ' ').title()}",
            f"Level: {latest.get('seniority', 'unknown')}",
            f"Overall Score: {latest.get('overall_score', 0):.0f}/100",
            f"Snapshots: {len(history)}",
            "",
        ]

        if len(history) >= 2:
            delta = self.get_growth_delta(profile_name)
            lines.append(f"Growth (last 2 snapshots):")
            lines.append(f"  Overall: {delta['overall_delta']:+.0f} points")
            lines.append(f"  Fastest growing: {delta.get('fastest_growing', 'N/A')}")
            lines.append(f"  Needs attention: {delta.get('needs_attention', 'N/A')}")
            lines.append("")

            for skill, data in delta.get("skill_deltas", {}).items():
                lines.append(
                    f"  {data['direction']}  {skill}: "
                    f"{data['old_score']} → {data['new_score']} "
                    f"({data['delta']:+d})"
                )
        else:
            lines.append("Skills:")
            for skill, data in latest.get("skills", {}).items():
                lines.append(f"  • {skill}: {data['score']}/100 ({data['level']})")

        return "\n".join(lines)
