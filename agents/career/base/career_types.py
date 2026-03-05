"""
Shared data types for the career agent system.

Provides the common structures used across all role agents:
skill levels, assessments, growth plans, and career profiles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class SkillLevel(str, Enum):
    """Progressive skill mastery levels."""
    BEGINNER = "beginner"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"

    @classmethod
    def from_score(cls, score: int) -> "SkillLevel":
        """Map a 0-100 score to a SkillLevel."""
        if score < 20:
            return cls.BEGINNER
        elif score < 40:
            return cls.DEVELOPING
        elif score < 60:
            return cls.PROFICIENT
        elif score < 80:
            return cls.ADVANCED
        else:
            return cls.EXPERT

    @property
    def next_level(self) -> Optional["SkillLevel"]:
        """Return the next level, or None if already expert."""
        levels = list(SkillLevel)
        idx = levels.index(self)
        return levels[idx + 1] if idx < len(levels) - 1 else None


@dataclass
class SkillAssessment:
    """Assessment of a single skill dimension."""
    skill_name: str
    level: SkillLevel
    score: int  # 0-100
    evidence: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)
    feedback: str = ""
    assessed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GrowthPlan:
    """Actionable growth plan for a specific skill or set of skills."""
    target_role: str
    target_level: SkillLevel
    current_level: SkillLevel
    actions: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    milestones: List[Dict] = field(default_factory=list)
    timeline_weeks: int = 12
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CareerProfile:
    """Complete career profile for a professional."""
    name: str
    role: str  # "product_manager", "software_engineer", "research_scientist", "tech_lead_manager"
    seniority: str = "mid"  # junior, mid, senior, staff, principal
    skills: Dict[str, SkillAssessment] = field(default_factory=dict)
    growth_history: List[Dict] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def overall_score(self) -> float:
        """Average score across all assessed skills."""
        if not self.skills:
            return 0.0
        return sum(s.score for s in self.skills.values()) / len(self.skills)

    def overall_level(self) -> SkillLevel:
        """Determine overall level from average score."""
        return SkillLevel.from_score(int(self.overall_score()))

    def top_skills(self, n: int = 3) -> List[SkillAssessment]:
        """Return the n highest-scored skills."""
        return sorted(self.skills.values(), key=lambda s: s.score, reverse=True)[:n]

    def weakest_skills(self, n: int = 3) -> List[SkillAssessment]:
        """Return the n lowest-scored skills."""
        return sorted(self.skills.values(), key=lambda s: s.score)[:n]
