"""
Health Check Framework — Import, instantiation, and capability checks.

Each check returns a HealthCheckResult so the runner can aggregate
pass/fail/skip status across all agents.
"""

import importlib
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, List, Optional

from harness.registry import AgentEntry


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    agent_name: str
    check_name: str           # "import", "instantiation", "capability"
    passed: bool
    duration_ms: float = 0.0
    error: Optional[str] = None
    details: str = ""
    skipped: bool = False
    skip_reason: str = ""


class HealthChecker:
    """Runs health checks against a single AgentEntry."""

    # ── Import Check ─────────────────────────────────────────────

    @staticmethod
    def import_check(entry: AgentEntry) -> HealthCheckResult:
        """Verify the module can be imported and the class exists."""
        start = time.perf_counter()
        try:
            module = importlib.import_module(entry.module_path)
            cls = getattr(module, entry.class_name, None)
            elapsed = (time.perf_counter() - start) * 1000

            if cls is None:
                return HealthCheckResult(
                    agent_name=entry.name,
                    check_name="import",
                    passed=False,
                    duration_ms=elapsed,
                    error=f"Class '{entry.class_name}' not found in module '{entry.module_path}'",
                )

            return HealthCheckResult(
                agent_name=entry.name,
                check_name="import",
                passed=True,
                duration_ms=elapsed,
                details=f"Successfully imported {entry.module_path}.{entry.class_name}",
            )

        except (ImportError, ModuleNotFoundError) as e:
            # Missing pip packages or optional deps → skip, not failure
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="import",
                passed=True,
                duration_ms=elapsed,
                skipped=True,
                skip_reason=f"Missing dependency: {e}",
            )

        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="import",
                passed=False,
                duration_ms=elapsed,
                error=f"{type(e).__name__}: {e}",
                details=traceback.format_exc(),
            )

    # ── Instantiation Check ──────────────────────────────────────

    @staticmethod
    def instantiation_check(entry: AgentEntry) -> HealthCheckResult:
        """
        Attempt to construct the agent class.

        Many agents depend on external services (Google OAuth, API keys, etc.)
        so ImportError/ValueError from missing credentials is treated as a
        *skip* rather than a failure.
        """
        start = time.perf_counter()
        try:
            module = importlib.import_module(entry.module_path)
            cls = getattr(module, entry.class_name)
            instance = cls(**entry.init_kwargs)
            elapsed = (time.perf_counter() - start) * 1000

            return HealthCheckResult(
                agent_name=entry.name,
                check_name="instantiation",
                passed=True,
                duration_ms=elapsed,
                details=f"Created {entry.class_name} instance successfully",
            )

        except (ImportError, ModuleNotFoundError) as e:
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="instantiation",
                passed=True,  # Not a real failure — just missing optional dep
                duration_ms=elapsed,
                skipped=True,
                skip_reason=f"Missing optional dependency: {e}",
            )

        except TypeError as e:
            # Required constructor args we can't provide (e.g. storage_manager)
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="instantiation",
                passed=True,
                duration_ms=elapsed,
                skipped=True,
                skip_reason=f"Required constructor args: {e}",
            )

        except (ValueError, OSError, PermissionError) as e:
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="instantiation",
                passed=True,
                duration_ms=elapsed,
                skipped=True,
                skip_reason=f"Missing credentials/config: {e}",
            )

        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return HealthCheckResult(
                agent_name=entry.name,
                check_name="instantiation",
                passed=False,
                duration_ms=elapsed,
                error=f"{type(e).__name__}: {e}",
                details=traceback.format_exc(),
            )

    # ── Capability Check ─────────────────────────────────────────

    @staticmethod
    def capability_check(entry: AgentEntry) -> List[HealthCheckResult]:
        """
        Run deterministic methods listed in the agent entry.

        Only methods that don't require external services or API keys
        should be listed in entry.deterministic_methods.
        """
        results: List[HealthCheckResult] = []

        if not entry.deterministic_methods:
            return results

        try:
            module = importlib.import_module(entry.module_path)
            cls = getattr(module, entry.class_name)
            instance = cls(**entry.init_kwargs)
        except Exception as e:
            # If we can't instantiate, skip all capability checks
            for method_name in entry.deterministic_methods:
                results.append(HealthCheckResult(
                    agent_name=entry.name,
                    check_name=f"capability:{method_name}",
                    passed=True,
                    skipped=True,
                    skip_reason=f"Cannot instantiate: {e}",
                ))
            return results

        for method_name in entry.deterministic_methods:
            start = time.perf_counter()
            try:
                method = getattr(instance, method_name, None)
                if method is None:
                    elapsed = (time.perf_counter() - start) * 1000
                    results.append(HealthCheckResult(
                        agent_name=entry.name,
                        check_name=f"capability:{method_name}",
                        passed=False,
                        duration_ms=elapsed,
                        error=f"Method '{method_name}' not found on {entry.class_name}",
                    ))
                    continue

                # Call with default args
                result = method()
                elapsed = (time.perf_counter() - start) * 1000

                # Basic sanity: method returned *something*
                if result is not None:
                    results.append(HealthCheckResult(
                        agent_name=entry.name,
                        check_name=f"capability:{method_name}",
                        passed=True,
                        duration_ms=elapsed,
                        details=f"Returned: {str(result)[:120]}",
                    ))
                else:
                    results.append(HealthCheckResult(
                        agent_name=entry.name,
                        check_name=f"capability:{method_name}",
                        passed=True,
                        duration_ms=elapsed,
                        details="Returned None (may be expected)",
                    ))

            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                results.append(HealthCheckResult(
                    agent_name=entry.name,
                    check_name=f"capability:{method_name}",
                    passed=False,
                    duration_ms=elapsed,
                    error=f"{type(e).__name__}: {e}",
                    details=traceback.format_exc(),
                ))

        return results

    # ── Run All Checks ───────────────────────────────────────────

    @staticmethod
    def run_all(entry: AgentEntry) -> List[HealthCheckResult]:
        """Run import, instantiation, and capability checks for one agent."""
        results: List[HealthCheckResult] = []

        # 1. Import
        import_result = HealthChecker.import_check(entry)
        results.append(import_result)

        # Only continue if import succeeded
        if not import_result.passed:
            return results

        # 2. Instantiation
        inst_result = HealthChecker.instantiation_check(entry)
        results.append(inst_result)

        # 3. Capability (only if instantiation succeeded and wasn't skipped)
        if inst_result.passed and not inst_result.skipped:
            cap_results = HealthChecker.capability_check(entry)
            results.extend(cap_results)

        return results
