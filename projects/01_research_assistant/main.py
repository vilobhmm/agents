"""Main entry point for Research Assistant"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from openclaw.core.scheduler import ProactiveScheduler
from projects.01_research_assistant.agent import ResearchAssistantAgent
from projects.01_research_assistant.config import ResearchAssistantConfig


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Main function"""
    load_dotenv()

    logger.info("Starting Research Assistant")

    # Initialize agent
    agent = ResearchAssistantAgent()
    config = ResearchAssistantConfig()

    # Initialize scheduler
    scheduler = ProactiveScheduler()

    # Schedule fetch and process job
    scheduler.schedule_agent(
        agent=agent,
        trigger=config.fetch_schedule,
        trigger_type="cron",
        job_id="fetch_articles",
    )

    # Schedule briefing job
    async def send_briefing():
        await agent.send_morning_briefing()

    scheduler.schedule_function(
        func=send_briefing,
        trigger=config.briefing_schedule,
        trigger_type="cron",
        job_id="send_briefing",
    )

    # Start scheduler
    scheduler.start()

    logger.info("Research Assistant is running")
    logger.info(f"Fetch schedule: {config.fetch_schedule}")
    logger.info(f"Briefing schedule: {config.briefing_schedule}")

    try:
        # Keep running
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down Research Assistant")
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
