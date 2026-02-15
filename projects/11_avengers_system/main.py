"""
Avengers System - Main Runner

Orchestrates all agents with scheduled tasks.
Runs background loops for each agent while WhatsApp manager handles user interaction.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from .black_widow import BlackWidowAgent
from .captain_america import CaptainAmericaAgent
from .coordination import coordination_hub
from .hawkeye import HawkeyeAgent
from .hulk import HulkAgent
from .iron_man import IronManAgent
from .thor import ThorAgent

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


class AvengersSystem:
    """
    Main orchestration system for all Avengers agents

    Manages:
    - Agent initialization
    - Scheduled tasks
    - Status monitoring
    - Coordination
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        # Initialize all agents
        logger.info("Initializing Avengers team...")

        self.iron_man = IronManAgent(api_key, coordination_hub)
        self.captain_america = CaptainAmericaAgent(api_key, coordination_hub)
        self.thor = ThorAgent(api_key, coordination_hub)
        self.black_widow = BlackWidowAgent(api_key, coordination_hub)
        self.hulk = HulkAgent(api_key, coordination_hub)
        self.hawkeye = HawkeyeAgent(api_key, coordination_hub)

        # Scheduler
        self.scheduler = AsyncIOScheduler()

        logger.info("✅ All agents initialized")

    def schedule_agent_tasks(self):
        """Schedule recurring tasks for all agents"""

        # Captain America - Research sweeps (3x daily)
        self.scheduler.add_job(
            self.captain_america.run_research_sweep,
            "cron",
            hour="7,13,19",  # 7 AM, 1 PM, 7 PM
            id="captain_research",
        )

        self.scheduler.add_job(
            self.captain_america.submit_status_report,
            "cron",
            hour="*/4",  # Every 4 hours
            id="captain_status",
        )

        # Thor - Process research and tweet (every 30 min)
        self.scheduler.add_job(
            self.thor.process_research_updates,
            "cron",
            minute="*/30",
            id="thor_tweets",
        )

        self.scheduler.add_job(
            self.thor.submit_status_report,
            "cron",
            hour="*/4",
            id="thor_status",
        )

        # Black Widow - Weekly posts (Monday & Thursday 9 AM)
        self.scheduler.add_job(
            self.black_widow.weekly_post_generation,
            "cron",
            day_of_week="mon,thu",
            hour=9,
            id="black_widow_posts",
        )

        self.scheduler.add_job(
            self.black_widow.submit_status_report,
            "cron",
            hour="*/4",
            id="black_widow_status",
        )

        # Hulk - Process build requests (every 2 hours)
        self.scheduler.add_job(
            self.hulk.process_build_requests,
            "cron",
            hour="*/2",
            id="hulk_builds",
        )

        self.scheduler.add_job(
            self.hulk.submit_status_report,
            "cron",
            hour="*/4",
            id="hulk_status",
        )

        # Hawkeye - Weekly newsletter (Friday 8 AM)
        self.scheduler.add_job(
            self.hawkeye.weekly_generation_task,
            "cron",
            day_of_week="fri",
            hour=8,
            id="hawkeye_newsletter",
        )

        self.scheduler.add_job(
            self.hawkeye.submit_status_report,
            "cron",
            hour="*/4",
            id="hawkeye_status",
        )

        # Iron Man - Send briefings
        # Morning briefing (6 AM)
        self.scheduler.add_job(
            self._send_morning_briefing,
            "cron",
            hour=6,
            id="iron_man_morning",
        )

        # Evening summary (8 PM)
        self.scheduler.add_job(
            self._send_evening_summary,
            "cron",
            hour=20,
            id="iron_man_evening",
        )

        logger.info("📅 All agent tasks scheduled")

    async def _send_morning_briefing(self):
        """Send morning briefing"""
        # This would integrate with WhatsApp
        briefing = await self.iron_man.morning_briefing()
        logger.info(f"☀️ Morning briefing ready:\n{briefing}")

        # Send via WhatsApp (handled by whatsapp_manager)

    async def _send_evening_summary(self):
        """Send evening summary"""
        summary = await self.iron_man.evening_summary()
        logger.info(f"🌙 Evening summary ready:\n{summary}")

        # Send via WhatsApp (handled by whatsapp_manager)

    def start(self):
        """Start the system"""
        logger.info("🚀 Starting Avengers System...")

        # Schedule tasks
        self.schedule_agent_tasks()

        # Start scheduler
        self.scheduler.start()

        logger.info("✅ System running")
        logger.info("🛡⚡ Avengers team operational")

        # Print schedule
        logger.info("\n📅 Scheduled Jobs:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  • {job.id}: {job.next_run_time}")

    async def run_forever(self):
        """Keep system running"""
        try:
            while True:
                await asyncio.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.scheduler.shutdown()


def main():
    """Main entry point"""
    load_dotenv()

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("Please set it in .env file")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🛡⚡ AVENGERS AI OPERATING SYSTEM")
    print("=" * 60)
    print("\nSix agents. Clear ownership. No overlap.")
    print("Continuous output.\n")
    print("=" * 60 + "\n")

    # Create and start system
    system = AvengersSystem(api_key)
    system.start()

    print("\n" + "=" * 60)
    print("✅ SYSTEM OPERATIONAL")
    print("=" * 60)
    print("\nAgents active:")
    print("  🧠 Iron Man - Chief of Staff")
    print("  🛡 Captain America - Research")
    print("  ⚡ Thor - Twitter")
    print("  🕷 Black Widow - LinkedIn")
    print("  🔨 Hulk - GitHub")
    print("  🎯 Hawkeye - Newsletter")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")

    # Run forever
    asyncio.run(system.run_forever())


if __name__ == "__main__":
    main()
