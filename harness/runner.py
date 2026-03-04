"""
Harness Runner — Orchestrates health checks across all agents.

Runs checks sequentially per agent, prints a rich terminal report,
and returns structured results for JSON output or pytest assertions.
"""

import json
import sys
import time
from typing import Dict, List, Optional

from harness.registry import AgentRegistry, AgentEntry
from harness.health import HealthChecker, HealthCheckResult


class HarnessRunner:
    """
    Runs health checks across all registered agents and produces reports.

    Usage:
        runner = HarnessRunner()
        results = runner.run()
        runner.print_report(results)
        sys.exit(runner.exit_code(results))
    """

    def __init__(self, category: Optional[str] = None, verbose: bool = False):
        self.category = category
        self.verbose = verbose

    # ── Run ───────────────────────────────────────────────────────

    def run(self) -> Dict[str, List[HealthCheckResult]]:
        """
        Run all health checks.

        Returns:
            dict mapping agent name -> list of HealthCheckResult
        """
        if self.category:
            agents = AgentRegistry.get_by_category(self.category)
        else:
            agents = AgentRegistry.get_all_agents()

        results: Dict[str, List[HealthCheckResult]] = {}

        for entry in agents:
            agent_results = HealthChecker.run_all(entry)
            results[entry.name] = agent_results

        return results

    # ── Report ───────────────────────────────────────────────────

    def print_report(self, results: Dict[str, List[HealthCheckResult]]) -> None:
        """Print a rich terminal report."""
        total_checks = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_time_ms = 0.0

        print()
        print("=" * 72)
        print("  🤖  MULTI-AGENT HARNESS — Health Check Report")
        print("=" * 72)

        if self.category:
            print(f"  Category filter: {self.category}")
            print("-" * 72)

        for agent_name, checks in results.items():
            # Determine overall status for this agent
            agent_failed = any(not c.passed for c in checks)
            agent_skipped = all(c.skipped for c in checks if c.passed)
            agent_time = sum(c.duration_ms for c in checks)
            total_time_ms += agent_time

            if agent_failed:
                status_icon = "❌"
            elif agent_skipped:
                status_icon = "⏭️ "
            else:
                status_icon = "✅"

            print(f"\n  {status_icon}  {agent_name}  ({agent_time:.0f}ms)")

            for check in checks:
                total_checks += 1
                if check.skipped:
                    total_skipped += 1
                    icon = "⏭️ "
                    detail = f"SKIP: {check.skip_reason}"
                elif check.passed:
                    total_passed += 1
                    icon = "✓"
                    detail = check.details[:80] if check.details else ""
                else:
                    total_failed += 1
                    icon = "✗"
                    detail = check.error or ""

                line = f"      {icon}  {check.check_name}"
                if detail:
                    line += f"  — {detail}"
                print(line)

                # Verbose: show full traceback for failures
                if self.verbose and not check.passed and check.details:
                    for tb_line in check.details.strip().split("\n"):
                        print(f"          {tb_line}")

        # ── Summary ──────────────────────────────────────────────
        print()
        print("=" * 72)
        print("  📊  SUMMARY")
        print("=" * 72)
        print(f"  Agents tested : {len(results)}")
        print(f"  Total checks  : {total_checks}")
        print(f"  ✅ Passed      : {total_passed}")
        print(f"  ❌ Failed      : {total_failed}")
        print(f"  ⏭️  Skipped    : {total_skipped}")
        print(f"  ⏱️  Total time : {total_time_ms:.0f}ms")
        print("-" * 72)

        if total_failed == 0:
            print("  🎉  ALL AGENTS HEALTHY!")
        else:
            print(f"  ⚠️   {total_failed} check(s) failed. See details above.")

        print("=" * 72)
        print()

    # ── JSON Output ──────────────────────────────────────────────

    def to_json(self, results: Dict[str, List[HealthCheckResult]]) -> str:
        """Serialize results to JSON."""
        data = {}
        for agent_name, checks in results.items():
            data[agent_name] = [
                {
                    "check_name": c.check_name,
                    "passed": c.passed,
                    "skipped": c.skipped,
                    "duration_ms": round(c.duration_ms, 2),
                    "error": c.error,
                    "details": c.details if self.verbose else "",
                    "skip_reason": c.skip_reason,
                }
                for c in checks
            ]

        summary = self._compute_summary(results)
        return json.dumps({"agents": data, "summary": summary}, indent=2)

    # ── Exit Code ────────────────────────────────────────────────

    def exit_code(self, results: Dict[str, List[HealthCheckResult]]) -> int:
        """Return 0 if everything passed, 1 if any check failed."""
        for checks in results.values():
            for check in checks:
                if not check.passed:
                    return 1
        return 0

    # ── Helpers ──────────────────────────────────────────────────

    def _compute_summary(self, results: Dict[str, List[HealthCheckResult]]) -> Dict:
        total = sum(len(checks) for checks in results.values())
        passed = sum(1 for checks in results.values() for c in checks if c.passed and not c.skipped)
        failed = sum(1 for checks in results.values() for c in checks if not c.passed)
        skipped = sum(1 for checks in results.values() for c in checks if c.skipped)
        return {
            "agents_tested": len(results),
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "all_healthy": failed == 0,
        }
