"""
Simple Agent Example

This example shows how to create a basic OpenClaw agent.
"""

import asyncio
import os
from dotenv import load_dotenv

from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.chat import ConsoleChat


class SimpleAgent(Agent):
    """A simple example agent"""

    async def process(self, input_data: dict) -> dict:
        """Process some input"""
        message = input_data.get("message", "Hello!")

        # Use Claude to respond
        response = await self.chat(message)

        return {"response": response}


async def main():
    """Run the simple agent"""
    load_dotenv()

    # Create agent config
    config = AgentConfig(
        name="Simple Agent",
        description="A simple example agent that responds to messages.",
    )

    # Create agent
    agent = SimpleAgent(config, api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Create console chat interface
    console = ConsoleChat(agent)

    # Run interactive chat
    await console.run()


if __name__ == "__main__":
    asyncio.run(main())
