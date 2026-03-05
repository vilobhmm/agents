"""
Market & User Research Module.

Capabilities: user research planning, feedback analysis, personas,
journey mapping, market trend analysis.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PMResearch:
    """Market and user research capabilities for Product Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def user_research_plan(self, product: str, questions: List[str]) -> Dict:
        """
        Create a user research plan.

        Args:
            product: Product/feature being researched
            questions: Key research questions

        Returns:
            Research methodology with interview guides and survey design
        """
        questions_text = "\n".join(f"- {q}" for q in questions)
        prompt = f"""Create a user research plan:

Product: {product}
Key Questions:
{questions_text}

Provide:
1. **Research Objectives**: What we need to learn
2. **Methodology Mix**: Qualitative + quantitative methods
   - User interviews (how many, who, guide)
   - Surveys (sample size, distribution)
   - Usability testing (tasks, metrics)
   - Analytics review (what data to pull)
3. **Participant Criteria**: Who to recruit and how
4. **Interview Guide**: 15-20 questions (open-ended, probing)
5. **Survey Design**: Key questions with response types
6. **Timeline**: Week-by-week execution plan
7. **Analysis Framework**: How to synthesize findings
8. **Deliverables**: What outputs to produce"""

        response = await self._ask_claude(prompt, "You are a UX researcher with 10+ years of experience in product research.")
        return {"product": product, "research_plan": response, "timestamp": datetime.now().isoformat()}

    async def analyze_user_feedback(self, feedback_data: str) -> Dict:
        """
        Analyze user feedback to extract themes and priorities.

        Args:
            feedback_data: Raw feedback (reviews, tickets, interviews, NPS comments)

        Returns:
            Themed analysis with prioritized insights
        """
        prompt = f"""Analyze this user feedback:

{feedback_data}

Provide:
1. **Themes** (ranked by frequency):
   - Theme name, frequency, sentiment, representative quotes
2. **Sentiment Analysis**: Overall and per-theme
3. **Pain Points** (ranked by severity): What frustrates users most
4. **Unmet Needs**: What users want but don't have
5. **Delighters**: What users love
6. **Feature Requests**: Specific asks with priority
7. **User Segments**: Different user types with different needs
8. **Actionable Insights**: Top 5 things to do based on this feedback
9. **Quick Wins**: Changes that would have immediate impact"""

        response = await self._ask_claude(prompt, "You are a product insights analyst expert at mining user feedback for actionable insights.")
        return {"analysis": response, "timestamp": datetime.now().isoformat()}

    async def create_persona(self, research_data: str) -> Dict:
        """
        Create a user persona from research data.

        Args:
            research_data: Qualitative research findings

        Returns:
            Detailed user persona
        """
        prompt = f"""Create a detailed user persona based on this research:

{research_data}

Include:
1. **Name & Photo Description**: Realistic fictional person
2. **Demographics**: Age, role, company size, tech savviness
3. **Goals**: What they're trying to achieve (3-5)
4. **Frustrations**: What blocks them (3-5)
5. **Behaviors**: How they currently work, tools they use
6. **Motivations**: What drives their decisions
7. **Quote**: A characteristic quote that captures their mindset
8. **Day in the Life**: Typical workday narrative
9. **Product Relationship**: How they'd discover, evaluate, and use our product
10. **Decision Criteria**: What matters most when choosing a solution"""

        response = await self._ask_claude(prompt, "You are a UX researcher specializing in persona development.")
        return {"persona": response, "timestamp": datetime.now().isoformat()}

    async def journey_map(self, persona: str, product: str) -> Dict:
        """
        Create a user journey map.

        Args:
            persona: User persona description
            product: Product being mapped

        Returns:
            Journey map with stages, emotions, pain points, and opportunities
        """
        prompt = f"""Create a user journey map:

Persona: {persona}
Product: {product}

Map these stages:
1. **Awareness**: How they discover the product
2. **Evaluation**: How they assess fit
3. **Onboarding**: First-time experience
4. **Regular Use**: Day-to-day workflow
5. **Advanced Use**: Power user behaviors
6. **Advocacy**: How they become champions

For each stage provide:
- **Actions**: What the user does
- **Thinking**: What's on their mind
- **Emotions**: How they feel (😊😐😞)
- **Pain Points**: Frustrations at this stage
- **Opportunities**: How to improve the experience
- **Touchpoints**: Where they interact with the product
- **Metrics**: How to measure success at this stage"""

        response = await self._ask_claude(prompt, "You are a service designer and CX strategist.")
        return {"persona": persona, "product": product, "journey_map": response, "timestamp": datetime.now().isoformat()}

    async def market_trend_analysis(self, industry: str) -> Dict:
        """
        Analyze market trends for an industry.

        Args:
            industry: Industry to analyze

        Returns:
            Trends analysis with opportunities and threats
        """
        prompt = f"""Analyze current market trends in: {industry}

Cover:
1. **Macro Trends**: Broad technological and societal shifts
2. **Industry Trends**: Specific to this market
3. **Customer Behavior Shifts**: How buyer preferences are changing
4. **Technology Enablers**: New tech creating opportunities
5. **Regulatory Changes**: Policy/compliance shifts
6. **Competitive Dynamics**: How the competitive landscape is evolving
7. **Emerging Categories**: New product categories forming
8. **Opportunities**: Top 5 opportunities based on trends
9. **Threats**: Top 5 threats to existing players
10. **Predictions**: 3-year outlook"""

        response = await self._ask_claude(prompt, "You are an industry analyst covering technology markets.")
        return {"industry": industry, "trends": response, "timestamp": datetime.now().isoformat()}

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
