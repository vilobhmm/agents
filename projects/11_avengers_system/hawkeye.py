"""
Hawkeye - Newsletter & Intelligence Distillation Agent

Filters everything into clarity.
One shot. No fluff.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from anthropic import Anthropic

from .coordination import AgentReport, CoordinationHub, coordination_hub

logger = logging.getLogger(__name__)


class HawkeyeAgent:
    """
    Hawkeye - Newsletter & Intelligence Distillation

    Converts research + prototypes into structured communication:
    - Weekly AI digest
    - Research summaries
    - Prototype highlights
    - Clean narrative flow

    Core principle: "One shot. No fluff."
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Hawkeye"
        self.emoji = "🎯"
        self.agent_key = "hawkeye"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub

        self.newsletters = []

        logger.info(f"{self.emoji} {self.name} initialized")

    async def generate_weekly_newsletter(self) -> str:
        """
        Generate weekly newsletter from all agent activities

        Returns:
            str: Newsletter content (markdown)
        """
        logger.info(f"{self.emoji} Generating weekly newsletter...")

        # Gather intelligence from last 7 days
        week_ago = datetime.now() - timedelta(days=7)

        # Get research from Captain America
        research_entries = self.coordination.knowledge_base.get_by_source(
            "captain_america"
        )
        weekly_research = [
            e
            for e in research_entries
            if datetime.fromisoformat(e["timestamp"]) > week_ago
        ]

        # Get prototypes from Hulk
        hulk_entries = self.coordination.knowledge_base.get_by_source("hulk")
        weekly_prototypes = [
            e
            for e in hulk_entries
            if datetime.fromisoformat(e["timestamp"]) > week_ago
        ]

        # Get social media activity
        thor_entries = self.coordination.knowledge_base.get_by_source("thor")
        black_widow_entries = self.coordination.knowledge_base.get_by_source(
            "black_widow"
        )

        # Use Claude to synthesize newsletter
        prompt = f"""You are Hawkeye, the newsletter curator for an AI research lab.

Generate a weekly newsletter from this week's activities:

RESEARCH INTELLIGENCE ({len(weekly_research)} reports):
{self._format_research(weekly_research[:10])}

PROTOTYPES BUILT ({len(weekly_prototypes)}):
{self._format_prototypes(weekly_prototypes[:5])}

SOCIAL ACTIVITY:
Twitter: {len(thor_entries)} posts
LinkedIn: {len(black_widow_entries)} articles

Create a newsletter with these sections:

# This Week in AI
[Executive summary - 2-3 sentences of what mattered]

## 🔬 Research Highlights
[Top 3 developments, with impact assessment]

## 🛠 Prototypes & Code
[Prototypes built this week, with links]

## 💡 Key Insights
[Strategic takeaways - bullet points]

## 📊 Activity Summary
[Stats and metrics]

## 🎯 Next Week
[What to watch for]

---
*Curated by Hawkeye | AI Research Lab*

Keep it:
- Signal-only (no fluff)
- Actionable
- Clear narrative
- Professional but accessible

Output the newsletter in clean markdown."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        newsletter = response.content[0].text.strip()

        # Store newsletter
        newsletter_data = {
            "content": newsletter,
            "week": datetime.now().strftime("%Y-W%W"),
            "timestamp": datetime.now(),
        }

        self.newsletters.append(newsletter_data)

        # Store in knowledge base
        self.coordination.knowledge_base.add_entry(
            key=f"newsletter_{newsletter_data['week']}",
            value=newsletter_data,
            source=self.agent_key,
        )

        logger.info(f"{self.emoji} Newsletter generated: Week {newsletter_data['week']}")

        return newsletter

    def _format_research(self, entries: List[dict]) -> str:
        """Format research entries for prompt"""
        if not entries:
            return "No research this week"

        formatted = []
        for entry in entries[:5]:  # Top 5
            if "value" in entry and isinstance(entry["value"], dict):
                report = entry["value"]

                if "summary" in report:
                    formatted.append(f"• {report['summary'][:200]}")

        return "\n".join(formatted) if formatted else "No research this week"

    def _format_prototypes(self, entries: List[dict]) -> str:
        """Format prototype entries for prompt"""
        if not entries:
            return "No prototypes this week"

        formatted = []
        for entry in entries:
            if "value" in entry and isinstance(entry["value"], dict):
                proto = entry["value"]

                formatted.append(
                    f"• {proto.get('concept', 'Unknown')} - {proto.get('repo_url', '')}"
                )

        return "\n".join(formatted) if formatted else "No prototypes this week"

    async def send_newsletter(self, newsletter: str) -> bool:
        """
        Send newsletter (would integrate with email service)

        Args:
            newsletter: Newsletter content

        Returns:
            bool: Success status
        """
        # Placeholder - would integrate with email service like:
        # - Mailchimp
        # - SendGrid
        # - Substack API

        logger.info(f"{self.emoji} Newsletter ready to send")
        logger.info(f"Preview:\n{newsletter[:300]}...")

        # For now, just log
        return True

    async def weekly_generation_task(self):
        """
        Weekly newsletter generation task (runs Friday morning)
        """
        newsletter = await self.generate_weekly_newsletter()

        # Send newsletter
        await self.send_newsletter(newsletter)

    async def submit_status_report(self):
        """Submit status report"""
        report = AgentReport(
            agent_name=self.agent_key,
            status="Active",
            metrics={
                "newsletters_sent": len(self.newsletters),
                "last_newsletter": (
                    self.newsletters[-1]["week"] if self.newsletters else "Never"
                ),
            },
            next_action="Next newsletter: Friday 8 AM",
        )

        await self.coordination.submit_report(report)
