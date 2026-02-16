#!/usr/bin/env python3
"""Quick test script to verify agency system is working"""

import asyncio
import time
from pathlib import Path

from agency.core.queue import FileQueue
from agency.core.types import MessageData
from agency.config import load_config


async def test_send_message(agent_id: str, message: str):
    """Test sending a message to an agent"""
    print(f"\n🧪 Testing message to @{agent_id}")
    print(f"Message: {message}")

    # Load config
    config = load_config()

    # Validate agent exists
    if agent_id not in config.agents:
        print(f"❌ Agent '{agent_id}' not found!")
        print(f"Available agents: {', '.join(config.agents.keys())}")
        return False

    # Create message with @agent_id prefix
    message_text = f"@{agent_id} {message}"

    message_data = MessageData(
        channel="test",
        sender="test_user",
        sender_id="test_123",
        message=message_text,
        timestamp=time.time(),
        message_id=f"test_{int(time.time()*1000)}",
        metadata={"test": True}
    )

    # Queue message
    queue = FileQueue(config.queue_path)
    queue.enqueue(message_data, "incoming")

    print(f"✅ Message queued successfully!")
    print(f"Queue path: {config.queue_path}")
    print(f"Message will be processed when agency processor is running")

    return True


async def main():
    """Run tests"""
    print("=" * 60)
    print("🚀 Agency System Test")
    print("=" * 60)

    # Load and display config
    try:
        config = load_config()
        print(f"\n✅ Config loaded successfully")
        print(f"Agents: {len(config.agents)}")
        print(f"Teams: {len(config.teams)}")
        print(f"Queue: {config.queue_path}")
    except Exception as e:
        print(f"\n❌ Failed to load config: {e}")
        return

    # Test sending messages
    print("\n" + "=" * 60)
    print("Testing Message Sending")
    print("=" * 60)

    await test_send_message("cc", "Hello! Give me a brief status update.")
    await asyncio.sleep(1)

    await test_send_message("researcher", "What's interesting in AI today?")
    await asyncio.sleep(1)

    await test_send_message("job_hunter", "Find ML Engineer jobs at top companies")

    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the agency: agency start")
    print("2. Or start processor only: agency start --processor-only")
    print("3. Check logs: agency logs -f")
    print("4. Send messages via Telegram or CLI")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
