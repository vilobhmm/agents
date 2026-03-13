"""
Analyst Agent

The "researcher" agent that deep-dives into trending topics.
Takes curated items from the Curator and generates rich analysis
with Claude, identifying connections and assigning reading levels.
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.rag_recommendation.scrapers.trending_scraper import TrendingItem
from agents.rag_recommendation.scrapers.source_aggregator import AggregatedTopic

logger = logging.getLogger(__name__)


@dataclass
class TopicAnalysis:
    """Deep analysis of a trending topic cluster."""
    topic: str
    heat_score: float
    item_count: int
    summary: str                            # LLM-generated overview
    why_it_matters: str                     # significance explanation
    key_developments: List[str]             # bullet points
    related_topics: List[str]               # cross-references
    reading_level: str                      # "beginner" / "intermediate" / "advanced"
    top_items: List[Dict[str, Any]]         # serialized top items
    generated_at: str = ""

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "heat_score": self.heat_score,
            "item_count": self.item_count,
            "summary": self.summary,
            "why_it_matters": self.why_it_matters,
            "key_developments": self.key_developments,
            "related_topics": self.related_topics,
            "reading_level": self.reading_level,
            "top_items": self.top_items,
            "generated_at": self.generated_at,
        }


# ---------------------------------------------------------------------------
# Analyst prompts
# ---------------------------------------------------------------------------

ANALYSIS_SYSTEM = """You are an expert AI research analyst specializing in AI agents, 
agentic AI, and multi-agent systems. Your job is to analyze trending content and 
produce insightful, concise analysis that helps researchers and engineers stay current.

Always respond in valid JSON format with the following structure:
{
  "summary": "2-3 sentence overview of this topic cluster",
  "why_it_matters": "1-2 sentence significance explanation",
  "key_developments": ["development 1", "development 2", "development 3"],
  "related_topics": ["related topic 1", "related topic 2"],
  "reading_level": "beginner|intermediate|advanced"
}
"""

ANALYSIS_PROMPT = """Analyze these trending items for the topic "{topic}":

{items_text}

Based on these {count} items:
1. Summarize the overall trend in 2-3 sentences
2. Explain why this matters to AI practitioners
3. List 3-5 key developments or takeaways
4. Identify 2-3 related topics worth exploring
5. Assess the reading level (beginner/intermediate/advanced)

Respond ONLY with valid JSON matching the specified structure."""


class AnalystAgent:
    """
    Analyst Agent — generates deep analysis for trending topics.

    Uses Claude to synthesize insights from curated content.
    Falls back to rule-based analysis when API is unavailable.

    Usage:
        analyst = AnalystAgent()
        analyses = await analyst.analyze_topics(topics)
    """

    def __init__(self):
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
                    logger.warning("anthropic package not installed")
        return self._anthropic_client

    async def analyze_topics(
        self,
        topics: List[AggregatedTopic],
        max_topics: int = 10,
    ) -> List[TopicAnalysis]:
        """
        Analyze top trending topic clusters.

        Args:
            topics: Aggregated topics from Curator.
            max_topics: Max topics to analyze.

        Returns:
            List of TopicAnalysis objects.
        """
        logger.info(f"📊 Analyst Agent: analyzing {min(len(topics), max_topics)} topics...")

        analyses: List[TopicAnalysis] = []
        for topic in topics[:max_topics]:
            analysis = await self._analyze_single(topic)
            analyses.append(analysis)

        logger.info(f"Analyst: completed {len(analyses)} topic analyses")
        return analyses

    async def analyze_single_item(self, item: TrendingItem) -> Dict[str, Any]:
        """Generate a quick analysis for a single item."""
        return {
            "title": item.title,
            "source": item.source,
            "score": item.score,
            "quick_take": await self._generate_quick_take(item),
        }

    async def _analyze_single(self, topic: AggregatedTopic) -> TopicAnalysis:
        """Analyze a single topic cluster using LLM or fallback."""
        items_text = self._format_items_for_prompt(topic.items[:10])

        # Try LLM analysis
        if self._client:
            try:
                result = await self._llm_analyze(topic.topic, items_text, len(topic.items))
                return TopicAnalysis(
                    topic=topic.topic,
                    heat_score=topic.heat_score,
                    item_count=len(topic.items),
                    summary=result.get("summary", ""),
                    why_it_matters=result.get("why_it_matters", ""),
                    key_developments=result.get("key_developments", []),
                    related_topics=result.get("related_topics", []),
                    reading_level=result.get("reading_level", "intermediate"),
                    top_items=[i.to_dict() for i in topic.items[:5]],
                )
            except Exception as e:
                logger.warning(f"LLM analysis failed for '{topic.topic}': {e}")

        # Fallback: rule-based analysis
        return self._rule_based_analysis(topic)

    async def _llm_analyze(
        self, topic: str, items_text: str, count: int
    ) -> Dict[str, Any]:
        """Use Claude to analyze a topic."""
        import json as json_mod

        prompt = ANALYSIS_PROMPT.format(
            topic=topic, items_text=items_text, count=count
        )

        response = await asyncio.to_thread(
            self._client.messages.create,
            model=self._model,
            max_tokens=1024,
            system=ANALYSIS_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()

        # Extract JSON from response (handle markdown code blocks)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json_mod.loads(text)

    def _rule_based_analysis(self, topic: AggregatedTopic) -> TopicAnalysis:
        """Fallback analysis without LLM."""
        source_list = ", ".join(topic.unique_sources)
        titles = [i.title for i in topic.items[:5]]

        return TopicAnalysis(
            topic=topic.topic,
            heat_score=topic.heat_score,
            item_count=len(topic.items),
            summary=(
                f"{topic.topic} is trending with {len(topic.items)} items "
                f"across {source_list}. Key activity includes discussions, "
                f"new papers, and open-source projects."
            ),
            why_it_matters=(
                f"This topic is showing strong signals across {len(topic.unique_sources)} "
                f"sources, indicating growing industry and research interest."
            ),
            key_developments=[
                f"'{t[:80]}...'" if len(t) > 80 else f"'{t}'"
                for t in titles[:4]
            ],
            related_topics=self._infer_related(topic.topic),
            reading_level=self._infer_reading_level(topic),
            top_items=[i.to_dict() for i in topic.items[:5]],
        )

    async def _generate_quick_take(self, item: TrendingItem) -> str:
        """Generate a one-liner take on a single item."""
        if self._client:
            try:
                response = await asyncio.to_thread(
                    self._client.messages.create,
                    model=self._model,
                    max_tokens=100,
                    messages=[{
                        "role": "user",
                        "content": (
                            f"In one concise sentence, explain why this is noteworthy "
                            f"for AI practitioners:\n\n"
                            f"Title: {item.title}\n"
                            f"Summary: {item.summary[:200]}"
                        ),
                    }],
                )
                return response.content[0].text.strip()
            except Exception:
                pass
        return f"Trending on {item.source} with score {item.score:.2f}"

    def _format_items_for_prompt(self, items: List[TrendingItem]) -> str:
        """Format items as text for the LLM prompt."""
        lines = []
        for i, item in enumerate(items, 1):
            lines.append(f"{i}. [{item.source}] {item.title}")
            if item.summary:
                lines.append(f"   {item.summary[:150]}")
            lines.append(f"   URL: {item.url}")
            lines.append("")
        return "\n".join(lines)

    def _infer_related(self, topic: str) -> List[str]:
        """Infer related topics from known relationships."""
        relations = {
            "Agent Frameworks": ["Multi-Agent Systems", "Tool Use & Function Calling"],
            "Multi-Agent Systems": ["Agent Frameworks", "Reasoning & Planning"],
            "RAG & Retrieval": ["LLM Architecture", "Agent Memory"],
            "Reasoning & Planning": ["Multi-Agent Systems", "Autonomous Agents"],
            "Tool Use & Function Calling": ["Agent Frameworks", "Code Agents"],
            "Agent Memory": ["RAG & Retrieval", "Autonomous Agents"],
            "LLM Architecture": ["RAG & Retrieval", "Multimodal Agents"],
            "Autonomous Agents": ["Reasoning & Planning", "Agent Memory"],
            "Code Agents": ["Tool Use & Function Calling", "Autonomous Agents"],
            "Multimodal Agents": ["LLM Architecture", "Autonomous Agents"],
        }
        return relations.get(topic, ["AI Agents", "Agentic AI"])

    def _infer_reading_level(self, topic: AggregatedTopic) -> str:
        """Infer reading level from content sources."""
        arxiv_ratio = sum(1 for i in topic.items if i.source == "arxiv") / max(len(topic.items), 1)
        if arxiv_ratio > 0.6:
            return "advanced"
        elif arxiv_ratio > 0.3:
            return "intermediate"
        return "beginner"
