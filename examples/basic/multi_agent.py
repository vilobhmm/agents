"""
Multi-Agent Example

This example shows how to use the Orchestrator to coordinate multiple agents.
"""

import asyncio
import os
from dotenv import load_dotenv

from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.orchestrator import Orchestrator


class ResearchAgent(Agent):
    """Agent that researches topics"""

    async def process(self, input_data: dict) -> dict:
        topic = input_data.get("topic", "AI")

        prompt = f"Provide 3 key facts about {topic}. Be concise."
        facts = await self.chat(prompt)

        return {"topic": topic, "facts": facts}


class SummaryAgent(Agent):
    """Agent that summarizes information"""

    async def process(self, input_data: dict) -> dict:
        facts = input_data.get("facts", "")

        prompt = f"Summarize these facts in one sentence:\n{facts}"
        summary = await self.chat(prompt)

        return {"summary": summary}


async def main():
    """Run multi-agent workflow"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Create agents
    researcher = ResearchAgent(
        AgentConfig(name="Researcher", description="Researches topics"),
        api_key=api_key,
    )

    summarizer = SummaryAgent(
        AgentConfig(name="Summarizer", description="Summarizes information"),
        api_key=api_key,
    )

    # Create orchestrator
    orchestrator = Orchestrator([researcher, summarizer])

    # Define workflow
    workflow = [
        {"agent": "Researcher", "input": {"topic": "Quantum Computing"}},
        {"agent": "Summarizer", "input": {}},  # Will receive previous output
    ]

    # Run workflow
    print("Running multi-agent workflow...")
    results = await orchestrator.run_sequential(workflow)

    print("\n=== Results ===")
    for i, result in enumerate(results, 1):
        print(f"\nStep {i}:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
