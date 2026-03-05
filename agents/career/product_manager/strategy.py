"""
Product Strategy & Vision Module.

Capabilities: product vision, strategic planning, competitive analysis, market sizing.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PMStrategy:
    """Product strategy and vision capabilities for Product Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def define_product_vision(
        self, problem: str, users: str, market: str
    ) -> Dict:
        """
        Define a compelling product vision.

        Args:
            problem: The problem being solved
            users: Target users/personas
            market: Target market/industry

        Returns:
            Vision document with north star, principles, and success criteria
        """
        prompt = f"""Define a product vision:

Problem: {problem}
Target Users: {users}
Market: {market}

Provide:
1. **Vision Statement**: One sentence that inspires (like Amazon's "Earth's most customer-centric company")
2. **Mission**: How you'll achieve the vision
3. **Product Principles** (5-7): Guiding principles for decisions
4. **Value Proposition**: Clear articulation of unique value
5. **Success Criteria**: How you'll know you've achieved the vision
6. **Anti-Goals**: What you explicitly won't do
7. **3-Year Outlook**: Where the product should be in 3 years"""

        response = await self._ask_claude(prompt, "You are a visionary product leader at a top tech company.")
        return {"problem": problem, "users": users, "vision": response, "timestamp": datetime.now().isoformat()}

    async def create_product_strategy(
        self, vision: str, timeframe: str = "12 months"
    ) -> Dict:
        """
        Create a product strategy from vision to execution.

        Args:
            vision: Product vision statement
            timeframe: Planning horizon

        Returns:
            Strategic plan with pillars, bets, and sequencing
        """
        prompt = f"""Create a product strategy:

Vision: {vision}
Timeframe: {timeframe}

Structure:
1. **Strategic Pillars** (3-5): Major themes of investment
2. **Key Bets**: High-risk/high-reward initiatives per pillar
3. **Sequencing**: What to build first, second, third (and why)
4. **Dependencies**: Critical dependencies and how to unblock them
5. **Resource Allocation**: How to divide eng/design/data capacity
6. **Risk Register**: Top 5 strategic risks with mitigation
7. **Success Metrics**: KPIs per pillar
8. **Review Cadence**: When and how to reassess strategy"""

        response = await self._ask_claude(prompt, "You are a VP Product at a growth-stage tech company.")
        return {"vision": vision, "strategy": response, "timestamp": datetime.now().isoformat()}

    async def competitive_analysis(
        self, product: str, competitors: List[str]
    ) -> Dict:
        """
        Conduct competitive analysis.

        Args:
            product: Your product description
            competitors: List of competitor names/products

        Returns:
            Competitive landscape with positioning and differentiation
        """
        competitors_text = ", ".join(competitors)
        prompt = f"""Competitive analysis:

Your Product: {product}
Competitors: {competitors_text}

Analyze:
1. **Feature Comparison Matrix**: Your product vs each competitor across key dimensions
2. **Positioning Map**: Where each product sits (axes: price vs capability, or similar)
3. **Competitive Advantages**: Your unique strengths
4. **Competitive Gaps**: Where competitors are ahead
5. **Threat Assessment**: Which competitor is the biggest threat and why
6. **Differentiation Strategy**: How to win against each
7. **Market Trends**: Where the market is heading
8. **Recommended Actions**: Top 5 strategic moves"""

        response = await self._ask_claude(prompt, "You are a competitive intelligence analyst in tech.")
        return {"product": product, "competitors": competitors, "analysis": response, "timestamp": datetime.now().isoformat()}

    async def market_sizing(self, product: str, industry: str) -> Dict:
        """
        Estimate market size (TAM/SAM/SOM).

        Args:
            product: Product description
            industry: Target industry

        Returns:
            Market sizing with methodology and assumptions
        """
        prompt = f"""Market sizing analysis:

Product: {product}
Industry: {industry}

Provide:
1. **TAM** (Total Addressable Market): Global opportunity
2. **SAM** (Serviceable Addressable Market): Reachable segment
3. **SOM** (Serviceable Obtainable Market): Realistic capture in 3 years
4. **Methodology**: Top-down and bottom-up calculations
5. **Key Assumptions**: What you're assuming and sensitivity analysis
6. **Growth Rate**: CAGR and growth drivers
7. **Market Dynamics**: Tailwinds and headwinds
8. **Comparable Markets**: Reference points from adjacent markets

Use specific numbers and cite reasoning."""

        response = await self._ask_claude(prompt, "You are a market research analyst specializing in technology markets.")
        return {"product": product, "industry": industry, "sizing": response, "timestamp": datetime.now().isoformat()}

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
