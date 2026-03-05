"""
Launch & Landing Module.

Capabilities: launch plans, go/no-go assessment, post-launch reviews,
rollout planning, and landing scorecards.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PMLaunch:
    """Launch and landing capabilities for Product Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def create_launch_plan(self, feature: str, target_date: str) -> Dict:
        """Create a comprehensive launch plan."""
        prompt = f"""Create a product launch plan:

Feature: {feature}
Target Date: {target_date}

Include:
1. **Launch Checklist** (with owners and due dates):
   - Engineering readiness (code complete, QA, perf testing)
   - Design readiness (final assets, documentation)
   - Go-to-market (marketing, sales enablement, support training)
   - Legal/compliance (privacy review, terms, data handling)
   - Analytics (instrumentation, dashboards, alerts)
2. **Communication Plan**: Who to tell, when, and how
3. **Rollout Strategy**: Phased rollout with criteria for expansion
4. **Rollback Plan**: What triggers a rollback and how to execute
5. **Success Metrics**: Day 1, Week 1, Month 1 targets
6. **War Room Plan**: Who's on-call, escalation paths
7. **Post-Launch**: Review cadence and timeline"""

        response = await self._ask_claude(prompt, "You are a launch-experienced PM who has shipped features to millions of users.")
        return {"feature": feature, "target_date": target_date, "launch_plan": response, "timestamp": datetime.now().isoformat()}

    async def go_no_go_assessment(self, readiness_data: str) -> Dict:
        """Assess whether a launch should proceed."""
        prompt = f"""Conduct a Go/No-Go assessment:

Readiness Data:
{readiness_data}

Evaluate each dimension:
1. **Engineering** (Ready/Not Ready): Code quality, test coverage, perf
2. **Design** (Ready/Not Ready): UX testing, accessibility, polish
3. **Analytics** (Ready/Not Ready): Instrumentation, dashboards, alerts
4. **Support** (Ready/Not Ready): Documentation, training, staffing
5. **Legal** (Ready/Not Ready): Compliance, privacy, terms
6. **Marketing** (Ready/Not Ready): GTM materials, comms plan

**Overall Recommendation**: GO ✅ / CONDITIONAL GO ⚠️ / NO-GO ❌

If conditional:
- What must be true before launch
- Acceptable risks vs unacceptable risks
- Deadline for reassessment"""

        response = await self._ask_claude(prompt, "You are a VP Product making a launch decision.")
        return {"readiness": readiness_data, "assessment": response, "timestamp": datetime.now().isoformat()}

    async def post_launch_review(self, launch: str, metrics: str) -> Dict:
        """Conduct a post-launch review."""
        prompt = f"""Conduct a post-launch review:

Launch: {launch}
Results:
{metrics}

Structure:
1. **Executive Summary**: 3-sentence summary
2. **Goals vs Actuals**: Each goal and whether it was met
3. **What Went Well**: Things to repeat
4. **What Didn't Go Well**: Honest assessment of issues
5. **Root Causes**: Why things went wrong
6. **User Feedback**: Qualitative feedback themes
7. **Unexpected Outcomes**: Surprises (good and bad)
8. **Impact Assessment**: Business and user impact
9. **Action Items**: Specific follow-ups with owners
10. **Landing Plan**: What's needed to fully realize the value"""

        response = await self._ask_claude(prompt, "You are a senior PM conducting an honest post-launch review.")
        return {"launch": launch, "review": response, "timestamp": datetime.now().isoformat()}

    async def create_rollout_plan(self, feature: str, segments: List[str]) -> Dict:
        """Create a phased rollout plan."""
        segments_text = ", ".join(segments)
        prompt = f"""Create a phased rollout plan:

Feature: {feature}
Segments: {segments_text}

For each phase:
1. **Phase Name**: Descriptive name
2. **Audience**: Who gets access and why they're first
3. **% Rollout**: Percentage of traffic/users
4. **Duration**: How long before expanding
5. **Success Criteria**: Metrics that must be met to proceed
6. **Kill Criteria**: Metrics that would trigger a pause
7. **Monitoring**: What to watch closely
8. **Communication**: How to notify users in this phase

Also include:
- **Feature Flags**: Flag naming and configuration
- **Experiment Design**: A/B test setup if applicable
- **Emergency Procedures**: How to quickly disable"""

        response = await self._ask_claude(prompt, "You are a senior PM experienced with gradual rollouts at scale.")
        return {"feature": feature, "segments": segments, "rollout_plan": response, "timestamp": datetime.now().isoformat()}

    async def landing_scorecard(self, launch: str, goals: Dict) -> Dict:
        """Create a landing scorecard to assess final impact."""
        import json
        goals_text = json.dumps(goals, indent=2)
        prompt = f"""Create a landing scorecard:

Launch: {launch}
Goals:
{goals_text}

Evaluate 30/60/90 day performance:
1. **Adoption Scorecard**: Sign-ups, activation, retention vs targets
2. **Quality Scorecard**: Bug reports, performance, reliability
3. **Business Scorecard**: Revenue, cost, efficiency impact
4. **User Satisfaction**: NPS/CSAT change, qualitative sentiment
5. **Overall Landing Grade**: Fully Landed / Partially Landed / Not Landed
6. **Gap Analysis**: What's preventing full landing
7. **Remediation Plan**: What to do to close the gaps"""

        response = await self._ask_claude(prompt, "You are a PM evaluating whether a launched product has fully 'landed'.")
        return {"launch": launch, "scorecard": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929", max_tokens=4000,
                system=system, messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
