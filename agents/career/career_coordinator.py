"""
Career Coordinator — Top-level entry point for the career agent system.

Instantiates any role agent and provides cross-role capabilities:
role comparison, career transition planning, and holistic assessment.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from agents.career.product_manager.pm_coordinator import ProductManagerAgent
from agents.career.software_engineer.swe_coordinator import SoftwareEngineerAgent
from agents.career.research_scientist.scientist_coordinator import ResearchScientistAgent
from agents.career.tech_lead_manager.tlm_coordinator import TechLeadManagerAgent
from agents.career.base.skills_engine import SkillsEngine
from agents.career.base.growth_tracker import GrowthTracker

logger = logging.getLogger(__name__)

ROLE_MAP = {
    "product_manager": ProductManagerAgent,
    "software_engineer": SoftwareEngineerAgent,
    "research_scientist": ResearchScientistAgent,
    "tech_lead_manager": TechLeadManagerAgent,
}


class CareerCoordinator:
    """
    Top-level coordinator for the multi-role career agent system.

    Provides:
    - Role-specific agent access
    - Cross-role comparison
    - Career transition planning
    - Holistic skills assessment

    Usage:
        coordinator = CareerCoordinator()
        pm = coordinator.get_agent("product_manager")
        swe = coordinator.get_agent("software_engineer")

        # Use role-specific capabilities
        ranked = pm.prioritization.rice_score(features)
        design = await swe.design.create_design_doc(problem, constraints)

        # Cross-role capabilities
        transition = await coordinator.career_transition_plan("software_engineer", "product_manager")
    """

    AVAILABLE_ROLES = list(ROLE_MAP.keys())

    def __init__(self):
        """Initialize career coordinator."""
        self._agents: Dict = {}
        self.skills_engine = SkillsEngine()
        self.growth_tracker = GrowthTracker()
        logger.info("Career Coordinator initialized")

    def get_agent(self, role: str):
        """
        Get or create a role-specific agent.

        Args:
            role: One of "product_manager", "software_engineer",
                  "research_scientist", "tech_lead_manager"

        Returns:
            Role-specific agent instance
        """
        if role not in ROLE_MAP:
            raise ValueError(
                f"Unknown role: {role}. Available: {self.AVAILABLE_ROLES}"
            )

        if role not in self._agents:
            self._agents[role] = ROLE_MAP[role]()

        return self._agents[role]

    def list_roles(self) -> List[Dict]:
        """List all available roles with their capabilities."""
        role_info = {
            "product_manager": {
                "title": "Product Manager",
                "modules": ["strategy", "research", "prioritization", "goals", "stakeholders", "launch", "skills"],
                "capabilities_count": 30,
            },
            "software_engineer": {
                "title": "Software Engineer (IC)",
                "modules": ["design", "implementation", "quality", "skills"],
                "capabilities_count": 18,
            },
            "research_scientist": {
                "title": "Research Scientist",
                "modules": ["literature", "experimentation", "skills"],
                "capabilities_count": 16,
            },
            "tech_lead_manager": {
                "title": "Tech Lead Manager",
                "modules": ["technical", "people", "skills"],
                "capabilities_count": 18,
            },
        }
        return [
            {"role": role, **info}
            for role, info in role_info.items()
        ]

    async def career_transition_plan(
        self,
        from_role: str,
        to_role: str,
        current_evidence: Optional[Dict[str, List[str]]] = None,
    ) -> Dict:
        """
        Plan a career transition between roles.

        Args:
            from_role: Current role
            to_role: Target role
            current_evidence: Optional evidence of current skills

        Returns:
            Transition plan with skill gaps, actions, and timeline
        """
        if from_role not in ROLE_MAP or to_role not in ROLE_MAP:
            raise ValueError(f"Roles must be one of: {self.AVAILABLE_ROLES}")

        from_agent = self.get_agent(from_role)
        to_agent = self.get_agent(to_role)

        from_dims = set(from_agent.get_skill_dimensions().keys())
        to_dims = set(to_agent.get_skill_dimensions().keys())

        transferable = from_dims & to_dims
        new_skills = to_dims - from_dims
        deprecated = from_dims - to_dims

        prompt = f"""Create a career transition plan:

From: {from_role.replace('_', ' ').title()}
To: {to_role.replace('_', ' ').title()}

Transferable Skills: {', '.join(transferable) if transferable else 'None directly'}
New Skills Needed: {', '.join(new_skills) if new_skills else 'None'}
Skills to Deprioritize: {', '.join(deprecated) if deprecated else 'None'}

Provide:
1. **Transition Assessment**: Feasibility and typical timeline
2. **Transferable Skills**: How existing skills apply to new role
3. **Skill Gaps**: Critical gaps to address (ranked by importance)
4. **90-Day Plan**: First 3 months of transition
5. **6-Month Plan**: Building competency
6. **12-Month Plan**: Reaching proficiency
7. **Resources**: Books, courses, mentors, communities
8. **Common Pitfalls**: Mistakes people make in this transition
9. **Success Stories**: Patterns from people who've made this transition"""

        response = await self.skills_engine._ask_claude(
            prompt,
            "You are a career transition coach specializing in tech industry role changes."
        )

        return {
            "from_role": from_role,
            "to_role": to_role,
            "transferable_skills": list(transferable),
            "new_skills_needed": list(new_skills),
            "transition_plan": response,
            "timestamp": datetime.now().isoformat(),
        }

    def compare_roles(self, roles: Optional[List[str]] = None) -> Dict:
        """
        Compare skill dimensions across roles.

        Args:
            roles: Roles to compare (defaults to all)

        Returns:
            Comparison matrix of skill dimensions
        """
        roles = roles or self.AVAILABLE_ROLES
        comparison = {}

        for role in roles:
            agent = self.get_agent(role)
            dims = agent.get_skill_dimensions()
            comparison[role] = {
                "title": role.replace("_", " ").title(),
                "dimensions": list(dims.keys()),
                "dimension_count": len(dims),
            }

        # Find common and unique dimensions
        all_dims = set()
        for role_data in comparison.values():
            all_dims.update(role_data["dimensions"])

        for role_data in comparison.values():
            role_dims = set(role_data["dimensions"])
            role_data["unique_dimensions"] = list(role_dims - (all_dims - role_dims))
            role_data["shared_dimensions"] = list(role_dims & (all_dims - role_dims))

        return comparison
