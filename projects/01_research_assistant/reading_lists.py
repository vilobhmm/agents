"""Reading list integrations"""

import logging
import os
from typing import Dict, List

import requests


logger = logging.getLogger(__name__)


class PocketReader:
    """Pocket reading list integration"""

    def __init__(self):
        self.consumer_key = os.getenv("POCKET_CONSUMER_KEY")
        self.access_token = os.getenv("POCKET_ACCESS_TOKEN")
        self.base_url = "https://getpocket.com/v3"

    async def get_unread_articles(self, limit: int = 10) -> List[Dict]:
        """Get unread articles from Pocket"""
        if not self.consumer_key or not self.access_token:
            logger.warning("Pocket credentials not configured")
            return []

        try:
            response = requests.post(
                f"{self.base_url}/get",
                json={
                    "consumer_key": self.consumer_key,
                    "access_token": self.access_token,
                    "state": "unread",
                    "sort": "newest",
                    "count": limit,
                    "detailType": "complete",
                },
            )

            if response.status_code == 200:
                data = response.json()
                items = data.get("list", {})

                articles = []
                for item_id, item in items.items():
                    articles.append(
                        {
                            "id": item_id,
                            "title": item.get("resolved_title")
                            or item.get("given_title", "Untitled"),
                            "url": item.get("resolved_url") or item.get("given_url"),
                            "excerpt": item.get("excerpt", ""),
                            "source": "pocket",
                        }
                    )

                return articles
            else:
                logger.error(f"Pocket API error: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error fetching from Pocket: {e}")
            return []


class InstapaperReader:
    """Instapaper reading list integration"""

    def __init__(self):
        self.username = os.getenv("INSTAPAPER_USERNAME")
        self.password = os.getenv("INSTAPAPER_PASSWORD")
        self.base_url = "https://www.instapaper.com/api"

    async def get_unread_articles(self, limit: int = 10) -> List[Dict]:
        """Get unread articles from Instapaper"""
        if not self.username or not self.password:
            logger.warning("Instapaper credentials not configured")
            return []

        # Note: This is a simplified implementation
        # For production, use the full Instapaper API with OAuth
        logger.info("Instapaper integration requires OAuth setup")
        return []
