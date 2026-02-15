"""Multi-agent orchestration for OpenClaw"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from openclaw.core.agent import Agent


logger = logging.getLogger(__name__)


class Orchestrator:
    """Coordinates multiple agents working together"""

    def __init__(self, agents: Optional[List[Agent]] = None):
        self.agents: Dict[str, Agent] = {}
        if agents:
            for agent in agents:
                self.register_agent(agent)

    def register_agent(self, agent: Agent):
        """Register an agent with the orchestrator"""
        self.agents[agent.config.name] = agent
        logger.info(f"Registered agent: {agent.config.name}")

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)

    async def run_sequential(
        self, workflow: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Run agents sequentially, passing output from one to the next.

        Args:
            workflow: List of workflow steps, each with 'agent' name and 'input' data

        Returns:
            List of results from each step
        """
        results = []
        current_input = None

        for step in workflow:
            agent_name = step.get("agent")
            agent = self.get_agent(agent_name)

            if not agent:
                logger.error(f"Agent not found: {agent_name}")
                results.append({"error": f"Agent {agent_name} not found"})
                continue

            # Use output from previous step if no explicit input
            input_data = step.get("input", current_input)

            logger.info(f"Running agent: {agent_name}")
            result = await agent.process(input_data)
            results.append(result)

            # Pass output to next step
            current_input = result

        return results

    async def run_parallel(
        self, tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Run multiple agents in parallel.

        Args:
            tasks: List of tasks, each with 'agent' name and 'input' data

        Returns:
            List of results from all tasks
        """
        async_tasks = []

        for task in tasks:
            agent_name = task.get("agent")
            agent = self.get_agent(agent_name)

            if not agent:
                logger.error(f"Agent not found: {agent_name}")
                continue

            input_data = task.get("input")
            async_tasks.append(agent.process(input_data))

        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        return results

    async def run_conditional(
        self, agent_name: str, input_data: Dict[str, Any], condition: callable
    ) -> Optional[Dict[str, Any]]:
        """
        Run an agent conditionally based on a condition function.

        Args:
            agent_name: Name of agent to run
            input_data: Input data for the agent
            condition: Function that returns True if agent should run

        Returns:
            Result from agent if condition is True, None otherwise
        """
        if not condition(input_data):
            logger.info(f"Condition not met for agent: {agent_name}")
            return None

        agent = self.get_agent(agent_name)
        if not agent:
            logger.error(f"Agent not found: {agent_name}")
            return None

        return await agent.process(input_data)

    async def broadcast(
        self, message: str, agent_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Broadcast a message to multiple agents.

        Args:
            message: Message to broadcast
            agent_names: List of agent names (all if None)

        Returns:
            Dictionary of agent names to responses
        """
        targets = agent_names or list(self.agents.keys())
        results = {}

        tasks = []
        for name in targets:
            agent = self.get_agent(name)
            if agent:
                tasks.append((name, agent.chat(message)))

        responses = await asyncio.gather(
            *[task for _, task in tasks], return_exceptions=True
        )

        for (name, _), response in zip(tasks, responses):
            results[name] = response

        return results

    async def coordinate(
        self,
        coordinator_name: str,
        worker_names: List[str],
        task_description: str,
    ) -> Dict[str, Any]:
        """
        Use one agent to coordinate work among other agents.

        Args:
            coordinator_name: Name of coordinating agent
            worker_names: Names of worker agents
            task_description: Description of the task

        Returns:
            Results from coordination
        """
        coordinator = self.get_agent(coordinator_name)
        if not coordinator:
            raise ValueError(f"Coordinator agent not found: {coordinator_name}")

        # Coordinator decides how to delegate
        plan_prompt = f"""You are coordinating the following workers: {', '.join(worker_names)}

Task: {task_description}

Create a plan for how to delegate this work. For each worker, specify:
1. What they should do
2. What input they need
3. The order of execution

Return your plan as a structured response."""

        plan = await coordinator.chat(plan_prompt)
        coordinator.set_context("current_plan", plan)

        logger.info(f"Coordination plan: {plan}")

        # For now, return the plan
        # In a more sophisticated implementation, we would parse the plan
        # and execute it using run_sequential or run_parallel
        return {"plan": plan, "coordinator": coordinator_name}

    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agents.keys())

    def get_agent_info(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get information about an agent"""
        agent = self.get_agent(agent_name)
        if not agent:
            return None

        return {
            "name": agent.config.name,
            "description": agent.config.description,
            "model": agent.config.model,
            "proactive": agent.config.proactive,
            "schedule": agent.config.schedule,
        }
