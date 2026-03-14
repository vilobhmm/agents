# LeetCode Integration Guide

Complete guide for integrating LeetCode functionality with Claude and OpenClaw.

## Components

1. **MCP Server** (`server.py`) - Provides LeetCode API access via MCP protocol
2. **Skills Module** (`agents/base/leetcode_skills.py`) - Python interface for OpenClaw agents
3. **Claude Skill** (`~/.claude/skills/leetcode/SKILL.md`) - Skill definition for Claude Code

## Setup

### 1. Install Dependencies

```bash
cd mcp-servers/leetcode
pip install -r requirements.txt
```

### 2. Test the MCP Server

```bash
python test_server.py
```

Expected output:
```
✓ Title: Two Sum
✓ Difficulty: Easy
✓ ID: 1
...
```

### 3. Configure Claude Desktop

Add to Claude's MCP configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/mcp.json`

```json
{
  "mcpServers": {
    "leetcode": {
      "command": "python3",
      "args": ["/home/user/agents/mcp-servers/leetcode/server.py"],
      "env": {}
    }
  }
}
```

### 4. Restart Claude

After updating the config, restart Claude Desktop for changes to take effect.

### 5. Verify in Claude

In Claude, you can now use LeetCode tools:

```
Can you get me LeetCode problem #1?
```

Claude will use the `get_leetcode_problem` tool from the MCP server.

## Usage in Claude

### Get Today's Daily Challenge

```
What's today's LeetCode daily challenge?
```

### Get a Specific Problem

```
Show me LeetCode problem 42
```

or

```
Get the "trapping-rain-water" problem
```

### Search for Problems

```
Find 5 medium difficulty array problems
```

or

```
Search for easy dynamic programming problems
```

### Get Hints

```
I'm stuck on two-sum, can I get a hint?
```

## Usage in OpenClaw Agents

### Import the Skills

```python
from agents.base.leetcode_skills import LeetCodeSkills

# Initialize
skills = LeetCodeSkills()
```

### Get Daily Challenge

```python
# Get formatted daily challenge
challenge_text = await skills.start_daily_challenge()
print(challenge_text)

# Or get raw data
daily_data = await skills.get_daily_challenge()
```

### Get a Problem

```python
# Get formatted problem ready to solve
problem_text = await skills.get_problem_formatted("two-sum", language="python3")

# Or get raw problem data
problem_data = await skills.get_problem("two-sum", language="python3")
```

### Search Problems

```python
# Search for practice problems
problems = await skills.search_problems(
    difficulty="medium",
    tags=["array", "hash-table"],
    limit=10
)

for p in problems:
    print(f"{p['id']}: {p['title']} - {p['difficulty']}")
```

### Get Practice Set

```python
# Get curated practice problems for a topic
practice_problems = await skills.get_practice_set(
    topic="dynamic-programming",
    difficulty="easy",
    count=5
)
```

## Example: Interview Prep Agent

```python
from agents.base.leetcode_skills import LeetCodeSkills
from openclaw.core.agent import Agent, AgentConfig

class InterviewPrepAgent(Agent):
    """Agent to help with coding interview preparation."""

    def __init__(self):
        config = AgentConfig(
            name="Interview Prep Coach",
            description="Helps you prepare for coding interviews with LeetCode",
            model="claude-sonnet-4-5-20250929"
        )
        super().__init__(config)
        self.leetcode = LeetCodeSkills()

    async def daily_practice(self):
        """Start daily practice routine."""
        # Get today's challenge
        challenge = await self.leetcode.start_daily_challenge()

        # Present to user
        response = await self.chat(
            f"Here's today's practice problem:\\n\\n{challenge}\\n\\n"
            f"Would you like to start solving this, or would you prefer "
            f"a different problem?"
        )

        return response

    async def topic_practice(self, topic: str, difficulty: str = "easy"):
        """Practice a specific topic."""
        problems = await self.leetcode.get_practice_set(
            topic=topic,
            difficulty=difficulty,
            count=3
        )

        # Format problem list
        problem_list = "\\n".join([
            f"{i+1}. {p['title']} ({p['difficulty']})"
            for i, p in enumerate(problems)
        ])

        response = await self.chat(
            f"Here are some {difficulty} {topic} problems to practice:\\n\\n"
            f"{problem_list}\\n\\n"
            f"Which one would you like to start with?"
        )

        return response

    async def provide_hint(self, problem_id: str, hint_level: int = 1):
        """Provide progressive hints."""
        hints_data = await self.leetcode.get_hints(problem_id)
        hints = hints_data.get("hints", [])

        if not hints or hint_level > len(hints):
            return "No more hints available. Try thinking about the problem differently!"

        hint = hints[hint_level - 1]
        return f"**Hint {hint_level}**: {hint}"


# Usage
async def main():
    agent = InterviewPrepAgent()

    # Daily practice
    await agent.daily_practice()

    # Topic-specific practice
    await agent.topic_practice("array", "medium")

    # Get hints
    hint = await agent.provide_hint("two-sum", hint_level=1)
    print(hint)
```

## Example: Study Plan Generator

```python
async def create_study_plan(topics: List[str], days: int = 7):
    """Generate a week-long study plan."""
    skills = LeetCodeSkills()
    plan = {}

    for day, topic in enumerate(topics[:days], 1):
        problems = await skills.get_practice_set(
            topic=topic,
            difficulty="easy",  # Start with easy
            count=2
        )

        plan[f"Day {day}"] = {
            "topic": topic,
            "problems": problems
        }

    return plan


# Usage
topics = ["array", "hash-table", "two-pointers", "binary-search",
          "linked-list", "stack", "queue"]
plan = await create_study_plan(topics, days=7)
```

## Available MCP Tools

All tools are accessible via the MCP server:

1. **get_leetcode_problem** - Get problem by ID/slug
2. **get_daily_leetcode** - Today's challenge
3. **search_leetcode_problems** - Search by difficulty/tags
4. **get_leetcode_hints** - Get problem hints
5. **get_problem_stats** - Get statistics

## Skill Integration

The skill is automatically available in Claude Code:

```
/leetcode
```

This will invoke the LeetCode skill and you can ask for problems, hints, etc.

## Troubleshooting

### MCP Server Not Found

Ensure the path in your MCP config points to the correct location:

```bash
ls /home/user/agents/mcp-servers/leetcode/server.py
```

### Dependencies Missing

Install required packages:

```bash
pip install mcp httpx
```

### LeetCode API Issues

The server uses LeetCode's public GraphQL API. If you get errors:

1. Check your internet connection
2. Verify LeetCode.com is accessible
3. Check rate limiting (add delays between requests)

### Skills Not Appearing

1. Verify skill file exists: `~/.claude/skills/leetcode/SKILL.md`
2. Restart Claude
3. Check skill syntax in SKILL.md

## Advanced Usage

### Custom Language Support

Get problems in different languages:

```python
# JavaScript
problem = await skills.get_problem("two-sum", language="javascript")

# C++
problem = await skills.get_problem("two-sum", language="cpp")

# Java
problem = await skills.get_problem("two-sum", language="java")
```

### Batch Problem Fetching

```python
async def get_multiple_problems(problem_ids: List[str]):
    """Fetch multiple problems concurrently."""
    skills = LeetCodeSkills()

    tasks = [
        skills.get_problem(pid, language="python3")
        for pid in problem_ids
    ]

    problems = await asyncio.gather(*tasks)
    return problems


# Usage
problems = await get_multiple_problems(["1", "2", "3", "15", "42"])
```

### Custom Search Queries

```python
# Hard graph problems
graph_problems = await skills.search_problems(
    difficulty="hard",
    tags=["graph", "breadth-first-search"],
    limit=20
)

# Easy problems for beginners
beginner_problems = await skills.search_problems(
    difficulty="easy",
    tags=["array"],
    limit=50
)
```

## Contributing

To add new features to the MCP server:

1. Edit `server.py`
2. Add new tool definitions in `list_tools()`
3. Implement handlers in `call_tool()`
4. Update the README and this integration guide
5. Add corresponding methods to `leetcode_skills.py`
6. Update SKILL.md with new capabilities

## License

MIT
