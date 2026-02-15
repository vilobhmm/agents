"""Message routing - parse @agent_id and [@agent: message] patterns.

Simple routing without complex state machines, inspired by tinyclaw.
"""

import re
from typing import Dict, List, Optional, Tuple


def parse_agent_routing(message: str) -> Tuple[Optional[str], str]:
    """
    Parse @agent_id prefix from message.

    Examples:
        "@coder fix the bug" -> ("coder", "fix the bug")
        "@team dev review PR" -> ("dev", "review PR")
        "hello world" -> (None, "hello world")

    Args:
        message: Raw message text

    Returns:
        (agent_id, remaining_message) or (None, original_message)
    """
    # Match @agent_id at start of message
    match = re.match(r'^@([a-zA-Z0-9_-]+)\s+(.*)', message, re.DOTALL)

    if match:
        agent_id = match.group(1).lower()
        remaining = match.group(2).strip()
        return (agent_id, remaining)

    return (None, message)


def extract_teammate_mentions(message: str) -> List[Tuple[str, str]]:
    """
    Extract [@agent: message] mentions from text.

    Format: [@agent_id: directed message goes here]

    Examples:
        "I fixed it. [@reviewer: please review]"
        -> [("reviewer", "please review")]

        "[@coder: fix bug] [@tester: test it]"
        -> [("coder", "fix bug"), ("tester", "test it")]

    Args:
        message: Message text potentially containing mentions

    Returns:
        List of (agent_id, directed_message) tuples
    """
    # Pattern: [@agent_id: message]
    pattern = r'\[@([a-zA-Z0-9_-]+):\s*([^\]]+)\]'
    matches = re.findall(pattern, message)

    return [(agent_id.lower(), msg.strip()) for agent_id, msg in matches]


def get_shared_context(message: str) -> str:
    """
    Extract shared context (text outside of [@agent: ...] tags).

    Example:
        "Here's the context. [@coder: task1] [@reviewer: task2]"
        -> "Here's the context."

    Args:
        message: Message text

    Returns:
        Shared context text (empty if all text is in mentions)
    """
    # Remove all [@agent: ...] patterns
    pattern = r'\[@[a-zA-Z0-9_-]+:\s*[^\]]+\]'
    context = re.sub(pattern, '', message)

    return context.strip()


def build_agent_message(shared_context: str, directed_message: str) -> str:
    """
    Combine shared context with directed message for an agent.

    Args:
        shared_context: Context shared across all agents
        directed_message: Message directed to specific agent

    Returns:
        Combined message for agent
    """
    if shared_context and directed_message:
        return f"{shared_context}\n\n{directed_message}"
    elif shared_context:
        return shared_context
    else:
        return directed_message


def is_team_mention(agent_or_team_id: str, teams: Dict) -> bool:
    """
    Check if ID refers to a team.

    Args:
        agent_or_team_id: ID to check
        teams: Dictionary of team configs

    Returns:
        True if ID is a team ID
    """
    return agent_or_team_id in teams


def find_team_for_agent(agent_id: str, teams: Dict) -> Optional[str]:
    """
    Find the first team containing an agent.

    Args:
        agent_id: Agent ID to search for
        teams: Dictionary of team configs

    Returns:
        Team ID if found, None otherwise
    """
    for team_id, team_config in teams.items():
        if agent_id in team_config.agents:
            return team_id
    return None


def is_teammate(agent_id: str, team_config) -> bool:
    """
    Check if an agent is a member of a team.

    Args:
        agent_id: Agent ID to check
        team_config: Team configuration

    Returns:
        True if agent is in team
    """
    return agent_id in team_config.agents


def validate_mentions(
    mentions: List[Tuple[str, str]],
    team_config,
    agents: Dict
) -> List[Tuple[str, str, bool]]:
    """
    Validate teammate mentions.

    Args:
        mentions: List of (agent_id, message) tuples
        team_config: Team configuration
        agents: Available agents

    Returns:
        List of (agent_id, message, is_valid) tuples
    """
    validated = []

    for agent_id, message in mentions:
        # Check if agent exists
        if agent_id not in agents:
            validated.append((agent_id, message, False))
            continue

        # Check if agent is in team (if team context)
        if team_config and not is_teammate(agent_id, team_config):
            validated.append((agent_id, message, False))
            continue

        validated.append((agent_id, message, True))

    return validated


def format_pending_notice(pending_count: int) -> str:
    """
    Format a notice about pending teammate responses.

    This prevents "re-ask spirals" where agents keep mentioning
    teammates who haven't responded yet.

    Args:
        pending_count: Number of responses still pending

    Returns:
        Formatted notice text
    """
    if pending_count == 0:
        return ""

    if pending_count == 1:
        return ("\n\n[1 other teammate response is still being processed and will be "
                "delivered when ready. Do not re-mention teammates who haven't responded yet.]")

    return (f"\n\n[{pending_count} other teammate responses are still being processed and will be "
            f"delivered when ready. Do not re-mention teammates who haven't responded yet.]")
