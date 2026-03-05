"""
Experimentation & Publication Modules.

Covers: experiment design, statistical analysis, results interpretation,
paper outlines, abstracts, peer review responses, and grant proposals.
"""

import os, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ScientistExperimentation:
    """Experiment design, data analysis, and publication capabilities."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def design_experiment(self, hypothesis: str, constraints: Optional[str] = None) -> Dict:
        """Design a rigorous experiment."""
        const_text = f"\nConstraints: {constraints}" if constraints else ""
        prompt = f"""Design an experiment:

Hypothesis: {hypothesis}{const_text}

Provide complete protocol:
1. **Objective**: Clear experimental goal
2. **Method**: Step-by-step procedure
3. **Controls**: Positive, negative, and internal controls
4. **Variables**: IV, DV, controlled variables
5. **Sample Size**: Power analysis and justification
6. **Statistical Analysis Plan**: Tests to use, significance level
7. **Timeline**: Duration estimate per phase
8. **Success Criteria**: What results support/reject hypothesis
9. **Potential Pitfalls**: What could go wrong and mitigation"""

        response = await self._ask_claude(prompt, "You are an experimental scientist designing rigorous studies.")
        return {"hypothesis": hypothesis, "protocol": response, "timestamp": datetime.now().isoformat()}

    async def analyze_results(self, data_description: str) -> Dict:
        """Analyze experimental results."""
        prompt = f"""Analyze these results:

{data_description}

Provide:
1. **Descriptive Statistics**: Summary measures
2. **Hypothesis Test Results**: Which tests, p-values, effect sizes
3. **Visualization Suggestions**: Best plots for this data
4. **Interpretation**: What the results mean
5. **Limitations**: Caveats and confounds
6. **Next Steps**: Follow-up experiments suggested"""

        response = await self._ask_claude(prompt, "You are a biostatistician analyzing experimental data.")
        return {"analysis": response, "timestamp": datetime.now().isoformat()}

    async def paper_outline(self, research: str, venue: str = "top conference") -> Dict:
        """Create a research paper outline."""
        prompt = f"""Create a paper outline for {venue}:

Research: {research}

Structure (following venue standards):
1. **Title**: Compelling and descriptive
2. **Abstract**: 150-250 words covering problem, method, results, impact
3. **Introduction**: Context, problem, contribution, paper organization
4. **Related Work**: How this fits in the literature
5. **Methodology**: Technical approach (with subsections)
6. **Experiments**: Setup, baselines, metrics, results
7. **Discussion**: Interpretation, limitations, broader implications
8. **Conclusion**: Summary and future work
9. **Key Figures/Tables**: What visualizations to include"""

        response = await self._ask_claude(prompt, "You are a prolific researcher who publishes at top venues.")
        return {"venue": venue, "outline": response, "timestamp": datetime.now().isoformat()}

    async def write_abstract(self, research_summary: str) -> Dict:
        """Write a research paper abstract."""
        prompt = f"""Write an abstract (150-250 words):

Research: {research_summary}

Structure:
1. **Context**: Why this matters (1-2 sentences)
2. **Problem**: Specific gap/challenge
3. **Approach**: Your method (key innovation highlighted)
4. **Results**: Main findings (with numbers)
5. **Impact**: Why this matters for the field"""

        response = await self._ask_claude(prompt, "You are an experienced academic writer.")
        return {"abstract": response, "timestamp": datetime.now().isoformat()}

    async def peer_review_response(self, reviews: str) -> Dict:
        """Draft a response to peer review."""
        prompt = f"""Draft a peer review response:

Reviews:
{reviews}

For each reviewer concern:
1. **Acknowledge**: Thank and restate the concern
2. **Response**: Direct, specific answer
3. **Changes Made**: What was changed in the paper (quote new text)
4. **Justification**: If not changing, explain why respectfully

Be professional, thorough, and constructive."""

        response = await self._ask_claude(prompt, "You are a seasoned researcher responding to peer review.")
        return {"response": response, "timestamp": datetime.now().isoformat()}

    async def grant_proposal(self, research_plan: str) -> Dict:
        """Create a grant proposal structure."""
        prompt = f"""Create a grant proposal:

Research Plan: {research_plan}

Structure:
1. **Project Summary**: 1-page overview
2. **Specific Aims**: 3-4 concrete aims
3. **Significance**: Why this research matters
4. **Innovation**: What's new about this approach
5. **Approach**: Detailed methodology per aim
6. **Timeline & Milestones**: Gantt chart description
7. **Budget Justification**: Key cost categories
8. **Broader Impacts**: Societal and training impacts
9. **Preliminary Data**: Supporting evidence you have"""

        response = await self._ask_claude(prompt, "You are a grant writing expert with high success rates.")
        return {"proposal": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            r = self.claude.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=4000, system=system, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
