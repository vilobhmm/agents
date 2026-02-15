"""Web scraping utilities"""

import logging
from typing import Dict, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraping and content extraction"""

    def __init__(self, user_agent: Optional[str] = None):
        self.user_agent = user_agent or "OpenClaw/0.1.0"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    async def fetch_url(self, url: str) -> Optional[str]:
        """Fetch content from a URL"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def extract_text(self, url: str) -> Optional[str]:
        """Extract main text content from a URL"""
        html = await self.fetch_url(url)
        if not html:
            return None

        try:
            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None

    async def extract_links(self, url: str) -> List[str]:
        """Extract all links from a URL"""
        html = await self.fetch_url(url)
        if not html:
            return []

        try:
            soup = BeautifulSoup(html, "html.parser")
            links = []

            for link in soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("http"):
                    links.append(href)

            return links

        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []

    async def parse_feed(self, feed_url: str, max_entries: int = 10) -> List[Dict]:
        """
        Parse an RSS/Atom feed.

        Args:
            feed_url: Feed URL
            max_entries: Maximum number of entries to return

        Returns:
            List of feed entries
        """
        try:
            feed = feedparser.parse(feed_url)
            entries = []

            for entry in feed.entries[:max_entries]:
                entries.append(
                    {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", ""),
                        "author": entry.get("author", ""),
                    }
                )

            return entries

        except Exception as e:
            logger.error(f"Error parsing feed: {e}")
            return []

    async def download_file(self, url: str, output_path: str) -> bool:
        """Download a file from a URL"""
        try:
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded {url} to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return False
