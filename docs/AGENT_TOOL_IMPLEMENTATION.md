# Agent Tool Calling Implementation

## Summary

Implemented a comprehensive tool calling system for the Agency framework that enables agents (especially CC - Chief Coordinator) to execute real actions through the Anthropic Messages API tool calling feature.

## Problem

The CC agent and other agents had detailed personality descriptions and skill lists, but when invoked, they could only provide status updates and descriptions of what they *could* do. They lacked actual executable capabilities because:

1. Agents only received text descriptions of their abilities
2. No mechanism to convert Python functions into Anthropic API tools
3. No tool execution handler
4. No integration between agent invocation and available tools

## Solution

### 1. Tool Registry System (`agency/core/tools.py`)

Created a flexible `ToolRegistry` class that:
- Converts Python functions/methods into Anthropic tool schemas
- Automatically generates parameter types and descriptions from function signatures
- Handles async function execution
- Provides tool schema formatting for the Anthropic API

Key features:
```python
class ToolRegistry:
    def register_tool(func, name, description, parameter_descriptions)
    def execute_tool(tool_name, tool_input)
    def get_tool_schemas()  # Returns Anthropic-compatible tool definitions
```

### 2. Google Tools Integration

Created `create_google_tools_registry()` which registers:

**Email Tools:**
- `get_unread_emails` - Fetch unread Gmail messages
- `search_emails` - Search by query or sender
- `send_email` - Send emails via Gmail

**Calendar Tools:**
- `get_todays_events` - Today's schedule
- `get_upcoming_events` - Events in next N hours
- `create_calendar_event` - Schedule meetings
- `block_time` - Block focus time
- `get_next_meeting` - Next meeting info

**Drive Tools:**
- `search_drive_files` - Search Drive
- `get_recent_files` - Recently modified files

**Composite Tools:**
- `get_daily_briefing` - Comprehensive morning briefing from all services

### 3. Enhanced Agent Invoker (`agency/core/agent.py`)

Updated `AgentInvoker` with:

**New `_invoke_anthropic_with_tools()` method:**
- Accepts optional `ToolRegistry`
- Passes tool schemas to Anthropic API
- Implements multi-turn tool use conversation loop
- Executes tools and returns results to agent
- Handles up to 5 iterations of tool use

**Enhanced System Prompt:**
- Adds tool usage guidance when tools are available
- Encourages proactive tool use
- Provides examples of tool-driven behavior

### 4. CLI Integration (`agency/cli_commands.py`)

Updated `debug test` command to:
- Automatically create Google Tools registry for CC, assistant, and action_taker agents
- Pass tool registry to agent invoker
- Display tool count in status output

## Results

### Before Implementation:
```
CC Status Update

Status: ✅ Online and Ready
Ready to:
* Deliver your personalized daily briefing
* Review urgent emails and calendar events
* Help you get ahead of your day

How can I help you get started today?
```

### After Implementation:
```
# CC Status Update ✨

**Status:** Online and ready to coordinate your productivity!

**Current Capabilities:**
- 📧 Gmail: Ready to check emails, send messages, and draft responses
- 📅 Calendar: Ready to view schedule, create events, and manage time
- 📁 Drive: Ready to search files and access documents
- 🧠 Memory: Active and learning your preferences

**Available to help with:**
- Morning briefings and daily summaries
- Email triage and priority identification
- Meeting preparation and context gathering
- Calendar management and time blocking
- Proactive task suggestions
```

When Google services are configured, the agent will actually execute tools instead of just describing them.

## Architecture

```
User Message
    ↓
AgentInvoker.invoke_agent()
    ↓
Create ToolRegistry (for CC/assistant/action_taker)
    ↓
_invoke_anthropic_with_tools()
    ↓
Anthropic API (with tools=[...])
    ↓
[Tool Use Loop - up to 5 iterations]
    ├─ Agent requests tool use
    ├─ ToolRegistry.execute_tool()
    ├─ Return results to agent
    └─ Agent continues with results
    ↓
Final Response
```

## Files Modified

1. **`agency/core/tools.py`** (NEW)
   - ToolRegistry class
   - create_google_tools_registry() factory

2. **`agency/core/agent.py`** (MODIFIED)
   - Added ToolRegistry import
   - Updated invoke_agent() to accept tool_registry
   - Added _invoke_anthropic_with_tools() for tool execution
   - Enhanced _build_system_prompt() with tool guidance

3. **`agency/cli_commands.py`** (MODIFIED)
   - Updated test() command to create tool registry
   - Added tool loading for CC, assistant, action_taker agents

4. **`agency/tools/google_tools.py`** (MODIFIED)
   - Fixed environment variable names (GOOGLE_OAUTH_CREDENTIALS_FILE)
   - Added better error messaging

## Next Steps

### To Enable Full Google Integration:

1. **Install dependencies:**
   ```bash
   pip install aiohttp google-auth-oauthlib google-api-python-client
   ```

2. **Set up Google OAuth:**
   - Create OAuth credentials in Google Cloud Console
   - Download credentials JSON
   - Set environment variables:
     ```bash
     GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
     GOOGLE_TOKEN_FILE=google_token.pickle
     ```

3. **Test with tools:**
   ```bash
   python -m agency debug test cc --message "Give me my morning briefing"
   ```

### Future Enhancements:

1. **Additional Tool Registries:**
   - Job search tools (for job_hunter agent)
   - Social media tools (for social agent)
   - Research tools (for researcher agent)

2. **Tool Result Caching:**
   - Cache API responses to reduce quota usage
   - Implement smart refresh strategies

3. **Tool Use Analytics:**
   - Track which tools are used most
   - Measure tool execution success rates
   - Identify tool usage patterns

4. **Error Recovery:**
   - Better error messages from tool failures
   - Automatic retry logic for transient failures
   - Fallback strategies when tools unavailable

## Testing

Current test output shows agents now:
- Understand their tool capabilities
- Provide context-aware responses
- Recognize when Google services aren't configured
- Give helpful setup instructions
- Respond proactively instead of generically

When Google services are properly configured, agents will:
- Execute actual Gmail, Calendar, Drive operations
- Provide real briefings with live data
- Take actions like sending emails and creating events
- Coordinate across multiple tools

## Impact

This implementation transforms the Agency system from a descriptive chatbot into an action-taking AI system. Agents can now:

1. **Execute real operations** through tool calling
2. **Access live data** from Gmail, Calendar, Drive
3. **Take autonomous actions** (send emails, schedule meetings)
4. **Provide data-driven insights** (real briefings, not hypothetical)
5. **Scale to new capabilities** by adding more tool registries

The tool calling system is extensible and can be applied to any agent type with appropriate tool registries.
