"""
Curator Agent

The "scout" agent that discovers and filters trending AI content.
Scrapes all sources, deduplicates, ranks by trending score,
and categorizes into topic clusters.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from agents.rag_recommendation.scrapers.trending_scraper import TrendingScraper, TrendingItem
from agents.rag_recommendation.scrapers.source_aggregator import SourceAggregator, AggregatedTopic

logger = logging.getLogger(__name__)


@dataclass
class CuratedFeed:
    """Output of the Curator Agent — a structured trending feed."""
    timestamp: str
    total_items: int
    total_topics: int
    topics: List[AggregatedTopic]
    top_items: List[TrendingItem]       # top 30 items flat-ranked
    source_breakdown: Dict[str, int]    # items per source
    metadata: Dict = field(default_factory=dict)

    def summary_text(self) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"🔍 **Curated Feed** — {self.timestamp}",
            f"Found **{self.total_items}** trending items across **{len(self.source_breakdown)}** sources",
            f"Organized into **{self.total_topics}** topic clusters\n",
            "**Top Topics by Heat:**",
        ]
        for t in self.topics[:8]:
            heat_bar = "🔥" * max(1, int(t.heat_score * 5))
            lines.append(
                f"  {heat_bar} **{t.topic}** — {len(t.items)} items "
                f"({', '.join(t.unique_sources)})"
            )

        lines.append("\n**Source Breakdown:**")
        for source, count in sorted(self.source_breakdown.items(), key=lambda x: -x[1]):
            lines.append(f"  • {source}: {count}")

        return "\n".join(lines)


class CuratorAgent:
    """
    Curator Agent — discovers and ranks trending AI content.

    Pipeline:
    1. Scrape all 6 sources in parallel
    2. Filter for AI agent / agentic AI relevance
    3. Deduplicate across sources
    4. Score with recency + engagement + source weight
    5. Cluster into topic categories
    6. Return CuratedFeed

    Usage:
        curator = CuratorAgent()
        feed = await curator.curate()
    """

    def __init__(self):
        self.scraper = TrendingScraper()
        self.aggregator = SourceAggregator()
        self._history: List[CuratedFeed] = []

    async def curate(self, filter_agents: bool = True) -> CuratedFeed:
        """
        Run the full curation pipeline.

        Args:
            filter_agents: If True, only keep AI-agent-related items.

        Returns:
            CuratedFeed with topics and ranked items.
        """
        logger.info("🔍 Curator Agent: starting curation pipeline...")

        # Step 1: Scrape all sources
        raw_items = await self.scraper.scrape_all(filter_agents=filter_agents)
        logger.info(f"Curator: scraped {len(raw_items)} raw items")

        # Step 2: Aggregate — dedup, score, cluster
        topics = self.aggregator.aggregate(raw_items)
        flat_ranked = self.aggregator.get_flat_ranked(raw_items)

        # Step 3: Build source breakdown
        source_counts: Dict[str, int] = {}
        for item in flat_ranked:
            source_counts[item.source] = source_counts.get(item.source, 0) + 1

        # Step 4: Compose feed
        feed = CuratedFeed(
            timestamp=datetime.now().isoformat(),
            total_items=len(flat_ranked),
            total_topics=len(topics),
            topics=topics,
            top_items=flat_ranked[:30],
            source_breakdown=source_counts,
        )

        self._history.append(feed)
        logger.info(
            f"Curator: produced feed with {feed.total_items} items, "
            f"{feed.total_topics} topics"
        )
        return feed

    async def get_latest_by_source(self, source: str) -> List[TrendingItem]:
        """Get items filtered by a specific source."""
        raw_items = await self.scraper.scrape_all(filter_agents=True)
        return [i for i in raw_items if i.source == source]

    async def get_topic_items(self, topic_name: str) -> List[TrendingItem]:
        """Get items for a specific topic cluster."""
        feed = await self.curate()
        for topic in feed.topics:
            if topic.topic.lower() == topic_name.lower():
                return topic.items
        return []
