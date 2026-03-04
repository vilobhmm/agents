"""
Multi-Agent Harness — Discover, validate, and smoke-test every agent.

Usage:
    python -m harness            # run all checks
    python -m harness --verbose  # with full tracebacks
    python -m harness --json     # machine-readable output
"""

from harness.registry import AgentRegistry, AgentEntry
from harness.health import HealthChecker, HealthCheckResult
from harness.runner import HarnessRunner

__all__ = [
    "AgentRegistry",
    "AgentEntry",
    "HealthChecker",
    "HealthCheckResult",
    "HarnessRunner",
]
