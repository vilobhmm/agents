"""
Recommender Agent

The "advisor" agent that personalizes topic recommendations.
Uses RAG retrieval from the vector store to match trending content
against user interests and generates personalized explanations.
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.rag_recommendation.rag.vector_store import VectorStore
from agents.rag_recommendation.agents.analyst_agent import TopicAnalysis
from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

logger = logging.getLogger(__name__)


@dataclass
class Recommendation:
    """A single personalized recommendation."""
    rank: int
    title: str
    url: str
    source: str
    topic: str
    score: float                       # combined relevance + trending
    why_read: str                      # personalized explanation
    reading_level: str
    tags: List[str] = field(default_factory=list)
    related_items: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "rank": self.rank,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "topic": self.topic,
            "score": round(self.score, 3),
            "why_read": self.why_read,
            "reading_level": self.reading_level,
            "tags": self.tags,
            "related_items": self.related_items,
        }


@dataclass
class RecommendationSet:
    """Output of the Recommender Agent."""
    generated_at: str
    total_recommendations: int
    user_interests: List[str]
    recommendations: List[Recommendation]
    topic_coverage: Dict[str, int]      # topic → count

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at,
            "total_recommendations": self.total_recommendations,
            "user_interests": self.user_interests,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "topic_coverage": self.topic_coverage,
        }

    def summary_text(self) -> str:
        lines = [
            f"💡 **Personalized Recommendations** — {self.generated_at}",
            f"Generated **{self.total_recommendations}** recommendations",
            f"Based on interests: {', '.join(self.user_interests)}\n",
        ]
        for rec in self.recommendations[:10]:
            score_bar = "⭐" * max(1, int(rec.score * 5))
            lines.append(f"{rec.rank}. {score_bar} **{rec.title}**")
            lines.append(f"   📌 {rec.topic} | 📖 {rec.reading_level} | 🔗 {rec.source}")
            lines.append(f"   💬 {rec.why_read}")
            lines.append(f"   🌐 {rec.url}\n")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Recommender prompts
# ---------------------------------------------------------------------------

WHY_READ_SYSTEM = """You are a personalized AI reading advisor. Given a user's interests 
and a trending item, write a compelling 1-2 sentence explanation of why they should 
read it. Be specific, practical, and concise. Reference the user's interests directly."""

WHY_READ_PROMPT = """User interests: {interests}

Trending item:
Title: {title}
Source: {source}
Summary: {summary}
Topic: {topic}

Write a 1-2 sentence "why you should read this" explanation personalized to the user's interests."""


class RecommenderAgent:
    """
    Recommender Agent — personalizes trending content via RAG.

    Pipeline:
    1. Embed user interests
    2. Search vector store for semantically similar past content
    3. Cross-reference with current trending + analyzed topics
    4. Rank by relevance × trending score
    5. Generate personalized "why read" explanations
    6. Return RecommendationSet

    Usage:
        recommender = RecommenderAgent(vector_store)
        recs = await recommender.recommend(analyses, user_interests=["RAG", "agents"])
    """

    DEFAULT_INTERESTS = [
        "AI agents", "agentic AI", "multi-agent systems",
        "LLM reasoning", "agent frameworks", "RAG",
        "tool use", "autonomous agents",
    ]

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.vector_store = vector_store or VectorStore()
        self._anthropic_client = None
        self._model = "claude-sonnet-4-5-20250929"

    @property
    def _client(self):
        if self._anthropic_client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                try:
                    import anthropic
                    self._anthropic_client = anthropic.Anthropic(api_key=api_key)
                except ImportError:
                    pass
        return self._anthropic_client

    async def recommend(
        self,
        analyses: List[TopicAnalysis],
        user_interests: Optional[List[str]] = None,
        max_recommendations: int = 20,
    ) -> RecommendationSet:
        """
        Generate personalized recommendations.

        Args:
            analyses: Topic analyses from Analyst Agent.
            user_interests: User's topics of interest.
            max_recommendations: Max recs to return.

        Returns:
            RecommendationSet with ranked, personalized recommendations.
        """
        interests = user_interests or self.DEFAULT_INTERESTS
        logger.info(
            f"💡 Recommender Agent: generating recs for interests={interests[:5]}..."
        )

        # Step 1: Collect all candidate items from analyses
        candidates: List[Dict[str, Any]] = []
        for analysis in analyses:
            for item_dict in analysis.top_items:
                candidates.append({
                    **item_dict,
                    "topic": analysis.topic,
                    "heat_score": analysis.heat_score,
                    "reading_level": analysis.reading_level,
                    "analysis_summary": analysis.summary,
                })

        # Step 2: RAG retrieval — find semantically similar past items
        interest_query = " ".join(interests)
        rag_results = self.vector_store.search(
            "trending_topics", interest_query, n_results=30
        )
        rag_ids = {r["id"] for r in rag_results}
        rag_scores = {r["id"]: 1.0 - r.get("distance", 0.5) for r in rag_results}

        # Step 3: Score candidates (trending × relevance)
        scored: List[Dict[str, Any]] = []
        for c in candidates:
            item_id = c.get("item_id", "")
            rag_boost = rag_scores.get(item_id, 0.3)
            trending_score = c.get("score", 0.5)
            heat = c.get("heat_score", 0.5)

            # Combined score: 40% trending, 30% RAG relevance, 30% heat
            combined = (trending_score * 0.4) + (rag_boost * 0.3) + (heat * 0.3)

            # Interest keyword match bonus
            title_lower = c.get("title", "").lower()
            summary_lower = c.get("summary", "").lower()
            text = f"{title_lower} {summary_lower}"
            match_count = sum(1 for i in interests if i.lower() in text)
            combined += match_count * 0.05

            c["combined_score"] = min(1.0, combined)
            scored.append(c)

        # Step 4: Rank and deduplicate
        scored.sort(key=lambda x: x["combined_score"], reverse=True)
        seen_titles: set = set()
        unique_scored: List[Dict[str, Any]] = []
        for c in scored:
            title_norm = c.get("title", "").lower().strip()
            if title_norm not in seen_titles:
                seen_titles.add(title_norm)
                unique_scored.append(c)

        # Step 5: Generate personalized "why read" explanations
        recommendations: List[Recommendation] = []
        for rank, c in enumerate(unique_scored[:max_recommendations], 1):
            why_read = await self._generate_why_read(c, interests)

            # Find related items
            related = []
            if c.get("item_id"):
                similar = self.vector_store.get_similar(
                    "trending_topics", c["item_id"], n_results=3
                )
                related = [s.get("document", "")[:60] for s in similar]

            recommendations.append(Recommendation(
                rank=rank,
                title=c.get("title", ""),
                url=c.get("url", ""),
                source=c.get("source", ""),
                topic=c.get("topic", ""),
                score=c["combined_score"],
                why_read=why_read,
                reading_level=c.get("reading_level", "intermediate"),
                tags=c.get("tags", []) if isinstance(c.get("tags"), list) else [],
                related_items=related,
            ))

        # Topic coverage stats
        coverage: Dict[str, int] = {}
        for r in recommendations:
            coverage[r.topic] = coverage.get(r.topic, 0) + 1

        rec_set = RecommendationSet(
            generated_at=datetime.now().isoformat(),
            total_recommendations=len(recommendations),
            user_interests=interests,
            recommendations=recommendations,
            topic_coverage=coverage,
        )

        logger.info(f"Recommender: generated {len(recommendations)} recommendations")
        return rec_set

    async def add_user_interest(self, interest: str):
        """Track a user interest in the vector store for future personalization."""
        self.vector_store.add_items(
            "user_preferences",
            ids=[f"interest_{interest.lower().replace(' ', '_')}"],
            texts=[interest],
            metadatas=[{"type": "interest", "added_at": datetime.now().isoformat()}],
        )

    async def _generate_why_read(
        self, candidate: Dict[str, Any], interests: List[str]
    ) -> str:
        """Generate a personalized 'why read' explanation."""
        if self._client:
            try:
                prompt = WHY_READ_PROMPT.format(
                    interests=", ".join(interests),
                    title=candidate.get("title", ""),
                    source=candidate.get("source", ""),
                    summary=candidate.get("summary", "")[:200],
                    topic=candidate.get("topic", ""),
                )
                response = await asyncio.to_thread(
                    self._client.messages.create,
                    model=self._model,
                    max_tokens=100,
                    system=WHY_READ_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text.strip()
            except Exception as e:
                logger.debug(f"LLM why_read failed: {e}")

        # Fallback
        topic = candidate.get("topic", "AI")
        source = candidate.get("source", "")
        return (
            f"Trending in {topic} on {source}. "
            f"Relevant to your interest in {interests[0] if interests else 'AI agents'}."
        )
