"""
Avengers AI Operating System

A sophisticated multi-agent system where specialized AI agents work together.
Interact with Iron Man (Chief of Staff) via WhatsApp to orchestrate your AI team.
"""

from .black_widow import BlackWidowAgent
from .captain_america import CaptainAmericaAgent
from .coordination import CoordinationHub, Priority, Task, TaskStatus, coordination_hub
from .hawkeye import HawkeyeAgent
from .hulk import HulkAgent
from .iron_man import IronManAgent
from .thor import ThorAgent

__all__ = [
    "IronManAgent",
    "CaptainAmericaAgent",
    "ThorAgent",
    "BlackWidowAgent",
    "HulkAgent",
    "HawkeyeAgent",
    "CoordinationHub",
    "coordination_hub",
    "Task",
    "TaskStatus",
    "Priority",
]
