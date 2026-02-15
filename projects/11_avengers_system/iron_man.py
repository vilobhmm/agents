"""
Iron Man - Chief of Staff Agent

The central orchestrator and primary user interface.
Manages all other agents and provides consolidated updates.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from anthropic import Anthropic

from .coordination import (
    AgentReport,
    CoordinationHub,
    Priority,
    Task,
    TaskStatus,
    coordination_hub,
)

logger = logging.getLogger(__name__)


class IronManAgent:
    """
    Iron Man - Chief of Staff

    The only agent the user interacts with directly.
    Orchestrates all other agents and maintains complete visibility.
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Iron Man"
        self.emoji = "🧠"
        self.role = "Chief of Staff"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub

        # Agent registry
        self.agents = {
            "captain_america": {
                "name": "Captain America",
                "emoji": "🛡",
                "role": "Research & Intelligence",
            },
            "thor": {"name": "Thor", "emoji": "⚡", "role": "X/Twitter Operator"},
            "black_widow": {
                "name": "Black Widow",
                "emoji": "🕷",
                "role": "LinkedIn Authority",
            },
            "hulk": {
                "name": "Hulk",
                "emoji": "🔨",
                "role": "GitHub Prototype Builder",
            },
            "hawkeye": {
                "name": "Hawkeye",
                "emoji": "🎯",
                "role": "Newsletter Curator",
            },
        }

        # Conversation history for context
        self.conversation_history: List[Dict[str, str]] = []

        logger.info("Iron Man initialized - Chief of Staff ready")

    async def handle_user_message(self, message: str) -> str:
        """
        Handle incoming message from user via WhatsApp

        This is the main entry point for all user interactions.
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})

        # Parse user intent
        if message.lower() == "status":
            response = await self.get_full_status()
        elif message.lower().startswith("assign "):
            task_desc = message[7:].strip()
            response = await self.assign_task_from_user(task_desc)
        elif message.lower().startswith("report "):
            agent = message[7:].strip().lower()
            response = await self.get_agent_report(agent)
        elif message.lower() == "sprint":
            response = await self.get_sprint_status()
        elif message.lower() == "help":
            response = self.get_help_text()
        else:
            # General conversation - use Claude to understand and respond
            response = await self.chat(message)

        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    async def chat(self, message: str) -> str:
        """
        General conversation using Claude

        Handles open-ended questions, strategy discussions, etc.
        """
        # Build context with current system state
        system_context = await self._build_system_context()

        # Create prompt
        messages = [
            {
                "role": "user",
                "content": f"""You are Iron Man, the Chief of Staff for the Avengers AI team.

You manage 5 specialized agents:
- 🛡 Captain America: Research & Intelligence
- ⚡ Thor: X/Twitter content
- 🕷 Black Widow: LinkedIn authority
- 🔨 Hulk: GitHub prototypes
- 🎯 Hawkeye: Newsletter curation

Current system state:
{system_context}

User message: {message}

Respond as Iron Man - strategic, decisive, and action-oriented.
If the user is asking about work or status, provide concrete information.
If they're asking you to do something, delegate to the right agent(s).
Keep responses concise and clear.""",
            }
        ]

        # Add recent conversation history for context
        if len(self.conversation_history) > 0:
            messages = (
                [{"role": "system", "content": "Previous conversation:"}]
                + self.conversation_history[-4:]  # Last 2 exchanges
                + messages
            )

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=messages,
        )

        return response.content[0].text

    async def _build_system_context(self) -> str:
        """Build current system state context"""
        # Get all agent statuses
        statuses = await self.coordination.get_all_status()

        # Get active tasks
        active_tasks = await self.coordination.get_active_tasks()
        pending_tasks = await self.coordination.get_pending_tasks()

        # Get recent knowledge
        recent_knowledge = self.coordination.knowledge_base.get_recent(5)

        context = f"""
Active Tasks: {len(active_tasks)}
Pending Tasks: {len(pending_tasks)}

Agent Statuses:
"""

        for agent_key, agent_info in self.agents.items():
            report = statuses.get(agent_key)
            if report:
                context += f"- {agent_info['emoji']} {agent_info['name']}: {report.status}\n"
            else:
                context += f"- {agent_info['emoji']} {agent_info['name']}: No recent report\n"

        context += f"\nRecent Activity: {len(recent_knowledge)} knowledge entries\n"

        return context

    async def get_full_status(self) -> str:
        """Get comprehensive status of all agents"""
        status_msg = f"{self.emoji} *AVENGERS STATUS*\n\n"

        # Get all agent reports
        statuses = await self.coordination.get_all_status()

        for agent_key, agent_info in self.agents.items():
            report = statuses.get(agent_key)

            status_msg += f"{agent_info['emoji']} *{agent_info['name']}*: "

            if report:
                status_msg += f"{report.status}\n"

                if report.current_task:
                    status_msg += f"   Working on: {report.current_task.description}\n"

                if report.metrics:
                    for key, value in report.metrics.items():
                        status_msg += f"   {key}: {value}\n"

            else:
                status_msg += "No recent report\n"

            status_msg += "\n"

        # Add overall stats
        active_tasks = await self.coordination.get_active_tasks()
        pending_tasks = await self.coordination.get_pending_tasks()

        status_msg += f"*Overall*\n"
        status_msg += f"Active tasks: {len(active_tasks)}\n"
        status_msg += f"Pending tasks: {len(pending_tasks)}\n"

        return status_msg

    async def assign_task_from_user(self, task_description: str) -> str:
        """
        User wants to assign a task - figure out which agent should handle it
        """
        # Use Claude to determine best agent
        prompt = f"""Given this task: "{task_description}"

Which Avengers agent should handle it?

Agents:
- captain_america: Research, intelligence gathering, monitoring AI news
- thor: Twitter content, social media engagement, rapid commentary
- black_widow: LinkedIn posts, professional content, thought leadership
- hulk: Code prototypes, GitHub projects, technical implementations
- hawkeye: Newsletter content, summaries, curation

Respond with ONLY the agent key (lowercase, underscore separated).
Example: "captain_america" or "hulk"
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}],
        )

        agent_key = response.content[0].text.strip().lower()

        # Validate agent
        if agent_key not in self.agents:
            return f"❌ Could not determine appropriate agent for this task. Try being more specific or use: assign to <agent_name>: <task>"

        # Determine priority
        priority = Priority.MEDIUM
        if any(
            word in task_description.lower() for word in ["urgent", "asap", "now"]
        ):
            priority = Priority.URGENT
        elif any(word in task_description.lower() for word in ["important", "high"]):
            priority = Priority.HIGH

        # Create task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Assign task
        task = await self.coordination.assign_task(
            task_id=task_id,
            description=task_description,
            assigned_to=agent_key,
            priority=priority,
        )

        agent_info = self.agents[agent_key]

        response_msg = f"✅ *Task Assigned*\n\n"
        response_msg += f"Agent: {agent_info['emoji']} {agent_info['name']}\n"
        response_msg += f"Task: {task_description}\n"
        response_msg += f"Priority: {priority.value}\n"
        response_msg += f"ID: {task_id}\n\n"
        response_msg += f"I'll keep you updated on progress."

        return response_msg

    async def get_agent_report(self, agent_key: str) -> str:
        """Get detailed report for a specific agent"""
        if agent_key not in self.agents:
            return f"❌ Unknown agent: {agent_key}\n\nAvailable agents: {', '.join(self.agents.keys())}"

        agent_info = self.agents[agent_key]
        report = await self.coordination.get_agent_status(agent_key)

        if not report:
            return f"{agent_info['emoji']} *{agent_info['name']}*\n\nNo recent activity to report."

        msg = f"{agent_info['emoji']} *{agent_info['name'].upper()} REPORT*\n\n"

        # Current task
        if report.current_task:
            msg += f"*Current Task*: {report.current_task.description}\n"
            msg += f"Status: {report.current_task.status.value}\n"

            if report.current_task.started_at:
                duration = datetime.now() - report.current_task.started_at
                msg += f"Duration: {duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m\n"

            msg += "\n"

        # Recent completions
        if report.recent_completions:
            msg += f"*Recent Completions*:\n"
            for task in report.recent_completions[-3:]:  # Last 3
                msg += f"✅ {task.description}\n"

            msg += "\n"

        # Metrics
        if report.metrics:
            msg += f"*Metrics*:\n"
            for key, value in report.metrics.items():
                msg += f"- {key}: {value}\n"

            msg += "\n"

        # Next action
        if report.next_action:
            msg += f"*Next*: {report.next_action}\n"

        return msg

    async def get_sprint_status(self) -> str:
        """Get current sprint overview"""
        msg = f"{self.emoji} *CURRENT SPRINT*\n\n"

        # Get all active and pending tasks
        active = await self.coordination.get_active_tasks()
        pending = await self.coordination.get_pending_tasks()

        # Group by agent
        tasks_by_agent: Dict[str, List[Task]] = {}

        for task in active + pending:
            if task.assigned_to not in tasks_by_agent:
                tasks_by_agent[task.assigned_to] = []

            tasks_by_agent[task.assigned_to].append(task)

        # Display by agent
        for agent_key, tasks in tasks_by_agent.items():
            if agent_key in self.agents:
                agent_info = self.agents[agent_key]
                msg += f"{agent_info['emoji']} *{agent_info['name']}*\n"

                for task in tasks:
                    status_icon = "🔄" if task.status == TaskStatus.IN_PROGRESS else "⏸"
                    msg += f"  {status_icon} {task.description}\n"

                msg += "\n"

        if not tasks_by_agent:
            msg += "No active sprint tasks.\n\n"
            msg += "Assign tasks with: assign <task description>"

        return msg

    def get_help_text(self) -> str:
        """Get help text"""
        return f"""{self.emoji} *IRON MAN - COMMAND CENTER*

I orchestrate the Avengers AI team. Here's how to work with me:

*Commands*:
• `status` - Get status of all agents
• `assign <task>` - Assign a new task
• `report <agent>` - Get detailed agent report
• `sprint` - View current sprint
• `help` - Show this message

*Agent Names*:
• captain_america - Research & Intelligence
• thor - X/Twitter content
• black_widow - LinkedIn authority
• hulk - GitHub prototypes
• hawkeye - Newsletter curation

*Examples*:
• "status"
• "assign Build a RAG demo"
• "report hulk"
• "What's the most important AI news?"
• "Start a 2-week sprint on transformers"

*General Conversation*:
Just talk to me naturally! I understand context and can:
- Answer questions about the team's work
- Provide strategic guidance
- Make decisions about priorities
- Coordinate complex workflows

I'll delegate to the right agents automatically.
"""

    async def morning_briefing(self) -> str:
        """Generate morning briefing for user"""
        msg = f"☀️ *GOOD MORNING*\n\n"
        msg += f"Here's your Avengers team briefing:\n\n"

        # Get status from all agents
        statuses = await self.coordination.get_all_status()

        for agent_key in ["captain_america", "thor", "black_widow", "hulk", "hawkeye"]:
            report = statuses.get(agent_key)
            agent_info = self.agents[agent_key]

            if report and report.metrics:
                msg += f"{agent_info['emoji']} {agent_info['name']}: "

                # Show key metrics
                if "daily_summary" in report.metrics:
                    msg += report.metrics["daily_summary"]
                else:
                    msg += f"{report.status}"

                msg += "\n"

        # Active tasks
        active_tasks = await self.coordination.get_active_tasks()

        if active_tasks:
            msg += f"\n*In Progress* ({len(active_tasks)} tasks):\n"
            for task in active_tasks[:3]:  # Top 3
                agent = self.agents[task.assigned_to]
                msg += f"• {agent['emoji']} {task.description}\n"

        msg += f"\nReady for action. What's the priority today?"

        return msg

    async def evening_summary(self) -> str:
        """Generate evening summary for user"""
        msg = f"🌙 *DAY SUMMARY*\n\n"

        # Count completions today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        total_completed = 0
        completions_by_agent = {}

        for agent_key in self.agents.keys():
            tasks = await self.coordination.get_tasks_by_agent(agent_key)
            completed_today = [
                t
                for t in tasks
                if t.status == TaskStatus.COMPLETED
                and t.completed_at
                and t.completed_at >= today_start
            ]

            if completed_today:
                completions_by_agent[agent_key] = completed_today
                total_completed += len(completed_today)

        msg += f"*Completed Today*: {total_completed} tasks\n\n"

        # Show completions by agent
        for agent_key, tasks in completions_by_agent.items():
            agent_info = self.agents[agent_key]
            msg += f"{agent_info['emoji']} {agent_info['name']}: {len(tasks)}\n"

            for task in tasks[:2]:  # Show top 2
                msg += f"  ✅ {task.description}\n"

            msg += "\n"

        if total_completed == 0:
            msg += "No tasks completed today.\n\n"

        msg += f"Rest up. Tomorrow we build more."

        return msg
