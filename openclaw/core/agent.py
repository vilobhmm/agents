"""Base Agent class for OpenClaw"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import anthropic
from pydantic import BaseModel


logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for an Agent"""

    name: str
    description: str
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 1.0
    system_prompt: Optional[str] = None
    tools: List[Dict[str, Any]] = field(default_factory=list)
    proactive: bool = False
    schedule: Optional[str] = None  # Cron expression for proactive agents


class AgentMemory(BaseModel):
    """Memory storage for agent conversations"""

    messages: List[Dict[str, Any]] = []
    context: Dict[str, Any] = {}
    last_updated: datetime = datetime.now()


class Agent(ABC):
    """Base class for all OpenClaw agents"""

    def __init__(self, config: AgentConfig, api_key: Optional[str] = None):
        self.config = config
        self.client = anthropic.Anthropic(api_key=api_key)
        self.memory = AgentMemory()
        self.callbacks: List[Callable] = []
        logger.info(f"Initialized agent: {config.name}")

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and return results.
        Must be implemented by subclasses.
        """
        pass

    async def chat(self, message: str, **kwargs) -> str:
        """
        Send a message to Claude and get a response.
        """
        self.memory.messages.append({"role": "user", "content": message})

        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=self.config.system_prompt or self._default_system_prompt(),
                messages=self.memory.messages,
                tools=self.config.tools if self.config.tools else None,
                **kwargs,
            )

            # Handle tool use
            if response.stop_reason == "tool_use":
                tool_results = await self._handle_tools(response.content)
                # Continue conversation with tool results
                self.memory.messages.append(
                    {"role": "assistant", "content": response.content}
                )
                self.memory.messages.append({"role": "user", "content": tool_results})

                # Get final response
                response = self.client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    system=self.config.system_prompt
                    or self._default_system_prompt(),
                    messages=self.memory.messages,
                )

            # Extract text response
            response_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    response_text += block.text

            self.memory.messages.append(
                {"role": "assistant", "content": response_text}
            )
            self.memory.last_updated = datetime.now()

            return response_text

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise

    async def _handle_tools(self, content: List) -> List[Dict[str, Any]]:
        """Handle tool use requests from Claude"""
        tool_results = []

        for block in content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input

                logger.info(f"Executing tool: {tool_name}")

                # Execute the tool
                result = await self._execute_tool(tool_name, tool_input)

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    }
                )

        return tool_results

    async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a tool by name.
        Should be overridden by subclasses to implement custom tools.
        """
        logger.warning(f"Tool {tool_name} not implemented")
        return {"error": f"Tool {tool_name} not implemented"}

    def _default_system_prompt(self) -> str:
        """Default system prompt for the agent"""
        return f"""You are {self.config.name}, an AI agent built with OpenClaw.

{self.config.description}

You have access to various tools and integrations. Use them to help the user effectively.
Be proactive, helpful, and clear in your communication."""

    def add_callback(self, callback: Callable):
        """Add a callback to be called after processing"""
        self.callbacks.append(callback)

    async def notify(self, message: str, channel: str = "default"):
        """
        Send a notification to the user.
        Override this to implement custom notification logic.
        """
        logger.info(f"[{channel}] {message}")

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a value from agent context"""
        return self.memory.context.get(key, default)

    def set_context(self, key: str, value: Any):
        """Set a value in agent context"""
        self.memory.context[key] = value

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory = AgentMemory()
        logger.info(f"Cleared memory for agent: {self.config.name}")
