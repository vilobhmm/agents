"""
Recommendation Orchestrator

Coordinates the 3-agent pipeline:
1. Curator → scrapes & produces curated feed
2. Analyst → enriches top topics with analysis
3. Recommender → personalizes recommendations via RAG

Manages caching, vector store updates, and serves results.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents.rag_recommendation.agents.curator_agent import CuratorAgent, CuratedFeed
from agents.rag_recommendation.agents.analyst_agent import AnalystAgent, TopicAnalysis
from agents.rag_recommendation.agents.recommender_agent import (
    RecommenderAgent,
    RecommendationSet,
)
from agents.rag_recommendation.rag.vector_store import VectorStore
from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

logger = logging.getLogger(__name__)


class RecommendationOrchestrator:
    """
    Orchestrates the multi-agent recommendation pipeline.

    Usage:
        engine = RecommendationOrchestrator()
        result = await engine.run()
        print(result["recommendations"].summary_text())
    """

    def __init__(
        self,
        user_interests: Optional[List[str]] = None,
        persist_dir: Optional[str] = None,
    ):
        self.vector_store = VectorStore(persist_dir=persist_dir)
        self.curator = CuratorAgent()
        self.analyst = AnalystAgent()
        self.recommender = RecommenderAgent(vector_store=self.vector_store)
        self.user_interests = user_interests or [
            "AI agents", "agentic AI", "multi-agent systems",
            "LLM reasoning", "agent frameworks", "RAG",
        ]

        # Results cache
        self._last_result: Optional[Dict[str, Any]] = None
        self._last_run: Optional[str] = None

    async def run(self, max_recommendations: int = 20) -> Dict[str, Any]:
        """
        Execute the full 3-agent pipeline.

        Returns dict with keys: curated_feed, analyses, recommendations, metadata.
        """
        start = datetime.now()
        logger.info("🎯 Orchestrator: starting recommendation pipeline...")

        # ── Stage 1: Curator ──────────────────────────────────────────────
        logger.info("━━ Stage 1/3: Curator Agent ━━")
        feed: CuratedFeed = await self.curator.curate()
        logger.info(f"   Curator produced {feed.total_items} items in {feed.total_topics} topics")

        # ── Index into vector store ───────────────────────────────────────
        if feed.top_items:
            self._index_items(feed.top_items)

        # ── Stage 2: Analyst ──────────────────────────────────────────────
        logger.info("━━ Stage 2/3: Analyst Agent ━━")
        analyses: List[TopicAnalysis] = await self.analyst.analyze_topics(
            feed.topics, max_topics=10
        )
        logger.info(f"   Analyst produced {len(analyses)} topic analyses")

        # ── Index analyses ────────────────────────────────────────────────
        if analyses:
            self._index_analyses(analyses)

        # ── Stage 3: Recommender ──────────────────────────────────────────
        logger.info("━━ Stage 3/3: Recommender Agent ━━")
        recommendations: RecommendationSet = await self.recommender.recommend(
            analyses,
            user_interests=self.user_interests,
            max_recommendations=max_recommendations,
        )
        logger.info(f"   Recommender produced {recommendations.total_recommendations} recs")

        # ── Compose result ────────────────────────────────────────────────
        elapsed = (datetime.now() - start).total_seconds()
        result = {
            "curated_feed": feed,
            "analyses": analyses,
            "recommendations": recommendations,
            "metadata": {
                "pipeline_duration_seconds": round(elapsed, 2),
                "timestamp": datetime.now().isoformat(),
                "user_interests": self.user_interests,
                "vector_store_stats": self.vector_store.get_collection_stats(),
            },
        }

        self._last_result = result
        self._last_run = datetime.now().isoformat()

        logger.info(f"🎯 Orchestrator: pipeline complete in {elapsed:.1f}s")
        return result

    async def refresh(self) -> Dict[str, Any]:
        """Re-run the pipeline (alias for run)."""
        return await self.run()

    def get_cached_result(self) -> Optional[Dict[str, Any]]:
        """Return the last pipeline result if available."""
        return self._last_result

    def set_interests(self, interests: List[str]):
        """Update user interests for personalization."""
        self.user_interests = interests

    # ── Serialization for dashboard ─────────────────────────────────────

    def to_json(self, result: Optional[Dict[str, Any]] = None) -> str:
        """Serialize the pipeline result to JSON for the dashboard."""
        r = result or self._last_result
        if not r:
            return json.dumps({"error": "No results yet. Run the pipeline first."})

        feed: CuratedFeed = r["curated_feed"]
        analyses: List[TopicAnalysis] = r["analyses"]
        recs: RecommendationSet = r["recommendations"]

        payload = {
            "metadata": r["metadata"],
            "curated_feed": {
                "timestamp": feed.timestamp,
                "total_items": feed.total_items,
                "total_topics": feed.total_topics,
                "source_breakdown": feed.source_breakdown,
                "topics": [
                    {
                        "topic": t.topic,
                        "heat_score": round(t.heat_score, 3),
                        "item_count": len(t.items),
                        "sources": t.unique_sources,
                        "items": [i.to_dict() for i in t.items[:5]],
                    }
                    for t in feed.topics
                ],
                "top_items": [i.to_dict() for i in feed.top_items[:20]],
            },
            "analyses": [a.to_dict() for a in analyses],
            "recommendations": recs.to_dict(),
        }

        return json.dumps(payload, indent=2, default=str)

    # ── Vector store helpers ────────────────────────────────────────────

    def _index_items(self, items: List[TrendingItem]):
        """Index trending items into the vector store."""
        ids = [i.item_id for i in items]
        texts = [i.text_for_embedding for i in items]
        metadatas = [
            {
                "title": i.title,
                "url": i.url,
                "source": i.source,
                "score": i.score,
                "published_at": i.published_at,
                "tags": ", ".join(i.tags) if i.tags else "",
            }
            for i in items
        ]

        self.vector_store.add_items("trending_topics", ids, texts, metadatas)

    def _index_analyses(self, analyses: List[TopicAnalysis]):
        """Index topic analyses into the vector store."""
        ids = [f"analysis_{a.topic.lower().replace(' ', '_')}" for a in analyses]
        texts = [
            f"{a.topic}: {a.summary} {a.why_it_matters}"
            for a in analyses
        ]
        metadatas = [
            {
                "topic": a.topic,
                "heat_score": a.heat_score,
                "reading_level": a.reading_level,
                "item_count": a.item_count,
            }
            for a in analyses
        ]

        self.vector_store.add_items("topic_analysis", ids, texts, metadatas)
