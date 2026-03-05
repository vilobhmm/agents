"""
Stakeholder Management Module.

Capabilities: stakeholder mapping (RACI), PRD writing, exec summaries,
alignment checks, and status updates.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PMStakeholders:
    """Stakeholder management capabilities for Product Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def stakeholder_map(self, project: str, stakeholders: Optional[List[str]] = None) -> Dict:
        """Create a stakeholder map with RACI matrix."""
        stakeholders_text = ""
        if stakeholders:
            stakeholders_text = "\nKnown Stakeholders: " + ", ".join(stakeholders)

        prompt = f"""Create a stakeholder map for: {project}{stakeholders_text}

Provide:
1. **Stakeholder Identification**: All relevant stakeholders by function
2. **Influence/Interest Matrix**: Classify each as:
   - High Influence / High Interest → Manage Closely
   - High Influence / Low Interest → Keep Satisfied
   - Low Influence / High Interest → Keep Informed
   - Low Influence / Low Interest → Monitor
3. **RACI Matrix**: For key decisions/deliverables
   - R (Responsible), A (Accountable), C (Consulted), I (Informed)
4. **Communication Plan**: Frequency and format per stakeholder
5. **Risk Assessment**: Political risks and mitigation
6. **Engagement Strategy**: How to get and maintain buy-in"""

        response = await self._ask_claude(prompt, "You are an organizational effectiveness consultant specializing in stakeholder management.")
        return {"project": project, "stakeholder_map": response, "timestamp": datetime.now().isoformat()}

    async def create_prd(self, feature: str, context: str) -> Dict:
        """Create a Product Requirements Document."""
        prompt = f"""Write a Product Requirements Document (PRD):

Feature: {feature}
Context: {context}

Structure:
1. **Overview**: Problem statement, goals, non-goals
2. **Background**: Why now, what's changed, user need evidence
3. **User Stories**: As a [user], I want [action], so that [benefit]
4. **Requirements**:
   - Functional (P0, P1, P2)
   - Non-functional (performance, security, accessibility)
5. **Design**: High-level UX flows (describe, don't draw)
6. **Technical Considerations**: Architecture implications, dependencies
7. **Metrics**: Success criteria with specific targets
8. **Launch Plan**: Rollout strategy, feature flags, A/B tests
9. **Risks & Mitigations**: What could go wrong
10. **Open Questions**: Decisions still needed
11. **Timeline**: Key milestones and dates
12. **Appendix**: Research data, competitive analysis"""

        response = await self._ask_claude(prompt, "You are a senior PM at a top tech company writing product specs.")
        return {"feature": feature, "prd": response, "timestamp": datetime.now().isoformat()}

    async def write_exec_summary(self, project: str, audience: str) -> Dict:
        """Write an executive summary tailored to the audience."""
        prompt = f"""Write an executive summary:

Project: {project}
Audience: {audience}

Structure:
1. **TL;DR**: 2-3 sentence summary
2. **Problem**: What we're solving and why it matters (with data)
3. **Recommendation**: What we're proposing
4. **Impact**: Expected business and user impact
5. **Investment**: Resources, timeline, and cost
6. **Risks**: Top 3 risks with mitigation
7. **Ask**: What you need from this audience (decision, resources, alignment)

Keep it to one page. Lead with the conclusion. Use data."""

        response = await self._ask_claude(prompt, f"You are a PM presenting to {audience}. Be concise and impactful.")
        return {"project": project, "audience": audience, "summary": response, "timestamp": datetime.now().isoformat()}

    async def alignment_check(self, proposal: str, stakeholders: List[str]) -> Dict:
        """Assess alignment risks for a proposal."""
        stakeholders_text = ", ".join(stakeholders)
        prompt = f"""Assess alignment risks for this proposal:

Proposal: {proposal}
Key Stakeholders: {stakeholders_text}

Analyze:
1. **Likely Supporters**: Who will champion this and why
2. **Likely Resistors**: Who might push back and why
3. **Fence-Sitters**: Who's undecided and what they need
4. **Objections**: Top 5 objections you'll face
5. **Counter-Arguments**: How to address each objection
6. **Pre-Work Needed**: Conversations to have before the decision
7. **Decision Strategy**: How to structure the decision process
8. **Escalation Path**: If alignment can't be reached"""

        response = await self._ask_claude(prompt, "You are an organizational strategist skilled at navigating complex stakeholder dynamics.")
        return {"proposal": proposal, "alignment_check": response, "timestamp": datetime.now().isoformat()}

    async def status_update(self, project: str, audience: str, details: Optional[str] = None) -> Dict:
        """Generate a project status update."""
        details_text = f"\n\nProject Details: {details}" if details else ""
        prompt = f"""Write a project status update:

Project: {project}
Audience: {audience}{details_text}

Format (keep concise):
1. **Status**: 🟢 On Track / 🟡 At Risk / 🔴 Blocked
2. **Summary**: 2-3 sentences on current state
3. **Progress This Period**: Key accomplishments (bullet points)
4. **Next Period**: What's coming up
5. **Risks & Blockers**: Issues needing attention
6. **Decisions Needed**: Any asks from the audience
7. **Metrics Update**: Key metrics and their trends

Keep this to half a page maximum."""

        response = await self._ask_claude(prompt, f"You are a PM writing a status update for {audience}.")
        return {"project": project, "audience": audience, "update": response, "timestamp": datetime.now().isoformat()}

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
