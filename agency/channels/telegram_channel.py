"""Telegram channel integration for agency system.

Connects Telegram bot to the file-based queue system.
"""

import asyncio
import logging
from pathlib import Path
import time
from typing import Optional
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from agency.core.types import MessageData
from agency.core.queue import FileQueue


logger = logging.getLogger(__name__)


class TelegramChannel:
    """
    Telegram bot channel integration.

    Responsibilities:
    1. Receive messages from Telegram
    2. Write to incoming queue
    3. Poll outgoing queue
    4. Send responses back to Telegram
    """

    def __init__(
        self,
        bot_token: str,
        queue: FileQueue,
        allowed_users: Optional[list] = None
    ):
        """
        Initialize Telegram channel.

        Args:
            bot_token: Telegram bot token
            queue: File queue instance
            allowed_users: List of allowed user IDs (if None, allow all)
        """
        self.bot_token = bot_token
        self.queue = queue
        self.allowed_users = set(allowed_users) if allowed_users else None

        # Create Telegram application
        self.app = Application.builder().token(bot_token).build()

        # Add handlers
        self.app.add_handler(CommandHandler("start", self._handle_start))
        self.app.add_handler(CommandHandler("help", self._handle_help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

        logger.info("Telegram channel initialized")

    async def start(self):
        """Start Telegram bot (runs forever)"""
        logger.info("Starting Telegram bot...")

        # Start polling outgoing queue in background
        asyncio.create_task(self._poll_outgoing())

        # Start bot
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Telegram bot...")
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()

    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        await update.message.reply_text(
            f"👋 Hi {user.first_name}!\n\n"
            "I'm your Agency assistant. I coordinate a team of AI agents to help you.\n\n"
            "**How to use:**\n"
            "Send messages in this format:\n"
            "`@agent_id your message here`\n\n"
            "**Example:**\n"
            "`@researcher What's new in AI today?`\n\n"
            "Type /help to see available agents and teams."
        )

    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
**Available Commands:**

• `/start` - Start the bot
• `/help` - Show this help message

**How to talk to agents:**

Use `@agent_id` to route messages:
```
@researcher What's new in AI?
@social Post a tweet about AI trends
@writer Draft a newsletter
```

**Available Agents:**
• `@researcher` - Research assistant (AI news, papers, trends)
• `@social` - Social media manager (Twitter, LinkedIn)
• `@writer` - Content writer (newsletters, articles)

**Teams:**
• `@content` - Full content creation team

Just message me naturally with an @mention!
"""
        await update.message.reply_text(help_text)

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        user = update.effective_user
        message_text = update.message.text

        # Check if user is allowed
        if self.allowed_users and str(user.id) not in self.allowed_users:
            logger.warning(f"Unauthorized user: {user.id} ({user.username})")
            await update.message.reply_text(
                "Sorry, you're not authorized to use this bot. "
                "Contact the administrator to get access."
            )
            return

        # Create message data
        message_data = MessageData(
            channel="telegram",
            sender=user.username or user.first_name,
            sender_id=str(user.id),
            message=message_text,
            timestamp=time.time(),
            message_id=str(update.message.message_id),
            metadata={
                "chat_id": update.effective_chat.id,
                "user_id": user.id,
            }
        )

        # Enqueue message
        self.queue.enqueue(message_data, "incoming")

        logger.info(f"Received message from {user.username}: {message_text[:50]}")

        # Send acknowledgment
        await update.message.reply_text("✓ Message received, processing...")

    async def _poll_outgoing(self):
        """Poll outgoing queue and send responses to Telegram"""
        logger.info("Starting outgoing queue poller...")

        while True:
            try:
                # Check outgoing queue
                for queued_message in self.queue.iter_outgoing():
                    if queued_message.data.channel != "telegram":
                        continue

                    # Get chat ID from metadata
                    chat_id = queued_message.data.metadata.get("chat_id")
                    if not chat_id:
                        logger.error("No chat_id in message metadata")
                        self.queue.delete_outgoing(queued_message.path)
                        continue

                    # Send response
                    try:
                        await self.app.bot.send_message(
                            chat_id=chat_id,
                            text=queued_message.data.message
                        )

                        logger.info(f"Sent response to chat {chat_id}")

                        # Delete from outgoing queue
                        self.queue.delete_outgoing(queued_message.path)

                    except Exception as e:
                        logger.error(f"Error sending message to Telegram: {e}")
                        # Don't delete - will retry

                # Sleep briefly
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Error in outgoing poller: {e}", exc_info=True)
                await asyncio.sleep(1)
