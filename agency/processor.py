"""Main queue processor - the heart of the agency system.

Handles message routing, agent invocation, and team coordination.
Inspired by tinyclaw's elegant actor model.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Optional
import time

from agency.core.types import AgencyConfig, MessageData
from agency.core.queue import FileQueue
from agency.core.agent import AgentInvoker
from agency.core.conversation import ConversationManager
from agency.core import router


logger = logging.getLogger(__name__)


class AgencyProcessor:
    """
    Main processor for the agency system.

    Architecture (inspired by tinyclaw):
    - File-based queues (incoming → processing → outgoing)
    - Per-agent promise chains (sequential per agent, parallel across agents)
    - Actor model (no central orchestrator)
    - Simple conversation tracking (pending counter)
    """

    def __init__(self, config: AgencyConfig):
        """
        Initialize agency processor.

        Args:
            config: Agency configuration
        """
        self.config = config
        self.queue = FileQueue(config.queue_path)
        self.invoker = AgentInvoker(
            anthropic_api_key=config.anthropic_api_key,
            openai_api_key=config.openai_api_key
        )
        self.conv_manager = ConversationManager(
            config.queue_path / "conversations"
        )

        # Per-agent promise chains (for sequential processing per agent)
        self.agent_chains: Dict[str, asyncio.Task] = {}

        logger.info("Agency processor initialized")

    async def start(self):
        """Start processing messages (runs forever)"""
        logger.info("Starting agency processor...")

        # Recover orphaned messages
        recovered = self.queue.recover_orphaned()
        if recovered:
            logger.info(f"Recovered {recovered} orphaned messages")

        # Main processing loop
        while True:
            try:
                # Dequeue next message
                queued_message = self.queue.dequeue()

                if not queued_message:
                    # No messages, sleep briefly
                    await asyncio.sleep(0.1)
                    continue

                # Route and process message
                await self._route_message(queued_message)

            except KeyboardInterrupt:
                logger.info("Shutting down processor...")
                break
            except Exception as e:
                logger.error(f"Error in processor loop: {e}", exc_info=True)
                await asyncio.sleep(1)

    async def _route_message(self, queued_message):
        """
        Route message to appropriate agent(s).

        This implements the core routing logic:
        1. Parse @agent_id or @team_id from message
        2. Create or get conversation
        3. Enqueue for processing on per-agent chain
        """
        message = queued_message.data

        # Parse routing
        target_id, remaining_message = router.parse_agent_routing(message.message)

        if not target_id:
            logger.warning(f"No routing target in message: {message.message[:50]}")
            self.queue.complete(queued_message)
            return

        # Check if target is a team
        is_team = router.is_team_mention(target_id, self.config.teams)

        if is_team:
            # Route to team leader
            team_config = self.config.teams[target_id]
            target_agent_id = team_config.leader_agent
            team_context = self._build_team_context(team_config)
        else:
            # Route directly to agent
            target_agent_id = target_id
            # Check if agent belongs to a team
            team_id = router.find_team_for_agent(target_agent_id, self.config.teams)
            if team_id:
                team_context = self._build_team_context(self.config.teams[team_id])
            else:
                team_context = None

        # Validate agent exists
        if target_agent_id not in self.config.agents:
            logger.error(f"Unknown agent: {target_agent_id}")
            self.queue.complete(queued_message)
            return

        # Create or get conversation
        if message.conversation_id:
            conversation = self.conv_manager.get_conversation(message.conversation_id)
            if not conversation:
                logger.error(f"Conversation not found: {message.conversation_id}")
                self.queue.complete(queued_message)
                return
        else:
            conversation = self.conv_manager.create_conversation(message, team_context)
            message.conversation_id = conversation.id

        # Process on per-agent chain
        await self._process_on_agent_chain(
            target_agent_id,
            message,
            conversation,
            queued_message
        )

    async def _process_on_agent_chain(self, agent_id: str, message: MessageData, conversation, queued_message):
        """
        Process message on per-agent promise chain.

        Key insight from tinyclaw: Each agent has a sequential queue (promise chain)
        but different agents process in parallel.
        """
        # Get or create agent's promise chain
        if agent_id in self.agent_chains:
            # Wait for previous messages to this agent
            try:
                await self.agent_chains[agent_id]
            except Exception as e:
                logger.error(f"Previous task for {agent_id} failed: {e}")

        # Create new task for this agent
        task = asyncio.create_task(
            self._process_message(agent_id, message, conversation, queued_message)
        )
        self.agent_chains[agent_id] = task

    async def _process_message(self, agent_id: str, message: MessageData, conversation, queued_message):
        """
        Process a message (invoke agent, handle response).

        This is the core processing logic:
        1. Invoke agent with message
        2. Parse response for teammate mentions
        3. Enqueue messages to mentioned teammates
        4. Update conversation state
        5. Send response if conversation complete
        """
        try:
            agent_config = self.config.agents[agent_id]

            logger.info(f"Processing message for agent {agent_id}")

            # Build message with pending notice
            if conversation.pending > 1:
                pending_notice = router.format_pending_notice(conversation.pending - 1)
                agent_message = message.message + pending_notice
            else:
                agent_message = message.message

            # Invoke agent
            start_time = time.time()
            response = await self.invoker.invoke_agent(
                agent_config=agent_config,
                message=agent_message,
                workspace_path=self.config.workspace_path,
                team_context=conversation.team_context,
                reset=False
            )
            elapsed = time.time() - start_time

            logger.info(f"Agent {agent_id} responded in {elapsed:.2f}s")

            # Extract teammate mentions from response
            mentions = router.extract_teammate_mentions(response)

            # Validate mentions (if team context)
            if conversation.team_context and mentions:
                validated = router.validate_mentions(
                    mentions,
                    conversation.team_context,
                    self.config.agents
                )
                # Filter to valid mentions
                mentions = [(aid, msg) for aid, msg, valid in validated if valid]

            # Add response to conversation
            conversation = self.conv_manager.add_response(
                conv_id=conversation.id,
                agent_id=agent_id,
                agent_name=agent_config.name,
                response=response,
                mentions=mentions,
                files=[]
            )

            # Enqueue messages to mentioned teammates
            if mentions:
                await self._enqueue_teammate_mentions(
                    mentions,
                    conversation,
                    message.channel
                )

            # Check if conversation complete
            if self.conv_manager.is_complete(conversation.id):
                await self._complete_conversation(conversation, message.channel)
            elif self.conv_manager.is_loop_detected(conversation.id):
                logger.error(f"Loop detected in conversation {conversation.id}")
                await self._complete_conversation(conversation, message.channel)

        except Exception as e:
            logger.error(f"Error processing message for {agent_id}: {e}", exc_info=True)
        finally:
            # Mark message as complete
            self.queue.complete(queued_message)

    async def _enqueue_teammate_mentions(self, mentions: list, conversation, channel: str):
        """
        Enqueue messages to mentioned teammates.

        Args:
            mentions: List of (agent_id, message) tuples
            conversation: Current conversation
            channel: Source channel
        """
        shared_context = router.get_shared_context(conversation.responses[-1].response)

        for agent_id, directed_message in mentions:
            # Build full message for teammate
            full_message = router.build_agent_message(shared_context, directed_message)

            # Create message data
            teammate_message = MessageData(
                channel=channel,
                sender=conversation.sender,
                sender_id=conversation.sender_id,
                message=full_message,
                timestamp=time.time(),
                message_id=f"{conversation.original_message_id}_mention_{agent_id}",
                agent=agent_id,
                conversation_id=conversation.id,
                files=[],
                metadata={"from_agent": conversation.responses[-1].agent_id}
            )

            # Enqueue to incoming queue
            self.queue.enqueue(teammate_message, "incoming")

            logger.info(f"Enqueued message to teammate {agent_id}")

    async def _complete_conversation(self, conversation, channel: str):
        """
        Complete conversation and send aggregated response.

        Args:
            conversation: Conversation to complete
            channel: Channel to send response to
        """
        # Get aggregated response
        response_text = self.conv_manager.get_aggregated_response(conversation.id)

        # Create outgoing message
        outgoing_message = MessageData(
            channel=channel,
            sender=conversation.sender,
            sender_id=conversation.sender_id,
            message=response_text,
            timestamp=time.time(),
            message_id=conversation.original_message_id,
            metadata={
                "conversation_id": conversation.id,
                "original_message": conversation.original_message,
                "agents": [step.agent_id for step in conversation.responses],
            }
        )

        # Enqueue to outgoing
        self.queue.enqueue(outgoing_message, "outgoing")

        # Complete conversation
        self.conv_manager.complete_conversation(conversation.id)

        logger.info(f"Completed conversation {conversation.id}")

    def _build_team_context(self, team_config) -> Dict:
        """Build team context dictionary for agents"""
        return {
            "team_id": team_config.team_id,
            "name": team_config.name,
            "leader_agent": team_config.leader_agent,
            "agents": [
                {
                    "agent_id": aid,
                    "name": self.config.agents[aid].name,
                    "personality": self.config.agents[aid].personality,
                }
                for aid in team_config.agents
                if aid in self.config.agents
            ]
        }
