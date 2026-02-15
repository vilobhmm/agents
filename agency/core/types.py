"""Core data types for the agency system.

Inspired by tinyclaw's simplicity - minimal types, maximum flexibility.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum


class Provider(str, Enum):
    """AI provider types"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


@dataclass
class AgentConfig:
    """
    Configuration for a single agent.

    Each agent is fully isolated with its own:
    - Working directory
    - Conversation history
    - Context files
    """
    name: str                           # Display name
    agent_id: str                       # Unique identifier (lowercase, no spaces)
    provider: Provider                  # AI provider
    model: str                          # Model name
    working_directory: Path             # Isolated workspace
    personality: Optional[str] = None   # Agent's personality/role description
    skills: List[str] = field(default_factory=list)  # Special skills/capabilities


@dataclass
class TeamConfig:
    """
    Configuration for a team of agents.

    Teams enable multi-agent coordination through:
    - Leader-based routing
    - Teammate mentions ([@agent: message])
    - Conversation aggregation
    """
    name: str                           # Team display name
    team_id: str                        # Unique identifier
    agents: List[str]                   # List of agent IDs in team
    leader_agent: str                   # Agent ID of team leader
    description: Optional[str] = None   # Team purpose


@dataclass
class MessageData:
    """
    A message in the system.

    This is the core data structure that flows through queues.
    """
    channel: str                        # Source channel (telegram, discord, etc.)
    sender: str                         # Sender display name
    sender_id: str                      # Unique sender ID
    message: str                        # Message content
    timestamp: float                    # Unix timestamp
    message_id: str                     # Unique message ID
    agent: Optional[str] = None         # Target agent ID (if routed)
    team: Optional[str] = None          # Target team ID (if routed)
    conversation_id: Optional[str] = None  # Conversation this belongs to
    files: List[Path] = field(default_factory=list)  # Attached files
    metadata: Dict = field(default_factory=dict)  # Channel-specific metadata


@dataclass
class ChainStep:
    """
    A step in a conversation chain (one agent's response).
    """
    agent_id: str
    agent_name: str
    response: str
    timestamp: float
    files: List[Path] = field(default_factory=list)
    mentions: List[tuple[str, str]] = field(default_factory=list)  # [(agent_id, message), ...]


@dataclass
class Conversation:
    """
    Tracks a multi-agent conversation.

    Key insight from tinyclaw: Use a simple counter (pending) to track
    completion instead of complex state machines.
    """
    id: str                             # Unique conversation ID
    channel: str                        # Source channel
    sender: str                         # Original sender
    sender_id: str                      # Original sender ID
    original_message: str               # Initial message
    original_message_id: str            # Initial message ID
    pending: int                        # Number of in-flight responses
    responses: List[ChainStep] = field(default_factory=list)  # Collected responses
    total_messages: int = 0             # Loop protection counter
    files: Set[Path] = field(default_factory=set)  # Accumulated files
    team_context: Optional[Dict] = None  # Team info if team conversation
    outgoing_mentions: Dict[str, int] = field(default_factory=dict)  # Track per-agent mentions
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    max_messages: int = 50              # Loop protection limit


@dataclass
class QueuedMessage:
    """A message in the queue with its file path"""
    path: Path
    data: MessageData
    created_at: float


@dataclass
class AgencyConfig:
    """
    Root configuration for the agency system.
    """
    workspace_path: Path                # Root workspace for all agents
    queue_path: Path                    # Queue directory
    agents: Dict[str, AgentConfig]      # agent_id -> config
    teams: Dict[str, TeamConfig]        # team_id -> config
    channels: List[str]                 # Enabled channels
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None


# Channel-specific configurations

@dataclass
class TelegramConfig:
    """Telegram bot configuration"""
    bot_token: str
    chat_id: Optional[str] = None
    allowed_users: List[str] = field(default_factory=list)


@dataclass
class DiscordConfig:
    """Discord bot configuration"""
    bot_token: str
    allowed_channels: List[str] = field(default_factory=list)
    allowed_users: List[str] = field(default_factory=list)


@dataclass
class SlackConfig:
    """Slack bot configuration"""
    bot_token: str
    signing_secret: str
    app_token: str
