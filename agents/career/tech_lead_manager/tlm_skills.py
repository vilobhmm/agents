"""
TLM Skills Assessment — Dual-track (technical + people) rubric.
"""

import logging, re
from typing import Dict, List
from agents.career.base.career_types import SkillLevel, SkillAssessment

logger = logging.getLogger(__name__)

TLM_SKILL_DIMENSIONS = {
    "technical_leadership": {
        "description": "Setting technical direction and raising the engineering bar",
        "beginner": "Makes good technical decisions within team scope",
        "developing": "Influences technical direction across 2-3 teams",
        "proficient": "Drives architecture across org, mentors tech leads",
        "advanced": "Sets technical strategy for large engineering org",
        "expert": "Industry-influential technical leader, defines standards",
    },
    "people_management": {
        "description": "Managing, developing, and retaining engineering talent",
        "beginner": "Manages 2-3 engineers with guidance from skip-level",
        "developing": "Manages 5-7 engineers independently, handles basic people issues",
        "proficient": "Manages 8-12 engineers including seniors, high team health",
        "advanced": "Manages managers, builds high-performing organizations",
        "expert": "Creates engineering cultures that attract top talent",
    },
    "strategic_thinking": {
        "description": "Connecting technical work to business strategy",
        "beginner": "Understands team's contribution to company goals",
        "developing": "Aligns team's work to org priorities",
        "proficient": "Shapes technical strategy for business impact",
        "advanced": "Influences company strategy through technical perspective",
        "expert": "Bridges technology and business at executive level",
    },
    "execution": {
        "description": "Delivering complex projects on time with quality",
        "beginner": "Delivers team's commitments reliably",
        "developing": "Manages multi-team projects with dependencies",
        "proficient": "Delivers complex cross-org programs systematically",
        "advanced": "Turns around troubled programs, consistently delivers at scale",
        "expert": "Delivers company-critical programs with flawless execution",
    },
    "communication": {
        "description": "Clear communication up, down, and across",
        "beginner": "Communicates clearly with team and manager",
        "developing": "Effective in cross-functional meetings and presentations",
        "proficient": "Skilled at exec communication, writes compelling docs",
        "advanced": "Inspires through communication, influences org direction",
        "expert": "Exceptional communicator, represents engineering externally",
    },
    "team_building": {
        "description": "Hiring, onboarding, and building effective teams",
        "beginner": "Participates in hiring, welcomes new team members",
        "developing": "Leads interviews, builds interview loops, owns onboarding",
        "proficient": "Builds and scales teams, strong hiring bar, low attrition",
        "advanced": "Creates hiring programs, builds diverse high-performing teams",
        "expert": "Creates world-class engineering organizations",
    },
    "cross_functional_influence": {
        "description": "Working effectively across engineering, product, design, etc.",
        "beginner": "Partners well with PM and design on team projects",
        "developing": "Drives alignment across functions for medium initiatives",
        "proficient": "Shapes cross-functional strategy, resolves org-level conflicts",
        "advanced": "Influences VP-level decisions across multiple functions",
        "expert": "Shapes company direction through cross-functional leadership",
    },
}


class TLMSkills:
    """TLM skills assessment with dual-track (technical + people) rubrics."""

    def __init__(self):
        self.dimensions = TLM_SKILL_DIMENSIONS

    def get_dimensions(self) -> Dict:
        return self.dimensions

    def assess_tlm_skills(self, evidence: Dict[str, List[str]]) -> Dict[str, SkillAssessment]:
        assessments = {}
        for dim, rubric in self.dimensions.items():
            de = evidence.get(dim, [])
            if not de:
                assessments[dim] = SkillAssessment(skill_name=dim, level=SkillLevel.BEGINNER, score=0, evidence=[], feedback="No evidence.")
                continue
            score = self._score_evidence(de)
            level = SkillLevel.from_score(score)
            assessments[dim] = SkillAssessment(skill_name=dim, level=level, score=score, evidence=de, feedback=f"Level: {level.value}. {rubric.get(level.value, '')}")
        return assessments

    def _score_evidence(self, evidence: List[str]) -> int:
        base = min(len(evidence) * 15, 60)
        bonus = 0
        for item in evidence:
            il = item.lower()
            if any(w in il for w in ["managed", "hired", "promoted", "mentored", "led", "scaled", "delivered"]):
                bonus += 4
            if re.search(r'\d+ engineers|\d+ reports|\d+%', item):
                bonus += 5
        return min(base + bonus, 95)
