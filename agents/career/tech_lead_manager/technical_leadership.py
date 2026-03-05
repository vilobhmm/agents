"""
Technical Leadership Module.

Capabilities: technical vision, ADRs, tech stack evaluation,
code health assessment, sprint planning.
"""

import os, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TLMTechnicalLeadership:
    """Technical leadership capabilities for Tech Lead Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def technical_vision(self, team: str, domain: str) -> Dict:
        """Create a technical vision document."""
        prompt = f"""Create a technical vision for:

Team: {team}
Domain: {domain}

Structure:
1. **Current State**: Where we are technically
2. **North Star**: Where we want to be in 2-3 years
3. **Key Principles**: 5-7 engineering principles to guide decisions
4. **Strategic Bets**: 3-5 major technical investments
5. **Architecture Evolution**: How the system should evolve
6. **Platform Investments**: Shared infrastructure to build
7. **Technical Debt Strategy**: How to manage debt alongside features
8. **Quality Bar**: Engineering standards and practices
9. **Innovation Time**: How to foster technical exploration
10. **Success Metrics**: Technical health KPIs"""

        response = await self._ask_claude(prompt, "You are a VP Engineering setting technical direction.")
        return {"team": team, "domain": domain, "vision": response, "timestamp": datetime.now().isoformat()}

    async def architecture_decision_record(self, decision: str, context: str) -> Dict:
        """Create an Architecture Decision Record (ADR)."""
        prompt = f"""Write an ADR:

Decision: {decision}
Context: {context}

Format:
1. **Title**: ADR-XXX: {decision}
2. **Status**: Proposed
3. **Context**: Why this decision is needed
4. **Decision**: What we're deciding
5. **Consequences**: Positive, negative, and neutral
6. **Alternatives Considered**: 2-3 alternatives with pros/cons
7. **Decision Criteria**: How we evaluated options
8. **Implementation Notes**: How to carry this out
9. **Review Date**: When to reassess this decision"""

        response = await self._ask_claude(prompt, "You are a principal engineer documenting architectural decisions.")
        return {"decision": decision, "adr": response, "timestamp": datetime.now().isoformat()}

    async def tech_stack_evaluation(self, requirements: str, options: List[str]) -> Dict:
        """Evaluate tech stack options."""
        options_text = ", ".join(options)
        prompt = f"""Evaluate technology options:

Requirements: {requirements}
Options: {options_text}

For each option:
1. **Fit Score** (1-10): How well it meets requirements
2. **Pros**: Key advantages
3. **Cons**: Key disadvantages
4. **Maturity**: Ecosystem health, community, documentation
5. **Team Readiness**: Learning curve, hiring market
6. **Operational Cost**: Infrastructure and maintenance burden
7. **Lock-in Risk**: How hard to migrate away

**Recommendation**: Which option and why
**Migration Path**: If switching from current stack"""

        response = await self._ask_claude(prompt, "You are a tech lead evaluating technology choices.")
        return {"requirements": requirements, "options": options, "evaluation": response, "timestamp": datetime.now().isoformat()}

    async def sprint_planning(self, backlog: str, capacity: str) -> Dict:
        """Plan a sprint from backlog and capacity."""
        prompt = f"""Plan a 2-week sprint:

Backlog: {backlog}
Team Capacity: {capacity}

Provide:
1. **Sprint Goal**: Clear, measurable goal
2. **Selected Items**: Stories with estimates (story points)
3. **Capacity Allocation**: % features vs tech debt vs bugs
4. **Dependencies**: External dependencies and how to manage
5. **Risks**: What could block the sprint
6. **Stretch Goals**: If everything goes well
7. **Definition of Done**: Quality criteria for each item"""

        response = await self._ask_claude(prompt, "You are a tech lead planning a sprint for your team.")
        return {"sprint_plan": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            r = self.claude.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=4000, system=system, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
