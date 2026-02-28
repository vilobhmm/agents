"""
ADK (Agent Development Kit) Integration Framework

Core framework for integrating with Google's ADK ecosystem and third-party tools.
Following Google's ADK patterns for observability, integrations, and multi-agent systems.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime
from abc import ABC, abstractmethod
import json

logger = logging.getLogger(__name__)


class ADKIntegration(ABC):
    """Base class for all ADK integrations."""

    def __init__(self, name: str, config: Optional[Dict] = None):
        """Initialize integration."""
        self.name = name
        self.config = config or {}
        self.enabled = True
        self.metrics = {
            "calls": 0,
            "errors": 0,
            "last_call": None
        }

    @abstractmethod
    async def initialize(self):
        """Initialize the integration."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Dict:
        """Execute integration functionality."""
        pass

    async def health_check(self) -> Dict:
        """Check integration health."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "healthy": True,
            "metrics": self.metrics
        }

    def _record_call(self):
        """Record a call to this integration."""
        self.metrics["calls"] += 1
        self.metrics["last_call"] = datetime.now().isoformat()

    def _record_error(self):
        """Record an error."""
        self.metrics["errors"] += 1


class McpToolset:
    """
    Model Context Protocol (MCP) Toolset.

    Allows agents to use tools and integrations through a unified interface.
    """

    def __init__(self):
        """Initialize MCP toolset."""
        self.tools = {}
        self.integrations = {}
        logger.info("MCP Toolset initialized")

    def register_tool(
        self,
        name: str,
        func: Callable,
        description: str,
        parameters: Dict
    ):
        """
        Register a tool in the MCP toolset.

        Args:
            name: Tool name
            func: Function to execute
            description: Tool description
            parameters: Parameter schema
        """
        self.tools[name] = {
            "function": func,
            "description": description,
            "parameters": parameters,
            "calls": 0
        }
        logger.info(f"Registered tool: {name}")

    def register_integration(self, integration: ADKIntegration):
        """Register an ADK integration."""
        self.integrations[integration.name] = integration
        logger.info(f"Registered integration: {integration.name}")

    async def call_tool(self, name: str, **kwargs) -> Dict:
        """
        Call a registered tool.

        Args:
            name: Tool name
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        if name not in self.tools:
            return {"error": f"Tool '{name}' not found"}

        tool = self.tools[name]
        tool["calls"] += 1

        try:
            result = await tool["function"](**kwargs)
            return {
                "tool": name,
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Tool '{name}' error: {e}")
            return {
                "tool": name,
                "error": str(e),
                "success": False
            }

    async def call_integration(self, name: str, **kwargs) -> Dict:
        """Call a registered integration."""
        if name not in self.integrations:
            return {"error": f"Integration '{name}' not found"}

        integration = self.integrations[name]

        try:
            result = await integration.execute(**kwargs)
            return {
                "integration": name,
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Integration '{name}' error: {e}")
            return {
                "integration": name,
                "error": str(e),
                "success": False
            }

    def list_tools(self) -> List[Dict]:
        """List all registered tools."""
        return [
            {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"],
                "calls": tool["calls"]
            }
            for name, tool in self.tools.items()
        ]

    def list_integrations(self) -> List[str]:
        """List all registered integrations."""
        return list(self.integrations.keys())


class ADKAgent:
    """
    ADK-compatible agent with built-in integrations support.

    Follows Google ADK patterns for multi-agent systems.
    """

    def __init__(
        self,
        name: str,
        role: str,
        model: str = "claude-sonnet-4-5-20250929"
    ):
        """Initialize ADK agent."""
        self.name = name
        self.role = role
        self.model = model
        self.mcp = McpToolset()
        self.conversation_history = []
        self.metrics = {
            "tasks_completed": 0,
            "tools_used": 0,
            "integrations_used": 0
        }

        # Initialize Claude
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
        else:
            self.claude = None
            logger.warning(f"Agent {name}: Claude API not configured")

        logger.info(f"ADK Agent '{name}' initialized with role: {role}")

    def add_integration(self, integration: ADKIntegration):
        """Add an integration to this agent."""
        self.mcp.register_integration(integration)
        logger.info(f"Agent '{self.name}' added integration: {integration.name}")

    def add_tool(
        self,
        name: str,
        func: Callable,
        description: str,
        parameters: Dict
    ):
        """Add a tool to this agent."""
        self.mcp.register_tool(name, func, description, parameters)
        logger.info(f"Agent '{self.name}' added tool: {name}")

    async def execute_task(
        self,
        task: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Execute a task using available tools and integrations.

        Args:
            task: Task description
            context: Additional context

        Returns:
            Task result
        """
        logger.info(f"Agent '{self.name}' executing task: {task}")

        # Build system prompt with available tools
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.mcp.list_tools()
        ])

        integrations_description = "\n".join([
            f"- {integration}"
            for integration in self.mcp.list_integrations()
        ])

        system_prompt = f"""You are {self.name}, an AI agent with the role: {self.role}.

You have access to these tools:
{tools_description}

You have access to these integrations:
{integrations_description}

Execute tasks using available tools and integrations when needed.
Respond with your reasoning and actions."""

        # Execute task using Claude
        if self.claude:
            try:
                response = self.claude.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": task}
                    ]
                )

                result = response.content[0].text
                self.conversation_history.append({
                    "task": task,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

                self.metrics["tasks_completed"] += 1

                return {
                    "agent": self.name,
                    "task": task,
                    "result": result,
                    "success": True
                }

            except Exception as e:
                logger.error(f"Agent '{self.name}' task failed: {e}")
                return {
                    "agent": self.name,
                    "task": task,
                    "error": str(e),
                    "success": False
                }
        else:
            return {
                "agent": self.name,
                "error": "Claude API not configured",
                "success": False
            }

    async def call_tool(self, tool_name: str, **kwargs) -> Dict:
        """Call a tool."""
        self.metrics["tools_used"] += 1
        return await self.mcp.call_tool(tool_name, **kwargs)

    async def call_integration(self, integration_name: str, **kwargs) -> Dict:
        """Call an integration."""
        self.metrics["integrations_used"] += 1
        return await self.mcp.call_integration(integration_name, **kwargs)

    def get_metrics(self) -> Dict:
        """Get agent metrics."""
        return {
            "agent": self.name,
            "role": self.role,
            "metrics": self.metrics,
            "tools": len(self.mcp.tools),
            "integrations": len(self.mcp.integrations)
        }


class MultiAgentOrchestrator:
    """
    Multi-agent orchestrator following ADK patterns.

    Coordinates multiple agents working together.
    """

    def __init__(self):
        """Initialize orchestrator."""
        self.agents = {}
        self.workflows = {}
        logger.info("Multi-Agent Orchestrator initialized")

    def register_agent(self, agent: ADKAgent):
        """Register an agent."""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def register_workflow(
        self,
        name: str,
        steps: List[Dict]
    ):
        """
        Register a multi-agent workflow.

        Args:
            name: Workflow name
            steps: List of steps [{"agent": "name", "task": "description"}]
        """
        self.workflows[name] = steps
        logger.info(f"Registered workflow: {name}")

    async def execute_workflow(
        self,
        workflow_name: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Execute a multi-agent workflow.

        Args:
            workflow_name: Name of workflow to execute
            context: Shared context

        Returns:
            Workflow results
        """
        if workflow_name not in self.workflows:
            return {"error": f"Workflow '{workflow_name}' not found"}

        workflow = self.workflows[workflow_name]
        results = []

        logger.info(f"Executing workflow: {workflow_name}")

        for step in workflow:
            agent_name = step["agent"]
            task = step["task"]

            if agent_name not in self.agents:
                results.append({
                    "step": step,
                    "error": f"Agent '{agent_name}' not found"
                })
                continue

            agent = self.agents[agent_name]
            result = await agent.execute_task(task, context)
            results.append({
                "step": step,
                "result": result
            })

            # Update context with result
            if context is not None:
                context[f"{agent_name}_result"] = result

        return {
            "workflow": workflow_name,
            "steps": len(results),
            "results": results,
            "success": True
        }

    async def parallel_execution(
        self,
        tasks: List[Dict]
    ) -> List[Dict]:
        """
        Execute multiple tasks in parallel across agents.

        Args:
            tasks: [{"agent": "name", "task": "description"}]

        Returns:
            List of results
        """
        logger.info(f"Executing {len(tasks)} tasks in parallel")

        async def execute_task(task_spec):
            agent_name = task_spec["agent"]
            task = task_spec["task"]

            if agent_name not in self.agents:
                return {"error": f"Agent '{agent_name}' not found"}

            agent = self.agents[agent_name]
            return await agent.execute_task(task)

        results = await asyncio.gather(*[
            execute_task(task) for task in tasks
        ])

        return results

    def get_system_status(self) -> Dict:
        """Get status of all agents."""
        return {
            "orchestrator": "Multi-Agent Orchestrator",
            "agents": [
                agent.get_metrics()
                for agent in self.agents.values()
            ],
            "workflows": list(self.workflows.keys()),
            "timestamp": datetime.now().isoformat()
        }
