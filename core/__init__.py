"""
Agency - Multi-agent multi-channel coordination system.

Inspired by tinyclaw's elegant architecture:
- File-based queues (atomic, crash-safe, observable)
- Actor model (decentralized, message-driven)
- Per-agent promise chains (sequential per agent, parallel across agents)
- Simple conversation tracking (pending counter, not state machines)

Use cases:
- Research and intelligence gathering
- Social media management
- Content creation and newsletters
- Team coordination
- 24/7 autonomous operation
"""

__version__ = "0.1.0"

from core.types import (
    AgentConfig,
    TeamConfig,
    MessageData,
    AgencyConfig,
    Provider,
)
from core.config import load_config, get_telegram_config
from core.processor import AgencyProcessor
from core.queue import FileQueue

__all__ = [
    "AgentConfig",
    "TeamConfig",
    "MessageData",
    "AgencyConfig",
    "Provider",
    "load_config",
    "get_telegram_config",
    "AgencyProcessor",
    "FileQueue",
]
