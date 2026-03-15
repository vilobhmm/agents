# LeetCode Skill Submission Package

## Skill Information

**Name:** LeetCode
**Version:** 1.0.0
**Category:** Development / Education
**Author:** OpenClaw Team
**License:** MIT

## Description

Complete LeetCode integration for Claude Code enabling coding interview practice with:
- Problem fetching by ID or topic
- Daily challenges
- Progressive hints
- Multi-language support
- No authentication required

## Submission Checklist

### ✅ Core Components

- [x] **SKILL.md** - Skill definition with frontmatter
- [x] **package.json** - Metadata and dependencies
- [x] **README.md** - User-facing documentation
- [x] **MCP Server** (`../../mcp-servers/leetcode/server.py`)
- [x] **Requirements** (`../../mcp-servers/leetcode/requirements.txt`)
- [x] **Tests** (`../../mcp-servers/leetcode/test_server.py`)
- [x] **Examples** (`../../examples/leetcode_example.py`)
- [x] **Integration Guide** (`../../mcp-servers/leetcode/INTEGRATION.md`)

### ✅ Documentation

- [x] Installation instructions
- [x] Usage examples
- [x] MCP server setup guide
- [x] API documentation
- [x] Troubleshooting guide
- [x] Contributing guidelines

### ✅ Code Quality

- [x] Python 3.8+ compatible
- [x] Async/await architecture
- [x] Error handling
- [x] Type hints
- [x] Logging
- [x] Test suite

### ✅ MCP Compliance

- [x] Implements MCP protocol (stdio)
- [x] Tool definitions with schemas
- [x] Proper error responses
- [x] TextContent responses

### ✅ Security

- [x] No hardcoded credentials
- [x] Uses public API only
- [x] Input validation
- [x] Safe error messages

## Files Included

```
.skill-hub/leetcode/
├── SKILL.md              # Skill definition
├── package.json          # Metadata
├── README.md            # User documentation
└── SUBMISSION.md        # This file

../../mcp-servers/leetcode/
├── server.py            # MCP server implementation
├── test_server.py       # Test suite
├── requirements.txt     # Python dependencies
├── mcp-config.json      # Configuration example
├── README.md           # Technical documentation
└── INTEGRATION.md      # Integration guide

../../agents/base/
└── leetcode_skills.py  # OpenClaw integration

../../examples/
└── leetcode_example.py # Usage examples
```

## Installation & Testing

### Install
```bash
cd mcp-servers/leetcode
pip install -r requirements.txt
```

### Test
```bash
python test_server.py
```

### Configure
Add to `~/.config/claude/mcp.json`:
```json
{
  "mcpServers": {
    "leetcode": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-servers/leetcode/server.py"]
    }
  }
}
```

### Verify
```
/leetcode what's today's daily challenge?
```

## Tools Provided

1. **get_leetcode_problem**
   - Input: identifier (ID/slug), language (optional)
   - Output: Full problem with description, code, examples

2. **get_daily_leetcode**
   - Input: none
   - Output: Today's daily challenge

3. **search_leetcode_problems**
   - Input: difficulty, tags, limit
   - Output: List of matching problems

4. **get_leetcode_hints**
   - Input: identifier
   - Output: Progressive hints

5. **get_problem_stats**
   - Input: identifier
   - Output: Statistics and acceptance rate

## API Dependencies

- **LeetCode GraphQL API** (public, no auth)
- **Dependencies:** mcp>=0.9.0, httpx>=0.27.0
- **Python:** 3.8+

## Example Queries

```
What's today's LeetCode daily challenge?
Show me problem 42
Find 5 medium array problems
I'm stuck on two-sum, can I get a hint?
Search for easy dynamic programming problems
Get stats for problem 1
```

## Screenshots / Demos

### Daily Challenge Flow
```
User: What's today's LeetCode daily challenge?

Claude: [Uses get_daily_leetcode MCP tool]

📅 LeetCode Daily Challenge - 2024-03-14

# 42. Trapping Rain Water
**Difficulty**: Hard
**Topics**: Array, Two Pointers, Dynamic Programming

[Full problem description...]

**Starter Code** (python3):
def trap(self, height: List[int]) -> int:
    # Your code here
    pass

**URL**: https://leetcode.com/problems/trapping-rain-water/
```

### Search Flow
```
User: Find medium array problems

Claude: [Uses search_leetcode_problems MCP tool]

Found 10 medium array problems:

1. 3Sum - Array, Two Pointers (47.3% acceptance)
2. Container With Most Water - Array, Greedy (54.1% acceptance)
3. Product of Array Except Self - Array, Prefix Sum (66.8% acceptance)
...
```

### Hint Flow
```
User: I need a hint for two-sum

Claude: [Uses get_leetcode_hints MCP tool]

💡 Hints for Two Sum:

1. A brute force solution would use nested loops...
2. What if we used a hash table to store values?
3. For each number, check if target - number exists in the hash table
```

## Support & Maintenance

- **Repository:** https://github.com/vilobhmm/agents
- **Issues:** https://github.com/vilobhmm/agents/issues
- **Maintained by:** OpenClaw Team
- **Update frequency:** Active development

## License

MIT License - Free for personal and commercial use

## Submission Contact

**GitHub:** vilobhmm
**Repository:** https://github.com/vilobhmm/agents
**Branch:** claude/openclaw-weekend-projects-st5pW

## Additional Notes

This skill is part of the larger OpenClaw agent ecosystem and integrates seamlessly with:
- Claude Code (via MCP)
- OpenClaw agents (via LeetCodeSkills class)
- Custom agent implementations

The skill has been tested with Claude Sonnet 4.5 and works across platforms (macOS, Linux, Windows).

---

**Submission Date:** March 14, 2024
**Version:** 1.0.0
**Status:** Ready for review
