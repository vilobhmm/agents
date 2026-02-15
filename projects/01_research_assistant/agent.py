"""Research Assistant Agent"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration
from openclaw.tools.summarization import Summarizer
from openclaw.tools.web_scraping import WebScraper

from .config import ResearchAssistantConfig
from .reading_lists import PocketReader, InstapaperReader


logger = logging.getLogger(__name__)


class ResearchAssistantAgent(Agent):
    """Personal Research Assistant Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Research Assistant",
            description="I monitor your reading lists, summarize articles, and send briefings.",
            proactive=True,
        )

        super().__init__(config, api_key)

        # Load configuration
        self.app_config = ResearchAssistantConfig()

        # Initialize integrations
        self.whatsapp = WhatsAppIntegration()
        self.calendar = CalendarIntegration()
        self.notion = NotionIntegration()

        # Initialize tools
        self.summarizer = Summarizer(api_key)
        self.scraper = WebScraper()

        # Initialize reading list readers
        self.readers = {
            "pocket": PocketReader(),
            "instapaper": InstapaperReader(),
        }

        # Storage for processed articles
        self.articles = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        action = input_data.get("action", "fetch_and_process")

        if action == "fetch_and_process":
            return await self.fetch_and_process_articles()
        elif action == "send_briefing":
            return await self.send_morning_briefing()
        else:
            logger.warning(f"Unknown action: {action}")
            return {"error": f"Unknown action: {action}"}

    async def fetch_and_process_articles(self) -> Dict[str, Any]:
        """Fetch articles from reading lists and process them"""
        logger.info("Fetching articles from reading lists")

        all_articles = []

        # Fetch from all configured sources
        for source in self.app_config.sources:
            reader = self.readers.get(source)
            if reader:
                articles = await reader.get_unread_articles(
                    limit=self.app_config.max_articles_per_day
                )
                all_articles.extend(articles)

        logger.info(f"Fetched {len(all_articles)} articles")

        # Process each article
        processed_articles = []
        for article in all_articles[: self.app_config.max_articles_per_day]:
            processed = await self.process_article(article)
            if processed:
                processed_articles.append(processed)

        self.articles = processed_articles
        self.set_context("last_fetch", datetime.now().isoformat())

        return {
            "status": "success",
            "articles_processed": len(processed_articles),
            "articles": processed_articles,
        }

    async def process_article(self, article: Dict) -> Dict:
        """Process a single article"""
        logger.info(f"Processing: {article.get('title', 'Untitled')}")

        url = article.get("url")
        title = article.get("title", "Untitled")

        # Extract full text
        text = await self.scraper.extract_text(url)
        if not text or len(text) < 100:
            logger.warning(f"Could not extract text from {url}")
            return None

        # Generate summary
        summary = await self.summarizer.summarize(
            text, style=self.app_config.summary_style
        )

        # Extract key points
        key_points = await self.summarizer.extract_key_points(text)

        # Create Notion page
        notion_page_id = await self.create_notion_page(
            title=title,
            url=url,
            summary=summary,
            key_points=key_points,
            source=article.get("source", "unknown"),
        )

        return {
            "title": title,
            "url": url,
            "summary": summary,
            "key_points": key_points,
            "notion_page_id": notion_page_id,
            "source": article.get("source"),
        }

    async def create_notion_page(
        self, title: str, url: str, summary: str, key_points: List[str], source: str
    ) -> str:
        """Create a Notion page for an article"""

        # Format key points as text
        key_points_text = "\n".join(f"- {point}" for point in key_points)

        # Create page content
        content = self.app_config.notion_page_template.format(
            title=title,
            source=source,
            date=datetime.now().strftime("%Y-%m-%d"),
            url=url,
            summary=summary,
            key_points=key_points_text,
        )

        # Create blocks
        children = [
            self.notion.create_heading_block(title, level=1),
            self.notion.create_text_block(f"Source: {source}"),
            self.notion.create_text_block(
                f"Date: {datetime.now().strftime('%Y-%m-%d')}"
            ),
            self.notion.create_text_block(f"URL: {url}"),
            self.notion.create_heading_block("Summary", level=2),
            self.notion.create_text_block(summary),
            self.notion.create_heading_block("Key Takeaways", level=2),
        ]

        # Add key points
        for point in key_points:
            children.append(self.notion.create_bulleted_list_block(point))

        # Create page
        page_id = await self.notion.create_page(
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "URL": {"url": url},
                "Source": {"select": {"name": source}},
            },
            children=children,
        )

        logger.info(f"Created Notion page: {page_id}")
        return page_id

    async def send_morning_briefing(self) -> Dict[str, Any]:
        """Send morning briefing via WhatsApp"""
        logger.info("Sending morning briefing")

        if not self.articles:
            logger.info("No articles to brief")
            return {"status": "no_articles"}

        # Generate briefing
        articles_summary = []
        for i, article in enumerate(self.articles, 1):
            summary_text = f"{i}. *{article['title']}*\n"
            summary_text += f"   {article['summary']}\n"
            summary_text += f"   {article['url']}\n"
            articles_summary.append(summary_text)

        briefing = self.app_config.briefing_template.format(
            date=datetime.now().strftime("%B %d, %Y"),
            articles_summary="\n".join(articles_summary),
            reading_time=self.app_config.reading_block_duration,
            reading_block_time=self.app_config.reading_block_time,
        )

        # Send via WhatsApp
        recipient = os.getenv("WHATSAPP_RECIPIENT")
        if recipient:
            await self.whatsapp.send_message(recipient, briefing)
            logger.info("Briefing sent via WhatsApp")

        # Create calendar block if configured
        if self.app_config.create_reading_blocks and self.articles:
            await self.create_reading_block()

        return {"status": "success", "articles_count": len(self.articles)}

    async def create_reading_block(self):
        """Create a calendar block for reading"""
        hour, minute = map(int, self.app_config.reading_block_time.split(":"))
        start_time = datetime.now().replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )

        if start_time < datetime.now():
            start_time += timedelta(days=1)

        event_id = await self.calendar.create_block(
            title="📚 Deep Reading Session",
            duration_minutes=self.app_config.reading_block_duration,
            start_time=start_time,
        )

        logger.info(f"Created reading block: {event_id}")
        return event_id
