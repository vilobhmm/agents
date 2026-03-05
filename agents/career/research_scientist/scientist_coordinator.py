"""
Research Scientist Coordinator — Unified scientist agent.
"""

import logging
from typing import Dict, List
from datetime import datetime

from agents.career.research_scientist.literature import ScientistLiterature
from agents.career.research_scientist.experimentation import ScientistExperimentation
from agents.career.research_scientist.scientist_skills import ScientistSkills
from agents.career.base.skills_engine import SkillsEngine
from agents.career.base.growth_tracker import GrowthTracker

logger = logging.getLogger(__name__)


class ResearchScientistAgent:
    """
    AI Research Scientist — Your research co-pilot.

    Covers: literature review, hypothesis generation, experiment design,
    data analysis, publication, and skills assessment.
    """

    def __init__(self):
        self.literature = ScientistLiterature()
        self.experimentation = ScientistExperimentation()
        self.skills = ScientistSkills()
        self.skills_engine = SkillsEngine()
        self.growth_tracker = GrowthTracker()
        logger.info("Research Scientist Agent initialized")

    def get_skill_dimensions(self) -> Dict:
        return self.skills.get_dimensions()

    def assess_skills(self, evidence: Dict[str, List[str]]) -> Dict:
        return self.skills.assess_scientist_skills(evidence)

    async def full_research_workflow(self, topic: str, domain: str) -> Dict:
        """End-to-end research workflow: review → hypothesis → experiment → paper."""
        results = {}
        results["review"] = await self.literature.literature_review(topic)
        results["hypotheses"] = await self.literature.generate_hypothesis(topic, domain)
        results["experiment"] = await self.experimentation.design_experiment(topic)
        results["paper_outline"] = await self.experimentation.paper_outline(topic)
        return {"topic": topic, "workflow": results, "timestamp": datetime.now().isoformat()}
