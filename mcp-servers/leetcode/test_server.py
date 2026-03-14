#!/usr/bin/env python3
"""
Test script for the LeetCode MCP server.

This script tests the MCP tools without requiring the full MCP protocol.
"""

import asyncio
import sys
from pathlib import Path

# Add server to path
sys.path.insert(0, str(Path(__file__).parent))

from server import LeetCodeClient


async def test_get_problem():
    """Test getting a problem by slug."""
    print("\n=== Testing get_problem (two-sum) ===")
    client = LeetCodeClient()
    try:
        problem = await client.get_problem("two-sum")
        print(f"✓ Title: {problem['title']}")
        print(f"✓ Difficulty: {problem['difficulty']}")
        print(f"✓ ID: {problem['questionFrontendId']}")
        print(f"✓ Topics: {[t['name'] for t in problem.get('topicTags', [])]}")
        print(f"✓ Has starter code: {len(problem.get('codeSnippets', [])) > 0}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await client.close()


async def test_get_problem_by_id():
    """Test getting a problem by ID."""
    print("\n=== Testing get_problem_by_id (1) ===")
    client = LeetCodeClient()
    try:
        problem = await client.get_problem_by_id(1)
        print(f"✓ Title: {problem['title']}")
        print(f"✓ Should be 'Two Sum': {problem['title'] == 'Two Sum'}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await client.close()


async def test_daily_challenge():
    """Test getting daily challenge."""
    print("\n=== Testing get_daily_challenge ===")
    client = LeetCodeClient()
    try:
        daily = await client.get_daily_challenge()
        print(f"✓ Date: {daily['date']}")
        print(f"✓ Title: {daily['question']['title']}")
        print(f"✓ Difficulty: {daily['question']['difficulty']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await client.close()


async def test_search_problems():
    """Test searching problems."""
    print("\n=== Testing search_problems (medium, array) ===")
    client = LeetCodeClient()
    try:
        problems = await client.search_problems(
            difficulty="medium",
            tags=["array"],
            limit=5
        )
        print(f"✓ Found {len(problems)} problems")
        if problems:
            print(f"✓ First problem: {problems[0]['title']}")
            print(f"✓ Difficulty: {problems[0]['difficulty']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await client.close()


async def main():
    """Run all tests."""
    print("======================")
    print("LeetCode MCP Server Tests")
    print("======================")

    await test_get_problem()
    await test_get_problem_by_id()
    await test_daily_challenge()
    await test_search_problems()

    print("\n======================")
    print("All tests completed!")
    print("======================")


if __name__ == "__main__":
    asyncio.run(main())
