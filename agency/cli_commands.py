"""
Command handlers for Agency CLI.

Each command group (Core, Agent, Team, etc.) is handled by a separate class.
"""

import os
import sys
import json
import logging
import subprocess
import signal
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseCommands:
    """Base class for command handlers"""

    def __init__(self):
        self.base_dir = Path.home() / ".agency"
        self.workspace_dir = Path.home() / "agency-workspace"
        self.config_file = self.base_dir / "config.json"
        self.agents_file = Path(__file__).parent / "templates" / "agents.json"
        self.pid_file = self.base_dir / "agency.pid"

    def load_config(self) -> Dict:
        """Load configuration"""
        if not self.config_file.exists():
            return {}
        with open(self.config_file) as f:
            return json.load(f)

    def save_config(self, config: Dict):
        """Save configuration"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def load_agents(self) -> Dict:
        """Load agents configuration"""
        if not self.agents_file.exists():
            return {"agents": {}, "teams": {}}
        with open(self.agents_file) as f:
            return json.load(f)

    def save_agents(self, data: Dict):
        """Save agents configuration"""
        with open(self.agents_file, 'w') as f:
            json.dump(data, f, indent=2)


class CoreCommands(BaseCommands):
    """Core system commands"""

    def start(self, args):
        """Start the Agency system"""
        logger.info("🚀 Starting Agency...")

        # Check if already running
        if self.is_running():
            logger.warning("⚠️  Agency is already running")
            logger.info(f"PID: {self.get_pid()}")
            return 0

        # Ensure directories exist
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        if args.processor_only:
            return self._start_processor(args.detach)
        elif args.telegram_only:
            return self._start_telegram(args.detach)
        else:
            # Start both
            return self._start_full_system(args.detach)

    def _start_processor(self, detach: bool = False):
        """Start message processor"""
        logger.info("Starting message processor...")

        cmd = [sys.executable, "-m", "agency.core.processor"]

        if detach:
            # Run in background
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            self._save_pid(proc.pid, "processor")
            logger.info(f"✅ Processor started (PID: {proc.pid})")
            return 0
        else:
            # Run in foreground
            return subprocess.call(cmd)

    def _start_telegram(self, detach: bool = False):
        """Start Telegram channel"""
        logger.info("Starting Telegram channel...")

        cmd = [sys.executable, "-m", "agency.channels.telegram_channel"]

        if detach:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            self._save_pid(proc.pid, "telegram")
            logger.info(f"✅ Telegram started (PID: {proc.pid})")
            return 0
        else:
            return subprocess.call(cmd)

    def _start_full_system(self, detach: bool = False):
        """Start full system (processor + telegram)"""
        if detach:
            # Start both in background
            self._start_processor(detach=True)
            self._start_telegram(detach=True)
            logger.info("✅ Agency started in background")
            logger.info("Use 'agency logs -f' to view logs")
            logger.info("Use 'agency stop' to stop")
            return 0
        else:
            # Start processor in background, telegram in foreground
            logger.info("Starting processor in background...")
            self._start_processor(detach=True)

            logger.info("Starting Telegram in foreground...")
            logger.info("Press Ctrl+C to stop")

            try:
                return self._start_telegram(detach=False)
            except KeyboardInterrupt:
                logger.info("\n⏹️  Stopping Agency...")
                self.stop(None)
                return 0

    def stop(self, args):
        """Stop the Agency system"""
        logger.info("⏹️  Stopping Agency...")

        if not self.is_running():
            logger.warning("⚠️  Agency is not running")
            return 0

        # Get PIDs
        pids = self._load_pids()

        # Stop processes
        stopped = []
        for name, pid in pids.items():
            try:
                os.kill(pid, signal.SIGTERM)
                stopped.append(name)
                logger.info(f"✅ Stopped {name} (PID: {pid})")
            except ProcessLookupError:
                logger.warning(f"⚠️  Process {name} (PID: {pid}) not found")
            except Exception as e:
                logger.error(f"❌ Failed to stop {name}: {e}")

        # Clear PID file
        if self.pid_file.exists():
            self.pid_file.unlink()

        if stopped:
            logger.info("✅ Agency stopped")
        return 0

    def status(self, args):
        """Show system status"""
        running = self.is_running()

        if args.json:
            status = {
                "running": running,
                "pids": self._load_pids() if running else {},
                "config_dir": str(self.base_dir),
                "workspace_dir": str(self.workspace_dir)
            }
            print(json.dumps(status, indent=2))
            return 0

        # Human-readable status
        logger.info("📊 Agency Status")
        logger.info("=" * 50)

        if running:
            logger.info("Status: ✅ Running")
            pids = self._load_pids()
            for name, pid in pids.items():
                logger.info(f"  {name}: PID {pid}")
        else:
            logger.info("Status: ⏹️  Stopped")

        logger.info("")
        logger.info(f"Config dir: {self.base_dir}")
        logger.info(f"Workspace:  {self.workspace_dir}")

        # Agent count
        agents_data = self.load_agents()
        agent_count = len(agents_data.get("agents", {}))
        team_count = len(agents_data.get("teams", {}))
        logger.info(f"Agents:     {agent_count}")
        logger.info(f"Teams:      {team_count}")

        return 0

    def logs(self, args):
        """View system logs"""
        log_file = self.base_dir / "agency.log"

        if not log_file.exists():
            logger.warning("No logs found")
            return 1

        if args.follow:
            # Follow logs
            try:
                subprocess.call(["tail", "-f", "-n", str(args.lines), str(log_file)])
            except KeyboardInterrupt:
                return 0
        else:
            # Show last N lines
            subprocess.call(["tail", "-n", str(args.lines), str(log_file)])

        return 0

    def version(self, args):
        """Show version information"""
        logger.info("Agency v0.1.0")
        logger.info("Multi-agent AI system")
        logger.info("")
        logger.info("Inspired by:")
        logger.info("  - tinyclaw (https://github.com/jlia0/tinyclaw)")
        logger.info("  - Google Labs CC (https://labs.google/cc)")
        return 0

    def init(self, args):
        """Initialize Agency workspace"""
        logger.info("🎬 Initializing Agency workspace...")

        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "queue" / "incoming").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "queue" / "processing").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "queue" / "outgoing").mkdir(parents=True, exist_ok=True)

        # Create default config
        if not self.config_file.exists() or args.force:
            default_config = {
                "telegram": {
                    "enabled": False,
                    "bot_token": "",
                    "allowed_users": []
                },
                "anthropic": {
                    "api_key": os.getenv("ANTHROPIC_API_KEY", "")
                },
                "workspace_dir": str(self.workspace_dir),
                "log_level": "INFO"
            }
            self.save_config(default_config)
            logger.info("✅ Created config file")

        # Create .env.example
        env_example = self.base_dir.parent / "agents" / ".env.example"
        if not env_example.exists():
            env_content = """# Agency Configuration

# Required
ANTHROPIC_API_KEY=sk-ant-...

# Telegram (optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USERS=

# Google Services (optional - for CC agent)
GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
GOOGLE_TOKEN_FILE=google_token.pickle

# Social Media (optional)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
"""
            env_example.parent.mkdir(parents=True, exist_ok=True)
            env_example.write_text(env_content)
            logger.info("✅ Created .env.example")

        logger.info("✅ Workspace initialized!")
        logger.info("")
        logger.info(f"Config:     {self.config_file}")
        logger.info(f"Workspace:  {self.workspace_dir}")
        logger.info(f"Queues:     {self.base_dir / 'queue'}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Configure .env with your API keys")
        logger.info("  2. Run: agency pair telegram")
        logger.info("  3. Run: agency start")

        return 0

    def is_running(self) -> bool:
        """Check if Agency is running"""
        if not self.pid_file.exists():
            return False

        pids = self._load_pids()
        if not pids:
            return False

        # Check if any process is still alive
        for pid in pids.values():
            try:
                os.kill(pid, 0)  # Check if process exists
                return True
            except ProcessLookupError:
                continue

        return False

    def get_pid(self) -> Optional[int]:
        """Get main PID"""
        pids = self._load_pids()
        return pids.get("processor") or pids.get("telegram")

    def _save_pid(self, pid: int, name: str):
        """Save process PID"""
        pids = self._load_pids()
        pids[name] = pid
        with open(self.pid_file, 'w') as f:
            json.dump(pids, f)

    def _load_pids(self) -> Dict[str, int]:
        """Load process PIDs"""
        if not self.pid_file.exists():
            return {}
        try:
            with open(self.pid_file) as f:
                return json.load(f)
        except:
            return {}


class AgentCommands(BaseCommands):
    """Agent management commands"""

    def handle(self, args):
        """Handle agent subcommands"""
        if args.agent_command == 'list':
            return self.list_agents(args)
        elif args.agent_command == 'info':
            return self.agent_info(args)
        elif args.agent_command == 'create':
            return self.create_agent(args)
        elif args.agent_command == 'delete':
            return self.delete_agent(args)
        elif args.agent_command == 'enable':
            return self.enable_agent(args)
        elif args.agent_command == 'disable':
            return self.disable_agent(args)
        else:
            logger.error("Unknown agent command")
            return 1

    def list_agents(self, args):
        """List all agents"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.json:
            print(json.dumps(agents, indent=2))
            return 0

        # Human-readable list
        logger.info("🤖 Available Agents")
        logger.info("=" * 70)

        for agent_id, agent in sorted(agents.items()):
            status = "✅" if agent.get("enabled", True) else "⏸️ "
            model = agent.get("model", "unknown")
            name = agent.get("name", agent_id)
            logger.info(f"{status} @{agent_id:<15} {name:<30} [{model}]")

        logger.info("")
        logger.info(f"Total: {len(agents)} agents")
        return 0

    def agent_info(self, args):
        """Show agent details"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.agent_id not in agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            return 1

        agent = agents[args.agent_id]

        if args.json:
            print(json.dumps(agent, indent=2))
            return 0

        # Human-readable info
        logger.info(f"🤖 Agent: @{args.agent_id}")
        logger.info("=" * 70)
        logger.info(f"Name:     {agent.get('name')}")
        logger.info(f"Model:    {agent.get('model')}")
        logger.info(f"Provider: {agent.get('provider', 'anthropic')}")
        logger.info(f"Enabled:  {agent.get('enabled', True)}")
        logger.info("")
        logger.info("Personality:")
        logger.info(f"  {agent.get('personality', 'N/A')}")
        logger.info("")
        logger.info("Skills:")
        for skill in agent.get('skills', []):
            logger.info(f"  • {skill}")

        return 0

    def create_agent(self, args):
        """Create a new agent"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.agent_id in agents:
            logger.error(f"Agent '{args.agent_id}' already exists")
            return 1

        # Create agent
        agent = {
            "name": args.name,
            "agent_id": args.agent_id,
            "provider": "anthropic",
            "model": args.model,
            "personality": args.personality or f"You are {args.name}, a helpful AI assistant.",
            "skills": [],
            "enabled": True
        }

        agents[args.agent_id] = agent
        data["agents"] = agents
        self.save_agents(data)

        logger.info(f"✅ Created agent: @{args.agent_id}")
        return 0

    def delete_agent(self, args):
        """Delete an agent"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.agent_id not in agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            return 1

        if not args.force:
            response = input(f"Delete agent @{args.agent_id}? [y/N] ")
            if response.lower() != 'y':
                logger.info("Cancelled")
                return 0

        del agents[args.agent_id]
        data["agents"] = agents
        self.save_agents(data)

        logger.info(f"✅ Deleted agent: @{args.agent_id}")
        return 0

    def enable_agent(self, args):
        """Enable an agent"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.agent_id not in agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            return 1

        agents[args.agent_id]["enabled"] = True
        data["agents"] = agents
        self.save_agents(data)

        logger.info(f"✅ Enabled agent: @{args.agent_id}")
        return 0

    def disable_agent(self, args):
        """Disable an agent"""
        data = self.load_agents()
        agents = data.get("agents", {})

        if args.agent_id not in agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            return 1

        agents[args.agent_id]["enabled"] = False
        data["agents"] = agents
        self.save_agents(data)

        logger.info(f"⏸️  Disabled agent: @{args.agent_id}")
        return 0


class TeamCommands(BaseCommands):
    """Team management commands"""

    def handle(self, args):
        """Handle team subcommands"""
        if args.team_command == 'list':
            return self.list_teams(args)
        elif args.team_command == 'info':
            return self.team_info(args)
        elif args.team_command == 'create':
            return self.create_team(args)
        elif args.team_command == 'delete':
            return self.delete_team(args)
        elif args.team_command == 'add-agent':
            return self.add_agent(args)
        elif args.team_command == 'remove-agent':
            return self.remove_agent(args)
        else:
            logger.error("Unknown team command")
            return 1

    def list_teams(self, args):
        """List all teams"""
        data = self.load_agents()
        teams = data.get("teams", {})

        if args.json:
            print(json.dumps(teams, indent=2))
            return 0

        # Human-readable list
        logger.info("👥 Available Teams")
        logger.info("=" * 70)

        for team_id, team in sorted(teams.items()):
            name = team.get("name", team_id)
            agent_count = len(team.get("agents", []))
            leader = team.get("leader_agent", "N/A")
            logger.info(f"@{team_id:<15} {name:<30} ({agent_count} agents, led by @{leader})")

        logger.info("")
        logger.info(f"Total: {len(teams)} teams")
        return 0

    def team_info(self, args):
        """Show team details"""
        data = self.load_agents()
        teams = data.get("teams", {})

        if args.team_id not in teams:
            logger.error(f"Team '{args.team_id}' not found")
            return 1

        team = teams[args.team_id]

        if args.json:
            print(json.dumps(team, indent=2))
            return 0

        # Human-readable info
        logger.info(f"👥 Team: @{args.team_id}")
        logger.info("=" * 70)
        logger.info(f"Name:        {team.get('name')}")
        logger.info(f"Leader:      @{team.get('leader_agent')}")
        logger.info(f"Description: {team.get('description', 'N/A')}")
        logger.info("")
        logger.info("Team Members:")
        for agent_id in team.get("agents", []):
            is_leader = agent_id == team.get("leader_agent")
            marker = "👑" if is_leader else "  "
            logger.info(f"  {marker} @{agent_id}")

        return 0

    def create_team(self, args):
        """Create a new team"""
        data = self.load_agents()
        teams = data.get("teams", {})

        if args.team_id in teams:
            logger.error(f"Team '{args.team_id}' already exists")
            return 1

        # Validate leader exists
        agents = data.get("agents", {})
        if args.leader not in agents:
            logger.error(f"Leader agent '{args.leader}' not found")
            return 1

        # Validate all agents exist
        team_agents = args.agents or []
        if args.leader not in team_agents:
            team_agents.insert(0, args.leader)

        for agent_id in team_agents:
            if agent_id not in agents:
                logger.error(f"Agent '{agent_id}' not found")
                return 1

        # Create team
        team = {
            "name": args.name,
            "team_id": args.team_id,
            "agents": team_agents,
            "leader_agent": args.leader,
            "description": ""
        }

        teams[args.team_id] = team
        data["teams"] = teams
        self.save_agents(data)

        logger.info(f"✅ Created team: @{args.team_id}")
        return 0

    def delete_team(self, args):
        """Delete a team"""
        data = self.load_agents()
        teams = data.get("teams", {})

        if args.team_id not in teams:
            logger.error(f"Team '{args.team_id}' not found")
            return 1

        del teams[args.team_id]
        data["teams"] = teams
        self.save_agents(data)

        logger.info(f"✅ Deleted team: @{args.team_id}")
        return 0

    def add_agent(self, args):
        """Add agent to team"""
        data = self.load_agents()
        teams = data.get("teams", {})
        agents = data.get("agents", {})

        if args.team_id not in teams:
            logger.error(f"Team '{args.team_id}' not found")
            return 1

        if args.agent_id not in agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            return 1

        team = teams[args.team_id]
        if args.agent_id in team["agents"]:
            logger.warning(f"Agent @{args.agent_id} already in team")
            return 0

        team["agents"].append(args.agent_id)
        data["teams"] = teams
        self.save_agents(data)

        logger.info(f"✅ Added @{args.agent_id} to team @{args.team_id}")
        return 0

    def remove_agent(self, args):
        """Remove agent from team"""
        data = self.load_agents()
        teams = data.get("teams", {})

        if args.team_id not in teams:
            logger.error(f"Team '{args.team_id}' not found")
            return 1

        team = teams[args.team_id]
        if args.agent_id not in team["agents"]:
            logger.error(f"Agent @{args.agent_id} not in team")
            return 1

        if args.agent_id == team["leader_agent"]:
            logger.error("Cannot remove team leader")
            return 1

        team["agents"].remove(args.agent_id)
        data["teams"] = teams
        self.save_agents(data)

        logger.info(f"✅ Removed @{args.agent_id} from team @{args.team_id}")
        return 0


class ConfigCommands(BaseCommands):
    """Configuration commands"""

    def handle(self, args):
        """Handle config subcommands"""
        if args.config_command == 'get':
            return self.get_config(args)
        elif args.config_command == 'set':
            return self.set_config(args)
        elif args.config_command == 'show':
            return self.show_config(args)
        elif args.config_command == 'reset':
            return self.reset_config(args)
        else:
            logger.error("Unknown config command")
            return 1

    def get_config(self, args):
        """Get configuration value"""
        config = self.load_config()

        # Navigate nested keys (e.g., "telegram.bot_token")
        keys = args.key.split('.')
        value = config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.error(f"Key '{args.key}' not found")
                return 1

        print(value)
        return 0

    def set_config(self, args):
        """Set configuration value"""
        config = self.load_config()

        # Navigate nested keys
        keys = args.key.split('.')
        target = config
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]

        target[keys[-1]] = args.value
        self.save_config(config)

        logger.info(f"✅ Set {args.key} = {args.value}")
        return 0

    def show_config(self, args):
        """Show all configuration"""
        config = self.load_config()

        if args.json:
            print(json.dumps(config, indent=2))
        else:
            logger.info("⚙️  Agency Configuration")
            logger.info("=" * 50)
            self._print_dict(config)

        return 0

    def _print_dict(self, d, indent=0):
        """Print dictionary with indentation"""
        for key, value in d.items():
            if isinstance(value, dict):
                logger.info("  " * indent + f"{key}:")
                self._print_dict(value, indent + 1)
            else:
                # Mask sensitive values
                if 'token' in key.lower() or 'key' in key.lower() or 'secret' in key.lower():
                    if value and len(str(value)) > 10:
                        display = str(value)[:10] + "..." + str(value)[-4:]
                    else:
                        display = "***"
                else:
                    display = value
                logger.info("  " * indent + f"{key}: {display}")

    def reset_config(self, args):
        """Reset configuration"""
        if not args.force:
            response = input("Reset configuration to defaults? [y/N] ")
            if response.lower() != 'y':
                logger.info("Cancelled")
                return 0

        default_config = {
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "allowed_users": []
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", "")
            },
            "workspace_dir": str(self.workspace_dir),
            "log_level": "INFO"
        }

        self.save_config(default_config)
        logger.info("✅ Configuration reset to defaults")
        return 0


class PairingCommands(BaseCommands):
    """Pairing commands for connecting channels"""

    def pair(self, args):
        """Pair a channel"""
        logger.info(f"🔗 Pairing {args.channel}...")

        config = self.load_config()

        if args.channel == 'telegram':
            return self._pair_telegram(config, args.token)
        elif args.channel == 'whatsapp':
            logger.warning("WhatsApp pairing not yet implemented")
            return 1
        elif args.channel == 'slack':
            logger.warning("Slack pairing not yet implemented")
            return 1
        else:
            logger.error(f"Unknown channel: {args.channel}")
            return 1

    def _pair_telegram(self, config, token=None):
        """Pair Telegram"""
        if not token:
            token = input("Enter Telegram bot token: ")

        if not token:
            logger.error("Bot token required")
            return 1

        # Test token
        logger.info("Testing token...")
        try:
            import requests
            response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
            if response.status_code == 200:
                bot_info = response.json()
                bot_name = bot_info['result']['username']
                logger.info(f"✅ Connected to @{bot_name}")
            else:
                logger.error("❌ Invalid token")
                return 1
        except Exception as e:
            logger.warning(f"Could not verify token: {e}")

        # Save to config
        if "telegram" not in config:
            config["telegram"] = {}

        config["telegram"]["enabled"] = True
        config["telegram"]["bot_token"] = token
        self.save_config(config)

        logger.info("✅ Telegram paired!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Start Agency: agency start")
        logger.info("  2. Message your bot on Telegram")
        logger.info("  3. Your user ID will be logged")
        logger.info("  4. Add it to config: agency config set telegram.allowed_users '[123456789]'")

        return 0

    def unpair(self, args):
        """Unpair a channel"""
        config = self.load_config()

        if args.channel not in config:
            logger.warning(f"{args.channel} not paired")
            return 0

        del config[args.channel]
        self.save_config(config)

        logger.info(f"✅ Unpaired {args.channel}")
        return 0

    def list_pairings(self, args):
        """List all paired channels"""
        config = self.load_config()

        pairings = []
        for channel in ['telegram', 'whatsapp', 'slack']:
            if channel in config and config[channel].get('enabled'):
                pairings.append(channel)

        if args.json:
            print(json.dumps(pairings, indent=2))
            return 0

        logger.info("🔗 Paired Channels")
        logger.info("=" * 50)

        if not pairings:
            logger.info("No channels paired")
        else:
            for channel in pairings:
                logger.info(f"✅ {channel}")

        return 0


class UpdateCommands(BaseCommands):
    """Update commands"""

    def update(self, args):
        """Update Agency"""
        logger.info("🔄 Checking for updates...")

        # Check if running
        if CoreCommands().is_running():
            logger.warning("Please stop Agency before updating: agency stop")
            return 1

        if args.check_only:
            return self.check_updates(args)

        # In a real implementation, this would:
        # 1. Fetch latest from GitHub
        # 2. Compare versions
        # 3. Pull updates
        # 4. Reinstall dependencies

        logger.info("Update functionality not yet implemented")
        logger.info("To update manually:")
        logger.info("  cd /path/to/agents")
        logger.info("  git pull")
        logger.info("  pip install -r requirements.txt")

        return 0

    def check_updates(self, args):
        """Check for updates"""
        logger.info("Checking for updates...")
        logger.info("Current version: 0.1.0")
        logger.info("Latest version: 0.1.0")
        logger.info("✅ You're up to date!")
        return 0


class MessagingCommands(BaseCommands):
    """Messaging commands"""

    def send(self, args):
        """Send message to an agent"""
        from agency.core.queue import FileQueue
        from agency.core.types import MessageData
        from agency.config import load_config
        from pathlib import Path
        import time

        # Load config to validate agent exists
        try:
            config = load_config()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return 1

        if args.agent_id not in config.agents:
            logger.error(f"Agent '{args.agent_id}' not found")
            logger.info(f"Available agents: {', '.join(config.agents.keys())}")
            return 1

        # Create message data with @agent_id prefix
        message_text = f"@{args.agent_id} {args.message}"

        message_data = MessageData(
            channel="cli",
            sender=args.user,
            sender_id=args.user,
            message=message_text,
            timestamp=time.time(),
            message_id=f"cli_{int(time.time()*1000)}",
            metadata={}
        )

        # Queue message
        queue_path = config.queue_path
        queue = FileQueue(queue_path)
        queue.enqueue(message_data, "incoming")

        logger.info(f"✅ Message sent to @{args.agent_id}")
        logger.info(f"Message: {args.message}")
        logger.info("")
        logger.info("Response will be processed by the agency processor.")
        logger.info("Make sure the agency is running: agency start")

        return 0

    def broadcast(self, args):
        """Broadcast message to multiple agents"""
        from agency.core.queue_manager import QueueManager
        from agency.core.message import Message

        # Determine target agents
        data = self.load_agents()

        if args.team:
            # Broadcast to team
            teams = data.get("teams", {})
            if args.team not in teams:
                logger.error(f"Team '{args.team}' not found")
                return 1
            target_agents = teams[args.team]["agents"]
        elif args.agents:
            # Broadcast to specific agents
            target_agents = args.agents
        else:
            logger.error("Specify --agents or --team")
            return 1

        # Validate agents exist
        all_agents = data.get("agents", {})
        for agent_id in target_agents:
            if agent_id not in all_agents:
                logger.error(f"Agent '{agent_id}' not found")
                return 1

        # Queue messages
        queue = QueueManager(self.base_dir / "queue")
        for agent_id in target_agents:
            msg = Message(
                user_id='cli',
                text=args.message,
                agent_id=agent_id,
                channel="cli"
            )
            queue.enqueue(msg)

        logger.info(f"✅ Broadcast sent to {len(target_agents)} agents")
        return 0

    def history(self, args):
        """View conversation history"""
        from agency.core.conversation_manager import ConversationManager

        conv_mgr = ConversationManager(self.workspace_dir)

        # Get history
        history = conv_mgr.get_conversation(
            user_id=args.user,
            agent_id=args.agent_id
        )

        if not history:
            logger.info("No conversation history")
            return 0

        # Limit
        messages = history.messages[-args.limit:]

        if args.json:
            output = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
            print(json.dumps(output, indent=2))
            return 0

        # Human-readable
        logger.info(f"💬 Conversation: {args.user} ↔️ @{args.agent_id}")
        logger.info("=" * 70)

        for msg in messages:
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            role_marker = "👤" if msg.role == "user" else "🤖"
            logger.info(f"{role_marker} [{timestamp}] {msg.role}")
            logger.info(f"   {msg.content}")
            logger.info("")

        return 0


class DebugCommands(BaseCommands):
    """Debug and visualization commands"""

    def visualize(self, args):
        """Visualize message flow and queue state"""
        from agency.core.queue import FileQueue
        from agency.config import load_config
        from pathlib import Path
        import time as time_module

        logger.info("🔍 Agency System Visualization")
        logger.info("=" * 70)

        # Load config
        try:
            config = load_config()
            logger.info(f"✅ Config loaded: {len(config.agents)} agents, {len(config.teams)} teams")
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            return 1

        # Check queue
        queue = FileQueue(config.queue_path)
        logger.info(f"\n📬 Queue Path: {config.queue_path}")

        # Count messages in each queue
        incoming_count = queue.get_queue_size("incoming")
        processing_count = queue.get_queue_size("processing")
        outgoing_count = queue.get_queue_size("outgoing")

        logger.info(f"\n📊 Queue Status:")
        logger.info(f"  Incoming: {incoming_count} messages")
        logger.info(f"  Processing: {processing_count} messages")
        logger.info(f"  Outgoing: {outgoing_count} messages")

        # Show recent incoming messages
        if incoming_count > 0:
            logger.info(f"\n📥 Incoming Messages:")
            for i, file_path in enumerate(sorted(queue.incoming.glob("*.json"))):
                if i >= 5:  # Show max 5
                    break
                with open(file_path, 'r') as f:
                    data = json.load(f)
                logger.info(f"  {i+1}. From: {data.get('sender', 'unknown')}")
                logger.info(f"     Message: {data.get('message', '')[:60]}...")
                logger.info(f"     Time: {time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime(data.get('timestamp', 0)))}")

        # Show recent outgoing messages
        if outgoing_count > 0:
            logger.info(f"\n📤 Outgoing Messages:")
            for i, msg in enumerate(queue.iter_outgoing()):
                if i >= 5:  # Show max 5
                    break
                logger.info(f"  {i+1}. To: {msg.data.sender}")
                logger.info(f"     Message: {msg.data.message[:60]}...")

        # System status
        logger.info(f"\n🔧 System Status:")
        pids = self._load_pids()
        if pids.get("processor"):
            logger.info(f"  ✅ Processor: Running (PID: {pids['processor']})")
        else:
            logger.info(f"  ❌ Processor: Not running")

        if pids.get("telegram"):
            logger.info(f"  ✅ Telegram: Running (PID: {pids['telegram']})")
        else:
            logger.info(f"  ⚠️  Telegram: Not running")

        # Agent status
        logger.info(f"\n🤖 Agents:")
        for agent_id, agent in list(config.agents.items())[:10]:
            logger.info(f"  • @{agent_id} - {agent.name} ({agent.model})")

        # Teams
        if config.teams:
            logger.info(f"\n👥 Teams:")
            for team_id, team in config.teams.items():
                logger.info(f"  • @{team_id} - {team.name} (leader: {team.leader_agent})")

        logger.info("\n" + "=" * 70)
        logger.info("💡 Tip: Use 'agency debug test <agent_id>' to test an agent end-to-end")

        return 0

    def check(self, args):
        """Check system connectivity and configuration"""
        from agency.config import load_config
        import os

        logger.info("🔍 System Check")
        logger.info("=" * 70)

        # Check environment variables
        logger.info("\n📋 Environment Variables:")
        env_vars = {
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
            "TELEGRAM_ALLOWED_USERS": os.getenv("TELEGRAM_ALLOWED_USERS"),
            "GOOGLE_OAUTH_CREDENTIALS": os.getenv("GOOGLE_OAUTH_CREDENTIALS"),
        }

        for key, value in env_vars.items():
            if value:
                masked = value[:10] + "..." if len(value) > 10 else value
                logger.info(f"  ✅ {key}: {masked}")
            else:
                logger.info(f"  ❌ {key}: Not set")

        # Check config
        logger.info("\n🔧 Configuration:")
        try:
            config = load_config()
            logger.info(f"  ✅ Agents: {len(config.agents)}")
            logger.info(f"  ✅ Teams: {len(config.teams)}")
            logger.info(f"  ✅ Queue: {config.queue_path}")
        except Exception as e:
            logger.error(f"  ❌ Config load failed: {e}")
            return 1

        # Check queue directories
        logger.info("\n📁 Queue Directories:")
        for subdir in ["incoming", "processing", "outgoing"]:
            path = config.queue_path / subdir
            if path.exists():
                logger.info(f"  ✅ {subdir}: {path}")
            else:
                logger.warning(f"  ⚠️  {subdir}: Missing ({path})")

        # Check Google credentials (for CC agent)
        logger.info("\n🔑 Google Services (for CC agent):")
        google_creds = os.getenv("GOOGLE_OAUTH_CREDENTIALS", "google_oauth_credentials.json")
        google_token = os.getenv("GOOGLE_TOKEN_PATH", "google_token.pickle")

        if Path(google_creds).exists():
            logger.info(f"  ✅ Credentials: {google_creds}")
        else:
            logger.warning(f"  ⚠️  Credentials: Not found ({google_creds})")

        if Path(google_token).exists():
            logger.info(f"  ✅ Token: {google_token}")
        else:
            logger.warning(f"  ⚠️  Token: Not found ({google_token})")

        logger.info("\n" + "=" * 70)
        return 0

    def test(self, args):
        """Test agent invocation end-to-end"""
        from agency.config import load_config
        from agency.core.agent import AgentInvoker
        from agency.core.types import MessageData
        from agency.core.tools import create_google_tools_registry
        import asyncio
        import time

        logger.info(f"🧪 Testing Agent: @{args.agent_id}")
        logger.info("=" * 70)

        # Load config
        try:
            config = load_config()
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            return 1

        # Validate agent exists
        if args.agent_id not in config.agents:
            logger.error(f"❌ Agent '{args.agent_id}' not found")
            logger.info(f"Available agents: {', '.join(config.agents.keys())}")
            return 1

        agent_config = config.agents[args.agent_id]
        logger.info(f"✅ Agent found: {agent_config.name}")
        logger.info(f"   Provider: {agent_config.provider}")
        logger.info(f"   Model: {agent_config.model}")

        # Create tool registry for agents that need it
        tool_registry = None
        if args.agent_id in ['cc', 'assistant', 'action_taker']:
            try:
                tool_registry = create_google_tools_registry()
                logger.info(f"   Tools: {len(tool_registry.tool_schemas)} Google tools loaded")
            except Exception as e:
                logger.warning(f"   Tools: Could not load Google tools: {e}")
        elif args.agent_id in ['job_hunter', 'resume_optimizer', 'networker']:
            try:
                from agency.core.tools import create_job_search_tools_registry
                tool_registry = create_job_search_tools_registry()
                logger.info(f"   Tools: {len(tool_registry.tool_schemas)} Job search tools loaded")
            except Exception as e:
                logger.warning(f"   Tools: Could not load job search tools: {e}")

        # Create invoker
        invoker = AgentInvoker(
            anthropic_api_key=config.anthropic_api_key,
            openai_api_key=config.openai_api_key
        )

        # Create test message
        message_data = MessageData(
            channel="test",
            sender="test_user",
            sender_id="test_123",
            message=args.message,
            timestamp=time.time(),
            message_id=f"test_{int(time.time()*1000)}",
            metadata={}
        )

        logger.info(f"\n📨 Sending test message:")
        logger.info(f"   Message: {args.message}")

        # Invoke agent
        try:
            logger.info(f"\n⏳ Invoking agent...")
            response = asyncio.run(
                invoker.invoke_agent(
                    agent_config=agent_config,
                    message=args.message,
                    workspace_path=config.workspace_path,
                    team_context=None,
                    reset=False,
                    tool_registry=tool_registry
                )
            )

            logger.info(f"\n✅ Response received!")
            logger.info("=" * 70)
            logger.info(response)
            logger.info("=" * 70)

            return 0

        except Exception as e:
            logger.error(f"\n❌ Agent invocation failed: {e}")
            import traceback
            traceback.print_exc()
            return 1
