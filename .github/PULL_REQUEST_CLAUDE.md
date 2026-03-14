# Add LeetCode MCP Server and Skill

## Overview

This PR adds a complete LeetCode integration for Claude Code, enabling users to practice coding interviews directly within Claude.

## What's New

### MCP Server
A Model Context Protocol server providing 5 LeetCode tools:
- `get_leetcode_problem` - Fetch any problem by ID/slug
- `get_daily_leetcode` - Get today's daily challenge
- `search_leetcode_problems` - Search by difficulty/topic
- `get_leetcode_hints` - Progressive hints system
- `get_problem_stats` - View statistics

### Claude Skill
Native `/leetcode` skill with:
- Natural language interface
- Complete documentation
- Workflow guides
- Example queries

### Key Features
✅ No LeetCode login required (uses public API)
✅ Multi-language support (Python, JS, C++, Java, etc.)
✅ Progressive hints without spoilers
✅ Daily challenge integration
✅ Topic-based search
✅ Problem statistics

## Installation

```bash
# Install dependencies
pip install mcp httpx

# Add to Claude MCP config
{
  "mcpServers": {
    "leetcode": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## Usage Examples

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

## Files Added

### Core Server
- `mcp-servers/leetcode/server.py` - MCP server implementation
- `mcp-servers/leetcode/requirements.txt` - Dependencies
- `mcp-servers/leetcode/test_server.py` - Test suite

### Documentation
- `mcp-servers/leetcode/README.md` - Server documentation
- `mcp-servers/leetcode/INTEGRATION.md` - Integration guide
- `mcp-servers/leetcode/mcp-config.json` - Config example

### Skill Definition
- `.skill-hub/leetcode/SKILL.md` - Skill definition
- `.skill-hub/leetcode/package.json` - Metadata
- `.skill-hub/leetcode/README.md` - User docs

### Examples
- `examples/leetcode_example.py` - 7 complete examples

## Technical Details

**Protocol:** Model Context Protocol (stdio)
**API:** LeetCode GraphQL (public, no auth)
**Runtime:** Python 3.8+
**Dependencies:** mcp>=0.9.0, httpx>=0.27.0
**Architecture:** Async/await throughout

## Testing

```bash
cd mcp-servers/leetcode
pip install -r requirements.txt
python test_server.py
```

All tests pass:
- ✓ Get problem by slug
- ✓ Get problem by ID
- ✓ Get daily challenge
- ✓ Search problems

## MCP Compliance

- [x] Implements stdio transport
- [x] Tool definitions with JSON schemas
- [x] TextContent responses
- [x] Error handling
- [x] Logging

## Security

- [x] No hardcoded credentials
- [x] Public API only
- [x] Input validation
- [x] Safe error messages

## Documentation

- [x] README with installation
- [x] Integration guide
- [x] API documentation
- [x] Usage examples
- [x] Troubleshooting

## Benefits

1. **Interview Prep** - Practice coding interviews in Claude
2. **Daily Practice** - Consistent daily challenges
3. **Topic Mastery** - Focus on specific algorithms
4. **Progressive Learning** - Hints without spoilers
5. **No Setup** - No LeetCode account needed

## Use Cases

### Students
Practice for technical interviews with AI assistance

### Professionals
Keep skills sharp with daily challenges

### Educators
Create custom problem sets for students

### Agents
Build interview prep bots and study assistants

## Future Enhancements

Potential additions:
- Solution submission (with auth)
- User profile tracking
- Discussion integration
- Similar problem recommendations
- Progress tracking

## Checklist

- [x] Code tested and working
- [x] Documentation complete
- [x] Examples provided
- [x] MCP compliant
- [x] No breaking changes
- [x] Security reviewed

## Demo

### Daily Challenge
```
User: What's today's LeetCode daily challenge?

Claude: 📅 Today's LeetCode Daily Challenge

Problem #42: Trapping Rain Water
Difficulty: Hard
Topics: Array, Two Pointers, Dynamic Programming

[Full problem description with starter code]

Ready to start? I can provide hints if you get stuck!
```

### Search
```
User: Find medium array problems

Claude: I found 10 medium array problems:

1. 3Sum - Array, Two Pointers
2. Container With Most Water - Array, Greedy
3. Product of Array Except Self - Array, Prefix Sum
...

Which one would you like to work on?
```

## Maintainers

OpenClaw Team - [@vilobhmm](https://github.com/vilobhmm)

## License

MIT

---

**Ready to merge!** 🚀

This skill brings coding interview preparation directly into Claude Code with no external dependencies or authentication required.
