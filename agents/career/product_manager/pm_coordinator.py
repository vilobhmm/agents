"""
Product Manager Coordinator — Unified PM agent.

Composes all PM modules into a single interface.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from agents.career.product_manager.strategy import PMStrategy
from agents.career.product_manager.research import PMResearch
from agents.career.product_manager.prioritization import PMPrioritization
from agents.career.product_manager.goals_metrics import PMGoalsMetrics
from agents.career.product_manager.stakeholders import PMStakeholders
from agents.career.product_manager.launch import PMLaunch
from agents.career.product_manager.pm_skills import PMSkills
from agents.career.base.skills_engine import SkillsEngine
from agents.career.base.growth_tracker import GrowthTracker

logger = logging.getLogger(__name__)


class ProductManagerAgent:
    """
    AI Product Manager — Your PM co-pilot.

    Covers the full PM lifecycle:
    - Strategy & vision
    - Market & user research
    - Prioritization (RICE, ICE, MoSCoW, Kano)
    - Goals, OKRs & metrics
    - Stakeholder management
    - Launch & landing
    - Skills assessment & growth

    Usage:
        pm = ProductManagerAgent()

        # Strategy
        vision = await pm.strategy.define_product_vision(...)
        strategy = await pm.strategy.create_product_strategy(...)

        # Prioritization (deterministic)
        ranked = pm.prioritization.rice_score(features)

        # Skills
        skills = pm.skills.assess_pm_skills(evidence)
    """

    def __init__(self):
        """Initialize all PM modules."""
        self.strategy = PMStrategy()
        self.research = PMResearch()
        self.prioritization = PMPrioritization()
        self.goals = PMGoalsMetrics()
        self.stakeholders = PMStakeholders()
        self.launch = PMLaunch()
        self.skills = PMSkills()
        self.skills_engine = SkillsEngine()
        self.growth_tracker = GrowthTracker()

        logger.info("Product Manager Agent initialized")

    # ── End-to-End Workflows ─────────────────────────────────────

    async def product_lifecycle(self, idea: str, market: str) -> Dict:
        """
        Run the complete product lifecycle: idea → strategy → launch plan.

        Args:
            idea: Product idea description
            market: Target market

        Returns:
            Complete lifecycle document
        """
        logger.info(f"Running product lifecycle for: {idea}")
        results = {}

        # 1. Vision
        results["vision"] = await self.strategy.define_product_vision(
            problem=idea, users="target users", market=market
        )

        # 2. Market sizing
        results["market"] = await self.strategy.market_sizing(idea, market)

        # 3. OKRs
        results["okrs"] = await self.goals.create_okrs(idea)

        # 4. Launch plan
        results["launch_plan"] = await self.launch.create_launch_plan(idea, "TBD")

        return {
            "idea": idea,
            "market": market,
            "lifecycle": results,
            "timestamp": datetime.now().isoformat(),
        }

    def get_skill_dimensions(self) -> Dict:
        """Return PM skill dimensions with rubrics."""
        return self.skills.get_dimensions()

    def assess_skills(self, evidence: Dict[str, List[str]]) -> Dict:
        """Assess PM skills from evidence."""
        return self.skills.assess_pm_skills(evidence)
