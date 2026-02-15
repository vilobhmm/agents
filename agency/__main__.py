"""
Agency - Multi-Agent Multi-Channel Coordination System

Main entry point with CLI commands (inspired by tinyclaw).
"""

import argparse
import asyncio
import logging
import os
import sys
import shutil
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Agency - Multi-Agent Multi-Channel Coordination System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m agency start              Start full system (processor + Telegram)
  python -m agency process            Run queue processor only
  python -m agency telegram           Run Telegram bot only
  python -m agency send "message"     Send test message to default agent
  python -m agency send "message" researcher  Send to specific agent
  python -m agency reset              Reset conversation state
  python -m agency clear              Clear all persistent data
  python -m agency status             Show system status

For more information, see AGENCY_README.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # start command - full system
    start_parser = subparsers.add_parser(
        'start',
        help='Start full system (processor + Telegram bot)'
    )
    start_parser.add_argument(
        '--config',
        type=Path,
        help='Path to agents.json config file'
    )
    start_parser.add_argument(
        '--workspace',
        type=Path,
        help='Root workspace directory'
    )

    # process command - processor only
    process_parser = subparsers.add_parser(
        'process',
        help='Run queue processor only (no Telegram bot)'
    )
    process_parser.add_argument(
        '--config',
        type=Path,
        help='Path to agents.json config file'
    )
    process_parser.add_argument(
        '--workspace',
        type=Path,
        help='Root workspace directory'
    )

    # telegram command - Telegram bot only
    telegram_parser = subparsers.add_parser(
        'telegram',
        help='Run Telegram bot only (no processor)'
    )
    telegram_parser.add_argument(
        '--config',
        type=Path,
        help='Path to agents.json config file'
    )

    # send command - send test message
    send_parser = subparsers.add_parser(
        'send',
        help='Send a test message to an agent'
    )
    send_parser.add_argument(
        'message',
        type=str,
        help='Message text to send'
    )
    send_parser.add_argument(
        'agent',
        type=str,
        nargs='?',
        default='researcher',
        help='Agent ID to send to (default: researcher)'
    )
    send_parser.add_argument(
        '--config',
        type=Path,
        help='Path to agents.json config file'
    )

    # reset command - reset conversation state
    reset_parser = subparsers.add_parser(
        'reset',
        help='Reset conversation state (clear active conversations)'
    )
    reset_parser.add_argument(
        '--workspace',
        type=Path,
        help='Root workspace directory'
    )

    # clear command - clear all data
    clear_parser = subparsers.add_parser(
        'clear',
        help='Clear all persistent data (conversations, queue, workspaces)'
    )
    clear_parser.add_argument(
        '--workspace',
        type=Path,
        help='Root workspace directory'
    )
    clear_parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )

    # status command - show system status
    status_parser = subparsers.add_parser(
        'status',
        help='Show system status (queue sizes, active conversations)'
    )
    status_parser.add_argument(
        '--config',
        type=Path,
        help='Path to agents.json config file'
    )

    # init command - initialize workspace
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize workspace and create example config'
    )
    init_parser.add_argument(
        '--workspace',
        type=Path,
        help='Root workspace directory'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Run command
    try:
        if args.command == 'start':
            asyncio.run(cmd_start(args))
        elif args.command == 'process':
            asyncio.run(cmd_process(args))
        elif args.command == 'telegram':
            asyncio.run(cmd_telegram(args))
        elif args.command == 'send':
            asyncio.run(cmd_send(args))
        elif args.command == 'reset':
            cmd_reset(args)
        elif args.command == 'clear':
            cmd_clear(args)
        elif args.command == 'status':
            cmd_status(args)
        elif args.command == 'init':
            cmd_init(args)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


async def cmd_start(args):
    """Start full system (processor + Telegram bot)"""
    from agency.config import load_config, get_telegram_config
    from agency.processor import AgencyProcessor
    from agency.channels.telegram_channel import TelegramChannel

    logger.info("🚀 Starting Agency System...")

    # Load configuration
    config = load_config(
        config_path=args.config,
        workspace_path=args.workspace
    )

    # Get Telegram config
    bot_token, allowed_users = get_telegram_config()

    # Create processor
    processor = AgencyProcessor(config)

    # Create Telegram channel
    telegram = TelegramChannel(bot_token, processor.queue, allowed_users)

    # Start both in parallel
    logger.info("✅ Starting processor and Telegram bot...")
    await asyncio.gather(
        processor.start(),
        telegram.start()
    )


async def cmd_process(args):
    """Run queue processor only"""
    from agency.config import load_config
    from agency.processor import AgencyProcessor

    logger.info("🚀 Starting Queue Processor...")

    # Load configuration
    config = load_config(
        config_path=args.config,
        workspace_path=args.workspace
    )

    # Create and start processor
    processor = AgencyProcessor(config)
    await processor.start()


async def cmd_telegram(args):
    """Run Telegram bot only"""
    from agency.config import load_config, get_telegram_config
    from agency.core.queue import FileQueue
    from agency.channels.telegram_channel import TelegramChannel

    logger.info("🚀 Starting Telegram Bot...")

    # Load configuration
    config = load_config(config_path=args.config)

    # Get Telegram config
    bot_token, allowed_users = get_telegram_config()

    # Create queue
    queue = FileQueue(config.queue_path)

    # Create and start Telegram channel
    telegram = TelegramChannel(bot_token, queue, allowed_users)
    await telegram.start()


async def cmd_send(args):
    """Send a test message to an agent"""
    from agency.config import load_config
    from agency.core.queue import FileQueue
    from agency.core.types import MessageData
    import time

    logger.info(f"📤 Sending message to @{args.agent}...")

    # Load configuration
    config = load_config(config_path=args.config)

    # Validate agent exists
    if args.agent not in config.agents:
        available = ", ".join(config.agents.keys())
        logger.error(f"Unknown agent: {args.agent}")
        logger.error(f"Available agents: {available}")
        sys.exit(1)

    # Create queue
    queue = FileQueue(config.queue_path)

    # Create message with @agent_id prefix
    message_text = f"@{args.agent} {args.message}"

    # Create message data
    message = MessageData(
        channel="cli",
        sender="CLI User",
        sender_id="cli",
        message=message_text,
        timestamp=time.time(),
        message_id=f"cli_{int(time.time())}",
        metadata={"source": "cli"}
    )

    # Enqueue message
    file_path = queue.enqueue(message, "incoming")

    logger.info(f"✅ Message queued: {file_path.name}")
    logger.info(f"💬 Waiting for response...")

    # Poll for response
    max_wait = 120  # 2 minutes
    start_time = time.time()

    while time.time() - start_time < max_wait:
        # Check outgoing queue
        for queued_message in queue.iter_outgoing():
            if queued_message.data.channel == "cli":
                logger.info("\n" + "=" * 60)
                logger.info("📨 RESPONSE")
                logger.info("=" * 60)
                print(queued_message.data.message)
                logger.info("=" * 60)

                # Delete from outgoing
                queue.delete_outgoing(queued_message.path)
                return

        await asyncio.sleep(0.5)

    logger.error("❌ Timeout waiting for response")
    logger.info("Make sure the processor is running: python -m agency process")


def cmd_reset(args):
    """Reset conversation state"""
    from agency.config import load_config

    logger.info("🔄 Resetting conversation state...")

    # Load configuration
    config = load_config(workspace_path=args.workspace)

    # Clear conversation state
    conversations_dir = config.queue_path / "conversations"
    if conversations_dir.exists():
        count = len(list(conversations_dir.glob("*.json")))
        for file in conversations_dir.glob("*.json"):
            file.unlink()
        logger.info(f"✅ Cleared {count} active conversations")
    else:
        logger.info("ℹ️  No conversations to clear")

    logger.info("✅ Conversation state reset complete")


def cmd_clear(args):
    """Clear all persistent data"""
    from agency.config import load_config

    logger.info("⚠️  WARNING: This will clear ALL persistent data!")
    logger.info("  - Queue (incoming, processing, outgoing)")
    logger.info("  - Conversations")
    logger.info("  - Agent workspaces")
    logger.info("  - Chat history")

    if not args.force:
        response = input("\nAre you sure? Type 'yes' to confirm: ")
        if response.lower() != 'yes':
            logger.info("❌ Aborted")
            return

    # Load configuration
    config = load_config(workspace_path=args.workspace)

    # Clear queue
    logger.info("Clearing queue...")
    for subdir in ['incoming', 'processing', 'outgoing']:
        queue_dir = config.queue_path / subdir
        if queue_dir.exists():
            count = len(list(queue_dir.glob("*.json")))
            for file in queue_dir.glob("*.json"):
                file.unlink()
            logger.info(f"  ✓ Cleared {count} files from {subdir}/")

    # Clear conversations
    logger.info("Clearing conversations...")
    conversations_dir = config.queue_path / "conversations"
    if conversations_dir.exists():
        count = len(list(conversations_dir.glob("*.json")))
        for file in conversations_dir.glob("*.json"):
            file.unlink()
        logger.info(f"  ✓ Cleared {count} conversations")

    # Clear chats
    logger.info("Clearing chat history...")
    chats_dir = config.queue_path / "chats"
    if chats_dir.exists():
        shutil.rmtree(chats_dir)
        logger.info(f"  ✓ Cleared chat history")

    # Clear workspaces
    logger.info("Clearing agent workspaces...")
    if config.workspace_path.exists():
        count = len(list(config.workspace_path.iterdir()))
        shutil.rmtree(config.workspace_path)
        logger.info(f"  ✓ Cleared {count} agent workspaces")

    logger.info("✅ All data cleared!")


def cmd_status(args):
    """Show system status"""
    from agency.config import load_config
    from agency.core.queue import FileQueue
    from agency.core.conversation import ConversationManager

    # Load configuration
    config = load_config(config_path=args.config)

    # Create queue and conversation manager
    queue = FileQueue(config.queue_path)
    conv_manager = ConversationManager(config.queue_path / "conversations")

    # Get queue sizes
    incoming = queue.get_queue_size("incoming")
    processing = queue.get_queue_size("processing")
    outgoing = queue.get_queue_size("outgoing")

    # Get conversation count
    active_conversations = len(conv_manager.conversations)

    # Print status
    print("\n" + "=" * 60)
    print("📊 AGENCY SYSTEM STATUS")
    print("=" * 60)

    print("\n📦 Queue Status:")
    print(f"  Incoming:   {incoming} messages")
    print(f"  Processing: {processing} messages")
    print(f"  Outgoing:   {outgoing} messages")

    print("\n💬 Conversations:")
    print(f"  Active: {active_conversations}")

    print("\n🤖 Configured Agents:")
    for agent_id, agent_config in config.agents.items():
        print(f"  @{agent_id:<15} - {agent_config.name}")

    print("\n👥 Configured Teams:")
    for team_id, team_config in config.teams.items():
        members = ", ".join(f"@{a}" for a in team_config.agents)
        print(f"  @{team_id:<15} - {team_config.name}")
        print(f"    {' ' * 17} Members: {members}")

    print("\n📍 Paths:")
    print(f"  Workspace: {config.workspace_path}")
    print(f"  Queue:     {config.queue_path}")

    print("=" * 60 + "\n")


def cmd_init(args):
    """Initialize workspace and create example config"""
    from agency.config import load_config
    import shutil

    logger.info("🔧 Initializing Agency workspace...")

    # Default workspace
    workspace = args.workspace or Path.home() / "agency-workspace"

    # Load/create configuration (this will create directories)
    config = load_config(workspace_path=workspace)

    # Copy example config if it doesn't exist
    user_config_path = Path.cwd() / "agents.json"
    if not user_config_path.exists():
        template_path = Path(__file__).parent / "templates" / "agents.json"
        if template_path.exists():
            shutil.copy(template_path, user_config_path)
            logger.info(f"✅ Created config file: {user_config_path}")
        else:
            logger.warning("⚠️  Template config not found")

    # Create .env template if it doesn't exist
    env_path = Path.cwd() / ".env.example"
    if not env_path.exists():
        env_content = """# Agency Configuration

# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here
TELEGRAM_BOT_TOKEN=123456:ABC-your-token

# Optional
TELEGRAM_ALLOWED_USERS=user1,user2  # Comma-separated user IDs
OPENAI_API_KEY=sk-...               # For OpenAI models

# External Service Integrations (see QUICK_INTEGRATION_GUIDE.md)
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_BEARER_TOKEN=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...

LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
LINKEDIN_ACCESS_TOKEN=...

GITHUB_TOKEN=ghp_...
GITHUB_USERNAME=...

GOOGLE_OAUTH_CREDENTIALS_FILE=/path/to/google_oauth_credentials.json
GOOGLE_TOKEN_FILE=/path/to/google_token.pickle
"""
        env_path.write_text(env_content)
        logger.info(f"✅ Created .env template: {env_path}")

    logger.info(f"\n✅ Workspace initialized!")
    logger.info(f"\n📍 Paths:")
    logger.info(f"  Workspace: {config.workspace_path}")
    logger.info(f"  Queue:     {config.queue_path}")
    logger.info(f"  Config:    {user_config_path if user_config_path.exists() else 'using default'}")

    logger.info(f"\n📝 Next steps:")
    logger.info(f"  1. Edit .env.example and rename to .env")
    logger.info(f"  2. Set ANTHROPIC_API_KEY and TELEGRAM_BOT_TOKEN")
    logger.info(f"  3. Run: python -m agency start")


if __name__ == '__main__':
    main()
