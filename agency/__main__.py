"""
Main entry point for agency system.

Usage:
    python -m agency [command]

Commands:
    start     - Start the agency system (processor + channels)
    process   - Start only the processor
    telegram  - Start only the Telegram channel
    send      - Send a test message to the queue
"""

import asyncio
import logging
import sys
from pathlib import Path

from agency import load_config, get_telegram_config, AgencyProcessor
from agency.channels.telegram_channel import TelegramChannel
from agency.core.queue import FileQueue
from agency.core.types import MessageData
import time


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_processor(config_path: Path = None):
    """Run the agency processor"""
    config = load_config(config_path)
    processor = AgencyProcessor(config)
    await processor.start()


async def run_telegram(config_path: Path = None):
    """Run the Telegram channel"""
    config = load_config(config_path)
    bot_token, allowed_users = get_telegram_config()

    channel = TelegramChannel(
        bot_token=bot_token,
        queue=FileQueue(config.queue_path),
        allowed_users=allowed_users
    )
    await channel.start()


async def run_full_system(config_path: Path = None):
    """Run both processor and Telegram channel"""
    config = load_config(config_path)
    bot_token, allowed_users = get_telegram_config()

    # Create processor
    processor = AgencyProcessor(config)

    # Create Telegram channel
    telegram = TelegramChannel(
        bot_token=bot_token,
        queue=FileQueue(config.queue_path),
        allowed_users=allowed_users
    )

    # Run both concurrently
    await asyncio.gather(
        processor.start(),
        telegram.start()
    )


def send_test_message(message: str, agent: str = "researcher"):
    """Send a test message to the queue"""
    config = load_config()
    queue = FileQueue(config.queue_path)

    message_data = MessageData(
        channel="cli",
        sender="test_user",
        sender_id="test_123",
        message=f"@{agent} {message}",
        timestamp=time.time(),
        message_id="test_msg_1",
        metadata={"source": "cli"}
    )

    path = queue.enqueue(message_data, "incoming")
    print(f"✓ Message enqueued: {path.name}")
    print(f"  Agent: {agent}")
    print(f"  Message: {message}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python -m agency [command]")
        print("\nCommands:")
        print("  start     - Start full system (processor + Telegram)")
        print("  process   - Start only the processor")
        print("  telegram  - Start only the Telegram bot")
        print("  send      - Send a test message")
        print("\nExamples:")
        print("  python -m agency start")
        print("  python -m agency send \"What's new in AI?\" researcher")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        logger.info("Starting agency system (processor + Telegram)...")
        asyncio.run(run_full_system())

    elif command == "process":
        logger.info("Starting agency processor...")
        asyncio.run(run_processor())

    elif command == "telegram":
        logger.info("Starting Telegram channel...")
        asyncio.run(run_telegram())

    elif command == "send":
        if len(sys.argv) < 3:
            print("Usage: python -m agency send <message> [agent]")
            sys.exit(1)

        message = sys.argv[2]
        agent = sys.argv[3] if len(sys.argv) > 3 else "researcher"
        send_test_message(message, agent)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
