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

from agency.core.types import MessageData, AgencyConfig
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
        allowed_users: Optional[list] = None,
        config: Optional[AgencyConfig] = None
    ):
        """
        Initialize Telegram channel.

        Args:
            bot_token: Telegram bot token
            queue: File queue instance
            allowed_users: List of allowed user IDs (if None, allow all)
            config: Agency configuration (for dynamic help generation)
        """
        self.bot_token = bot_token
        self.queue = queue
        self.allowed_users = set(allowed_users) if allowed_users else None
        self.config = config

        # Create Telegram application
        self.app = Application.builder().token(bot_token).build()

        # Add command handlers
        self.app.add_handler(CommandHandler("start", self._handle_start))
        self.app.add_handler(CommandHandler("help", self._handle_help))
        self.app.add_handler(CommandHandler("status", self._handle_status))
        self.app.add_handler(CommandHandler("agents", self._handle_agents))
        self.app.add_handler(CommandHandler("teams", self._handle_teams))
        self.app.add_handler(CommandHandler("briefing", self._handle_briefing))
        self.app.add_handler(CommandHandler("jobs", self._handle_jobs))
        self.app.add_handler(CommandHandler("research", self._handle_research))

        # Add message handler (non-commands)
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
            "**Quick Commands:**\n"
            "• `/briefing` - Daily briefing\n"
            "• `/jobs` - Job opportunities\n"
            "• `/research` - AI research\n"
            "• `/help` - Full command list\n\n"
            "**Talk to agents:**\n"
            "`@cc Good morning briefing`\n"
            "`@researcher What's new in AI?`\n\n"
            "Type /help to see all agents and teams."
        )

    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command - dynamically generated from agency config"""

        if self.config:
            # Generate dynamic help from actual config
            help_text = "🤖 **Agency - Your AI Assistant Team**\n\n"

            # Available Agents section
            if self.config.agents:
                help_text += "**Available Agents:**\n"
                for agent_id, agent in self.config.agents.items():
                    # Create a short description from the first line of personality
                    desc = agent.personality.split('.')[0] if agent.personality else agent.name
                    help_text += f"• `@{agent_id}` - {agent.name}\n"
                help_text += "\n"

            # Available Teams section
            if self.config.teams:
                help_text += "**Available Teams:**\n"
                for team_id, team in self.config.teams.items():
                    desc = team.description if team.description else team.name
                    help_text += f"• `@{team_id}` - {desc}\n"
                help_text += "\n"

            # Commands
            help_text += "**Quick Commands:**\n"
            help_text += "• `/briefing` - Daily briefing from CC\n"
            help_text += "• `/jobs` - Find job opportunities\n"
            help_text += "• `/research` - Latest AI research\n"
            help_text += "• `/agents` - List all agents\n"
            help_text += "• `/teams` - List all teams\n"
            help_text += "• `/status` - System status\n\n"

            # Usage examples
            help_text += "**Or talk directly:**\n"
            help_text += "`@cc Good morning briefing`\n"
            help_text += "`@job_hunter Find ML Engineer roles`\n"
            help_text += "`@researcher What's new in AI?`\n\n"
            help_text += "✅ Your agency is running!"
        else:
            # Fallback help if config not provided
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

Just message me naturally with an @mention!
"""

        await update.message.reply_text(help_text)

    async def _handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - show system status"""
        status_text = "📊 **Agency Status**\n\n"

        if self.config:
            status_text += f"✅ **Running**\n\n"
            status_text += f"**Agents:** {len(self.config.agents)}\n"
            status_text += f"**Teams:** {len(self.config.teams)}\n"
            status_text += f"**Queue:** {self.queue.queue_path}\n\n"
            status_text += "Use /agents or /teams to see details."
        else:
            status_text += "⚠️ Configuration not loaded\n"
            status_text += "Agency may be running with limited functionality."

        await update.message.reply_text(status_text)

    async def _handle_agents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /agents command - list all agents with details"""
        if not self.config or not self.config.agents:
            await update.message.reply_text("⚠️ No agents configured")
            return

        agents_text = "👥 **Available Agents**\n\n"

        for agent_id, agent in self.config.agents.items():
            agents_text += f"**@{agent_id}** - {agent.name}\n"
            agents_text += f"_{agent.provider} / {agent.model}_\n"

            # Add first sentence of personality as description
            if agent.personality:
                desc = agent.personality.split('.')[0] + '.'
                agents_text += f"{desc}\n"

            agents_text += "\n"

        agents_text += "💡 **Usage:** `@agent_id your message`"

        await update.message.reply_text(agents_text)

    async def _handle_teams(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /teams command - list all teams with details"""
        if not self.config or not self.config.teams:
            await update.message.reply_text("⚠️ No teams configured")
            return

        teams_text = "👨‍👩‍👧‍👦 **Available Teams**\n\n"

        for team_id, team in self.config.teams.items():
            teams_text += f"**@{team_id}** - {team.name}\n"
            teams_text += f"_Leader: {team.leader_agent}_\n"

            if team.description:
                teams_text += f"{team.description}\n"

            teams_text += f"**Members:** {', '.join(team.agents)}\n\n"

        teams_text += "💡 **Usage:** `@team_id your message`"

        await update.message.reply_text(teams_text)

    async def _handle_briefing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /briefing command - shortcut for @cc daily briefing"""
        user = update.effective_user

        # Check if cc agent exists
        if self.config and "cc" not in self.config.agents:
            await update.message.reply_text(
                "⚠️ CC agent not configured. Use /agents to see available agents."
            )
            return

        # Create message data for @cc briefing
        message_data = MessageData(
            channel="telegram",
            sender=user.username or user.first_name,
            sender_id=str(user.id),
            message="@cc Good morning! Please give me a daily briefing with my calendar, emails, and priorities.",
            timestamp=time.time(),
            message_id=str(update.message.message_id),
            metadata={
                "chat_id": update.effective_chat.id,
                "user_id": user.id,
            }
        )

        # Enqueue message
        self.queue.enqueue(message_data, "incoming")

        logger.info(f"Briefing requested by {user.username}")
        await update.message.reply_text("📋 Preparing your daily briefing...")

    async def _handle_jobs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /jobs command - shortcut for @job_hunter job search"""
        user = update.effective_user

        # Check if job_hunter agent exists
        if self.config and "job_hunter" not in self.config.agents:
            await update.message.reply_text(
                "⚠️ Job Hunter agent not configured. Use /agents to see available agents."
            )
            return

        # Create message data for @job_hunter
        message_data = MessageData(
            channel="telegram",
            sender=user.username or user.first_name,
            sender_id=str(user.id),
            message="@job_hunter Find new ML Engineer and AI Research job opportunities at top companies like Anthropic, OpenAI, Google DeepMind, and Meta.",
            timestamp=time.time(),
            message_id=str(update.message.message_id),
            metadata={
                "chat_id": update.effective_chat.id,
                "user_id": user.id,
            }
        )

        # Enqueue message
        self.queue.enqueue(message_data, "incoming")

        logger.info(f"Job search requested by {user.username}")
        await update.message.reply_text("💼 Searching for job opportunities...")

    async def _handle_research(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /research command - shortcut for @researcher daily research"""
        user = update.effective_user

        # Check if researcher agent exists
        if self.config and "researcher" not in self.config.agents:
            await update.message.reply_text(
                "⚠️ Researcher agent not configured. Use /agents to see available agents."
            )
            return

        # Create message data for @researcher
        message_data = MessageData(
            channel="telegram",
            sender=user.username or user.first_name,
            sender_id=str(user.id),
            message="@researcher What's new and interesting in AI today? Check ArXiv, Twitter, Hacker News, and major AI labs.",
            timestamp=time.time(),
            message_id=str(update.message.message_id),
            metadata={
                "chat_id": update.effective_chat.id,
                "user_id": user.id,
            }
        )

        # Enqueue message
        self.queue.enqueue(message_data, "incoming")

        logger.info(f"Research requested by {user.username}")
        await update.message.reply_text("🔬 Researching latest AI developments...")

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


def main():
    """Main entry point for running Telegram channel"""
    import sys
    from dotenv import load_dotenv
    from agency.config import load_config

    # Load environment variables
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get configuration from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment")
        sys.exit(1)

    allowed_users_str = os.getenv("TELEGRAM_ALLOWED_USERS", "")
    allowed_users = [u.strip() for u in allowed_users_str.split(",") if u.strip()]

    # Load agency config for dynamic help
    try:
        agency_config = load_config()
        logger.info(f"Loaded agency config: {len(agency_config.agents)} agents, {len(agency_config.teams)} teams")
    except Exception as e:
        logger.warning(f"Could not load agency config: {e}. Help will use fallback.")
        agency_config = None

    # Create queue (use default path)
    queue_path = Path.home() / ".agency" / "queue"
    queue = FileQueue(queue_path)

    # Create and start channel
    channel = TelegramChannel(
        bot_token=bot_token,
        queue=queue,
        allowed_users=allowed_users if allowed_users else None,
        config=agency_config
    )

    # Run
    asyncio.run(channel.start())


if __name__ == '__main__':
    main()
