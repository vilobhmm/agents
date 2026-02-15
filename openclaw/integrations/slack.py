"""Slack integration"""

import logging
import os
from typing import Dict, List, Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)


class SlackIntegration:
    """Slack API integration"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        if not self.token:
            logger.warning("Slack bot token not provided")
            self.client = None
        else:
            self.client = WebClient(token=self.token)
            logger.info("Slack client initialized")

    async def send_message(self, channel: str, text: str, **kwargs) -> bool:
        """
        Send a message to a Slack channel.

        Args:
            channel: Channel ID or name
            text: Message text
            **kwargs: Additional Slack API parameters

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Slack client not initialized")
            return False

        try:
            response = self.client.chat_postMessage(
                channel=channel, text=text, **kwargs
            )
            logger.info(f"Message sent to {channel}")
            return response["ok"]
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
            return False

    async def get_messages(
        self, channel: str, limit: int = 10
    ) -> List[Dict]:
        """
        Get recent messages from a channel.

        Args:
            channel: Channel ID
            limit: Number of messages to retrieve

        Returns:
            List of messages
        """
        if not self.client:
            logger.error("Slack client not initialized")
            return []

        try:
            response = self.client.conversations_history(
                channel=channel, limit=limit
            )
            return response["messages"]
        except SlackApiError as e:
            logger.error(f"Error fetching messages: {e.response['error']}")
            return []

    async def search_messages(self, query: str, count: int = 20) -> List[Dict]:
        """
        Search for messages.

        Args:
            query: Search query
            count: Number of results

        Returns:
            List of matching messages
        """
        if not self.client:
            logger.error("Slack client not initialized")
            return []

        try:
            response = self.client.search_messages(query=query, count=count)
            return response["messages"]["matches"]
        except SlackApiError as e:
            logger.error(f"Error searching messages: {e.response['error']}")
            return []

    async def update_status(self, status_text: str, status_emoji: str = ":robot_face:") -> bool:
        """
        Update user status.

        Args:
            status_text: Status message
            status_emoji: Status emoji

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Slack client not initialized")
            return False

        try:
            response = self.client.users_profile_set(
                profile={
                    "status_text": status_text,
                    "status_emoji": status_emoji,
                }
            )
            return response["ok"]
        except SlackApiError as e:
            logger.error(f"Error updating status: {e.response['error']}")
            return False

    async def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        if not self.client:
            return None

        try:
            response = self.client.users_info(user=user_id)
            return response["user"]
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e.response['error']}")
            return None
