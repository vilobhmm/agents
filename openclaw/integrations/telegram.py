"""Telegram integration"""

import logging
import os
from typing import List, Optional

from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


logger = logging.getLogger(__name__)


class TelegramIntegration:
    """Telegram Bot integration"""

    def __init__(
        self,
        token: Optional[str] = None,
        chat_id: Optional[str] = None,
    ):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

        if not self.token:
            logger.warning("Telegram bot token not provided")
            self.bot = None
        else:
            self.bot = Bot(token=self.token)
            logger.info("Telegram bot initialized")

    async def send_message(
        self, message: str, chat_id: Optional[str] = None, parse_mode: str = "Markdown"
    ) -> bool:
        """
        Send a message via Telegram.

        Args:
            message: Message text
            chat_id: Chat ID (uses default if not provided)
            parse_mode: Message formatting (Markdown or HTML)

        Returns:
            True if successful
        """
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False

        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            logger.error("No chat ID provided")
            return False

        try:
            await self.bot.send_message(
                chat_id=target_chat_id, text=message, parse_mode=parse_mode
            )
            logger.info(f"Telegram message sent to {target_chat_id}")
            return True

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    async def send_photo(
        self, photo_url: str, caption: Optional[str] = None, chat_id: Optional[str] = None
    ) -> bool:
        """Send a photo via Telegram"""
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False

        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            logger.error("No chat ID provided")
            return False

        try:
            await self.bot.send_photo(
                chat_id=target_chat_id, photo=photo_url, caption=caption
            )
            logger.info(f"Telegram photo sent to {target_chat_id}")
            return True

        except Exception as e:
            logger.error(f"Error sending Telegram photo: {e}")
            return False

    async def send_document(
        self, document_url: str, caption: Optional[str] = None, chat_id: Optional[str] = None
    ) -> bool:
        """Send a document via Telegram"""
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False

        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            logger.error("No chat ID provided")
            return False

        try:
            await self.bot.send_document(
                chat_id=target_chat_id, document=document_url, caption=caption
            )
            logger.info(f"Telegram document sent to {target_chat_id}")
            return True

        except Exception as e:
            logger.error(f"Error sending Telegram document: {e}")
            return False

    def create_application(self) -> Application:
        """Create a Telegram application for handling updates"""
        if not self.token:
            raise ValueError("Telegram bot token not provided")

        return Application.builder().token(self.token).build()

    async def get_updates(self) -> List[Update]:
        """Get recent updates"""
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return []

        try:
            updates = await self.bot.get_updates()
            return updates
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []
