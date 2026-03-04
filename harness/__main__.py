#!/usr/bin/env python3
"""
Multi-Agent Harness CLI

Usage:
    python -m harness                     # run all checks
    python -m harness --verbose           # with full tracebacks
    python -m harness --category voice    # filter by category
    python -m harness --json              # machine-readable output
    python -m harness --list              # list all registered agents
"""

import argparse
import sys

from harness.registry import AgentRegistry
from harness.runner import HarnessRunner


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="harness",
        description="Multi-Agent Harness — Discover, validate, and smoke-test every agent.",
    )
    parser.add_argument(
        "--category",
        choices=AgentRegistry.get_categories(),
        help="Only run checks for agents in this category",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show full tracebacks for failures",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON (for CI integration)",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        dest="list_agents",
        help="List all registered agents and exit",
    )

    args = parser.parse_args()

    # ── List mode ─────────────────────────────────────────────
    if args.list_agents:
        agents = AgentRegistry.get_all_agents()
        print(f"\n  📋  Registered Agents ({len(agents)} total)\n")
        current_cat = None
        for agent in sorted(agents, key=lambda a: (a.category, a.name)):
            if agent.category != current_cat:
                current_cat = agent.category
                print(f"  ── {current_cat.upper()} ──")
            print(f"    • {agent.name}")
            print(f"      {agent.module_path}.{agent.class_name}")
            if agent.description:
                print(f"      {agent.description}")
            print()
        return 0

    # ── Run harness ───────────────────────────────────────────
    runner = HarnessRunner(category=args.category, verbose=args.verbose)
    results = runner.run()

    if args.json_output:
        print(runner.to_json(results))
    else:
        runner.print_report(results)

    return runner.exit_code(results)


if __name__ == "__main__":
    sys.exit(main())
