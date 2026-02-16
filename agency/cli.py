#!/usr/bin/env python3
"""
Agency CLI - Command-line interface for the Agency multi-agent system.

Inspired by tinyclaw: https://github.com/jlia0/tinyclaw
"""

import argparse
import sys
import os
import json
import logging
from pathlib import Path
from typing import Optional, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class AgencyCLI:
    """Main CLI handler for Agency"""

    def __init__(self):
        self.base_dir = Path.home() / ".agency"
        self.workspace_dir = Path.home() / "agency-workspace"
        self.config_file = self.base_dir / "config.json"

    def run(self, args: List[str] = None):
        """Run the CLI with given arguments"""
        parser = argparse.ArgumentParser(
            prog='agency',
            description='Agency - Multi-agent AI system',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  agency start              Start the full system
  agency agent list         List all agents
  agency team info cc_team  Show team details
  agency send "Hello" cc    Send message to CC agent

For more help: agency <command> --help
"""
        )

        subparsers = parser.add_subparsers(dest='command', help='Command to run')

        # Core commands
        self._add_core_commands(subparsers)

        # Agent commands
        self._add_agent_commands(subparsers)

        # Team commands
        self._add_team_commands(subparsers)

        # Configuration commands
        self._add_config_commands(subparsers)

        # Pairing commands
        self._add_pairing_commands(subparsers)

        # Update commands
        self._add_update_commands(subparsers)

        # Messaging commands
        self._add_messaging_commands(subparsers)

        # Debug commands
        self._add_debug_commands(subparsers)

        # Parse arguments
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            parser.print_help()
            return 0

        # Route to appropriate handler
        try:
            return self._execute_command(parsed_args)
        except Exception as e:
            logger.error(f"Error: {e}")
            return 1

    def _add_core_commands(self, subparsers):
        """Add core system commands"""
        # Start
        start_parser = subparsers.add_parser(
            'start',
            help='Start the Agency system (processor + channels)'
        )
        start_parser.add_argument(
            '--processor-only',
            action='store_true',
            help='Start only the message processor'
        )
        start_parser.add_argument(
            '--telegram-only',
            action='store_true',
            help='Start only the Telegram channel'
        )
        start_parser.add_argument(
            '--detach',
            action='store_true',
            help='Run in background'
        )

        # Stop
        stop_parser = subparsers.add_parser(
            'stop',
            help='Stop the Agency system'
        )

        # Status
        status_parser = subparsers.add_parser(
            'status',
            help='Show system status'
        )
        status_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Logs
        logs_parser = subparsers.add_parser(
            'logs',
            help='View system logs'
        )
        logs_parser.add_argument(
            '--follow',
            '-f',
            action='store_true',
            help='Follow log output'
        )
        logs_parser.add_argument(
            '--lines',
            '-n',
            type=int,
            default=50,
            help='Number of lines to show (default: 50)'
        )

        # Version
        version_parser = subparsers.add_parser(
            'version',
            help='Show version information'
        )

        # Init
        init_parser = subparsers.add_parser(
            'init',
            help='Initialize Agency workspace'
        )
        init_parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing configuration'
        )

    def _add_agent_commands(self, subparsers):
        """Add agent management commands"""
        agent_parser = subparsers.add_parser(
            'agent',
            help='Manage agents'
        )
        agent_subparsers = agent_parser.add_subparsers(dest='agent_command')

        # List agents
        list_parser = agent_subparsers.add_parser(
            'list',
            help='List all agents'
        )
        list_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Agent info
        info_parser = agent_subparsers.add_parser(
            'info',
            help='Show agent details'
        )
        info_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )
        info_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Create agent
        create_parser = agent_subparsers.add_parser(
            'create',
            help='Create a new agent'
        )
        create_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )
        create_parser.add_argument(
            '--name',
            required=True,
            help='Agent name'
        )
        create_parser.add_argument(
            '--model',
            choices=['opus', 'sonnet', 'haiku'],
            default='sonnet',
            help='Model to use'
        )
        create_parser.add_argument(
            '--personality',
            help='Agent personality/system prompt'
        )

        # Delete agent
        delete_parser = agent_subparsers.add_parser(
            'delete',
            help='Delete an agent'
        )
        delete_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )
        delete_parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation'
        )

        # Enable/disable agent
        enable_parser = agent_subparsers.add_parser(
            'enable',
            help='Enable an agent'
        )
        enable_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )

        disable_parser = agent_subparsers.add_parser(
            'disable',
            help='Disable an agent'
        )
        disable_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )

    def _add_team_commands(self, subparsers):
        """Add team management commands"""
        team_parser = subparsers.add_parser(
            'team',
            help='Manage teams'
        )
        team_subparsers = team_parser.add_subparsers(dest='team_command')

        # List teams
        list_parser = team_subparsers.add_parser(
            'list',
            help='List all teams'
        )
        list_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Team info
        info_parser = team_subparsers.add_parser(
            'info',
            help='Show team details'
        )
        info_parser.add_argument(
            'team_id',
            help='Team ID'
        )
        info_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Create team
        create_parser = team_subparsers.add_parser(
            'create',
            help='Create a new team'
        )
        create_parser.add_argument(
            'team_id',
            help='Team ID'
        )
        create_parser.add_argument(
            '--name',
            required=True,
            help='Team name'
        )
        create_parser.add_argument(
            '--leader',
            required=True,
            help='Leader agent ID'
        )
        create_parser.add_argument(
            '--agents',
            nargs='+',
            help='Agent IDs (space-separated)'
        )

        # Delete team
        delete_parser = team_subparsers.add_parser(
            'delete',
            help='Delete a team'
        )
        delete_parser.add_argument(
            'team_id',
            help='Team ID'
        )

        # Add agent to team
        add_parser = team_subparsers.add_parser(
            'add-agent',
            help='Add agent to team'
        )
        add_parser.add_argument(
            'team_id',
            help='Team ID'
        )
        add_parser.add_argument(
            'agent_id',
            help='Agent ID to add'
        )

        # Remove agent from team
        remove_parser = team_subparsers.add_parser(
            'remove-agent',
            help='Remove agent from team'
        )
        remove_parser.add_argument(
            'team_id',
            help='Team ID'
        )
        remove_parser.add_argument(
            'agent_id',
            help='Agent ID to remove'
        )

    def _add_config_commands(self, subparsers):
        """Add configuration commands"""
        config_parser = subparsers.add_parser(
            'config',
            help='Manage configuration'
        )
        config_subparsers = config_parser.add_subparsers(dest='config_command')

        # Get config value
        get_parser = config_subparsers.add_parser(
            'get',
            help='Get configuration value'
        )
        get_parser.add_argument(
            'key',
            help='Configuration key (e.g., telegram.bot_token)'
        )

        # Set config value
        set_parser = config_subparsers.add_parser(
            'set',
            help='Set configuration value'
        )
        set_parser.add_argument(
            'key',
            help='Configuration key'
        )
        set_parser.add_argument(
            'value',
            help='Configuration value'
        )

        # Show all config
        show_parser = config_subparsers.add_parser(
            'show',
            help='Show all configuration'
        )
        show_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

        # Reset config
        reset_parser = config_subparsers.add_parser(
            'reset',
            help='Reset configuration to defaults'
        )
        reset_parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation'
        )

    def _add_pairing_commands(self, subparsers):
        """Add pairing commands for connecting channels"""
        pair_parser = subparsers.add_parser(
            'pair',
            help='Pair a channel (Telegram, WhatsApp, etc.)'
        )
        pair_parser.add_argument(
            'channel',
            choices=['telegram', 'whatsapp', 'slack'],
            help='Channel to pair'
        )
        pair_parser.add_argument(
            '--token',
            help='Bot token or credentials'
        )

        unpair_parser = subparsers.add_parser(
            'unpair',
            help='Unpair a channel'
        )
        unpair_parser.add_argument(
            'channel',
            help='Channel to unpair'
        )

        list_pairings_parser = subparsers.add_parser(
            'list-pairings',
            help='List all paired channels'
        )
        list_pairings_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

    def _add_update_commands(self, subparsers):
        """Add update commands"""
        update_parser = subparsers.add_parser(
            'update',
            help='Update Agency to latest version'
        )
        update_parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only check for updates, don\'t install'
        )
        update_parser.add_argument(
            '--version',
            help='Update to specific version'
        )

        check_updates_parser = subparsers.add_parser(
            'check-updates',
            help='Check for available updates'
        )

    def _add_debug_commands(self, subparsers):
        """Add debugging and visualization commands"""
        # Debug command
        debug_parser = subparsers.add_parser(
            'debug',
            help='Debug and visualize system state'
        )
        debug_subparsers = debug_parser.add_subparsers(dest='debug_command')

        # Visualize message flow
        visualize_parser = debug_subparsers.add_parser(
            'visualize',
            help='Visualize message flow and queue state'
        )

        # Check connectivity
        check_parser = debug_subparsers.add_parser(
            'check',
            help='Check system connectivity and configuration'
        )

        # Trace message
        trace_parser = debug_subparsers.add_parser(
            'trace',
            help='Trace a specific message through the system'
        )
        trace_parser.add_argument(
            'message_id',
            help='Message ID to trace'
        )

        # Test agent
        test_parser = debug_subparsers.add_parser(
            'test',
            help='Test agent invocation end-to-end'
        )
        test_parser.add_argument(
            'agent_id',
            help='Agent ID to test'
        )
        test_parser.add_argument(
            '--message',
            default='Hello, please respond with a brief status update.',
            help='Test message to send'
        )

    def _add_messaging_commands(self, subparsers):
        """Add messaging commands"""
        # Send message
        send_parser = subparsers.add_parser(
            'send',
            help='Send message to an agent'
        )
        send_parser.add_argument(
            'message',
            help='Message to send'
        )
        send_parser.add_argument(
            'agent_id',
            help='Agent ID to send to'
        )
        send_parser.add_argument(
            '--user',
            default='cli',
            help='User ID (default: cli)'
        )

        # Broadcast
        broadcast_parser = subparsers.add_parser(
            'broadcast',
            help='Broadcast message to multiple agents'
        )
        broadcast_parser.add_argument(
            'message',
            help='Message to broadcast'
        )
        broadcast_parser.add_argument(
            '--agents',
            nargs='+',
            help='Agent IDs (space-separated)'
        )
        broadcast_parser.add_argument(
            '--team',
            help='Team ID to broadcast to'
        )

        # History
        history_parser = subparsers.add_parser(
            'history',
            help='View conversation history'
        )
        history_parser.add_argument(
            'agent_id',
            help='Agent ID'
        )
        history_parser.add_argument(
            '--user',
            default='cli',
            help='User ID (default: cli)'
        )
        history_parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Number of messages (default: 10)'
        )
        history_parser.add_argument(
            '--json',
            action='store_true',
            help='Output as JSON'
        )

    def _execute_command(self, args):
        """Execute the parsed command"""
        # Import command handlers
        from agency.cli_commands import (
            CoreCommands,
            AgentCommands,
            TeamCommands,
            ConfigCommands,
            PairingCommands,
            UpdateCommands,
            MessagingCommands,
            DebugCommands
        )

        # Route to appropriate handler
        if args.command == 'start':
            return CoreCommands().start(args)
        elif args.command == 'stop':
            return CoreCommands().stop(args)
        elif args.command == 'status':
            return CoreCommands().status(args)
        elif args.command == 'logs':
            return CoreCommands().logs(args)
        elif args.command == 'version':
            return CoreCommands().version(args)
        elif args.command == 'init':
            return CoreCommands().init(args)

        elif args.command == 'agent':
            return AgentCommands().handle(args)
        elif args.command == 'team':
            return TeamCommands().handle(args)
        elif args.command == 'config':
            return ConfigCommands().handle(args)

        elif args.command == 'pair':
            return PairingCommands().pair(args)
        elif args.command == 'unpair':
            return PairingCommands().unpair(args)
        elif args.command == 'list-pairings':
            return PairingCommands().list_pairings(args)

        elif args.command == 'update':
            return UpdateCommands().update(args)
        elif args.command == 'check-updates':
            return UpdateCommands().check_updates(args)

        elif args.command == 'send':
            return MessagingCommands().send(args)
        elif args.command == 'broadcast':
            return MessagingCommands().broadcast(args)
        elif args.command == 'history':
            return MessagingCommands().history(args)

        elif args.command == 'debug':
            debug_cmd = DebugCommands()
            if args.debug_command == 'visualize':
                return debug_cmd.visualize(args)
            elif args.debug_command == 'check':
                return debug_cmd.check(args)
            elif args.debug_command == 'test':
                return debug_cmd.test(args)
            else:
                logger.error(f"Unknown debug command: {args.debug_command}")
                return 1

        else:
            logger.error(f"Unknown command: {args.command}")
            return 1


def main():
    """Main entry point"""
    cli = AgencyCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
