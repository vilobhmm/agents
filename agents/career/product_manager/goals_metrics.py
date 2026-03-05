"""
Goals, OKRs & Metrics Module.

Capabilities: OKR creation, north star definition, metrics frameworks,
dashboard specs, and launch success measurement.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PMGoalsMetrics:
    """Goal setting and metrics capabilities for Product Managers."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def create_okrs(self, vision: str, timeframe: str = "quarterly") -> Dict:
        """Create OKRs from a product vision."""
        prompt = f"""Create OKRs for this product vision:

Vision: {vision}
Timeframe: {timeframe}

Provide 3-5 Objectives, each with 3-4 Key Results:

For each Objective:
- **Objective**: Qualitative, inspirational goal
- **Key Results**: Quantitative, measurable outcomes
  - Format: "Increase X from Y to Z"
  - Must be specific and time-bound

Also include:
- **Leading Indicators**: Early signals of progress
- **Lagging Indicators**: Final outcome metrics
- **Health Metrics**: Guardrails to ensure quality isn't sacrificed
- **Scoring Guide**: How to grade 0.0 to 1.0

Follow Google's OKR best practices: ambitious (70% completion = success)."""

        response = await self._ask_claude(prompt, "You are an OKR coach who has implemented OKRs at Google, Intel, and multiple startups.")
        return {"vision": vision, "timeframe": timeframe, "okrs": response, "timestamp": datetime.now().isoformat()}

    async def define_north_star(self, product: str) -> Dict:
        """Define the North Star metric for a product."""
        prompt = f"""Define the North Star metric for: {product}

Provide:
1. **North Star Metric**: Single metric that captures core value delivery
2. **Why This Metric**: Why it reflects value creation for users AND business
3. **Input Metrics** (3-5): Levers that drive the North Star
4. **Counter Metrics** (2-3): Guardrails against gaming the metric
5. **Measurement**: How to calculate it, data sources needed
6. **Benchmarks**: What "good" looks like at different stages
7. **Frequency**: How often to review

Examples: Airbnb = Nights Booked, Spotify = Time Spent Listening, Slack = DAU/MAU."""

        response = await self._ask_claude(prompt, "You are a growth product manager expert in defining product metrics.")
        return {"product": product, "north_star": response, "timestamp": datetime.now().isoformat()}

    async def metrics_framework(self, product: str) -> Dict:
        """Create a comprehensive metrics framework."""
        prompt = f"""Create a metrics framework for: {product}

Structure using the HEART framework + pirate metrics:

**HEART Framework:**
- **Happiness**: User satisfaction metrics (NPS, CSAT, SUS)
- **Engagement**: Depth & frequency of use
- **Adoption**: New user onboarding metrics
- **Retention**: Cohort retention, churn rates
- **Task Success**: Core task completion rates

**Pirate Metrics (AARRR):**
- **Acquisition**: Where users come from
- **Activation**: First value moment
- **Retention**: Coming back
- **Revenue**: Monetization
- **Referral**: Word of mouth

For each metric:
- Definition and formula
- Data source
- Target/benchmark
- Alert threshold
- Review frequency"""

        response = await self._ask_claude(prompt, "You are a data-driven PM who builds metrics-driven product organizations.")
        return {"product": product, "framework": response, "timestamp": datetime.now().isoformat()}

    async def create_dashboard_spec(self, metrics: List[str]) -> Dict:
        """Design a product metrics dashboard."""
        metrics_text = "\n".join(f"- {m}" for m in metrics)
        prompt = f"""Design a product metrics dashboard:

Metrics to include:
{metrics_text}

Provide:
1. **Dashboard Layout**: Sections and visual hierarchy
2. **Chart Types**: Best visualization for each metric (line, bar, funnel, cohort, etc.)
3. **Timeframes**: Default view + available drill-downs
4. **Filters**: Required dimensions (segment, platform, geo, etc.)
5. **Alerts**: Thresholds for automated notifications
6. **Data Requirements**: Tables, queries, refresh frequency
7. **Executive Summary**: Auto-generated health score (green/yellow/red)"""

        response = await self._ask_claude(prompt, "You are a product analytics expert who designs dashboards.")
        return {"metrics": metrics, "dashboard_spec": response, "timestamp": datetime.now().isoformat()}

    async def measure_launch_success(self, launch: str, metrics: Dict) -> Dict:
        """Evaluate a product launch against success criteria."""
        import json
        metrics_text = json.dumps(metrics, indent=2)
        prompt = f"""Evaluate this product launch:

Launch: {launch}
Metrics Results:
{metrics_text}

Provide:
1. **Overall Grade**: A/B/C/D/F with justification
2. **Goals Met**: Which targets were hit, which were missed
3. **Bright Spots**: What went exceptionally well
4. **Issues**: Problems that emerged
5. **User Impact**: Qualitative assessment of user delight
6. **Business Impact**: Revenue, efficiency, strategic value
7. **Lessons Learned**: What to do differently next time
8. **Follow-up Actions**: Immediate next steps (bugs, iterations, optimizations)
9. **Landing Plan**: What's needed to fully "land" this launch"""

        response = await self._ask_claude(prompt, "You are a senior PM evaluating product launches.")
        return {"launch": launch, "metrics": metrics, "evaluation": response, "timestamp": datetime.now().isoformat()}

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
