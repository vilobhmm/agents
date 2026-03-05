"""
Tech Lead Manager Coordinator — Unified TLM agent.
"""

import logging
from typing import Dict, List
from datetime import datetime

from agents.career.tech_lead_manager.technical_leadership import TLMTechnicalLeadership
from agents.career.tech_lead_manager.people_management import TLMPeopleManagement
from agents.career.tech_lead_manager.tlm_skills import TLMSkills
from agents.career.base.skills_engine import SkillsEngine
from agents.career.base.growth_tracker import GrowthTracker

logger = logging.getLogger(__name__)


class TechLeadManagerAgent:
    """
    AI Tech Lead Manager — Your hybrid technical + people leadership co-pilot.

    Covers: technical vision, ADRs, sprint planning, 1:1s, performance reviews,
    career development, team health, hiring, project management, post-mortems.
    """

    def __init__(self):
        self.technical = TLMTechnicalLeadership()
        self.people = TLMPeopleManagement()
        self.skills = TLMSkills()
        self.skills_engine = SkillsEngine()
        self.growth_tracker = GrowthTracker()
        logger.info("Tech Lead Manager Agent initialized")

    def get_skill_dimensions(self) -> Dict:
        return self.skills.get_dimensions()

    def assess_skills(self, evidence: Dict[str, List[str]]) -> Dict:
        return self.skills.assess_tlm_skills(evidence)
