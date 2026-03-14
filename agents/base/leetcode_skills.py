"""
LeetCode Skills - Problem solving and practice capabilities.

These skills integrate with the LeetCode MCP server to help with:
- Getting practice problems
- Working on daily challenges
- Searching for problems by topic/difficulty
- Tracking progress
"""

import asyncio
import json
import logging
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class LeetCodeSkills:
    """Skills for LeetCode problem solving and practice."""

    def __init__(self, mcp_server_path: Optional[str] = None):
        """
        Initialize LeetCode skills.

        Args:
            mcp_server_path: Path to the LeetCode MCP server (optional)
        """
        if mcp_server_path is None:
            # Default to the standard location
            mcp_server_path = str(Path(__file__).parent.parent.parent / "mcp-servers" / "leetcode" / "server.py")

        self.mcp_server_path = mcp_server_path
        self.server_available = Path(mcp_server_path).exists()

        if not self.server_available:
            logger.warning(f"LeetCode MCP server not found at {mcp_server_path}")

    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool via the server.

        Note: This is a simplified implementation. In production, you'd use
        the official MCP client library or Claude's native MCP support.
        """
        if not self.server_available:
            return {"error": "MCP server not available"}

        try:
            # For demonstration - in production use proper MCP client
            logger.info(f"Calling MCP tool: {tool_name} with args: {arguments}")

            # Placeholder - actual implementation would use MCP protocol
            return {
                "tool": tool_name,
                "arguments": arguments,
                "note": "Use Claude with MCP support to execute this tool"
            }

        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {"error": str(e)}

    async def get_problem(self, identifier: str, language: str = "python3") -> Dict[str, Any]:
        """
        Get a LeetCode problem by ID or slug.

        Args:
            identifier: Problem ID (e.g., '1', '42') or slug (e.g., 'two-sum')
            language: Programming language for starter code (default: python3)

        Returns:
            Problem details including description, starter code, examples, etc.

        Example:
            >>> problem = await skills.get_problem("1")
            >>> print(problem["title"])  # "Two Sum"
            >>> print(problem["difficulty"])  # "Easy"
        """
        return await self._call_mcp_tool(
            "get_leetcode_problem",
            {"identifier": identifier, "language": language}
        )

    async def get_daily_challenge(self) -> Dict[str, Any]:
        """
        Get today's LeetCode daily challenge.

        Returns:
            Daily challenge details including problem info and URL

        Example:
            >>> daily = await skills.get_daily_challenge()
            >>> print(daily["title"])
            >>> print(daily["difficulty"])
        """
        return await self._call_mcp_tool("get_daily_leetcode", {})

    async def search_problems(
        self,
        difficulty: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for LeetCode problems by difficulty and/or tags.

        Args:
            difficulty: Problem difficulty ('easy', 'medium', or 'hard')
            tags: List of topic tags (e.g., ['array', 'hash-table', 'two-pointers'])
            limit: Maximum number of results (default: 10, max: 50)

        Returns:
            List of matching problems with basic info

        Example:
            >>> problems = await skills.search_problems(
            ...     difficulty="medium",
            ...     tags=["array", "dynamic-programming"],
            ...     limit=5
            ... )
            >>> for p in problems:
            ...     print(f"{p['id']}: {p['title']} - {p['difficulty']}")
        """
        args = {"limit": limit}
        if difficulty:
            args["difficulty"] = difficulty
        if tags:
            args["tags"] = tags

        return await self._call_mcp_tool("search_leetcode_problems", args)

    async def get_hints(self, identifier: str) -> Dict[str, Any]:
        """
        Get hints for a LeetCode problem.

        Args:
            identifier: Problem ID or slug

        Returns:
            List of hints to help solve the problem

        Example:
            >>> hints = await skills.get_hints("two-sum")
            >>> for i, hint in enumerate(hints["hints"], 1):
            ...     print(f"Hint {i}: {hint}")
        """
        return await self._call_mcp_tool("get_leetcode_hints", {"identifier": identifier})

    async def get_stats(self, identifier: str) -> Dict[str, Any]:
        """
        Get statistics for a LeetCode problem.

        Args:
            identifier: Problem ID or slug

        Returns:
            Problem statistics including acceptance rate, submissions, etc.

        Example:
            >>> stats = await skills.get_stats("1")
            >>> print(f"Acceptance Rate: {stats['acceptance_rate']}")
            >>> print(f"Total Accepted: {stats['total_accepted']}")
        """
        return await self._call_mcp_tool("get_problem_stats", {"identifier": identifier})

    async def get_practice_set(
        self,
        topic: str,
        difficulty: str = "easy",
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get a curated practice set for a specific topic.

        Args:
            topic: Topic to practice (e.g., 'array', 'binary-tree', 'dp')
            difficulty: Difficulty level (default: 'easy')
            count: Number of problems to get (default: 5)

        Returns:
            List of problems suitable for practicing the topic

        Example:
            >>> practice = await skills.get_practice_set("array", "easy", 5)
            >>> for p in practice:
            ...     print(f"Practice: {p['title']}")
        """
        return await self.search_problems(
            difficulty=difficulty,
            tags=[topic],
            limit=count
        )

    # Helper methods for common workflows

    async def start_daily_challenge(self) -> str:
        """
        Get today's daily challenge and format it for solving.

        Returns:
            Formatted challenge description ready to work on
        """
        daily = await self.get_daily_challenge()

        if "error" in daily:
            return f"Error getting daily challenge: {daily['error']}"

        # Get full problem details
        problem = await self.get_problem(str(daily.get("id", daily.get("identifier", ""))))

        if "error" in problem:
            return f"Error getting problem details: {problem['error']}"

        return f"""
📅 LeetCode Daily Challenge - {daily.get('date', 'Today')}

# {problem.get('title', 'N/A')}
**Difficulty**: {problem.get('difficulty', 'N/A')}
**Topics**: {', '.join(problem.get('topics', []))}

{problem.get('description', 'Use the MCP tool to get the full description')}

**Starter Code** ({problem.get('language', 'python3')}):
```python
{problem.get('starter_code', '# Use MCP tool to get starter code')}
```

**URL**: {problem.get('url', 'N/A')}
"""

    async def get_problem_formatted(self, identifier: str, language: str = "python3") -> str:
        """
        Get a problem formatted and ready to solve.

        Args:
            identifier: Problem ID or slug
            language: Programming language (default: python3)

        Returns:
            Formatted problem description with starter code
        """
        problem = await self.get_problem(identifier, language)

        if "error" in problem:
            return f"Error: {problem['error']}"

        hints_data = await self.get_hints(identifier)
        hints = hints_data.get("hints", [])

        return f"""
# {problem.get('id', 'N/A')}. {problem.get('title', 'N/A')}

**Difficulty**: {problem.get('difficulty', 'N/A')}
**Topics**: {', '.join(problem.get('topics', []))}
**Likes**: {problem.get('likes', 0)} | **Dislikes**: {problem.get('dislikes', 0)}

## Problem Description

{problem.get('description', 'Use MCP tool to get description')}

## Starter Code

```{language}
{problem.get('starter_code', '# Use MCP tool to get starter code')}
```

## Hints

{chr(10).join(f"{i}. {hint}" for i, hint in enumerate(hints, 1)) if hints else "No hints available"}

## Test Cases

```
{problem.get('sample_test_case', 'Use MCP tool to get test cases')}
```

**Problem URL**: {problem.get('url', 'N/A')}
"""


# Convenience functions for direct use

async def get_daily_leetcode() -> str:
    """Quick function to get today's daily challenge."""
    skills = LeetCodeSkills()
    return await skills.start_daily_challenge()


async def solve_leetcode(problem_id: str, language: str = "python3") -> str:
    """Quick function to get a problem ready to solve."""
    skills = LeetCodeSkills()
    return await skills.get_problem_formatted(problem_id, language)


async def practice_topic(topic: str, difficulty: str = "easy", count: int = 5) -> List[Dict[str, Any]]:
    """Quick function to get practice problems for a topic."""
    skills = LeetCodeSkills()
    return await skills.get_practice_set(topic, difficulty, count)
