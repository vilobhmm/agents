"""Configuration management for agency system."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional

from agency.core.types import (
    AgencyConfig,
    AgentConfig,
    TeamConfig,
    Provider,
)


logger = logging.getLogger(__name__)


def load_config(
    config_path: Optional[Path] = None,
    workspace_path: Optional[Path] = None,
    queue_path: Optional[Path] = None,
) -> AgencyConfig:
    """
    Load agency configuration.

    Args:
        config_path: Path to agents.json config file
        workspace_path: Root workspace directory
        queue_path: Queue directory

    Returns:
        AgencyConfig instance
    """
    # Default paths
    if not config_path:
        config_path = Path(__file__).parent / "templates" / "agents.json"

    if not workspace_path:
        workspace_path = Path.home() / "agency-workspace"

    if not queue_path:
        queue_path = Path.home() / ".agency" / "queue"

    # Load JSON config
    with open(config_path, 'r') as f:
        data = json.load(f)

    # Parse agents
    agents = {}
    for agent_id, agent_data in data.get("agents", {}).items():
        agents[agent_id] = AgentConfig(
            name=agent_data["name"],
            agent_id=agent_id,
            provider=Provider(agent_data["provider"]),
            model=agent_data["model"],
            working_directory=workspace_path / agent_id,
            personality=agent_data.get("personality"),
            skills=agent_data.get("skills", []),
        )

    # Parse teams
    teams = {}
    for team_id, team_data in data.get("teams", {}).items():
        teams[team_id] = TeamConfig(
            name=team_data["name"],
            team_id=team_id,
            agents=team_data["agents"],
            leader_agent=team_data["leader_agent"],
            description=team_data.get("description"),
        )

    # Get API keys from environment
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Create config
    config = AgencyConfig(
        workspace_path=workspace_path,
        queue_path=queue_path,
        agents=agents,
        teams=teams,
        channels=["telegram"],  # Default to Telegram
        anthropic_api_key=anthropic_api_key,
        openai_api_key=openai_api_key,
    )

    logger.info(f"Loaded configuration: {len(agents)} agents, {len(teams)} teams")

    return config


def get_telegram_config() -> tuple[str, Optional[list]]:
    """
    Get Telegram configuration from environment.

    Returns:
        (bot_token, allowed_users)
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")

    # Parse allowed users (comma-separated)
    allowed_users_str = os.getenv("TELEGRAM_ALLOWED_USERS")
    allowed_users = None
    if allowed_users_str:
        allowed_users = [u.strip() for u in allowed_users_str.split(",")]

    return (bot_token, allowed_users)
