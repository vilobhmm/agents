"""
Agent Coordination Layer

Provides shared communication and knowledge infrastructure for all Avengers agents.
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Task priority levels"""

    URGENT = "urgent"  # 1 hour response time
    HIGH = "high"  # 4 hours
    MEDIUM = "medium"  # 1 day
    LOW = "low"  # 1 week


class TaskStatus(Enum):
    """Task status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task:
    """Represents a task that can be assigned to agents"""

    def __init__(
        self,
        task_id: str,
        description: str,
        assigned_to: str,
        priority: Priority = Priority.MEDIUM,
        dependencies: Optional[List[str]] = None,
    ):
        self.task_id = task_id
        self.description = description
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.dependencies = dependencies or []
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

    def start(self):
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def complete(self, result: str):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def block(self, reason: str):
        """Mark task as blocked"""
        self.status = TaskStatus.BLOCKED
        self.metadata["blocked_reason"] = reason

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "result": self.result,
            "metadata": self.metadata,
        }


class AgentReport:
    """Represents a status report from an agent"""

    def __init__(
        self,
        agent_name: str,
        status: str,
        current_task: Optional[Task] = None,
        recent_completions: Optional[List[Task]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        next_action: Optional[str] = None,
    ):
        self.agent_name = agent_name
        self.status = status
        self.current_task = current_task
        self.recent_completions = recent_completions or []
        self.metrics = metrics or {}
        self.next_action = next_action
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "agent_name": self.agent_name,
            "status": self.status,
            "current_task": (
                self.current_task.to_dict() if self.current_task else None
            ),
            "recent_completions": [t.to_dict() for t in self.recent_completions],
            "metrics": self.metrics,
            "next_action": self.next_action,
            "timestamp": self.timestamp.isoformat(),
        }


class KnowledgeBase:
    """Shared knowledge base accessible to all agents"""

    def __init__(self):
        self.entries: Dict[str, Any] = {}
        self.timeline: List[Dict[str, Any]] = []

    def add_entry(self, key: str, value: Any, source: str):
        """Add knowledge entry"""
        entry = {
            "key": key,
            "value": value,
            "source": source,
            "timestamp": datetime.now().isoformat(),
        }

        self.entries[key] = entry
        self.timeline.append(entry)

        logger.info(f"Knowledge added: {key} from {source}")

    def get_entry(self, key: str) -> Optional[Any]:
        """Get knowledge entry"""
        entry = self.entries.get(key)
        return entry["value"] if entry else None

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge base"""
        # Simple keyword search
        results = []
        for key, entry in self.entries.items():
            if query.lower() in key.lower() or query.lower() in str(
                entry["value"]
            ).lower():
                results.append(entry)

        return results

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent knowledge entries"""
        return self.timeline[-limit:]

    def get_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Get all entries from a specific source"""
        return [e for e in self.timeline if e["source"] == source]


class CoordinationHub:
    """Central coordination hub for all agents"""

    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.tasks: Dict[str, Task] = {}
        self.agent_reports: Dict[str, AgentReport] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()

    async def assign_task(
        self,
        task_id: str,
        description: str,
        assigned_to: str,
        priority: Priority = Priority.MEDIUM,
        dependencies: Optional[List[str]] = None,
    ) -> Task:
        """Assign a task to an agent"""
        task = Task(task_id, description, assigned_to, priority, dependencies)
        self.tasks[task_id] = task

        # Add to knowledge base
        self.knowledge_base.add_entry(
            f"task_{task_id}",
            task.to_dict(),
            source="coordination_hub",
        )

        # Send message to agent
        await self.send_message(
            to=assigned_to,
            message_type="task_assignment",
            content=task.to_dict(),
        )

        logger.info(f"Task {task_id} assigned to {assigned_to}")

        return task

    async def update_task(
        self, task_id: str, status: TaskStatus, result: Optional[str] = None
    ):
        """Update task status"""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return

        task = self.tasks[task_id]

        if status == TaskStatus.IN_PROGRESS:
            task.start()
        elif status == TaskStatus.COMPLETED:
            task.complete(result or "")
        elif status == TaskStatus.BLOCKED:
            task.block(result or "Unknown reason")

        # Update knowledge base
        self.knowledge_base.add_entry(
            f"task_{task_id}",
            task.to_dict(),
            source="coordination_hub",
        )

        logger.info(f"Task {task_id} updated to {status.value}")

    async def submit_report(self, report: AgentReport):
        """Submit agent status report"""
        self.agent_reports[report.agent_name] = report

        # Add to knowledge base
        self.knowledge_base.add_entry(
            f"report_{report.agent_name}_{report.timestamp.isoformat()}",
            report.to_dict(),
            source=report.agent_name,
        )

        logger.info(f"Report received from {report.agent_name}")

    async def send_message(self, to: str, message_type: str, content: Any):
        """Send message to an agent"""
        message = {
            "to": to,
            "type": message_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }

        await self.message_queue.put(message)

        logger.debug(f"Message sent to {to}: {message_type}")

    async def get_agent_status(self, agent_name: str) -> Optional[AgentReport]:
        """Get latest status from an agent"""
        return self.agent_reports.get(agent_name)

    async def get_all_status(self) -> Dict[str, AgentReport]:
        """Get status from all agents"""
        return self.agent_reports.copy()

    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get task status"""
        return self.tasks.get(task_id)

    async def get_tasks_by_agent(self, agent_name: str) -> List[Task]:
        """Get all tasks assigned to an agent"""
        return [t for t in self.tasks.values() if t.assigned_to == agent_name]

    async def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [
            t for t in self.tasks.values() if t.status == TaskStatus.PENDING
        ]

    async def get_active_tasks(self) -> List[Task]:
        """Get all active (in progress) tasks"""
        return [
            t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS
        ]

    async def broadcast(self, message_type: str, content: Any):
        """Broadcast message to all agents"""
        for agent_name in self.agent_reports.keys():
            await self.send_message(agent_name, message_type, content)

        logger.info(f"Broadcast sent: {message_type}")


# Global coordination hub instance
coordination_hub = CoordinationHub()
