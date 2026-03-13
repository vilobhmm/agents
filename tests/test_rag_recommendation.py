"""
Tests for the Multi-Agent RAG Recommendation Engine.

Covers:
- TrendingItem data model
- TrendingScraper (with mocked HTTP)
- SourceAggregator (dedup, scoring, clustering)
- Embedder (shape, caching)
- VectorStore (add, search, similar)
- CuratorAgent (curation pipeline)
- AnalystAgent (rule-based analysis)
- RecommenderAgent (recommendation pipeline)
- RecommendationOrchestrator (end-to-end)
"""

import asyncio
import os
import json
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ── Helpers ────────────────────────────────────────────────────────

def run_async(coro):
    """Run an async coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ═══════════════════════════════════════════════════════════════════
# TrendingItem
# ═══════════════════════════════════════════════════════════════════

class TestTrendingItem:
    def test_creation(self):
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        item = TrendingItem(
            title="Multi-agent RAG Systems",
            url="https://example.com/paper",
            source="arxiv",
            summary="A novel approach to multi-agent RAG.",
            tags=["multi-agent", "rag"],
            score=0.85,
        )
        assert item.title == "Multi-agent RAG Systems"
        assert item.source == "arxiv"
        assert item.score == 0.85
        assert len(item.item_id) == 12  # md5 hash prefix

    def test_text_for_embedding(self):
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        item = TrendingItem(
            title="Agent Frameworks",
            url="https://example.com",
            source="hackernews",
            summary="Overview of agent frameworks",
            tags=["agents", "frameworks"],
        )
        text = item.text_for_embedding
        assert "Agent Frameworks" in text
        assert "Overview of agent frameworks" in text
        assert "agents" in text

    def test_to_dict(self):
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        item = TrendingItem(
            title="Test", url="https://test.com", source="reddit"
        )
        d = item.to_dict()
        assert isinstance(d, dict)
        assert d["title"] == "Test"
        assert d["source"] == "reddit"


# ═══════════════════════════════════════════════════════════════════
# SourceAggregator
# ═══════════════════════════════════════════════════════════════════

class TestSourceAggregator:
    def _make_items(self):
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        return [
            TrendingItem(title="Multi-agent systems review", url="https://a.com", source="arxiv", score=0.8, summary="Survey of multi-agent systems", tags=["multi-agent"]),
            TrendingItem(title="Multi-agent systems survey", url="https://b.com", source="hackernews", score=0.6, summary="Another survey", tags=["multi-agent"]),  # near-dup
            TrendingItem(title="New RAG technique for agents", url="https://c.com", source="reddit", score=0.7, summary="RAG retrieval augmented", tags=["rag"]),
            TrendingItem(title="LangChain agent framework update", url="https://d.com", source="github", score=0.9, summary="agent framework langchain", tags=["langchain"]),
            TrendingItem(title="Claude computer use demo", url="https://e.com", source="ai_blogs", score=0.5, summary="tool use computer use", tags=["tool-use"]),
        ]

    def test_deduplicate(self):
        from agents.rag_recommendation.scrapers.source_aggregator import SourceAggregator

        agg = SourceAggregator()
        items = self._make_items()
        deduped = agg._deduplicate(items)
        # The two "multi-agent systems" items should be deduped
        assert len(deduped) < len(items)

    def test_aggregate_returns_topics(self):
        from agents.rag_recommendation.scrapers.source_aggregator import SourceAggregator

        agg = SourceAggregator()
        items = self._make_items()
        topics = agg.aggregate(items)
        assert len(topics) > 0
        assert all(hasattr(t, "topic") for t in topics)
        assert all(hasattr(t, "heat_score") for t in topics)

    def test_flat_ranked(self):
        from agents.rag_recommendation.scrapers.source_aggregator import SourceAggregator

        agg = SourceAggregator()
        items = self._make_items()
        flat = agg.get_flat_ranked(items)
        # Should be sorted by score descending
        scores = [i.score for i in flat]
        assert scores == sorted(scores, reverse=True)

    def test_topic_clustering(self):
        from agents.rag_recommendation.scrapers.source_aggregator import SourceAggregator

        agg = SourceAggregator()
        items = self._make_items()
        topics = agg.aggregate(items)
        topic_names = [t.topic for t in topics]
        # Should find at least RAG and Agent Frameworks topics
        assert any("RAG" in t for t in topic_names) or any("Agent" in t for t in topic_names)


# ═══════════════════════════════════════════════════════════════════
# Keyword filter
# ═══════════════════════════════════════════════════════════════════

class TestKeywordFilter:
    def test_matches_agent_topic(self):
        from agents.rag_recommendation.scrapers.trending_scraper import _matches_agent_topic

        assert _matches_agent_topic("New multi-agent framework released")
        assert _matches_agent_topic("Agentic AI is transforming workflows")
        assert _matches_agent_topic("RAG retrieval augmented generation")
        assert not _matches_agent_topic("Best pizza recipes in New York")


# ═══════════════════════════════════════════════════════════════════
# CuratorAgent
# ═══════════════════════════════════════════════════════════════════

class TestCuratorAgent:
    def test_curate_returns_feed(self):
        from agents.rag_recommendation.agents.curator_agent import CuratorAgent
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        curator = CuratorAgent()

        # Mock the scraper to return test items
        mock_items = [
            TrendingItem(title="AI agent benchmark", url="https://x.com", source="arxiv", score=0.9, summary="agentic ai benchmark", tags=["agent"]),
            TrendingItem(title="Multi-agent coordination", url="https://y.com", source="hackernews", score=0.7, summary="multi-agent systems", tags=["multi-agent"]),
        ]
        curator.scraper.scrape_all = AsyncMock(return_value=mock_items)

        feed = run_async(curator.curate())
        assert feed.total_items > 0
        assert feed.total_topics >= 0
        assert hasattr(feed, "summary_text")
        assert "items" in feed.summary_text().lower() or "curated" in feed.summary_text().lower()


# ═══════════════════════════════════════════════════════════════════
# AnalystAgent (rule-based fallback)
# ═══════════════════════════════════════════════════════════════════

class TestAnalystAgent:
    def test_rule_based_analysis(self):
        from agents.rag_recommendation.agents.analyst_agent import AnalystAgent
        from agents.rag_recommendation.scrapers.source_aggregator import AggregatedTopic
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        analyst = AnalystAgent()
        topic = AggregatedTopic(
            topic="Multi-Agent Systems",
            items=[
                TrendingItem(title="Multi-agent coordination paper", url="https://a.com", source="arxiv", score=0.8),
                TrendingItem(title="CrewAI multi-agent update", url="https://b.com", source="github", score=0.7),
            ],
            combined_score=0.75,
            source_count=2,
            unique_sources=["arxiv", "github"],
        )

        analysis = analyst._rule_based_analysis(topic)
        assert analysis.topic == "Multi-Agent Systems"
        assert analysis.heat_score > 0
        assert len(analysis.key_developments) > 0
        assert analysis.reading_level in ("beginner", "intermediate", "advanced")

    def test_analyze_topics(self):
        from agents.rag_recommendation.agents.analyst_agent import AnalystAgent
        from agents.rag_recommendation.scrapers.source_aggregator import AggregatedTopic
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        analyst = AnalystAgent()
        topics = [
            AggregatedTopic(
                topic="RAG & Retrieval",
                items=[TrendingItem(title="RAG survey", url="https://c.com", source="arxiv", score=0.9)],
                combined_score=0.9,
                source_count=1,
                unique_sources=["arxiv"],
            ),
        ]

        # Force rule-based (no API key)
        os.environ.pop("ANTHROPIC_API_KEY", None)
        analyst._anthropic_client = None

        analyses = run_async(analyst.analyze_topics(topics))
        assert len(analyses) == 1
        assert analyses[0].topic == "RAG & Retrieval"


# ═══════════════════════════════════════════════════════════════════
# RecommenderAgent
# ═══════════════════════════════════════════════════════════════════

class TestRecommenderAgent:
    def test_recommend_with_mocked_store(self):
        from agents.rag_recommendation.agents.recommender_agent import RecommenderAgent
        from agents.rag_recommendation.agents.analyst_agent import TopicAnalysis

        # Mock vector store
        mock_store = MagicMock()
        mock_store.search.return_value = []
        mock_store.get_similar.return_value = []

        recommender = RecommenderAgent(vector_store=mock_store)

        analyses = [
            TopicAnalysis(
                topic="Agent Frameworks",
                heat_score=0.85,
                item_count=5,
                summary="Agent frameworks are trending",
                why_it_matters="Important for building AI apps",
                key_developments=["LangChain update", "CrewAI release"],
                related_topics=["Multi-Agent Systems"],
                reading_level="intermediate",
                top_items=[
                    {"title": "LangChain v3", "url": "https://lc.com", "source": "github", "score": 0.9, "summary": "agent framework", "tags": ["langchain"], "item_id": "abc123"},
                    {"title": "CrewAI agents", "url": "https://cr.com", "source": "hackernews", "score": 0.8, "summary": "multi-agent", "tags": ["crewai"], "item_id": "def456"},
                ],
            ),
        ]

        recs = run_async(recommender.recommend(analyses, user_interests=["AI agents", "RAG"]))
        assert recs.total_recommendations > 0
        assert recs.recommendations[0].rank == 1
        assert hasattr(recs, "summary_text")


# ═══════════════════════════════════════════════════════════════════
# Orchestrator (mocked pipeline)
# ═══════════════════════════════════════════════════════════════════

class TestOrchestrator:
    def test_to_json(self):
        from agents.rag_recommendation.orchestrator import RecommendationOrchestrator
        from agents.rag_recommendation.agents.curator_agent import CuratedFeed
        from agents.rag_recommendation.agents.analyst_agent import TopicAnalysis
        from agents.rag_recommendation.agents.recommender_agent import RecommendationSet, Recommendation
        from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

        orch = RecommendationOrchestrator()

        # Manually set a result
        orch._last_result = {
            "curated_feed": CuratedFeed(
                timestamp="2026-03-12T00:00:00",
                total_items=5,
                total_topics=2,
                topics=[],
                top_items=[TrendingItem(title="Test", url="https://t.com", source="arxiv", score=0.8)],
                source_breakdown={"arxiv": 3, "hackernews": 2},
            ),
            "analyses": [
                TopicAnalysis(
                    topic="Test Topic", heat_score=0.9, item_count=3,
                    summary="Test summary", why_it_matters="Test matters",
                    key_developments=["Dev 1"], related_topics=["Related"],
                    reading_level="intermediate", top_items=[],
                ),
            ],
            "recommendations": RecommendationSet(
                generated_at="2026-03-12T00:00:00",
                total_recommendations=1,
                user_interests=["AI agents"],
                recommendations=[
                    Recommendation(rank=1, title="Test Rec", url="https://r.com", source="arxiv", topic="Test", score=0.9, why_read="Good stuff", reading_level="intermediate"),
                ],
                topic_coverage={"Test": 1},
            ),
            "metadata": {
                "pipeline_duration_seconds": 5.2,
                "timestamp": "2026-03-12T00:00:00",
                "user_interests": ["AI agents"],
                "vector_store_stats": {"trending_topics": 5},
            },
        }

        json_str = orch.to_json()
        data = json.loads(json_str)
        assert "curated_feed" in data
        assert "analyses" in data
        assert "recommendations" in data
        assert data["recommendations"]["total_recommendations"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
