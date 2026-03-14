#!/usr/bin/env python3
"""
Example: Using LeetCode Skills in OpenClaw

This example shows how to use the LeetCode skills to create
an interview preparation assistant.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base.leetcode_skills import LeetCodeSkills


async def example_1_daily_challenge():
    """Example 1: Get and display today's daily challenge."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Today's Daily Challenge")
    print("="*60)

    skills = LeetCodeSkills()

    # Get today's challenge formatted and ready to solve
    challenge = await skills.start_daily_challenge()

    print(challenge)


async def example_2_specific_problem():
    """Example 2: Get a specific problem by ID."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Get Problem #1 (Two Sum)")
    print("="*60)

    skills = LeetCodeSkills()

    # Get problem formatted for solving
    problem = await skills.get_problem_formatted("1", language="python3")

    print(problem)


async def example_3_search_and_practice():
    """Example 3: Search for problems and create practice set."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Practice Easy Array Problems")
    print("="*60)

    skills = LeetCodeSkills()

    # Get a practice set
    problems = await skills.get_practice_set(
        topic="array",
        difficulty="easy",
        count=5
    )

    print(f"\n📚 Found {len(problems)} practice problems:\n")

    for i, problem in enumerate(problems, 1):
        print(f"{i}. {problem['title']}")
        print(f"   Difficulty: {problem['difficulty']}")
        print(f"   Topics: {', '.join(problem['topics'])}")
        print(f"   URL: {problem['url']}")
        print()


async def example_4_progressive_hints():
    """Example 4: Get hints for a problem progressively."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Progressive Hints for Two Sum")
    print("="*60)

    skills = LeetCodeSkills()

    # Get hints for a problem
    hints_data = await skills.get_hints("two-sum")

    print(f"\n💡 Hints for: {hints_data['title']}\n")

    for i, hint in enumerate(hints_data.get('hints', []), 1):
        print(f"Hint {i}: {hint}")
        print()


async def example_5_study_plan():
    """Example 5: Create a weekly study plan."""
    print("\n" + "="*60)
    print("EXAMPLE 5: 7-Day Study Plan")
    print("="*60)

    skills = LeetCodeSkills()

    # Topics to cover
    topics = [
        "array",
        "hash-table",
        "two-pointers",
        "binary-search",
        "linked-list",
        "stack",
        "dynamic-programming"
    ]

    print("\n📅 Your 7-Day Interview Prep Plan:\n")

    for day, topic in enumerate(topics, 1):
        problems = await skills.get_practice_set(
            topic=topic,
            difficulty="easy",
            count=2
        )

        print(f"Day {day}: {topic.replace('-', ' ').title()}")
        for p in problems:
            print(f"  • {p['title']} ({p['difficulty']})")
        print()


async def example_6_problem_stats():
    """Example 6: Get statistics for a problem."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Problem Statistics")
    print("="*60)

    skills = LeetCodeSkills()

    # Get stats for a popular problem
    stats = await skills.get_stats("two-sum")

    print(f"\n📊 Statistics for: {stats['title']}\n")
    print(f"Total Accepted: {stats.get('total_accepted', 'N/A')}")
    print(f"Total Submissions: {stats.get('total_submissions', 'N/A')}")
    print(f"Acceptance Rate: {stats.get('acceptance_rate', 'N/A')}")
    print(f"Likes: {stats.get('likes', 0)}")
    print(f"Dislikes: {stats.get('dislikes', 0)}")
    print()


async def example_7_interview_prep_agent():
    """Example 7: Simple interview prep assistant."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Interview Prep Assistant")
    print("="*60)

    skills = LeetCodeSkills()

    # Simulate an interactive session
    print("\n🤖 Interview Prep Assistant: Hello! Let's practice coding!")
    print("\nI recommend starting with today's daily challenge.")
    print("It's a great way to stay consistent.\n")

    # Get daily challenge
    daily = await skills.get_daily_challenge()

    print(f"📅 Today's Challenge: {daily.get('title', 'N/A')}")
    print(f"   Difficulty: {daily.get('difficulty', 'N/A')}")
    print(f"   Topics: {', '.join([t['name'] for t in daily.get('topics', [])])}")
    print(f"   URL: {daily.get('url', 'N/A')}")

    print("\n🤖 Would you like to:")
    print("   1. Start solving this problem")
    print("   2. Get hints")
    print("   3. See statistics")
    print("   4. Search for different problems")

    # Simulate choosing option 2 (hints)
    print("\n[User chooses: 2 - Get hints]\n")

    hints_data = await skills.get_hints(str(daily.get('id', '')))
    hints = hints_data.get('hints', [])

    if hints:
        print(f"💡 Hint 1: {hints[0]}")
        print("\n🤖 Take your time! Let me know if you need another hint.")
    else:
        print("🤖 No hints available for this problem. Try breaking it down!")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("LeetCode Skills Examples")
    print("="*60)
    print("\nNOTE: These examples require the LeetCode MCP server")
    print("to be running and accessible.")
    print("\nIn this demo mode, tool calls will return placeholder data.")
    print("="*60)

    # Run examples
    await example_1_daily_challenge()
    await example_2_specific_problem()
    await example_3_search_and_practice()
    await example_4_progressive_hints()
    await example_5_study_plan()
    await example_6_problem_stats()
    await example_7_interview_prep_agent()

    print("\n" + "="*60)
    print("Examples Complete!")
    print("="*60)
    print("\nTo use these skills in production:")
    print("1. Configure the MCP server in Claude")
    print("2. Use the /leetcode skill in Claude Code")
    print("3. Import LeetCodeSkills in your OpenClaw agents")
    print("\nSee INTEGRATION.md for full setup guide.")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
