"""Chat interface for OpenClaw agents"""

import logging
from typing import Dict, List, Optional, Protocol

from openclaw.core.agent import Agent


logger = logging.getLogger(__name__)


class MessagePlatform(Protocol):
    """Protocol for message platform integrations"""

    async def send_message(self, recipient: str, message: str) -> bool:
        """Send a message to a recipient"""
        ...

    async def receive_messages(self) -> List[Dict]:
        """Receive new messages"""
        ...


class ChatInterface:
    """Chat-first interface for interacting with agents"""

    def __init__(self, agent: Agent, platform: Optional[MessagePlatform] = None):
        self.agent = agent
        self.platform = platform
        self.conversation_active = False

    async def send(self, message: str) -> str:
        """
        Send a message to the agent and get a response.

        Args:
            message: Message to send

        Returns:
            Agent's response
        """
        logger.info(f"User: {message}")
        response = await self.agent.chat(message)
        logger.info(f"{self.agent.config.name}: {response}")
        return response

    async def send_to_platform(self, recipient: str, message: str) -> bool:
        """
        Send a message via the configured platform.

        Args:
            recipient: Recipient identifier (phone number, chat ID, etc.)
            message: Message to send

        Returns:
            True if successful
        """
        if not self.platform:
            logger.error("No message platform configured")
            return False

        try:
            return await self.platform.send_message(recipient, message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def receive_from_platform(self) -> List[Dict]:
        """
        Receive messages from the configured platform.

        Returns:
            List of messages
        """
        if not self.platform:
            logger.warning("No message platform configured")
            return []

        try:
            return await self.platform.receive_messages()
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            return []

    async def start_conversation(self, greeting: Optional[str] = None):
        """Start a conversation with the agent"""
        self.conversation_active = True
        if greeting:
            await self.send(greeting)

    def end_conversation(self):
        """End the current conversation"""
        self.conversation_active = False
        logger.info(f"Conversation ended with {self.agent.config.name}")

    async def handle_incoming(self, process_func=None):
        """
        Handle incoming messages from the platform.

        Args:
            process_func: Optional function to process each message
                         Signature: async def process(message: Dict) -> str
        """
        messages = await self.receive_from_platform()

        for msg in messages:
            sender = msg.get("sender")
            text = msg.get("text", "")

            logger.info(f"Incoming from {sender}: {text}")

            # Process message
            if process_func:
                response = await process_func(msg)
            else:
                response = await self.send(text)

            # Send response back
            if response:
                await self.send_to_platform(sender, response)

    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.agent.memory.messages

    def clear_history(self):
        """Clear conversation history"""
        self.agent.clear_memory()


class ConsoleChat(ChatInterface):
    """Console-based chat interface for testing"""

    def __init__(self, agent: Agent):
        super().__init__(agent, platform=None)

    async def run(self):
        """Run interactive console chat"""
        print(f"\n=== Chat with {self.agent.config.name} ===")
        print(f"{self.agent.config.description}")
        print("Type 'exit' or 'quit' to end the conversation.\n")

        self.conversation_active = True

        while self.conversation_active:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    self.end_conversation()
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                response = await self.send(user_input)
                print(f"\n{self.agent.config.name}: {response}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.end_conversation()
                break
            except Exception as e:
                logger.error(f"Error in console chat: {e}")
                print(f"Error: {e}")
