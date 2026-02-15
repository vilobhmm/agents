"""
Telegram Manager for Avengers System

Provides Telegram interface for interacting with Iron Man.
User sends messages → Iron Man responds → Iron Man coordinates other agents

This is the EASIEST way to control your AI team (easier than WhatsApp).
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .coordination import coordination_hub
from .iron_man import IronManAgent

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("avengers.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Global Iron Man instance
iron_man: IronManAgent = None


def initialize_iron_man():
    """Initialize Iron Man agent"""
    global iron_man

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env")

    iron_man = IronManAgent(api_key=api_key, coordination=coordination_hub)

    logger.info("🧠 Iron Man initialized and ready")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started Avengers system")

    welcome = f"""🛡⚡ *AVENGERS AI OPERATING SYSTEM*

Welcome {user.first_name}! I'm *Iron Man*, your Chief of Staff.

I coordinate your AI team of 6 specialized agents:

🛡 *Captain America* - Research & Intelligence
⚡ *Thor* - X/Twitter Content
🕷 *Black Widow* - LinkedIn Authority
🔨 *Hulk* - GitHub Prototypes
🎯 *Hawkeye* - Newsletter Curation

*How to work with me:*

📊 `/status` - Get all agent statuses
📝 `/assign <task>` - Assign a new task
📈 `/report <agent>` - Get detailed report
🎯 `/sprint` - View current sprint
❓ `/help` - Show all commands

*Or just talk to me naturally:*
• "What's the most important AI news today?"
• "Build a RAG demo"
• "What did the team accomplish this week?"

I understand context and delegate to the right agents automatically.

*Ready to build in public?*
Type `/status` to see your team."""

    await update.message.reply_text(welcome, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    await update.message.reply_text("📊 Getting status from all agents...")

    response = await iron_man.handle_user_message("status")

    await update.message.reply_text(response, parse_mode="Markdown")


async def assign_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /assign command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/assign <task description>`\n\n"
            "Example: `/assign Build a LoRA fine-tuning demo`",
            parse_mode="Markdown",
        )
        return

    task_description = " ".join(context.args)

    await update.message.reply_text(f"🧠 Analyzing task and assigning to right agent...")

    response = await iron_man.handle_user_message(f"assign {task_description}")

    await update.message.reply_text(response, parse_mode="Markdown")


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/report <agent_name>`\n\n"
            "*Available agents:*\n"
            "• captain_america\n"
            "• thor\n"
            "• black_widow\n"
            "• hulk\n"
            "• hawkeye",
            parse_mode="Markdown",
        )
        return

    agent_name = context.args[0].lower()

    await update.message.reply_text(f"📋 Getting report from {agent_name}...")

    response = await iron_man.handle_user_message(f"report {agent_name}")

    await update.message.reply_text(response, parse_mode="Markdown")


async def sprint_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sprint command"""
    await update.message.reply_text("🎯 Loading current sprint...")

    response = await iron_man.handle_user_message("sprint")

    await update.message.reply_text(response, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    response = await iron_man.get_help_text()

    await update.message.reply_text(response, parse_mode="Markdown")


async def morning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /morning command - get morning briefing"""
    await update.message.reply_text("☀️ Generating your morning briefing...")

    briefing = await iron_man.morning_briefing()

    await update.message.reply_text(briefing, parse_mode="Markdown")


async def evening_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /evening command - get evening summary"""
    await update.message.reply_text("🌙 Generating evening summary...")

    summary = await iron_man.evening_summary()

    await update.message.reply_text(summary, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages (natural conversation with Iron Man)"""
    message_text = update.message.text

    logger.info(f"User message: {message_text}")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    # Process with Iron Man
    response = await iron_man.handle_user_message(message_text)

    # Send response (split if too long)
    if len(response) > 4000:
        # Split into chunks
        chunks = [response[i : i + 4000] for i in range(0, len(response), 4000)]

        for chunk in chunks:
            await update.message.reply_text(chunk, parse_mode="Markdown")
    else:
        await update.message.reply_text(response, parse_mode="Markdown")


async def send_scheduled_briefing(application: Application):
    """Send morning briefing to user (called by scheduler)"""
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID not set, cannot send briefing")
        return

    briefing = await iron_man.morning_briefing()

    await application.bot.send_message(
        chat_id=int(chat_id), text=briefing, parse_mode="Markdown"
    )

    logger.info("📤 Morning briefing sent to Telegram")


async def send_scheduled_summary(application: Application):
    """Send evening summary to user (called by scheduler)"""
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID not set, cannot send summary")
        return

    summary = await iron_man.evening_summary()

    await application.bot.send_message(
        chat_id=int(chat_id), text=summary, parse_mode="Markdown"
    )

    logger.info("📤 Evening summary sent to Telegram")


def main():
    """Main entry point"""
    load_dotenv()

    # Get bot token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("\n❌ Error: TELEGRAM_BOT_TOKEN not found!")
        print("Please add your bot token to .env file")
        print("\nTo create a bot:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot and follow instructions")
        print("3. Copy the token and add to .env\n")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🛡⚡ AVENGERS AI OPERATING SYSTEM - TELEGRAM INTERFACE")
    print("=" * 60)
    print("\n*Multi-agent Agentic - Personal. Proactive. Powerful.*\n")
    print("Initializing agents...")

    # Initialize Iron Man
    initialize_iron_man()

    print("\n✅ Iron Man ready")
    print("✅ All agents coordinated")
    print("\n" + "=" * 60)
    print("🚀 SYSTEM READY")
    print("=" * 60)
    print("\nInteract with Iron Man via Telegram!")
    print("\nCommands:")
    print("  /start - Get started")
    print("  /status - Agent statuses")
    print("  /assign <task> - Assign task")
    print("  /report <agent> - Agent report")
    print("  /sprint - Current sprint")
    print("  /morning - Morning briefing")
    print("  /evening - Evening summary")
    print("  /help - All commands")
    print("\nOr just chat naturally with Iron Man!")
    print("=" * 60 + "\n")

    # Create application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("assign", assign_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CommandHandler("sprint", sprint_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("morning", morning_command))
    application.add_handler(CommandHandler("evening", evening_command))

    # Add message handler for natural conversation
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Run bot
    logger.info("🤖 Telegram bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
