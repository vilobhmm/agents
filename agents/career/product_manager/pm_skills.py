"""
PM Skills Assessment — Role-specific skills rubric.

Covers the core PM competency dimensions used at Google/Meta-style PM ladders.
"""

import logging
from typing import Dict, List
from agents.career.base.career_types import SkillLevel, SkillAssessment

logger = logging.getLogger(__name__)


# PM competency dimensions with rubrics
PM_SKILL_DIMENSIONS = {
    "product_sense": {
        "description": "Ability to identify user needs, define the right product, and make good product decisions",
        "beginner": "Can articulate user needs but relies on others for product direction",
        "developing": "Contributes to product decisions with some guidance",
        "proficient": "Independently identifies opportunities and makes sound product decisions",
        "advanced": "Shapes product strategy, anticipates market shifts, makes high-judgment calls",
        "expert": "Defines category-creating products, exceptional instinct validated by results",
    },
    "execution": {
        "description": "Ability to ship products on time, at quality, with clear communication",
        "beginner": "Can execute well-defined tasks with guidance",
        "developing": "Manages small features end-to-end with some oversight",
        "proficient": "Ships medium-sized projects independently, manages cross-functional teams",
        "advanced": "Delivers complex multi-quarter programs, unblocks ambiguity",
        "expert": "Consistently ships high-impact programs across org boundaries",
    },
    "strategic_impact": {
        "description": "Ability to connect product work to business outcomes and long-term strategy",
        "beginner": "Understands how their feature connects to broader goals",
        "developing": "Can articulate strategic rationale for their work",
        "proficient": "Shapes product strategy for their area, drives measurable business impact",
        "advanced": "Influences multi-product strategy, creates new strategic directions",
        "expert": "Defines company-level strategy, consistently delivers outsized business impact",
    },
    "leadership": {
        "description": "Ability to influence without authority, build alignment, and develop others",
        "beginner": "Collaborates well within their team",
        "developing": "Influences peers and gains buy-in for ideas",
        "proficient": "Leads cross-functional teams, resolves conflicts, mentors juniors",
        "advanced": "Influences senior leadership, builds and develops PM teams",
        "expert": "Shapes organizational culture, builds world-class PM organizations",
    },
    "analytical_rigor": {
        "description": "Ability to use data to make decisions, define metrics, and measure impact",
        "beginner": "Can read dashboards and track basic metrics",
        "developing": "Defines success metrics and analyzes experiment results",
        "proficient": "Designs metric frameworks, runs A/B tests, makes data-driven decisions",
        "advanced": "Creates novel measurement approaches, builds data culture on team",
        "expert": "Pioneers measurement methodologies, industry-recognized analytics expertise",
    },
    "technical_depth": {
        "description": "Understanding of technology to make informed product decisions",
        "beginner": "Basic understanding of tech stack and constraints",
        "developing": "Can have productive conversations with engineers about tradeoffs",
        "proficient": "Understands system architecture, makes informed technical tradeoff decisions",
        "advanced": "Shapes technical direction, identifies innovative technical approaches",
        "expert": "Deep technical expertise that enables breakthrough product innovation",
    },
    "user_empathy": {
        "description": "Deep understanding of users and ability to advocate for their needs",
        "beginner": "Relies on others' research to understand users",
        "developing": "Conducts user research and synthesizes findings",
        "proficient": "Deeply understands user segments, anticipates needs, advocates effectively",
        "advanced": "Shapes user research strategy, identifies non-obvious user insights",
        "expert": "Legendary user advocate, creates products users love before they know they need them",
    },
}


class PMSkills:
    """PM-specific skills assessment using industry-standard rubrics."""

    def __init__(self):
        self.dimensions = PM_SKILL_DIMENSIONS

    def get_dimensions(self) -> Dict[str, Dict]:
        """Return all PM skill dimensions with rubrics."""
        return self.dimensions

    def assess_pm_skills(self, evidence: Dict[str, List[str]]) -> Dict[str, SkillAssessment]:
        """
        Assess PM skills based on provided evidence.

        Args:
            evidence: Dict mapping dimension name → list of evidence items.
                     Evidence items are descriptions of things the PM has done.

        Returns:
            Dict mapping dimension → SkillAssessment

        Example:
            >>> skills.assess_pm_skills({
            ...     "product_sense": ["Led discovery for new search feature", "Increased activation by 15%"],
            ...     "execution": ["Shipped 3 features on time in Q2"],
            ... })
        """
        assessments = {}

        for dimension, rubric in self.dimensions.items():
            dim_evidence = evidence.get(dimension, [])

            if not dim_evidence:
                assessments[dimension] = SkillAssessment(
                    skill_name=dimension,
                    level=SkillLevel.BEGINNER,
                    score=0,
                    evidence=[],
                    feedback="No evidence provided for this dimension.",
                )
                continue

            # Heuristic scoring based on evidence quantity and quality indicators
            score = self._score_evidence(dim_evidence)
            level = SkillLevel.from_score(score)

            assessments[dimension] = SkillAssessment(
                skill_name=dimension,
                level=level,
                score=score,
                evidence=dim_evidence,
                strengths=self._identify_strengths(dim_evidence),
                growth_areas=[rubric.get(level.next_level.value, "")] if level.next_level else [],
                feedback=f"Level: {level.value}. {rubric.get(level.value, '')}",
            )

        return assessments

    def _score_evidence(self, evidence: List[str]) -> int:
        """Score evidence heuristically (0-100)."""
        if not evidence:
            return 0

        base_score = min(len(evidence) * 15, 60)  # More evidence = higher base

        # Quality signals
        quality_bonus = 0
        quality_words = ["led", "shipped", "increased", "reduced", "built", "designed",
                        "launched", "grew", "defined", "created", "influenced", "mentored"]
        for item in evidence:
            item_lower = item.lower()
            for word in quality_words:
                if word in item_lower:
                    quality_bonus += 3
                    break

        # Quantitative signals
        import re
        for item in evidence:
            if re.search(r'\d+%|\d+x|\$\d+', item):
                quality_bonus += 5

        return min(base_score + quality_bonus, 95)

    def _identify_strengths(self, evidence: List[str]) -> List[str]:
        """Identify strengths from evidence."""
        strengths = []
        if len(evidence) >= 3:
            strengths.append("Depth of experience demonstrated")
        for item in evidence:
            if any(w in item.lower() for w in ["led", "owned", "drove"]):
                strengths.append("Shows ownership and leadership")
                break
        for item in evidence:
            if any(w in item.lower() for w in ["increased", "grew", "reduced", "improved"]):
                strengths.append("Impact-oriented with measurable results")
                break
        return strengths[:3]
