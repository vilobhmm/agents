"""
Scientist Skills Assessment — Research-specific rubric.
"""

import logging, re
from typing import Dict, List
from agents.career.base.career_types import SkillLevel, SkillAssessment

logger = logging.getLogger(__name__)

SCIENTIST_SKILL_DIMENSIONS = {
    "research_methodology": {
        "description": "Rigor in designing and executing research",
        "beginner": "Follows established protocols",
        "developing": "Adapts methods, identifies limitations",
        "proficient": "Designs novel experiments, strong statistical skills",
        "advanced": "Creates new methodologies adopted by others",
        "expert": "Defines methodological standards for the field",
    },
    "analytical_rigor": {
        "description": "Depth and correctness of analysis",
        "beginner": "Applies basic statistical tests",
        "developing": "Uses appropriate methods, interprets correctly",
        "proficient": "Advanced analysis, identifies subtle patterns",
        "advanced": "Develops new analytical frameworks",
        "expert": "Creates analytical tools used community-wide",
    },
    "publication_impact": {
        "description": "Quality and influence of published work",
        "beginner": "Contributing to papers as co-author",
        "developing": "First-author papers at workshops/lower-tier venues",
        "proficient": "First-author at top venues, moderate citations",
        "advanced": "High-impact papers, significant citation count",
        "expert": "Seminal papers that shape the field, h-index leader",
    },
    "mentorship": {
        "description": "Developing other researchers",
        "beginner": "Learning from mentors",
        "developing": "Helps peers, co-mentors undergrads",
        "proficient": "Mentors grad students, serves on committees",
        "advanced": "Builds and leads research groups",
        "expert": "Creates research cultures, produces research leaders",
    },
    "grant_writing": {
        "description": "Securing research funding",
        "beginner": "Contributes to proposals",
        "developing": "Writes sections, assists with budgets",
        "proficient": "Leads proposals, secures funding",
        "advanced": "High success rate, large grants, diverse funding",
        "expert": "Multi-million funding portfolio, advisory roles",
    },
    "collaboration": {
        "description": "Working effectively across teams and disciplines",
        "beginner": "Collaborates within immediate team",
        "developing": "Reaches out to other groups for expertise",
        "proficient": "Leads multi-group collaborations",
        "advanced": "Builds cross-institutional research programs",
        "expert": "Creates large-scale collaborative initiatives",
    },
    "innovation": {
        "description": "Generating novel ideas and approaches",
        "beginner": "Incremental improvements to existing work",
        "developing": "Identifies new angles within existing paradigms",
        "proficient": "Creates new approaches that others adopt",
        "advanced": "Opens new research directions",
        "expert": "Paradigm-shifting contributions",
    },
}


class ScientistSkills:
    """Research Scientist skills assessment."""

    def __init__(self):
        self.dimensions = SCIENTIST_SKILL_DIMENSIONS

    def get_dimensions(self) -> Dict:
        return self.dimensions

    def assess_scientist_skills(self, evidence: Dict[str, List[str]]) -> Dict[str, SkillAssessment]:
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
            if any(w in il for w in ["published", "cited", "presented", "funded", "awarded", "discovered"]):
                bonus += 5
            if re.search(r'\d+ papers|\d+ citations|\$\d+', item):
                bonus += 5
        return min(base + bonus, 95)
