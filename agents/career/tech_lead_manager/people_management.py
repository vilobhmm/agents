"""
People Management & Cross-Functional Modules.

Covers: 1:1 prep, performance reviews, career development, team health,
hiring plans, feedback, project plans, risk assessment, status reports, post-mortems.
"""

import os, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TLMPeopleManagement:
    """People management and cross-functional coordination for TLMs."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    # ── People Management ────────────────────────────────────────

    async def one_on_one_prep(self, report: str, context: str) -> Dict:
        """Prepare for a 1:1 meeting."""
        prompt = f"""Prepare a 1:1 agenda:

Report: {report}
Context: {context}

Structure:
1. **Check-In**: How they're doing (personal + professional)
2. **Progress Review**: What they've accomplished since last 1:1
3. **Blockers**: What's in their way
4. **Growth Discussion**: Career development, skill building
5. **Feedback**: Specific feedback to give (SBI format)
6. **Coaching Questions**: Open-ended questions to help them think
7. **Action Items**: Follow-ups from last meeting
8. **Notes Section**: Space for key takeaways"""

        response = await self._ask_claude(prompt, "You are an experienced engineering manager preparing for a 1:1.")
        return {"report": report, "agenda": response, "timestamp": datetime.now().isoformat()}

    async def performance_review(self, evidence: str, expectations: str) -> Dict:
        """Write a performance review."""
        prompt = f"""Write a performance review:

Evidence: {evidence}
Level Expectations: {expectations}

Structure:
1. **Summary**: Overall assessment (2-3 sentences)
2. **Strengths**: 3-5 specific strengths with examples
3. **Growth Areas**: 2-3 areas for improvement with specific feedback
4. **Impact**: Key contributions and their business impact
5. **Rating Rationale**: Justification for performance rating
6. **Development Plan**: Next quarter focus areas
7. **Career Discussion**: Trajectory and next steps

Use specific examples. Be honest but constructive. Follow SBI (Situation-Behavior-Impact) format."""

        response = await self._ask_claude(prompt, "You are a manager writing a fair, calibrated performance review.")
        return {"review": response, "timestamp": datetime.now().isoformat()}

    async def career_development_plan(self, report: str, aspirations: str) -> Dict:
        """Create a career development plan."""
        prompt = f"""Create a career development plan:

Engineer: {report}
Aspirations: {aspirations}

Include:
1. **Current State**: Skills and level assessment
2. **Target State**: Where they want to be in 12-18 months
3. **Skill Gaps**: What needs development
4. **Development Activities**:
   - Projects: Stretch assignments to pursue
   - Learning: Courses, books, conferences
   - Mentoring: Who to learn from
   - Visibility: How to increase impact and exposure
5. **Milestones**: Quarterly checkpoints
6. **Manager Support**: How you'll help enable growth
7. **Success Criteria**: How to know they're on track"""

        response = await self._ask_claude(prompt, "You are a manager who excels at developing engineers' careers.")
        return {"plan": response, "timestamp": datetime.now().isoformat()}

    async def team_health_check(self, signals: str) -> Dict:
        """Assess team health from signals."""
        prompt = f"""Assess team health:

Signals: {signals}

Evaluate these dimensions (🟢🟡🔴):
1. **Psychological Safety**: Can people speak up?
2. **Velocity**: Is the team shipping effectively?
3. **Quality**: Are they building well?
4. **Sustainability**: Is pace sustainable?
5. **Growth**: Are individuals developing?
6. **Collaboration**: Do they work well together?
7. **Alignment**: Are they working on the right things?
8. **Satisfaction**: Are people happy and engaged?

For each dimension:
- Rating with reasoning
- Warning signs to watch
- Recommended actions"""

        response = await self._ask_claude(prompt, "You are an experienced engineering leader assessing team health.")
        return {"health_check": response, "timestamp": datetime.now().isoformat()}

    async def hiring_plan(self, roadmap: str, team: str) -> Dict:
        """Create a hiring plan."""
        prompt = f"""Create a hiring plan:

Product Roadmap: {roadmap}
Current Team: {team}

Provide:
1. **Gap Analysis**: Skills needed vs current team
2. **Role Priorities**: Ranked hiring order with timing
3. **Job Descriptions**: For top 2-3 roles
4. **Sourcing Strategy**: Where to find candidates
5. **Interview Process**: Stages and what to assess
6. **Assessment Criteria**: Technical and cultural bar
7. **Timeline**: Realistic hiring timeline per role
8. **Onboarding Plan**: First 30/60/90 days for new hires"""

        response = await self._ask_claude(prompt, "You are an engineering manager building a world-class team.")
        return {"hiring_plan": response, "timestamp": datetime.now().isoformat()}

    # ── Cross-Functional ─────────────────────────────────────────

    async def project_plan(self, requirements: str, dependencies: str) -> Dict:
        """Create a cross-functional project plan."""
        prompt = f"""Create a project plan:

Requirements: {requirements}
Dependencies: {dependencies}

Include:
1. **Project Charter**: Scope, goals, non-goals
2. **Work Breakdown**: Tasks with estimates and owners
3. **Critical Path**: Dependencies and timeline
4. **Resource Plan**: Who's needed when
5. **Risk Register**: Risks with probability and mitigation
6. **Communication Plan**: Stakeholder updates cadence
7. **Milestones**: Key checkpoints with go/no-go criteria
8. **Escalation Path**: When and how to escalate"""

        response = await self._ask_claude(prompt, "You are a tech lead managing a cross-functional project.")
        return {"plan": response, "timestamp": datetime.now().isoformat()}

    async def post_mortem(self, incident: str) -> Dict:
        """Conduct a blameless post-mortem."""
        prompt = f"""Write a blameless post-mortem:

Incident: {incident}

Structure:
1. **Summary**: What happened, impact, duration
2. **Timeline**: Minute-by-minute events
3. **Root Cause Analysis**: 5 Whys
4. **Contributing Factors**: What made it worse
5. **What Went Well**: Effective response actions
6. **What Could Be Improved**: Process gaps
7. **Action Items**: Preventive measures (with owners and dates)
8. **Learnings**: Key takeaways for the team

Tone: Blameless, focused on systems not people."""

        response = await self._ask_claude(prompt, "You are an engineering leader conducting a blameless post-mortem.")
        return {"post_mortem": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            r = self.claude.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=4000, system=system, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
