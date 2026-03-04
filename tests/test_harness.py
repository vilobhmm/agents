"""
Pytest test suite for the multi-agent harness.

Verifies that all agents can be discovered, imported, and instantiated.
Run with:
    python -m pytest tests/test_harness.py -v
"""

import pytest
from harness.registry import AgentRegistry, AgentEntry
from harness.health import HealthChecker, HealthCheckResult
from harness.runner import HarnessRunner


# ── Registry Tests ───────────────────────────────────────────────


class TestAgentRegistry:
    """Tests for the agent registry."""

    def test_registry_returns_agents(self):
        """Registry should return a non-empty list of agents."""
        agents = AgentRegistry.get_all_agents()
        assert len(agents) > 0, "Registry returned no agents"

    def test_registry_has_minimum_agents(self):
        """Registry should contain at least 15 agent entries."""
        agents = AgentRegistry.get_all_agents()
        assert len(agents) >= 15, f"Expected ≥15 agents, got {len(agents)}"

    def test_all_entries_are_agent_entry(self):
        """Every returned item should be an AgentEntry."""
        for agent in AgentRegistry.get_all_agents():
            assert isinstance(agent, AgentEntry), f"{agent} is not an AgentEntry"

    def test_no_duplicate_names(self):
        """Agent names should be unique."""
        names = [a.name for a in AgentRegistry.get_all_agents()]
        assert len(names) == len(set(names)), f"Duplicate names: {[n for n in names if names.count(n) > 1]}"

    def test_categories_not_empty(self):
        """Should have multiple categories."""
        categories = AgentRegistry.get_categories()
        assert len(categories) >= 3, f"Expected ≥3 categories, got {categories}"

    def test_get_by_category(self):
        """Filtering by category should return a subset."""
        all_agents = AgentRegistry.get_all_agents()
        for cat in AgentRegistry.get_categories():
            subset = AgentRegistry.get_by_category(cat)
            assert len(subset) > 0, f"No agents in category '{cat}'"
            assert all(a.category == cat for a in subset)
            assert len(subset) <= len(all_agents)

    def test_expected_categories_present(self):
        """Specific expected categories should exist."""
        categories = AgentRegistry.get_categories()
        for expected in ["core", "voice", "productivity"]:
            assert expected in categories, f"Missing category: {expected}"


# ── Import Tests ─────────────────────────────────────────────────


def _all_agents():
    """Helper to get all agents for parametrize."""
    return AgentRegistry.get_all_agents()


class TestAgentImports:
    """Verify every registered agent can be imported."""

    @pytest.mark.parametrize(
        "agent",
        _all_agents(),
        ids=[a.name for a in _all_agents()],
    )
    def test_agent_importable(self, agent: AgentEntry):
        """Each agent module should be importable and its class should exist."""
        result = HealthChecker.import_check(agent)
        assert result.passed, f"Import failed for {agent.name}: {result.error}"


# ── Instantiation Tests ─────────────────────────────────────────


class TestAgentInstantiation:
    """Verify every registered agent can be instantiated."""

    @pytest.mark.parametrize(
        "agent",
        _all_agents(),
        ids=[a.name for a in _all_agents()],
    )
    def test_agent_instantiable(self, agent: AgentEntry):
        """
        Each agent should instantiate without crashing.

        Missing external dependencies (API keys, OAuth tokens) cause
        a skip, not a failure — the health check framework handles this.
        """
        result = HealthChecker.instantiation_check(agent)
        if result.skipped:
            pytest.skip(result.skip_reason)
        assert result.passed, f"Instantiation failed for {agent.name}: {result.error}"


# ── Capability Tests ─────────────────────────────────────────────


class TestDeterministicCapabilities:
    """Verify deterministic (no-external-dep) methods work correctly."""

    @pytest.mark.parametrize(
        "agent",
        [a for a in _all_agents() if a.deterministic_methods],
        ids=[a.name for a in _all_agents() if a.deterministic_methods],
    )
    def test_capability_methods(self, agent: AgentEntry):
        """Deterministic methods should execute and return a value."""
        results = HealthChecker.capability_check(agent)

        for result in results:
            if result.skipped:
                pytest.skip(result.skip_reason)
            assert result.passed, (
                f"Capability check '{result.check_name}' failed for "
                f"{agent.name}: {result.error}"
            )


# ── Runner Tests ─────────────────────────────────────────────────


class TestHarnessRunner:
    """Tests for the harness runner itself."""

    def test_runner_produces_results_for_all_agents(self):
        """Runner should produce results for every registered agent."""
        runner = HarnessRunner()
        results = runner.run()

        all_agents = AgentRegistry.get_all_agents()
        assert len(results) == len(all_agents), (
            f"Runner returned results for {len(results)} agents, "
            f"expected {len(all_agents)}"
        )

    def test_runner_category_filter(self):
        """Runner with category filter should only include matching agents."""
        for cat in AgentRegistry.get_categories():
            runner = HarnessRunner(category=cat)
            results = runner.run()
            expected = AgentRegistry.get_by_category(cat)
            assert len(results) == len(expected), (
                f"Category '{cat}': got {len(results)}, expected {len(expected)}"
            )

    def test_runner_exit_code_type(self):
        """Exit code should be 0 or 1."""
        runner = HarnessRunner()
        results = runner.run()
        code = runner.exit_code(results)
        assert code in (0, 1), f"Unexpected exit code: {code}"

    def test_runner_json_output(self):
        """JSON output should be valid JSON."""
        import json
        runner = HarnessRunner()
        results = runner.run()
        json_str = runner.to_json(results)
        parsed = json.loads(json_str)
        assert "agents" in parsed
        assert "summary" in parsed
        assert isinstance(parsed["summary"]["all_healthy"], bool)

    def test_runner_report_does_not_crash(self, capsys):
        """print_report should run without errors."""
        runner = HarnessRunner()
        results = runner.run()
        runner.print_report(results)
        captured = capsys.readouterr()
        assert "MULTI-AGENT HARNESS" in captured.out
        assert "SUMMARY" in captured.out
