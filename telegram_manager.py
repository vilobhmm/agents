"""
OpenClaw Telegram Manager

Control and manage all your AI agents via Telegram like virtual employees.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from openclaw.core.scheduler import ProactiveScheduler

# Import all agents
from projects.01_research_assistant.agent import ResearchAssistantAgent
from projects.02_meeting_prep.agent import MeetingPrepAgent
from projects.03_code_review.agent import CodeReviewAgent
from projects.04_expense_tracker.agent import ExpenseTrackerAgent
from projects.09_email_triage.agent import EmailTriageAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("openclaw.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class AgentManager:
    """Manages all AI agents via Telegram"""

    def __init__(self):
        self.scheduler = ProactiveScheduler()
        self.agents: Dict[str, any] = {}
        self.agent_status: Dict[str, dict] = {}
        self.conversation_mode: Dict[int, str] = {}  # user_id -> agent_name

        # Initialize agents (not activated yet)
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all available agents"""
        api_key = os.getenv("ANTHROPIC_API_KEY")

        self.agents = {
            "research": {
                "name": "Research Assistant",
                "emoji": "📚",
                "description": "Monitors reading lists, summarizes articles, sends briefings",
                "instance": None,
                "schedule": "0 2 * * *",  # 2 AM daily
                "active": False,
            },
            "meeting": {
                "name": "Meeting Prep",
                "emoji": "📅",
                "description": "Scans calendar, generates briefings, suggests agenda",
                "instance": None,
                "schedule": "0 7 * * *",  # 7 AM daily
                "active": False,
            },
            "code": {
                "name": "Code Review",
                "emoji": "💻",
                "description": "Monitors PRs, analyzes code, drafts review comments",
                "instance": None,
                "schedule": "0 9 * * *",  # 9 AM daily
                "active": False,
            },
            "expense": {
                "name": "Expense Tracker",
                "emoji": "💰",
                "description": "Processes receipts, categorizes spending, sends reports",
                "instance": None,
                "schedule": "0 20 * * *",  # 8 PM daily
                "active": False,
            },
            "email": {
                "name": "Email Triage",
                "emoji": "📧",
                "description": "Categorizes emails, drafts responses, manages follow-ups",
                "instance": None,
                "schedule": "*/30 * * * *",  # Every 30 minutes
                "active": False,
            },
        }

        logger.info(f"Initialized {len(self.agents)} agents")

    async def activate_agent(self, agent_key: str) -> tuple[bool, str]:
        """Activate an agent"""
        if agent_key not in self.agents:
            return False, f"Unknown agent: {agent_key}"

        agent_info = self.agents[agent_key]

        if agent_info["active"]:
            return False, f"{agent_info['name']} is already active"

        try:
            # Create agent instance
            api_key = os.getenv("ANTHROPIC_API_KEY")

            if agent_key == "research":
                instance = ResearchAssistantAgent(api_key)
            elif agent_key == "meeting":
                instance = MeetingPrepAgent(api_key)
            elif agent_key == "code":
                repos = os.getenv("GITHUB_REPOS", "").split(",")
                instance = CodeReviewAgent(api_key, repos=repos)
            elif agent_key == "expense":
                instance = ExpenseTrackerAgent(api_key)
            elif agent_key == "email":
                instance = EmailTriageAgent(api_key)
            else:
                return False, "Agent not implemented yet"

            # Schedule agent
            self.scheduler.schedule_agent(
                agent=instance,
                trigger=agent_info["schedule"],
                trigger_type="cron",
                job_id=agent_key,
            )

            agent_info["instance"] = instance
            agent_info["active"] = True
            agent_info["activated_at"] = datetime.now()

            # Start scheduler if not running
            if not self.scheduler.running:
                self.scheduler.start()

            logger.info(f"Activated agent: {agent_key}")

            return True, f"✅ {agent_info['name']} activated!\n\nSchedule: {agent_info['schedule']}\nStatus: Running"

        except Exception as e:
            logger.error(f"Error activating {agent_key}: {e}")
            return False, f"Error activating agent: {str(e)}"

    async def deactivate_agent(self, agent_key: str) -> tuple[bool, str]:
        """Deactivate an agent"""
        if agent_key not in self.agents:
            return False, f"Unknown agent: {agent_key}"

        agent_info = self.agents[agent_key]

        if not agent_info["active"]:
            return False, f"{agent_info['name']} is not active"

        try:
            # Unschedule agent
            self.scheduler.unschedule_agent(agent_key)

            agent_info["instance"] = None
            agent_info["active"] = False
            agent_info["deactivated_at"] = datetime.now()

            logger.info(f"Deactivated agent: {agent_key}")

            return True, f"✅ {agent_info['name']} deactivated"

        except Exception as e:
            logger.error(f"Error deactivating {agent_key}: {e}")
            return False, f"Error deactivating agent: {str(e)}"

    async def get_status(self) -> str:
        """Get status of all agents"""
        active = []
        inactive = []

        for key, info in self.agents.items():
            if info["active"]:
                active.append(f"{info['emoji']} {info['name']}")
            else:
                inactive.append(f"{info['emoji']} {info['name']}")

        status = "📊 *Agent Status*\n\n"

        if active:
            status += f"✅ *Active ({len(active)}):*\n"
            status += "\n".join(f"  • {a}" for a in active)
            status += "\n\n"

        if inactive:
            status += f"💤 *Inactive ({len(inactive)}):*\n"
            status += "\n".join(f"  • {i}" for i in inactive)

        return status

    async def ask_agent(self, agent_key: str, question: str) -> tuple[bool, str]:
        """Ask an agent a question"""
        if agent_key not in self.agents:
            return False, f"Unknown agent: {agent_key}"

        agent_info = self.agents[agent_key]
        instance = agent_info["instance"]

        if not instance:
            return False, f"{agent_info['name']} is not active. Use /activate {agent_key} first."

        try:
            response = await instance.chat(question)
            return True, response
        except Exception as e:
            logger.error(f"Error asking {agent_key}: {e}")
            return False, f"Error: {str(e)}"


# Global manager instance
manager = AgentManager()


# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")

    welcome_message = f"""👋 *Welcome to OpenClaw Agent Manager!*

I manage your personal AI workforce. Your agents are standing by and ready to assist.

*Available Agents:*
"""

    for key, info in manager.agents.items():
        status_icon = "✅" if info["active"] else "💤"
        welcome_message += f"\n{status_icon} {info['emoji']} *{info['name']}*"
        welcome_message += f"\n   {info['description']}"

    welcome_message += "\n\n*Quick Start:*"
    welcome_message += "\n  • `/status` - View agent statuses"
    welcome_message += "\n  • `/activate <agent>` - Start an agent"
    welcome_message += "\n  • `/ask <agent> <question>` - Ask a question"
    welcome_message += "\n  • `/help` - See all commands"

    welcome_message += "\n\n*Example:*"
    welcome_message += "\n`/activate research`"
    welcome_message += "\n`/ask research What should I read today?`"

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """📖 *OpenClaw Commands*

*Agent Management:*
  `/status` - View all agent statuses
  `/agents` - List all available agents
  `/activate <agent>` - Activate an agent
  `/deactivate <agent>` - Deactivate an agent
  `/schedule` - View agent schedules

*Interaction:*
  `/ask <agent> <question>` - Ask an agent
  `/chat <agent>` - Start conversation
  `/report <agent>` - Get activity report

*Quick Actions:*
  `/morning` - Morning briefing
  `/today` - Today's overview
  `/urgent` - Check urgent items

*Agent Names:*
  • `research` - Research Assistant
  • `meeting` - Meeting Prep
  • `code` - Code Review
  • `expense` - Expense Tracker
  • `email` - Email Triage

*Examples:*
  `/activate research`
  `/ask email Do I have urgent emails?`
  `/deactivate code`

For detailed guide, see TELEGRAM_GUIDE.md
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    status = await manager.get_status()
    await update.message.reply_text(status, parse_mode="Markdown")


async def agents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /agents command"""
    message = "🤖 *Available Agents*\n\n"

    for key, info in manager.agents.items():
        status = "✅ Active" if info["active"] else "💤 Inactive"
        message += f"{info['emoji']} *{info['name']}*\n"
        message += f"Status: {status}\n"
        message += f"ID: `{key}`\n"
        message += f"Schedule: `{info['schedule']}`\n"
        message += f"Description: {info['description']}\n\n"

    message += "\nUse `/activate <agent_id>` to activate an agent"

    await update.message.reply_text(message, parse_mode="Markdown")


async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /activate command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/activate <agent>`\nExample: `/activate research`",
            parse_mode="Markdown",
        )
        return

    agent_key = context.args[0].lower()
    success, message = await manager.activate_agent(agent_key)

    await update.message.reply_text(message, parse_mode="Markdown")


async def deactivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deactivate command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/deactivate <agent>`\nExample: `/deactivate research`",
            parse_mode="Markdown",
        )
        return

    agent_key = context.args[0].lower()
    success, message = await manager.deactivate_agent(agent_key)

    await update.message.reply_text(message, parse_mode="Markdown")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ask command"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/ask <agent> <question>`\n"
            "Example: `/ask research What should I read today?`",
            parse_mode="Markdown",
        )
        return

    agent_key = context.args[0].lower()
    question = " ".join(context.args[1:])

    # Show typing indicator
    await update.message.chat.send_action("typing")

    # Get agent info for display
    agent_info = manager.agents.get(agent_key)
    if agent_info:
        await update.message.reply_text(
            f"🤔 Asking {agent_info['emoji']} {agent_info['name']}..."
        )

    success, response = await manager.ask_agent(agent_key, question)

    if success:
        # Split long responses
        max_length = 4000
        if len(response) > max_length:
            parts = [
                response[i : i + max_length]
                for i in range(0, len(response), max_length)
            ]
            for i, part in enumerate(parts):
                if i == 0:
                    await update.message.reply_text(
                        f"*{agent_info['name']}:*\n\n{part}", parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text(part)
        else:
            await update.message.reply_text(
                f"*{agent_info['name']}:*\n\n{response}", parse_mode="Markdown"
            )
    else:
        await update.message.reply_text(f"❌ {response}")


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /schedule command"""
    message = "📅 *Agent Schedules*\n\n"

    active_agents = {k: v for k, v in manager.agents.items() if v["active"]}

    if not active_agents:
        message += "No agents are currently active.\n\n"
        message += "Use `/activate <agent>` to activate an agent."
    else:
        for key, info in active_agents.items():
            message += f"{info['emoji']} *{info['name']}*\n"
            message += f"Schedule: `{info['schedule']}`\n"

            # Get next run time from scheduler
            job_info = manager.scheduler.get_job_info(key)
            if job_info:
                next_run = job_info.get("next_run")
                if next_run:
                    message += f"Next run: {next_run.strftime('%Y-%m-%d %H:%M')}\n"

            message += "\n"

    await update.message.reply_text(message, parse_mode="Markdown")


async def morning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /morning command - morning briefing"""
    await update.message.reply_text("☀️ Generating your morning briefing...")
    await update.message.chat.send_action("typing")

    briefing = "☀️ *Good Morning!* Here's your briefing:\n\n"

    # Check each active agent
    active_count = 0
    for key, info in manager.agents.items():
        if info["active"]:
            active_count += 1

    if active_count == 0:
        briefing += "No agents are currently active.\n\n"
        briefing += "💡 *Tip:* Activate agents with `/activate <agent>`\n"
        briefing += "Try: `/activate meeting` and `/activate email`"
    else:
        briefing += f"📊 *{active_count} agents* working for you\n\n"

        # Get updates from active agents (simplified)
        if "meeting" in manager.agents and manager.agents["meeting"]["active"]:
            briefing += "📅 *Meetings:* Check `/ask meeting What's on my calendar?`\n\n"

        if "email" in manager.agents and manager.agents["email"]["active"]:
            briefing += "📧 *Emails:* Check `/ask email Any urgent emails?`\n\n"

        if "research" in manager.agents and manager.agents["research"]["active"]:
            briefing += (
                "📚 *Reading:* Check `/ask research What should I read today?`\n\n"
            )

        briefing += "💡 Use `/today` for a full overview"

    await update.message.reply_text(briefing, parse_mode="Markdown")


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /today command - today's overview"""
    await update.message.reply_text("📊 Gathering today's overview...")
    await update.message.chat.send_action("typing")

    overview = f"📊 *Today's Overview* - {datetime.now().strftime('%B %d, %Y')}\n\n"

    active_agents = {k: v for k, v in manager.agents.items() if v["active"]}

    if not active_agents:
        overview += "No active agents.\n\n"
        overview += "💡 Activate agents to get personalized insights!"
    else:
        overview += f"✅ *{len(active_agents)} Active Agents*\n\n"

        for key, info in active_agents.items():
            overview += f"{info['emoji']} {info['name']}: Ready\n"

        overview += "\n*Quick Actions:*\n"
        overview += "• `/ask email Check urgent emails`\n"
        overview += "• `/ask meeting Show today's calendar`\n"
        overview += "• `/ask research Recommend an article`\n"

    await update.message.reply_text(overview, parse_mode="Markdown")


async def urgent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /urgent command - check urgent items"""
    await update.message.reply_text("⚡ Checking for urgent items...")
    await update.message.chat.send_action("typing")

    urgent = "⚡ *Urgent Items*\n\n"

    # Check email agent if active
    if "email" in manager.agents and manager.agents["email"]["active"]:
        success, response = await manager.ask_agent(
            "email", "Do I have any urgent emails?"
        )
        if success:
            urgent += f"📧 *Emails:*\n{response}\n\n"

    # Add more urgent checks here

    if urgent == "⚡ *Urgent Items*\n\n":
        urgent += "✅ No urgent items at the moment!\n\n"
        urgent += "You're all caught up 🎉"

    await update.message.reply_text(urgent, parse_mode="Markdown")


def main():
    """Start the Telegram bot"""
    load_dotenv()

    # Get bot token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        print("\n❌ Error: TELEGRAM_BOT_TOKEN not found!")
        print("Please add your bot token to .env file")
        print("See TELEGRAM_GUIDE.md for setup instructions\n")
        sys.exit(1)

    # Create application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("agents", agents_command))
    application.add_handler(CommandHandler("activate", activate_command))
    application.add_handler(CommandHandler("deactivate", deactivate_command))
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("morning", morning_command))
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(CommandHandler("urgent", urgent_command))

    # Start bot
    logger.info("Starting OpenClaw Telegram Manager...")
    print("\n" + "=" * 60)
    print("🚀 OpenClaw Telegram Manager Started!")
    print("=" * 60)
    print(f"\nBot is running and ready to receive commands")
    print(f"\nSend /start to your bot to begin")
    print(f"\nPress Ctrl+C to stop\n")

    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
