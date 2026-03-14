# LeetCode MCP Server

Model Context Protocol (MCP) server for interacting with LeetCode problems.

## Features

- **Get Problem**: Fetch any LeetCode problem by ID or slug
- **Daily Challenge**: Get today's daily challenge
- **Search**: Find problems by difficulty and topic tags
- **Hints**: Get problem hints to guide your solution
- **Stats**: View problem statistics and acceptance rates

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As MCP Server

The server runs via stdio and implements the MCP protocol:

```bash
python server.py
```

### Available Tools

1. **get_leetcode_problem** - Get problem details
   - Args: `identifier` (ID or slug), `language` (optional, default: python3)

2. **get_daily_leetcode** - Get today's daily challenge
   - Args: none

3. **search_leetcode_problems** - Search problems
   - Args: `difficulty` (easy/medium/hard), `tags` (array), `limit` (default: 10)

4. **get_leetcode_hints** - Get problem hints
   - Args: `identifier` (ID or slug)

5. **get_problem_stats** - Get problem statistics
   - Args: `identifier` (ID or slug)

## Configuration

Add to your Claude desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "leetcode": {
      "command": "python",
      "args": ["/path/to/mcp-servers/leetcode/server.py"]
    }
  }
}
```

## Examples

### Get Problem #1 (Two Sum)
```json
{
  "tool": "get_leetcode_problem",
  "arguments": {
    "identifier": "1",
    "language": "python3"
  }
}
```

### Get Daily Challenge
```json
{
  "tool": "get_daily_leetcode",
  "arguments": {}
}
```

### Search Medium Array Problems
```json
{
  "tool": "search_leetcode_problems",
  "arguments": {
    "difficulty": "medium",
    "tags": ["array", "hash-table"],
    "limit": 5
  }
}
```

## License

MIT
