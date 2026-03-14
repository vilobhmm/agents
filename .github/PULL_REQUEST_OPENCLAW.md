# Add LeetCode Integration: MCP Server, Skills, and Examples

## Summary

Complete LeetCode integration for OpenClaw with MCP server, Python skills module, Claude skill, and comprehensive examples for building interview prep agents.

## What's Added

### 1. MCP Server (`mcp-servers/leetcode/`)

Production-ready Model Context Protocol server with 5 tools:

#### Tools
- **get_leetcode_problem** - Get any problem with full details and starter code
- **get_daily_leetcode** - Today's daily coding challenge
- **search_leetcode_problems** - Search by difficulty, tags, and topics
- **get_leetcode_hints** - Progressive hints without spoilers
- **get_problem_stats** - Acceptance rates and statistics

#### Features
- Async/await architecture
- LeetCode GraphQL API integration
- Multi-language support (Python, JS, C++, Java, etc.)
- Comprehensive error handling
- Full test suite

### 2. Skills Module (`agents/base/leetcode_skills.py`)

Python API for OpenClaw agents:

```python
from agents.base.leetcode_skills import LeetCodeSkills

skills = LeetCodeSkills()

# Get daily challenge
daily = await skills.get_daily_challenge()

# Get problem
problem = await skills.get_problem("two-sum", language="python3")

# Search
problems = await skills.search_problems(
    difficulty="medium",
    tags=["array", "dynamic-programming"],
    limit=5
)

# Hints
hints = await skills.get_hints("two-sum")
```

#### Methods
- `get_problem()` - Fetch problem details
- `get_daily_challenge()` - Today's challenge
- `search_problems()` - Search with filters
- `get_hints()` - Progressive hints
- `get_stats()` - Problem statistics
- `get_practice_set()` - Curated practice problems
- `start_daily_challenge()` - Formatted daily challenge
- `get_problem_formatted()` - Ready-to-solve format

### 3. Claude Code Skill

Native `/leetcode` skill for Claude Code with:
- Natural language interface
- Complete documentation
- Workflow guides
- Example queries

### 4. Examples (`examples/leetcode_example.py`)

7 complete examples demonstrating:
1. Daily challenge workflow
2. Getting specific problems
3. Search and practice sets
4. Progressive hint system
5. 7-day study plan generator
6. Problem statistics
7. Interview prep assistant

## Use Cases

### Build Interview Prep Agents

```python
from agents.base.leetcode_skills import LeetCodeSkills
from openclaw.core.agent import Agent, AgentConfig

class InterviewPrepAgent(Agent):
    def __init__(self):
        config = AgentConfig(
            name="Interview Coach",
            description="Technical interview preparation assistant"
        )
        super().__init__(config)
        self.leetcode = LeetCodeSkills()

    async def daily_practice(self):
        challenge = await self.leetcode.start_daily_challenge()
        return await self.chat(f"Today's challenge:\n\n{challenge}")

    async def create_study_plan(self, topics, days=7):
        plan = {}
        for day, topic in enumerate(topics[:days], 1):
            problems = await self.leetcode.get_practice_set(
                topic, "easy", 2
            )
            plan[f"Day {day}"] = {"topic": topic, "problems": problems}
        return plan
```

### Agent Examples
- **Daily Practice Bot** - Sends daily challenges
- **Study Plan Generator** - Creates personalized plans
- **Hint Assistant** - Provides progressive help
- **Progress Tracker** - Tracks solved problems
- **Topic Coach** - Focused topic practice

## Integration

### With Existing Agents

Works seamlessly with:
- Research agents
- Productivity agents
- Voice agents
- Co-scientist agent

### With OpenClaw Core

Uses standard OpenClaw patterns:
- Async/await
- Skill-based architecture
- Agent base classes
- Tool integration

## Documentation

### Comprehensive Guides
- `README.md` - Server documentation
- `INTEGRATION.md` - Complete setup guide
- `SUBMISSION.md` - Skill hub submission
- Example code with comments

### Installation

```bash
cd mcp-servers/leetcode
pip install -r requirements.txt
python test_server.py  # Run tests
```

### Configuration

Claude MCP config:
```json
{
  "mcpServers": {
    "leetcode": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## Technical Details

**API:** LeetCode GraphQL (public, no auth required)
**Protocol:** Model Context Protocol (stdio)
**Language:** Python 3.8+
**Dependencies:** mcp>=0.9.0, httpx>=0.27.0
**Architecture:** Fully async
**Testing:** Complete test suite included

## Quality Checklist

- [x] Code follows OpenClaw patterns
- [x] Full async/await support
- [x] Comprehensive error handling
- [x] Type hints throughout
- [x] Logging implemented
- [x] Tests included and passing
- [x] Documentation complete
- [x] Examples provided
- [x] MCP compliant
- [x] Security reviewed

## Testing

```bash
# Run MCP server tests
cd mcp-servers/leetcode
python test_server.py

# Run examples
cd examples
python leetcode_example.py
```

All tests pass:
✅ Get problem by slug
✅ Get problem by ID
✅ Daily challenge
✅ Search problems
✅ Hints retrieval
✅ Statistics

## Files Changed

### Added
```
mcp-servers/leetcode/
├── server.py              # MCP server (540 lines)
├── test_server.py         # Test suite
├── requirements.txt       # Dependencies
├── README.md             # Documentation
├── INTEGRATION.md        # Setup guide
└── mcp-config.json       # Config example

agents/base/
└── leetcode_skills.py    # Skills module (380 lines)

examples/
└── leetcode_example.py   # 7 examples (270 lines)

.skill-hub/leetcode/
├── SKILL.md              # Skill definition
├── package.json          # Metadata
├── README.md            # User docs
└── SUBMISSION.md        # Submission info

.github/
├── PULL_REQUEST_CLAUDE.md   # Claude PR template
└── PULL_REQUEST_OPENCLAW.md # This file
```

### Modified
None - all new additions

## Breaking Changes

None - this is a pure addition with no impact on existing code.

## Performance

- Async operations throughout
- Efficient GraphQL queries
- Minimal memory footprint
- No blocking calls

## Security

- No credentials stored
- Public API only
- Input validation
- Safe error handling
- No PII collected

## Future Enhancements

Possible additions:
- Solution submission (requires auth)
- User profile integration
- Discussion forum access
- Similar problem recommendations
- Difficulty progression tracking
- Contest integration

## Screenshots

### Example Output

```
📅 LeetCode Daily Challenge - 2024-03-14

# 42. Trapping Rain Water
**Difficulty**: Hard
**Topics**: Array, Two Pointers, Dynamic Programming

Given n non-negative integers representing an elevation map where
the width of each bar is 1, compute how much water it can trap
after raining.

**Starter Code** (python3):
def trap(self, height: List[int]) -> int:
    pass

**URL**: https://leetcode.com/problems/trapping-rain-water/
```

## Contributors

OpenClaw Team - [@vilobhmm](https://github.com/vilobhmm)

Built with Claude Code Agent SDK

## License

MIT - Same as OpenClaw

---

## Review Checklist

- [ ] Code reviewed for quality
- [ ] Tests passing
- [ ] Documentation reviewed
- [ ] Examples tested
- [ ] Security reviewed
- [ ] Performance acceptable
- [ ] No breaking changes
- [ ] Integrates well with existing code

## Merge Instructions

1. Review code and documentation
2. Run tests: `python mcp-servers/leetcode/test_server.py`
3. Test examples: `python examples/leetcode_example.py`
4. Verify MCP server starts: `python mcp-servers/leetcode/server.py`
5. Merge to main

---

**Ready for review!** 🎯

This PR adds a complete, production-ready LeetCode integration that enables building interview prep agents and provides direct coding practice in Claude Code.
