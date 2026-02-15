"""
OpenClaw - AI Agent Framework

A powerful, chat-first AI agent framework for building proactive automation systems.
"""

from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.orchestrator import Orchestrator
from openclaw.core.scheduler import ProactiveScheduler
from openclaw.core.chat import ChatInterface

__version__ = "0.1.0"
__all__ = ["Agent", "AgentConfig", "Orchestrator", "ProactiveScheduler", "ChatInterface"]
