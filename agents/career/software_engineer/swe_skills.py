"""
SWE Skills Assessment — Role-specific skills rubric (L3-L8 style ladder).
"""

import logging, re
from typing import Dict, List
from agents.career.base.career_types import SkillLevel, SkillAssessment

logger = logging.getLogger(__name__)

SWE_SKILL_DIMENSIONS = {
    "coding": {
        "description": "Writing clean, efficient, maintainable code",
        "beginner": "Writes functional code with guidance, learning patterns",
        "developing": "Writes clean code independently, follows conventions",
        "proficient": "Writes production-quality code, mentors on code quality",
        "advanced": "Sets coding standards for team, masters multiple paradigms",
        "expert": "Creates frameworks and tools used across the organization",
    },
    "system_design": {
        "description": "Designing scalable, reliable distributed systems",
        "beginner": "Understands basic patterns (client-server, REST)",
        "developing": "Designs components within existing architecture",
        "proficient": "Designs medium-scale systems end-to-end",
        "advanced": "Designs large-scale distributed systems, makes org-wide architecture decisions",
        "expert": "Industry-recognized system design expertise, shapes platform strategy",
    },
    "debugging": {
        "description": "Systematic problem-solving and root cause analysis",
        "beginner": "Can debug simple issues with guidance",
        "developing": "Debugs most issues independently using logs and tools",
        "proficient": "Expert debugger across stack, creates debugging tools/patterns",
        "advanced": "Debugs the most complex cross-system issues others can't solve",
        "expert": "Creates debugging methodologies adopted org-wide",
    },
    "testing": {
        "description": "Quality assurance through comprehensive testing",
        "beginner": "Writes basic unit tests",
        "developing": "Writes comprehensive tests, understands test pyramid",
        "proficient": "Designs test strategies, champions testing culture",
        "advanced": "Creates testing frameworks, drives org-wide quality initiatives",
        "expert": "Pioneering testing methodologies, industry-recognized expertise",
    },
    "project_leadership": {
        "description": "Leading technical projects from planning to delivery",
        "beginner": "Completes assigned tasks on schedule",
        "developing": "Leads small features end-to-end",
        "proficient": "Leads medium projects, coordinates with cross-functional teams",
        "advanced": "Leads multi-quarter programs, drives org-level initiatives",
        "expert": "Leads company-critical programs with executive-level impact",
    },
    "mentorship": {
        "description": "Growing other engineers through teaching and guidance",
        "beginner": "Learning from others, asks good questions",
        "developing": "Helps teammates, answers questions effectively",
        "proficient": "Mentors junior engineers, improves onboarding",
        "advanced": "Develops senior engineers, shapes team growth culture",
        "expert": "Creates company-wide engineering development programs",
    },
    "technical_influence": {
        "description": "Influencing technical direction beyond immediate team",
        "beginner": "Contributes ideas within team",
        "developing": "Drives technical decisions within team",
        "proficient": "Influences technical direction across multiple teams",
        "advanced": "Shapes engineering culture and practices org-wide",
        "expert": "Industry thought leader, influences the broader engineering community",
    },
}


class SWESkills:
    """SWE-specific skills assessment using L3-L8 style rubrics."""

    def __init__(self):
        self.dimensions = SWE_SKILL_DIMENSIONS

    def get_dimensions(self) -> Dict:
        return self.dimensions

    def assess_swe_skills(self, evidence: Dict[str, List[str]]) -> Dict[str, SkillAssessment]:
        """Assess SWE skills from evidence."""
        assessments = {}
        for dimension, rubric in self.dimensions.items():
            dim_evidence = evidence.get(dimension, [])
            if not dim_evidence:
                assessments[dimension] = SkillAssessment(
                    skill_name=dimension, level=SkillLevel.BEGINNER, score=0,
                    evidence=[], feedback="No evidence provided.",
                )
                continue
            score = self._score_evidence(dim_evidence)
            level = SkillLevel.from_score(score)
            assessments[dimension] = SkillAssessment(
                skill_name=dimension, level=level, score=score,
                evidence=dim_evidence,
                feedback=f"Level: {level.value}. {rubric.get(level.value, '')}",
            )
        return assessments

    def _score_evidence(self, evidence: List[str]) -> int:
        base = min(len(evidence) * 15, 60)
        bonus = 0
        for item in evidence:
            il = item.lower()
            if any(w in il for w in ["designed", "architected", "led", "built", "optimized", "reduced"]):
                bonus += 4
            if re.search(r'\d+%|\d+x|\d+ms', item):
                bonus += 5
        return min(base + bonus, 95)
