"""Main entry point for Meeting Prep Agent"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from openclaw.core.scheduler import ProactiveScheduler
from projects.02_meeting_prep.agent import MeetingPrepAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Main function"""
    load_dotenv()

    logger.info("Starting Meeting Prep Agent")

    agent = MeetingPrepAgent()
    scheduler = ProactiveScheduler()

    # Run at 7 AM daily
    scheduler.schedule_agent(
        agent=agent,
        trigger="0 7 * * *",
        trigger_type="cron",
        job_id="meeting_prep",
    )

    scheduler.start()

    logger.info("Meeting Prep Agent is running (7 AM daily)")

    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down")
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
