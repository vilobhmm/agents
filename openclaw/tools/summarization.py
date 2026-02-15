"""Text summarization utilities"""

import logging
import os
from typing import List, Optional

import anthropic


logger = logging.getLogger(__name__)


class Summarizer:
    """Text summarization using Claude"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("Anthropic API key not provided")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    async def summarize(
        self,
        text: str,
        style: str = "concise",
        max_tokens: int = 1024,
    ) -> Optional[str]:
        """
        Summarize text.

        Args:
            text: Text to summarize
            style: Summarization style (concise, detailed, bullet_points)
            max_tokens: Maximum tokens in summary

        Returns:
            Summary text
        """
        if not self.client:
            logger.error("Summarizer not initialized")
            return None

        style_prompts = {
            "concise": "Provide a concise summary in 2-3 sentences.",
            "detailed": "Provide a detailed summary covering all key points.",
            "bullet_points": "Provide a summary as bullet points of key takeaways.",
        }

        prompt = f"""Please summarize the following text.

{style_prompts.get(style, style_prompts['concise'])}

Text to summarize:
{text}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            summary = ""
            for block in response.content:
                if hasattr(block, "text"):
                    summary += block.text

            return summary.strip()

        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return None

    async def extract_key_points(
        self, text: str, num_points: int = 5
    ) -> List[str]:
        """
        Extract key points from text.

        Args:
            text: Text to analyze
            num_points: Number of key points to extract

        Returns:
            List of key points
        """
        if not self.client:
            logger.error("Summarizer not initialized")
            return []

        prompt = f"""Extract the {num_points} most important key points from the following text.
Return only the key points, one per line, without numbering.

Text:
{text}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            points_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    points_text += block.text

            points = [
                p.strip("- ").strip()
                for p in points_text.strip().split("\n")
                if p.strip()
            ]
            return points[:num_points]

        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []

    async def generate_briefing(
        self, articles: List[dict], topic: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a briefing from multiple articles.

        Args:
            articles: List of article dicts with 'title', 'summary', 'url'
            topic: Optional topic/theme

        Returns:
            Briefing text
        """
        if not self.client:
            logger.error("Summarizer not initialized")
            return None

        articles_text = "\n\n".join(
            [
                f"Title: {a.get('title', 'Untitled')}\nSummary: {a.get('summary', '')}\nURL: {a.get('url', '')}"
                for a in articles
            ]
        )

        topic_context = f" on the topic of {topic}" if topic else ""
        prompt = f"""Generate a comprehensive briefing{topic_context} based on the following articles.

Include:
1. An overview of key themes
2. Important insights and takeaways
3. Notable trends or patterns

Articles:
{articles_text}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            briefing = ""
            for block in response.content:
                if hasattr(block, "text"):
                    briefing += block.text

            return briefing.strip()

        except Exception as e:
            logger.error(f"Error generating briefing: {e}")
            return None
