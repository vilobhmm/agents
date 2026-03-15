---
name: leetcode
description: Get LeetCode problems, practice coding challenges, and work on daily challenges. Use when user wants to solve LeetCode problems, practice algorithms, or get coding interview questions.
---

# LeetCode Problem Solving Skill

Help users solve LeetCode problems, practice algorithms, and prepare for coding interviews.

## Available MCP Tools

This skill uses the LeetCode MCP server which provides the following tools:

### 1. get_leetcode_problem
Get a specific LeetCode problem by ID or slug.

**Arguments:**
- `identifier` (required): Problem ID (e.g., "1", "42") or slug (e.g., "two-sum", "trapping-rain-water")
- `language` (optional): Programming language for starter code (default: "python3")

**Returns:** Problem details including:
- Title, ID, difficulty
- Full problem description with examples
- Topic tags
- Starter code in requested language
- Sample test cases
- Problem URL

**Example:**
```json
{
  "tool": "get_leetcode_problem",
  "arguments": {
    "identifier": "1",
    "language": "python3"
  }
}
```

### 2. get_daily_leetcode
Get today's LeetCode daily challenge.

**Arguments:** None

**Returns:** Daily challenge info including problem details and date

**Example:**
```json
{
  "tool": "get_daily_leetcode",
  "arguments": {}
}
```

### 3. search_leetcode_problems
Search for problems by difficulty and/or topic tags.

**Arguments:**
- `difficulty` (optional): "easy", "medium", or "hard"
- `tags` (optional): Array of topic tags (e.g., ["array", "hash-table", "dynamic-programming"])
- `limit` (optional): Max results, 1-50 (default: 10)

**Returns:** List of matching problems with basic info

**Example:**
```json
{
  "tool": "search_leetcode_problems",
  "arguments": {
    "difficulty": "medium",
    "tags": ["array", "two-pointers"],
    "limit": 5
  }
}
```

### 4. get_leetcode_hints
Get hints for a problem to help solve it step-by-step.

**Arguments:**
- `identifier` (required): Problem ID or slug

**Returns:** List of progressive hints

**Example:**
```json
{
  "tool": "get_leetcode_hints",
  "arguments": {
    "identifier": "two-sum"
  }
}
```

### 5. get_problem_stats
Get statistics for a problem (acceptance rate, submissions, etc.).

**Arguments:**
- `identifier` (required): Problem ID or slug

**Returns:** Problem statistics

**Example:**
```json
{
  "tool": "get_problem_stats",
  "arguments": {
    "identifier": "1"
  }
}
```

## Common Workflows

### Daily Challenge Workflow

When user asks for today's daily challenge:

1. Use `get_daily_leetcode` to get today's challenge
2. Use `get_leetcode_problem` with the problem ID to get full details
3. Present the problem in a clear format with:
   - Title and difficulty
   - Problem description
   - Starter code
   - Examples and constraints
4. Ask if they want hints or help solving it

### Practice by Topic Workflow

When user wants to practice a specific topic (e.g., "practice array problems"):

1. Use `search_leetcode_problems` with appropriate tags
2. Present a list of problems sorted by difficulty
3. Ask which problem they'd like to work on
4. Use `get_leetcode_problem` to get full details

### Problem Solving Workflow

When user asks for a specific problem (e.g., "get problem 42" or "show me two-sum"):

1. Use `get_leetcode_problem` with the identifier
2. Present the complete problem with starter code
3. Offer to show hints if they get stuck
4. Help them work through the solution step-by-step

### Hint System Workflow

When user is stuck:

1. Use `get_leetcode_hints` to get available hints
2. Reveal hints progressively (one at a time)
3. Only show the next hint if they're still stuck
4. Guide them toward the solution without giving it away

## Output Formatting

Present problems in a clear, readable format:

```markdown
# {problem_id}. {title}

**Difficulty**: {difficulty}
**Topics**: {comma-separated tags}
**Acceptance Rate**: {rate}%

## Problem Description

{description with examples and constraints}

## Starter Code

​```{language}
{starter_code}
​```

## Examples

{formatted examples from description}

## Hints

1. {hint 1}
2. {hint 2}
...

**Problem Link**: {url}
```

## Tips

1. **Be Progressive**: Don't give away solutions immediately. Start with hints.

2. **Explain Concepts**: When helping solve problems, explain the algorithmic concepts and patterns.

3. **Multiple Approaches**: Discuss different approaches (brute force, optimal, trade-offs).

4. **Time/Space Complexity**: Help users analyze complexity of their solutions.

5. **Test Cases**: Help users think about edge cases and test their solutions.

6. **Practice Plans**: For practice requests, create curated lists by difficulty progression.

## Common Topics

Popular topic tags to search:
- `array`, `string`, `hash-table`, `linked-list`
- `binary-tree`, `binary-search`, `graph`
- `dynamic-programming`, `backtracking`, `greedy`
- `two-pointers`, `sliding-window`, `stack`, `queue`
- `depth-first-search`, `breadth-first-search`
- `math`, `bit-manipulation`, `sorting`

## MCP Server Setup

The LeetCode MCP server must be configured in Claude's MCP settings:

**Location**: `~/.config/claude/mcp.json` or Claude desktop config

**Configuration**:
```json
{
  "mcpServers": {
    "leetcode": {
      "command": "python3",
      "args": ["/path/to/mcp-servers/leetcode/server.py"]
    }
  }
}
```

## Examples

### Example 1: Daily Challenge

**User**: "What's today's LeetCode daily challenge?"

**Response**:
1. Call `get_daily_leetcode`
2. Call `get_leetcode_problem` with the problem ID
3. Present formatted problem
4. Ask if they want to start solving or need hints

### Example 2: Practice Topic

**User**: "I want to practice medium array problems"

**Response**:
1. Call `search_leetcode_problems(difficulty="medium", tags=["array"], limit=10)`
2. Present list of 10 problems
3. Ask which one they'd like to work on
4. When they choose, get full problem details

### Example 3: Specific Problem

**User**: "Show me problem 3"

**Response**:
1. Call `get_leetcode_problem(identifier="3", language="python3")`
2. Present full problem with starter code
3. Offer to help with hints or discuss approach

### Example 4: Getting Hints

**User**: "I'm stuck on two-sum, can I get a hint?"

**Response**:
1. Call `get_leetcode_hints(identifier="two-sum")`
2. Show first hint only
3. Ask if they need another hint
4. Continue revealing progressively

## Integration with OpenClaw

This skill can be used in OpenClaw agents via the LeetCodeSkills class:

```python
from agents.base.leetcode_skills import LeetCodeSkills

# In your agent
skills = LeetCodeSkills()

# Get daily challenge
daily = await skills.get_daily_challenge()

# Get a specific problem
problem = await skills.get_problem("1", language="python3")

# Search for problems
problems = await skills.search_problems(
    difficulty="medium",
    tags=["array", "dynamic-programming"],
    limit=5
)
```

## Notes

- Problems are fetched from LeetCode's public GraphQL API
- No authentication required for fetching problems
- Submitting solutions requires LeetCode account (not yet implemented)
- All tools return JSON data that should be formatted for readability
