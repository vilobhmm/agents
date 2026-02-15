"""Research Paper Digest Pipeline Agent"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.telegram import TelegramIntegration
from openclaw.tools.summarization import Summarizer
from openclaw.tools.web_scraping import WebScraper


logger = logging.getLogger(__name__)


class ResearchDigestAgent(Agent):
    """Research Paper Digest Pipeline Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Research Digest",
            description="I monitor research feeds, analyze papers, and send curated digests.",
            proactive=True,
        )

        super().__init__(config, api_key)

        self.scraper = WebScraper()
        self.summarizer = Summarizer(api_key)
        self.notion = NotionIntegration()
        self.telegram = TelegramIntegration()

        # Configure topics
        self.topics = os.getenv("ARXIV_CATEGORIES", "cs.AI,cs.LG,cs.CL").split(",")

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Monitoring arXiv feeds")

        all_papers = []

        # Fetch papers for each topic
        for topic in self.topics:
            feed_url = f"http://export.arxiv.org/rss/{topic}"
            papers = await self.scraper.parse_feed(feed_url, max_entries=20)
            all_papers.extend(papers)

        logger.info(f"Found {len(all_papers)} new papers")

        # Analyze and filter papers
        relevant_papers = []
        for paper in all_papers:
            if await self.is_relevant(paper):
                analyzed = await self.analyze_paper(paper)
                if analyzed:
                    relevant_papers.append(analyzed)

        logger.info(f"Found {len(relevant_papers)} relevant papers")

        # Store in knowledge base
        for paper in relevant_papers:
            await self.store_paper(paper)

        # Send weekly digest
        if relevant_papers:
            await self.send_digest(relevant_papers)

        return {"status": "success", "papers_processed": len(relevant_papers)}

    async def is_relevant(self, paper: Dict) -> bool:
        """Check if paper is relevant to user interests"""

        prompt = f"""Is this paper relevant to AI/ML research and practical applications?

Title: {paper.get('title', '')}
Summary: {paper.get('summary', '')}

Answer with just YES or NO."""

        response = await self.chat(prompt)

        return "YES" in response.upper()

    async def analyze_paper(self, paper: Dict) -> Dict:
        """Analyze a research paper"""

        title = paper.get("title", "")
        summary = paper.get("summary", "")
        link = paper.get("link", "")

        logger.info(f"Analyzing: {title}")

        prompt = f"""Analyze this research paper:

Title: {title}
Abstract: {summary}

Provide a structured analysis:

**Problem:** What problem does this paper address?

**Method:** What approach/method does it propose?

**Results:** What are the key findings?

**Implications:** Why does this matter?

**Practical Applications:** How could this be used in practice?

Keep each section to 1-2 sentences."""

        analysis = await self.chat(prompt)

        return {
            "title": title,
            "url": link,
            "abstract": summary,
            "published": paper.get("published", ""),
            "author": paper.get("author", ""),
            "analysis": analysis,
        }

    async def store_paper(self, paper: Dict):
        """Store paper in Notion knowledge base"""

        properties = {
            "Name": {"title": [{"text": {"content": paper.get("title", "")}}]},
            "URL": {"url": paper.get("url", "")},
            "Date": {
                "date": {
                    "start": paper.get("published", datetime.now().isoformat())
                }
            },
        }

        children = [
            self.notion.create_heading_block(paper.get("title", ""), level=1),
            self.notion.create_text_block(f"Author: {paper.get('author', '')}"),
            self.notion.create_text_block(f"Published: {paper.get('published', '')}"),
            self.notion.create_text_block(f"URL: {paper.get('url', '')}"),
            self.notion.create_heading_block("Abstract", level=2),
            self.notion.create_text_block(paper.get("abstract", "")),
            self.notion.create_heading_block("Analysis", level=2),
            self.notion.create_text_block(paper.get("analysis", "")),
        ]

        page_id = await self.notion.create_page(properties=properties, children=children)

        logger.info(f"Stored paper in Notion: {page_id}")

    async def send_digest(self, papers: List[Dict]):
        """Send weekly research digest"""

        # Select top 5 papers
        top_papers = papers[:5]

        digest = "📚 Weekly Research Digest\n\n"

        for i, paper in enumerate(top_papers, 1):
            digest += f"{i}. *{paper['title']}*\n"
            digest += f"   {paper['analysis'][:300]}...\n"
            digest += f"   {paper['url']}\n\n"

        digest += f"\nTotal papers analyzed: {len(papers)}"

        await self.telegram.send_message(digest)
        logger.info("Sent research digest")
