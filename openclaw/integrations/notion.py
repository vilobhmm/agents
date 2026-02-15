"""Notion integration"""

import logging
import os
from typing import Any, Dict, List, Optional

from notion_client import Client


logger = logging.getLogger(__name__)


class NotionIntegration:
    """Notion API integration"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        database_id: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")

        if not self.api_key:
            logger.warning("Notion API key not provided")
            self.client = None
        else:
            self.client = Client(auth=self.api_key)
            logger.info("Notion client initialized")

    async def create_page(
        self,
        database_id: Optional[str] = None,
        properties: Optional[Dict] = None,
        children: Optional[List] = None,
    ) -> Optional[str]:
        """
        Create a new page in a database.

        Args:
            database_id: Database ID (uses default if not provided)
            properties: Page properties
            children: Page content blocks

        Returns:
            Page ID if successful
        """
        if not self.client:
            logger.error("Notion client not initialized")
            return None

        db_id = database_id or self.database_id
        if not db_id:
            logger.error("No database ID provided")
            return None

        try:
            page_data = {"parent": {"database_id": db_id}}

            if properties:
                page_data["properties"] = properties
            if children:
                page_data["children"] = children

            response = self.client.pages.create(**page_data)
            logger.info(f"Created Notion page: {response['id']}")
            return response["id"]

        except Exception as e:
            logger.error(f"Error creating Notion page: {e}")
            return None

    async def update_page(
        self, page_id: str, properties: Dict
    ) -> bool:
        """
        Update a page's properties.

        Args:
            page_id: Page ID
            properties: Properties to update

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Notion client not initialized")
            return False

        try:
            self.client.pages.update(page_id=page_id, properties=properties)
            logger.info(f"Updated Notion page: {page_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating Notion page: {e}")
            return False

    async def query_database(
        self,
        database_id: Optional[str] = None,
        filter_dict: Optional[Dict] = None,
        sorts: Optional[List] = None,
    ) -> List[Dict]:
        """
        Query a database.

        Args:
            database_id: Database ID
            filter_dict: Filter criteria
            sorts: Sort criteria

        Returns:
            List of pages
        """
        if not self.client:
            logger.error("Notion client not initialized")
            return []

        db_id = database_id or self.database_id
        if not db_id:
            logger.error("No database ID provided")
            return []

        try:
            query_params = {}
            if filter_dict:
                query_params["filter"] = filter_dict
            if sorts:
                query_params["sorts"] = sorts

            response = self.client.databases.query(
                database_id=db_id, **query_params
            )
            return response["results"]

        except Exception as e:
            logger.error(f"Error querying Notion database: {e}")
            return []

    async def append_block_children(
        self, block_id: str, children: List[Dict]
    ) -> bool:
        """
        Append blocks to a page.

        Args:
            block_id: Page/block ID
            children: Blocks to append

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Notion client not initialized")
            return False

        try:
            self.client.blocks.children.append(block_id=block_id, children=children)
            logger.info(f"Appended blocks to: {block_id}")
            return True

        except Exception as e:
            logger.error(f"Error appending blocks: {e}")
            return False

    def create_text_block(self, text: str) -> Dict:
        """Create a paragraph text block"""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            },
        }

    def create_heading_block(self, text: str, level: int = 2) -> Dict:
        """Create a heading block"""
        heading_type = f"heading_{level}"
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            },
        }

    def create_bulleted_list_block(self, text: str) -> Dict:
        """Create a bulleted list item"""
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            },
        }
