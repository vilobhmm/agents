"""
Skills Assessment Engine — Core engine used by all role agents.

Provides AI-powered skill assessment, growth planning, peer calibration,
and development roadmap generation.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

from agents.career.base.career_types import (
    SkillLevel, SkillAssessment, GrowthPlan, CareerProfile,
)

logger = logging.getLogger(__name__)


class SkillsEngine:
    """
    AI-powered skills assessment engine.

    Used by all role-specific agents to evaluate skills,
    generate growth plans, and track development.
    """

    def __init__(self):
        """Initialize skills engine with optional Claude API."""
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False
            logger.warning("Claude API not configured for skills engine")

    # ── Assessment ───────────────────────────────────────────────

    async def assess_skill(
        self,
        skill_name: str,
        role: str,
        evidence: List[str],
        rubric: Optional[Dict] = None,
    ) -> SkillAssessment:
        """
        Assess a single skill dimension based on evidence.

        Args:
            skill_name: Name of the skill (e.g., "product_sense", "system_design")
            role: Role context (e.g., "product_manager", "software_engineer")
            evidence: List of evidence items demonstrating the skill
            rubric: Optional custom rubric for evaluation

        Returns:
            SkillAssessment with score, level, strengths, and growth areas
        """
        logger.info(f"Assessing skill: {skill_name} for {role}")

        evidence_text = "\n".join(f"- {e}" for e in evidence)
        rubric_text = ""
        if rubric:
            rubric_text = "\n\nRubric:\n" + "\n".join(
                f"- {level}: {desc}" for level, desc in rubric.items()
            )

        prompt = f"""Assess this professional's skill level based on the evidence provided.

Role: {role}
Skill: {skill_name}{rubric_text}

Evidence:
{evidence_text}

Provide your assessment as a structured analysis:

1. **Score** (0-100): Numerical score based on evidence quality and depth
2. **Level**: beginner / developing / proficient / advanced / expert
3. **Strengths**: 2-3 specific strengths demonstrated
4. **Growth Areas**: 2-3 specific areas for improvement
5. **Feedback**: Constructive paragraph summarizing the assessment

Be calibrated: a score of 50 means solid mid-level performance.
Only give 80+ for genuinely exceptional, demonstrated expertise."""

        response = await self._ask_claude(
            prompt,
            system=f"You are a senior {role.replace('_', ' ')} and career coach with deep expertise in evaluating professional skills."
        )

        # Parse score from response (default to 50 if parsing fails)
        score = self._extract_score(response)
        level = SkillLevel.from_score(score)

        return SkillAssessment(
            skill_name=skill_name,
            level=level,
            score=score,
            evidence=evidence,
            feedback=response,
        )

    async def generate_growth_plan(
        self,
        profile: CareerProfile,
        target_role: Optional[str] = None,
        target_level: Optional[str] = None,
        timeframe_weeks: int = 12,
    ) -> GrowthPlan:
        """
        Generate an actionable growth plan.

        Args:
            profile: Current career profile with assessed skills
            target_role: Target role (defaults to current role)
            target_level: Target seniority level
            timeframe_weeks: Planning horizon in weeks

        Returns:
            GrowthPlan with actions, resources, and milestones
        """
        logger.info(f"Generating growth plan for {profile.name}")

        target_role = target_role or profile.role

        skills_summary = "\n".join(
            f"- {name}: {a.level.value} ({a.score}/100)"
            for name, a in profile.skills.items()
        )

        prompt = f"""Create a personalized growth plan for this professional:

Current Role: {profile.role.replace('_', ' ').title()}
Current Level: {profile.seniority}
Target Role: {target_role.replace('_', ' ').title()}
Target Level: {target_level or 'next level up'}
Timeframe: {timeframe_weeks} weeks

Current Skills:
{skills_summary}

Goals: {', '.join(profile.goals) if profile.goals else 'Not specified'}

Provide:

1. **Priority Skills to Develop**: Top 3 skills with highest impact
2. **Actions** (10-15 specific actions):
   - Each should be concrete and measurable
   - Include what to do, how often, and expected outcome
3. **Resources**: Books, courses, communities, tools
4. **Milestones**: Weekly or bi-weekly checkpoints
5. **Quick Wins**: 3 things to do this week

Be specific and actionable — no generic advice."""

        response = await self._ask_claude(
            prompt,
            system="You are a world-class career coach specializing in tech industry professional development."
        )

        current_level = profile.overall_level()
        target = SkillLevel.from_score(
            min(100, int(profile.overall_score()) + 20)
        )

        return GrowthPlan(
            target_role=target_role,
            target_level=target,
            current_level=current_level,
            actions=[response],  # Full plan as single action
            timeline_weeks=timeframe_weeks,
        )

    async def peer_calibration(
        self,
        self_assessment: Dict[str, int],
        role: str,
        seniority: str,
    ) -> Dict:
        """
        Calibrate self-assessment against industry standards.

        Args:
            self_assessment: skill_name -> self-rated score (0-100)
            role: Current role
            seniority: Current seniority level

        Returns:
            Calibrated scores with industry benchmarks
        """
        logger.info(f"Calibrating assessment for {role} at {seniority} level")

        scores_text = "\n".join(
            f"- {skill}: {score}/100" for skill, score in self_assessment.items()
        )

        prompt = f"""A {seniority} {role.replace('_', ' ')} has self-assessed their skills:

{scores_text}

For each skill:
1. **Industry Benchmark**: What score would you expect at this level?
2. **Calibrated Score**: Adjusted score based on typical self-assessment bias
3. **Assessment**: Is this person over-rating, under-rating, or well-calibrated?
4. **Gap Analysis**: Biggest gaps vs expectations for their level

Note: Most people over-rate by 10-20%. Senior people tend to under-rate.
Provide honest, calibrated feedback."""

        response = await self._ask_claude(
            prompt,
            system=f"You are a hiring manager who has evaluated hundreds of {role.replace('_', ' ')}s."
        )

        return {
            "self_assessment": self_assessment,
            "role": role,
            "seniority": seniority,
            "calibration": response,
            "timestamp": datetime.now().isoformat(),
        }

    async def create_development_roadmap(
        self,
        profile: CareerProfile,
        timeframe_months: int = 6,
    ) -> Dict:
        """
        Create a phased development roadmap.

        Args:
            profile: Current career profile
            timeframe_months: Roadmap duration in months

        Returns:
            Phased roadmap with monthly goals and metrics
        """
        logger.info(f"Creating {timeframe_months}-month roadmap for {profile.name}")

        skills_summary = "\n".join(
            f"- {name}: {a.level.value} ({a.score}/100)"
            for name, a in profile.skills.items()
        )

        prompt = f"""Create a {timeframe_months}-month development roadmap:

Profile:
- Role: {profile.role.replace('_', ' ').title()}
- Level: {profile.seniority}
- Overall Score: {profile.overall_score():.0f}/100

Skills:
{skills_summary}

For each month, provide:
1. **Focus Area**: Primary skill to develop
2. **Goals**: 2-3 specific, measurable goals
3. **Activities**: What to do daily/weekly
4. **Deliverables**: Tangible outputs to demonstrate growth
5. **Success Metrics**: How to measure progress

Also include:
- **Risks**: What could derail the plan
- **Accountability**: How to stay on track
- **Review Points**: When to reassess and adjust"""

        response = await self._ask_claude(
            prompt,
            system="You are an executive coach who creates structured development programs."
        )

        return {
            "profile_name": profile.name,
            "role": profile.role,
            "timeframe_months": timeframe_months,
            "roadmap": response,
            "timestamp": datetime.now().isoformat(),
        }

    # ── Helpers ──────────────────────────────────────────────────

    def _extract_score(self, text: str) -> int:
        """Extract numerical score from Claude's response."""
        import re
        # Look for patterns like "Score: 65" or "**Score**: 72"
        patterns = [
            r'\*?\*?Score\*?\*?\s*[:\-–]\s*(\d+)',
            r'(\d+)\s*/\s*100',
            r'score\s+(?:of\s+)?(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return max(0, min(100, score))
        return 50  # Default mid-level

    async def _ask_claude(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
    ) -> str:
        """Ask Claude a question."""
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."

        try:
            response = self.claude.messages.create(
                model=model,
                max_tokens=4000,
                system=system or "You are a helpful career development assistant.",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
