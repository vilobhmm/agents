"""
Implementation & Code Review Module.

Capabilities: code review, refactoring plans, debugging strategy, PR checklists.
"""

import os, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SWEImplementation:
    """Implementation and code review capabilities."""

    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False

    async def code_review(self, code: str, context: str = "") -> Dict:
        """Review code for quality, correctness, and best practices."""
        prompt = f"""Review this code:

Context: {context}

```
{code}
```

Provide severity-rated feedback:
1. **🔴 Critical**: Bugs, security issues, data loss risks
2. **🟡 Important**: Performance issues, error handling gaps, design concerns
3. **🟢 Suggestions**: Style, readability, best practices
4. **✅ Strengths**: What's well done
5. **Summary**: Overall assessment and top 3 action items"""

        response = await self._ask_claude(prompt, "You are a senior engineer doing a thorough code review.")
        return {"review": response, "timestamp": datetime.now().isoformat()}

    async def refactoring_plan(self, codebase_desc: str) -> Dict:
        """Create a systematic refactoring plan."""
        prompt = f"""Create a refactoring plan for this codebase:

{codebase_desc}

Provide:
1. **Current Issues**: What needs refactoring and why
2. **Priority Order**: Which refactors to do first (safety, impact, effort)
3. **Phase 1 (Quick Wins)**: Safe, high-impact changes (< 1 day each)
4. **Phase 2 (Medium Effort)**: Structural improvements (1-3 days each)
5. **Phase 3 (Major)**: Large-scale changes (need design doc)
6. **Risk Assessment**: What could break during refactoring
7. **Testing Strategy**: How to validate each refactoring step
8. **Migration Guide**: How to do changes without breaking production"""

        response = await self._ask_claude(prompt, "You are a senior engineer planning a safe, incremental refactoring.")
        return {"refactoring_plan": response, "timestamp": datetime.now().isoformat()}

    async def debug_strategy(self, bug_description: str) -> Dict:
        """Create a systematic debugging strategy."""
        prompt = f"""Create a debugging strategy for:

{bug_description}

Provide:
1. **Hypothesis List**: Ranked most-to-least likely causes
2. **Investigation Steps**: For each hypothesis, what to check
3. **Data to Collect**: Logs, metrics, traces to examine
4. **Reproduction Steps**: How to reliably reproduce
5. **Isolation Strategy**: How to narrow down the cause
6. **Fix Approach**: Once root cause is found, how to fix safely
7. **Verification**: How to confirm the fix works
8. **Prevention**: How to prevent this class of bugs in the future"""

        response = await self._ask_claude(prompt, "You are a debugging expert and SRE.")
        return {"strategy": response, "timestamp": datetime.now().isoformat()}

    async def pr_review_checklist(self, pr_description: str) -> Dict:
        """Generate a customized PR review checklist."""
        prompt = f"""Create a PR review checklist for:

{pr_description}

Checklist categories:
1. **Correctness**: Logic, edge cases, error handling
2. **Security**: Auth, input validation, data exposure
3. **Performance**: N+1 queries, caching, memory leaks
4. **Testing**: Coverage, edge cases, integration tests
5. **Observability**: Logging, metrics, alerting
6. **Documentation**: Comments, README updates, API docs
7. **Backwards Compatibility**: Breaking changes, migrations
8. **Code Quality**: Naming, structure, SOLID principles"""

        response = await self._ask_claude(prompt, "You are a tech lead reviewing a PR.")
        return {"checklist": response, "timestamp": datetime.now().isoformat()}

    async def _ask_claude(self, prompt: str, system: str) -> str:
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."
        try:
            r = self.claude.messages.create(model="claude-sonnet-4-5-20250929", max_tokens=4000, system=system, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"
