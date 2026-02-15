"""Conversation tracking and management.

Handles multi-agent conversations with pending response tracking.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
import uuid

from agency.core.types import Conversation, ChainStep, MessageData


logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages multi-agent conversations.

    Key insight from tinyclaw: Use a simple counter (pending) to track
    completion instead of complex state machines.

    Conversation flow:
        pending: 1  ← Initial message to agent
        pending: 3  ← Agent mentions 2 teammates
        pending: 2  ← 1st teammate responds
        pending: 1  ← 2nd teammate responds
        pending: 0  ← Complete! Aggregate and send
    """

    def __init__(self, state_path: Path):
        """
        Initialize conversation manager.

        Args:
            state_path: Directory to store conversation state
        """
        self.state_path = Path(state_path)
        self.state_path.mkdir(parents=True, exist_ok=True)
        self.conversations: Dict[str, Conversation] = {}

        # Load existing conversations
        self._load_conversations()

    def create_conversation(
        self,
        message: MessageData,
        team_context: Optional[Dict] = None
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            message: Initial message
            team_context: Team information if team conversation

        Returns:
            New conversation instance
        """
        conv_id = str(uuid.uuid4())

        conversation = Conversation(
            id=conv_id,
            channel=message.channel,
            sender=message.sender,
            sender_id=message.sender_id,
            original_message=message.message,
            original_message_id=message.message_id,
            pending=1,  # Starts with 1 (the initial agent)
            team_context=team_context,
        )

        self.conversations[conv_id] = conversation
        self._save_conversation(conversation)

        logger.info(f"Created conversation {conv_id}")
        return conversation

    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.conversations.get(conv_id)

    def add_response(
        self,
        conv_id: str,
        agent_id: str,
        agent_name: str,
        response: str,
        mentions: list,
        files: list
    ) -> Conversation:
        """
        Add an agent response to conversation.

        Args:
            conv_id: Conversation ID
            agent_id: Agent that responded
            agent_name: Agent display name
            response: Agent's response text
            mentions: List of (agent_id, message) teammate mentions
            files: List of file paths

        Returns:
            Updated conversation
        """
        conv = self.conversations.get(conv_id)
        if not conv:
            raise ValueError(f"Conversation not found: {conv_id}")

        # Create chain step
        step = ChainStep(
            agent_id=agent_id,
            agent_name=agent_name,
            response=response,
            timestamp=0,  # Will be set when saved
            files=files,
            mentions=mentions
        )

        # Add to responses
        conv.responses.append(step)
        conv.total_messages += 1

        # Update pending count
        # Decrement for this agent, increment for each new mention
        conv.pending -= 1
        conv.pending += len(mentions)

        # Track mentions per agent
        for mentioned_agent_id, _ in mentions:
            conv.outgoing_mentions[mentioned_agent_id] = \
                conv.outgoing_mentions.get(mentioned_agent_id, 0) + 1

        # Update files
        conv.files.update(files)

        self._save_conversation(conv)

        logger.info(
            f"Added response to conversation {conv_id}: "
            f"agent={agent_id}, mentions={len(mentions)}, pending={conv.pending}"
        )

        return conv

    def is_complete(self, conv_id: str) -> bool:
        """
        Check if conversation is complete (pending == 0).

        Args:
            conv_id: Conversation ID

        Returns:
            True if all responses received
        """
        conv = self.conversations.get(conv_id)
        if not conv:
            return True  # Unknown conversation = complete

        return conv.pending == 0

    def is_loop_detected(self, conv_id: str) -> bool:
        """
        Check if conversation has entered an infinite loop.

        Args:
            conv_id: Conversation ID

        Returns:
            True if loop detected (too many messages)
        """
        conv = self.conversations.get(conv_id)
        if not conv:
            return False

        return conv.total_messages >= conv.max_messages

    def get_aggregated_response(self, conv_id: str) -> str:
        """
        Get aggregated response from all agents.

        Args:
            conv_id: Conversation ID

        Returns:
            Formatted response text
        """
        conv = self.conversations.get(conv_id)
        if not conv:
            return ""

        if not conv.responses:
            return ""

        # Format responses
        parts = []

        for step in conv.responses:
            if len(conv.responses) == 1:
                # Single response - no need for headers
                parts.append(step.response)
            else:
                # Multi-agent - add headers
                parts.append(f"**{step.agent_name} (@{step.agent_id}):**\n{step.response}")

        return "\n\n---\n\n".join(parts)

    def complete_conversation(self, conv_id: str):
        """
        Mark conversation as complete and archive it.

        Args:
            conv_id: Conversation ID
        """
        conv = self.conversations.get(conv_id)
        if not conv:
            return

        # Save to archive
        if conv.team_context:
            self._archive_team_conversation(conv)

        # Remove from active conversations
        del self.conversations[conv_id]

        # Delete state file
        state_file = self.state_path / f"{conv_id}.json"
        if state_file.exists():
            state_file.unlink()

        logger.info(f"Completed conversation {conv_id}")

    def _save_conversation(self, conv: Conversation):
        """Save conversation state to file"""
        state_file = self.state_path / f"{conv.id}.json"

        data = {
            "id": conv.id,
            "channel": conv.channel,
            "sender": conv.sender,
            "sender_id": conv.sender_id,
            "original_message": conv.original_message,
            "original_message_id": conv.original_message_id,
            "pending": conv.pending,
            "responses": [
                {
                    "agent_id": step.agent_id,
                    "agent_name": step.agent_name,
                    "response": step.response,
                    "timestamp": step.timestamp,
                    "files": [str(f) for f in step.files],
                    "mentions": step.mentions,
                }
                for step in conv.responses
            ],
            "total_messages": conv.total_messages,
            "files": [str(f) for f in conv.files],
            "team_context": conv.team_context,
            "outgoing_mentions": conv.outgoing_mentions,
            "created_at": conv.created_at,
        }

        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_conversations(self):
        """Load existing conversations from state files"""
        for state_file in self.state_path.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)

                conv = Conversation(
                    id=data["id"],
                    channel=data["channel"],
                    sender=data["sender"],
                    sender_id=data["sender_id"],
                    original_message=data["original_message"],
                    original_message_id=data["original_message_id"],
                    pending=data["pending"],
                    responses=[
                        ChainStep(
                            agent_id=step["agent_id"],
                            agent_name=step["agent_name"],
                            response=step["response"],
                            timestamp=step["timestamp"],
                            files=[Path(f) for f in step["files"]],
                            mentions=step["mentions"],
                        )
                        for step in data["responses"]
                    ],
                    total_messages=data["total_messages"],
                    files=set(Path(f) for f in data["files"]),
                    team_context=data.get("team_context"),
                    outgoing_mentions=data.get("outgoing_mentions", {}),
                    created_at=data["created_at"],
                )

                self.conversations[conv.id] = conv

            except Exception as e:
                logger.error(f"Could not load conversation from {state_file}: {e}")

        logger.info(f"Loaded {len(self.conversations)} active conversations")

    def _archive_team_conversation(self, conv: Conversation):
        """Archive team conversation to chat history"""
        if not conv.team_context:
            return

        # Create archive directory
        team_id = conv.team_context.get('team_id')
        archive_dir = self.state_path.parent / "chats" / team_id
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Create archive file
        from datetime import datetime
        timestamp = datetime.fromtimestamp(conv.created_at).isoformat()
        archive_file = archive_dir / f"{timestamp}_{conv.id[:8]}.md"

        # Format conversation
        lines = [
            f"# Team Conversation: {conv.team_context.get('name')}",
            f"**Date:** {timestamp}",
            f"**Channel:** {conv.channel} | **Sender:** {conv.sender}",
            f"**Messages:** {conv.total_messages}",
            "",
            "## User Message",
            conv.original_message,
            "",
        ]

        for step in conv.responses:
            lines.append(f"## {step.agent_name} (@{step.agent_id})")
            lines.append(step.response)
            lines.append("")

        archive_file.write_text("\n".join(lines))
        logger.info(f"Archived team conversation to {archive_file}")
