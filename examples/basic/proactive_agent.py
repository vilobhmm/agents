"""
Proactive Agent Example

This example shows how to create an agent that runs on a schedule.
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.scheduler import ProactiveScheduler


class DailyReportAgent(Agent):
    """Agent that sends daily reports"""

    async def process(self, input_data: dict) -> dict:
        print(f"\n[{datetime.now()}] Generating daily report...")

        prompt = "Generate a motivational quote for the day."
        quote = await self.chat(prompt)

        print(f"\nDaily Quote: {quote}\n")

        return {"status": "success", "quote": quote}


async def main():
    """Run proactive agent"""
    load_dotenv()

    # Create agent
    agent = DailyReportAgent(
        AgentConfig(
            name="Daily Reporter",
            description="Sends daily motivational quotes",
            proactive=True,
        ),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    # Create scheduler
    scheduler = ProactiveScheduler()

    # Schedule agent to run every minute (for demo purposes)
    # In production, use: "0 9 * * *" for 9 AM daily
    scheduler.schedule_agent(
        agent=agent, trigger="1m", trigger_type="interval", job_id="daily_report"
    )

    # Start scheduler
    scheduler.start()

    print("Proactive agent started!")
    print("Will run every minute. Press Ctrl+C to stop.")
    print("\nJobs scheduled:")
    for job in scheduler.list_jobs():
        print(f"  - {job['id']}: Next run at {job['next_run']}")

    try:
        # Keep running
        while True:
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        scheduler.stop()
        print("Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
