"""
Literature Review & Hypothesis Module.

Capabilities: literature reviews, hypothesis generation, research gap analysis, paper critique.
"""

import os, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ScientistLiterature:
    """Literature and hypothesis capabilities for Research Scientists."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def literature_review(self, topic: str, depth: str = "comprehensive") -> Dict:
        """Conduct a structured literature review."""
        prompt = f"""Conduct a {depth} literature review on: {topic}

Provide:
1. **Summary**: Current state of research (2-3 paragraphs)
2. **Key Papers**: 10-15 seminal and recent papers (title, authors, year, contribution)
3. **Research Themes**: Major themes and schools of thought
4. **Methodologies**: Dominant experimental/theoretical approaches
5. **Research Gaps**: Open questions and under-explored areas
6. **Controversies**: Debates and unresolved disagreements
7. **Emerging Directions**: Where the field is heading
8. **Recommended Reading**: Top 5 papers to start with"""

        response = await self._ask_claude(prompt, "You are a research scientist conducting a thorough literature review.")
        return {"topic": topic, "depth": depth, "review": response, "timestamp": datetime.now().isoformat()}

    async def generate_hypothesis(self, observation: str, domain: str, background: Optional[str] = None) -> Dict:
        """Generate testable scientific hypotheses."""
        bg = f"\nBackground: {background}" if background else ""
        prompt = f"""Generate testable hypotheses:

Observation: {observation}
Domain: {domain}{bg}

For each hypothesis (generate 3-5):
1. **Hypothesis Statement**: Clear, falsifiable
2. **Null Hypothesis**: What disproves it
3. **Predictions**: Expected outcomes if true
4. **Test Method**: How to experimentally verify
5. **Variables**: Independent, dependent, control
6. **Novelty**: How this differs from existing hypotheses
7. **Impact**: Why this matters if confirmed"""

        response = await self._ask_claude(prompt, "You are a creative scientist skilled at hypothesis generation.")
        return {"observation": observation, "domain": domain, "hypotheses": response, "timestamp": datetime.now().isoformat()}

    async def research_gap_analysis(self, field: str) -> Dict:
        """Identify research gaps and opportunities."""
        prompt = f"""Analyze research gaps in: {field}

Provide:
1. **Knowledge Gaps**: What we don't know yet
2. **Methodology Gaps**: Better methods needed
3. **Application Gaps**: Theory not yet applied to practice
4. **Data Gaps**: Missing datasets or benchmarks
5. **Interdisciplinary Gaps**: Connections not yet made
6. **Opportunity Ranking**: Most impactful gaps to address
7. **Feasibility Assessment**: Which gaps are tractable now
8. **Research Proposals**: 3 concrete research projects to fill top gaps"""

        response = await self._ask_claude(prompt, "You are a research director identifying high-impact research opportunities.")
        return {"field": field, "gaps": response, "timestamp": datetime.now().isoformat()}

    async def paper_critique(self, paper_text: str) -> Dict:
        """Critique a research paper."""
        prompt = f"""Critique this paper:

{paper_text[:3000]}

Provide:
1. **Summary**: Main contribution in 2-3 sentences
2. **Strengths**: What's well done
3. **Weaknesses**: Methodological or logical issues
4. **Validity**: Are the conclusions supported by the evidence?
5. **Significance**: How important is this contribution?
6. **Reproducibility**: Could others replicate this?
7. **Questions**: What you'd ask the authors
8. **Recommendation**: Accept / Revise / Reject (with justification)"""

        response = await self._ask_claude(prompt, "You are a peer reviewer at a top journal.")
        return {"critique": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            r = self.claude.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=4000, system=system, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
