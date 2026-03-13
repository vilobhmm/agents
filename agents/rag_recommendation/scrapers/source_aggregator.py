"""
Source Aggregator

Aggregates, deduplicates, and normalizes trending items from multiple sources.
Computes a unified trending score and clusters items by topic.
"""

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Topic taxonomy
# ---------------------------------------------------------------------------

TOPIC_CLUSTERS: Dict[str, List[str]] = {
    "Agent Frameworks": [
        "agent framework", "autogen", "crewai", "langchain", "langgraph",
        "agent sdk", "openai agents sdk", "google adk", "agent protocol",
        "mcp", "model context protocol",
    ],
    "Multi-Agent Systems": [
        "multi-agent", "multiagent", "multi agent", "agent collaboration",
        "agent coordination", "swarm", "agent team", "agent orchestration",
    ],
    "RAG & Retrieval": [
        "rag", "retrieval augmented", "retrieval-augmented", "vector search",
        "embedding", "knowledge retrieval", "semantic search", "chunking",
        "hybrid search", "reranking",
    ],
    "Reasoning & Planning": [
        "reasoning", "chain of thought", "chain-of-thought", "cot",
        "planning", "tree of thought", "step by step", "think",
        "self-reflection", "critique",
    ],
    "Tool Use & Function Calling": [
        "tool use", "function calling", "tool calling", "computer use",
        "browser use", "code execution", "api calling", "action model",
    ],
    "Agent Memory": [
        "agent memory", "long-term memory", "episodic memory",
        "memory system", "context window", "memory management",
        "conversation memory", "knowledge graph",
    ],
    "LLM Architecture": [
        "transformer", "attention", "llm", "large language model",
        "foundation model", "gpt", "claude", "gemini", "llama",
        "fine-tuning", "distillation", "quantization",
    ],
    "Autonomous Agents": [
        "autonomous agent", "self-improving", "agentic ai", "agentic",
        "goal-directed", "self-play", "agent benchmark",
        "agent evaluation", "webagent",
    ],
    "Code Agents": [
        "code agent", "coding agent", "code generation", "code assistant",
        "pair programming", "devin", "cursor", "copilot", "swe-bench",
        "software engineering agent",
    ],
    "Multimodal Agents": [
        "multimodal agent", "vision agent", "image understanding",
        "video understanding", "voice agent", "audio agent",
        "visual reasoning",
    ],
}


@dataclass
class AggregatedTopic:
    """A cluster of related trending items grouped by topic."""
    topic: str
    items: List[TrendingItem] = field(default_factory=list)
    combined_score: float = 0.0
    source_count: int = 0
    unique_sources: List[str] = field(default_factory=list)

    @property
    def heat_score(self) -> float:
        """Cross-source heat: more sources = hotter topic."""
        source_bonus = len(self.unique_sources) * 0.15
        return min(1.0, self.combined_score + source_bonus)


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

class SourceAggregator:
    """
    Aggregates and deduplicates trending items from multiple sources.

    Public API:
        aggregator = SourceAggregator()
        topics = aggregator.aggregate(items)
    """

    SIMILARITY_THRESHOLD = 0.65  # fuzzy-match threshold for dedup

    def aggregate(self, items: List[TrendingItem]) -> List[AggregatedTopic]:
        """
        Full pipeline: dedup → score → cluster → rank.

        Returns sorted list of AggregatedTopic, hottest first.
        """
        deduped = self._deduplicate(items)
        scored = self._compute_scores(deduped)
        topics = self._cluster_by_topic(scored)
        topics.sort(key=lambda t: t.heat_score, reverse=True)
        return topics

    def get_flat_ranked(self, items: List[TrendingItem]) -> List[TrendingItem]:
        """Return a flat, deduplicated, score-ranked list (no clustering)."""
        deduped = self._deduplicate(items)
        scored = self._compute_scores(deduped)
        scored.sort(key=lambda i: i.score, reverse=True)
        return scored

    # -- dedup --------------------------------------------------------------

    def _deduplicate(self, items: List[TrendingItem]) -> List[TrendingItem]:
        """Remove near-duplicate items using fuzzy title matching."""
        if not items:
            return []

        unique: List[TrendingItem] = []
        seen_urls: set = set()

        for item in items:
            # Exact URL dedup
            if item.url in seen_urls:
                continue

            # Fuzzy title dedup
            is_dup = False
            for existing in unique:
                sim = SequenceMatcher(
                    None,
                    self._normalize_title(item.title),
                    self._normalize_title(existing.title),
                ).ratio()
                if sim >= self.SIMILARITY_THRESHOLD:
                    # Keep the one with higher score
                    if item.score > existing.score:
                        unique.remove(existing)
                        unique.append(item)
                    is_dup = True
                    break

            if not is_dup:
                unique.append(item)
                seen_urls.add(item.url)

        logger.info(f"Dedup: {len(items)} → {len(unique)} items")
        return unique

    def _normalize_title(self, title: str) -> str:
        """Normalize title for comparison."""
        title = title.lower().strip()
        title = re.sub(r"[^a-z0-9\s]", "", title)
        title = re.sub(r"\s+", " ", title)
        return title

    # -- scoring ------------------------------------------------------------

    def _compute_scores(self, items: List[TrendingItem]) -> List[TrendingItem]:
        """Enhance scores with recency and cross-source bonuses."""
        now = datetime.now()

        for item in items:
            recency_bonus = 0.0
            if item.published_at:
                try:
                    pub = datetime.fromisoformat(item.published_at.replace("Z", "+00:00"))
                    pub_naive = pub.replace(tzinfo=None)
                    hours_ago = (now - pub_naive).total_seconds() / 3600
                    if hours_ago < 6:
                        recency_bonus = 0.2
                    elif hours_ago < 24:
                        recency_bonus = 0.15
                    elif hours_ago < 72:
                        recency_bonus = 0.05
                except (ValueError, TypeError):
                    pass

            # Source weight
            source_weights = {
                "arxiv": 0.85,
                "hackernews": 0.9,
                "reddit": 0.7,
                "github": 0.8,
                "ai_blogs": 0.95,
                "huggingface": 0.85,
            }
            source_weight = source_weights.get(item.source, 0.5)

            # Final score
            item.score = min(1.0, (item.score * source_weight) + recency_bonus)

        return items

    # -- clustering ---------------------------------------------------------

    def _cluster_by_topic(self, items: List[TrendingItem]) -> List[AggregatedTopic]:
        """Cluster items into predefined topic categories."""
        topic_items: Dict[str, List[TrendingItem]] = defaultdict(list)
        unclustered: List[TrendingItem] = []

        for item in items:
            matched = False
            text = item.text_for_embedding.lower()
            for topic, keywords in TOPIC_CLUSTERS.items():
                if any(kw in text for kw in keywords):
                    topic_items[topic].append(item)
                    matched = True
                    break  # one cluster per item
            if not matched:
                unclustered.append(item)

        # Build AggregatedTopics
        result: List[AggregatedTopic] = []
        for topic, cluster_items in topic_items.items():
            sources = list(set(i.source for i in cluster_items))
            avg_score = sum(i.score for i in cluster_items) / len(cluster_items)
            result.append(AggregatedTopic(
                topic=topic,
                items=sorted(cluster_items, key=lambda i: i.score, reverse=True),
                combined_score=avg_score,
                source_count=len(sources),
                unique_sources=sources,
            ))

        # Add unclustered as "Other / Emerging"
        if unclustered:
            sources = list(set(i.source for i in unclustered))
            result.append(AggregatedTopic(
                topic="Other / Emerging",
                items=sorted(unclustered, key=lambda i: i.score, reverse=True),
                combined_score=sum(i.score for i in unclustered) / len(unclustered),
                source_count=len(sources),
                unique_sources=sources,
            ))

        return result
