"""
Captain America - Research & Intelligence Agent

Monitors frontier AI developments and produces intelligence reports.
Protects signal integrity by filtering noise.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import feedparser
import requests
from anthropic import Anthropic

from openclaw.tools.web_scraping import WebScrapingTool

from .coordination import AgentReport, CoordinationHub, TaskStatus, coordination_hub

logger = logging.getLogger(__name__)


class CaptainAmericaAgent:
    """
    Captain America - Research & Intelligence

    Runs structured research sweeps 3x daily across:
    - X/Twitter AI accounts
    - Hacker News
    - GitHub Trending
    - AI research labs blogs
    - arXiv papers

    Produces clean, verified intelligence reports.
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Captain America"
        self.emoji = "🛡"
        self.agent_key = "captain_america"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub
        self.scraper = WebScrapingTool()

        # Research sources
        self.sources = {
            "hacker_news": "https://hn.algolia.com/api/v1/search?tags=story&query=AI",
            "github_trending": "https://api.github.com/search/repositories?q=language:python+topic:ai&sort=stars&order=desc",
            "arxiv": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=20",
            "openai_blog": "https://openai.com/blog/rss",
            "anthropic_blog": "https://www.anthropic.com/news",
            "deepmind_blog": "https://deepmind.google/discover/blog/",
        }

        # Intelligence cache
        self.daily_intelligence: List[Dict] = []

        logger.info(f"{self.emoji} {self.name} initialized")

    async def run_research_sweep(self) -> dict:
        """
        Run a complete research sweep across all sources

        Returns:
            dict: Intelligence report
        """
        logger.info(f"{self.emoji} Starting research sweep...")

        updates = []

        # Fetch from each source
        updates.extend(await self._fetch_hacker_news())
        updates.extend(await self._fetch_github_trending())
        updates.extend(await self._fetch_arxiv())
        updates.extend(await self._fetch_blog_updates())

        # Filter and rank using Claude
        filtered_updates = await self._filter_and_rank(updates)

        # Generate report
        report = await self._generate_report(filtered_updates)

        # Store in coordination hub
        self.coordination.knowledge_base.add_entry(
            key=f"research_sweep_{datetime.now().isoformat()}",
            value=report,
            source=self.agent_key,
        )

        # Cache for daily summary
        self.daily_intelligence.extend(filtered_updates)

        logger.info(
            f"{self.emoji} Research sweep complete: {len(filtered_updates)} updates"
        )

        return report

    async def _fetch_hacker_news(self) -> List[Dict]:
        """Fetch AI-related stories from Hacker News"""
        try:
            response = requests.get(
                self.sources["hacker_news"], timeout=10
            )
            data = response.json()

            updates = []
            for hit in data.get("hits", [])[:10]:  # Top 10
                # Filter for AI relevance
                title = hit.get("title", "").lower()
                if any(
                    keyword in title
                    for keyword in [
                        "ai",
                        "llm",
                        "gpt",
                        "claude",
                        "transformer",
                        "model",
                        "ml",
                        "machine learning",
                    ]
                ):
                    updates.append(
                        {
                            "source": "Hacker News",
                            "title": hit.get("title"),
                            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                            "points": hit.get("points", 0),
                            "timestamp": hit.get("created_at"),
                        }
                    )

            return updates

        except Exception as e:
            logger.error(f"Error fetching Hacker News: {e}")
            return []

    async def _fetch_github_trending(self) -> List[Dict]:
        """Fetch trending AI repositories"""
        try:
            headers = {}
            if github_token := os.getenv("GITHUB_TOKEN"):
                headers["Authorization"] = f"token {github_token}"

            response = requests.get(
                self.sources["github_trending"],
                headers=headers,
                timeout=10,
            )
            data = response.json()

            updates = []
            for repo in data.get("items", [])[:5]:  # Top 5
                # Only include if updated recently (last 7 days)
                updated_at = datetime.fromisoformat(
                    repo["updated_at"].replace("Z", "+00:00")
                )

                if datetime.now() - updated_at.replace(tzinfo=None) < timedelta(days=7):
                    updates.append(
                        {
                            "source": "GitHub",
                            "title": f"{repo['full_name']} - {repo['description']}",
                            "url": repo["html_url"],
                            "stars": repo["stargazers_count"],
                            "timestamp": repo["updated_at"],
                        }
                    )

            return updates

        except Exception as e:
            logger.error(f"Error fetching GitHub: {e}")
            return []

    async def _fetch_arxiv(self) -> List[Dict]:
        """Fetch recent arXiv papers"""
        try:
            feed = feedparser.parse(self.sources["arxiv"])

            updates = []
            for entry in feed.entries[:10]:  # Top 10
                updates.append(
                    {
                        "source": "arXiv",
                        "title": entry.title,
                        "url": entry.link,
                        "summary": entry.summary[:200] + "...",
                        "timestamp": entry.published,
                    }
                )

            return updates

        except Exception as e:
            logger.error(f"Error fetching arXiv: {e}")
            return []

    async def _fetch_blog_updates(self) -> List[Dict]:
        """Fetch updates from major AI lab blogs"""
        updates = []

        # OpenAI RSS
        try:
            feed = feedparser.parse(self.sources["openai_blog"])
            for entry in feed.entries[:3]:
                updates.append(
                    {
                        "source": "OpenAI Blog",
                        "title": entry.title,
                        "url": entry.link,
                        "timestamp": entry.published,
                    }
                )
        except Exception as e:
            logger.error(f"Error fetching OpenAI blog: {e}")

        # Note: Anthropic and DeepMind would need web scraping
        # as they don't have RSS feeds

        return updates

    async def _filter_and_rank(self, updates: List[Dict]) -> List[Dict]:
        """Filter and rank updates by importance using Claude"""
        if not updates:
            return []

        # Prepare updates for Claude
        updates_text = "\n\n".join(
            [
                f"{i+1}. [{u['source']}] {u['title']}\n   URL: {u.get('url', 'N/A')}"
                for i, u in enumerate(updates)
            ]
        )

        prompt = f"""You are an AI research analyst. Review these AI/ML updates and:

1. Filter out noise (minor updates, duplicate topics)
2. Identify the most significant developments
3. Rank by importance and impact

Updates:
{updates_text}

Return ONLY the indices (1-based) of significant updates in order of importance.
Example: 3,1,7,12

Respond with just the comma-separated numbers."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse indices
        try:
            indices_text = response.content[0].text.strip()
            indices = [int(i.strip()) - 1 for i in indices_text.split(",")]

            # Return filtered and ranked updates
            return [updates[i] for i in indices if 0 <= i < len(updates)]

        except Exception as e:
            logger.error(f"Error parsing Claude response: {e}")
            return updates[:10]  # Fallback to first 10

    async def _generate_report(self, updates: List[Dict]) -> dict:
        """Generate structured intelligence report"""
        if not updates:
            return {
                "timestamp": datetime.now().isoformat(),
                "updates_count": 0,
                "summary": "No significant updates",
                "updates": [],
            }

        # Use Claude to generate summary
        updates_text = "\n\n".join(
            [f"• [{u['source']}] {u['title']}" for u in updates]
        )

        prompt = f"""Generate a concise intelligence summary of these AI developments:

{updates_text}

Format:
1. One-line executive summary
2. Key developments (bullet points)
3. Impact assessment

Keep it brief and actionable."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.content[0].text

        return {
            "timestamp": datetime.now().isoformat(),
            "updates_count": len(updates),
            "summary": summary,
            "updates": updates[:10],  # Top 10
        }

    async def submit_status_report(self):
        """Submit status report to coordination hub"""
        report = AgentReport(
            agent_name=self.agent_key,
            status="Active",
            metrics={
                "daily_intelligence": len(self.daily_intelligence),
                "last_sweep": (
                    datetime.now().strftime("%H:%M") if self.daily_intelligence else "Never"
                ),
            },
            next_action=f"Next sweep in {self._time_until_next_sweep()}",
        )

        await self.coordination.submit_report(report)

    def _time_until_next_sweep(self) -> str:
        """Calculate time until next scheduled sweep"""
        now = datetime.now()
        next_times = [7, 13, 19]  # 7 AM, 1 PM, 7 PM

        for hour in next_times:
            next_sweep = now.replace(hour=hour, minute=0, second=0, microsecond=0)

            if next_sweep > now:
                delta = next_sweep - now
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                return f"{hours}h {minutes}m"

        # Next day
        tomorrow = now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(
            days=1
        )
        delta = tomorrow - now
        return f"{delta.seconds // 3600}h"

    async def get_daily_briefing(self) -> str:
        """Generate daily briefing from accumulated intelligence"""
        if not self.daily_intelligence:
            return "No updates today."

        # Group by source
        by_source = {}
        for update in self.daily_intelligence:
            source = update["source"]
            if source not in by_source:
                by_source[source] = []

            by_source[source].append(update)

        briefing = f"{self.emoji} *DAILY INTELLIGENCE BRIEFING*\n\n"

        for source, updates in by_source.items():
            briefing += f"*{source}* ({len(updates)} updates)\n"

            for update in updates[:3]:  # Top 3 per source
                briefing += f"• {update['title']}\n"

            briefing += "\n"

        briefing += f"Total updates tracked: {len(self.daily_intelligence)}"

        return briefing


import os
