# LeetCode Skill for Claude Code

> 🚀 Practice coding interviews with LeetCode problems directly in Claude Code

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)
![MCP: Compatible](https://img.shields.io/badge/MCP-Compatible-purple.svg)

## Overview

The LeetCode skill brings coding interview preparation directly into Claude Code. Get problems, search by topic, receive progressive hints, and practice algorithms without leaving your development environment.

**No LeetCode login required** - uses the public API!

## ✨ Features

- 📅 **Daily Challenge** - Get today's LeetCode daily challenge
- 🔍 **Smart Search** - Find problems by difficulty, topic, or tags
- 💡 **Progressive Hints** - Get hints one at a time without spoilers
- 📊 **Statistics** - View acceptance rates and problem stats
- 🌐 **Multi-Language** - Starter code in Python, JavaScript, C++, Java, and more
- 🎯 **Practice Sets** - Curated problem sets for focused practice

## 🚀 Quick Start

### Installation

1. **Install the MCP server:**
```bash
cd mcp-servers/leetcode
pip install -r requirements.txt
```

2. **Configure Claude:**

Add to your MCP config (`~/.config/claude/mcp.json`):
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

3. **Restart Claude**

4. **Start practicing!**

### Usage

Use the `/leetcode` command or ask naturally:

```
/leetcode what's today's daily challenge?
```

```
Show me LeetCode problem 42
```

```
Find 5 medium array problems
```

```
I'm stuck on two-sum, can I get a hint?
```

## 🎯 Use Cases

### 1. Daily Practice
Start each day with a challenge:
```
What's today's LeetCode challenge?
```

### 2. Topic-Focused Practice
Master specific algorithms:
```
Find easy dynamic programming problems
```

### 3. Interview Preparation
Create custom study plans:
```
I need to practice arrays and hash tables
```

### 4. Learning with Hints
Get unstuck without spoilers:
```
Give me a hint for problem 3
```

## 🛠️ Available Tools

### get_leetcode_problem
Get any problem with full details and starter code.

**Example:**
```json
{
  "identifier": "two-sum",
  "language": "python3"
}
```

### get_daily_leetcode
Today's daily coding challenge.

### search_leetcode_problems
Search by difficulty and topics.

**Example:**
```json
{
  "difficulty": "medium",
  "tags": ["array", "two-pointers"],
  "limit": 5
}
```

### get_leetcode_hints
Progressive hints for any problem.

### get_problem_stats
View statistics and acceptance rates.

## 📚 Examples

### Daily Challenge Workflow
```
User: What's today's LeetCode daily challenge?

Claude: 📅 Today's LeetCode Daily Challenge

Problem #42: Trapping Rain Water
Difficulty: Hard
Topics: Array, Two Pointers, Dynamic Programming

[Full problem description with examples]
[Starter code in Python]
[Test cases]

Ready to start? I can provide hints if you get stuck!
```

### Search and Practice
```
User: I want to practice medium array problems

Claude: I found 10 medium array problems for you:

1. 3Sum (Medium) - Array, Two Pointers
2. Container With Most Water (Medium) - Array, Greedy
3. Product of Array Except Self (Medium) - Array, Prefix Sum
...

Which one would you like to work on?
```

### Progressive Hints
```
User: I'm stuck on two-sum

Claude: 💡 Hint 1: A brute force solution using nested loops would work, but can we do better than O(n²)?

[User tries again]

User: Still stuck, another hint?

Claude: 💡 Hint 2: What if we stored the numbers we've seen in a hash table? We could look up the complement in O(1) time.
```

## 🔧 Integration

### For Claude Code Users
Simply use the `/leetcode` skill command.

### For OpenClaw Agents
```python
from agents.base.leetcode_skills import LeetCodeSkills

skills = LeetCodeSkills()

# Get daily challenge
daily = await skills.get_daily_challenge()

# Create study plan
problems = await skills.get_practice_set("array", "easy", 5)

# Get hints
hints = await skills.get_hints("two-sum")
```

## 📖 Documentation

- **[Full Integration Guide](INTEGRATION.md)** - Complete setup and usage
- **[MCP Server README](../../mcp-servers/leetcode/README.md)** - Server details
- **[Examples](../../examples/leetcode_example.py)** - 7 complete examples

## 🎓 Learning Path

Recommended topics for interview prep:

**Week 1: Foundations**
- Arrays
- Strings
- Hash Tables

**Week 2: Linear Structures**
- Linked Lists
- Stacks & Queues

**Week 3: Trees & Graphs**
- Binary Trees
- Graph Traversal (DFS/BFS)

**Week 4: Advanced**
- Dynamic Programming
- Backtracking
- Greedy Algorithms

Use this skill to practice each topic systematically!

## 🤝 Contributing

Contributions welcome! To add features:

1. Fork the repository
2. Add your feature to `server.py`
3. Update documentation
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- Uses LeetCode's public GraphQL API
- Part of the [OpenClaw](https://github.com/vilobhmm/agents) agent ecosystem

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/vilobhmm/agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vilobhmm/agents/discussions)

---

**Built with ❤️ by the OpenClaw team**

Start practicing: `/leetcode`
