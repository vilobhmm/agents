"""
Software Engineer Coordinator — Unified SWE IC agent.
"""

import logging
from typing import Dict, List
from datetime import datetime

from agents.career.software_engineer.design import SWEDesign
from agents.career.software_engineer.implementation import SWEImplementation
from agents.career.software_engineer.quality import SWEQuality
from agents.career.software_engineer.swe_skills import SWESkills
from agents.career.base.skills_engine import SkillsEngine
from agents.career.base.growth_tracker import GrowthTracker

logger = logging.getLogger(__name__)


class SoftwareEngineerAgent:
    """
    AI Software Engineer IC — Your engineering co-pilot.

    Covers: design & architecture, implementation & code review,
    testing & quality, tech debt & performance, skills assessment.
    """

    def __init__(self):
        self.design = SWEDesign()
        self.implementation = SWEImplementation()
        self.quality = SWEQuality()
        self.skills = SWESkills()
        self.skills_engine = SkillsEngine()
        self.growth_tracker = GrowthTracker()
        logger.info("Software Engineer Agent initialized")

    def get_skill_dimensions(self) -> Dict:
        return self.skills.get_dimensions()

    def assess_skills(self, evidence: Dict[str, List[str]]) -> Dict:
        return self.skills.assess_swe_skills(evidence)
