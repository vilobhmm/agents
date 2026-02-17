"""Agent invocation and management.

Each agent runs in isolation with its own workspace and context.
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
import anthropic
from agency.core.tools import ToolRegistry


logger = logging.getLogger(__name__)


class AgentInvoker:
    """
    Invokes AI agents (Anthropic Claude or OpenAI).

    Handles:
    - Agent workspace setup
    - Context management
    - API invocation
    - Response parsing
    """

    def __init__(self, anthropic_api_key: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
        Initialize agent invoker.

        Args:
            anthropic_api_key: Anthropic API key
            openai_api_key: OpenAI API key
        """
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        # Initialize Anthropic client
        if self.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        else:
            self.anthropic_client = None

    async def invoke_agent(
        self,
        agent_config,
        message: str,
        workspace_path: Path,
        team_context: Optional[Dict] = None,
        reset: bool = False,
        tool_registry: Optional[ToolRegistry] = None,
    ) -> str:
        """
        Invoke an AI agent with a message.

        Args:
            agent_config: Agent configuration
            message: User message
            workspace_path: Root workspace directory
            team_context: Team information (if agent is part of a team)
            reset: Whether to reset conversation history
            tool_registry: Optional tool registry for agent capabilities

        Returns:
            Agent's response
        """
        # Setup agent workspace
        agent_dir = workspace_path / agent_config.agent_id
        self._setup_agent_directory(agent_dir, agent_config, team_context)

        # Load conversation history
        history_file = agent_dir / "conversation.json"
        history = self._load_history(history_file) if not reset and history_file.exists() else []

        # Build system prompt
        system_prompt = self._build_system_prompt(agent_dir, agent_config, team_context, tool_registry)

        # Add user message to history
        history.append({
            "role": "user",
            "content": message
        })

        # Invoke AI provider with tool support
        if agent_config.provider == "anthropic":
            response = await self._invoke_anthropic_with_tools(
                agent_config.model,
                system_prompt,
                history,
                tool_registry
            )
        elif agent_config.provider == "openai":
            response = await self._invoke_openai(
                agent_config.model,
                system_prompt,
                history
            )
        else:
            raise ValueError(f"Unknown provider: {agent_config.provider}")

        # Add response to history
        history.append({
            "role": "assistant",
            "content": response
        })

        # Save history
        self._save_history(history_file, history)

        return response

    def _setup_agent_directory(self, agent_dir: Path, agent_config, team_context: Optional[Dict]):
        """
        Setup agent workspace directory.

        Creates:
        - IDENTITY.md - Agent personality and role
        - TEAMMATES.md - Information about teammates (if in a team)
        - conversation.json - Conversation history
        """
        agent_dir.mkdir(parents=True, exist_ok=True)

        # Create IDENTITY.md
        identity_file = agent_dir / "IDENTITY.md"
        if not identity_file.exists():
            identity_content = f"""# Agent Identity

**Name:** {agent_config.name}
**ID:** {agent_config.agent_id}
**Role:** {agent_config.personality or 'General assistant'}

## Your Mission

{agent_config.personality or 'You are a helpful AI assistant.'}

## Your Skills

{chr(10).join(f'- {skill}' for skill in agent_config.skills) if agent_config.skills else '- General knowledge and assistance'}
"""
            identity_file.write_text(identity_content)

        # Create TEAMMATES.md (if in a team)
        if team_context:
            teammates_file = agent_dir / "TEAMMATES.md"
            teammates_content = f"""# Team Information

**Team:** {team_context['name']}
**Team ID:** @{team_context['team_id']}

## Teammates

{self._format_teammates(team_context, agent_config.agent_id)}

## Communication

To involve a teammate in the conversation, use this format:
[@teammate_id: your message to them]

Example: "I've analyzed the data. [@reviewer: please review my findings]"

Your teammate will receive your message and can respond. Multiple teammates can be mentioned in one message.
"""
            teammates_file.write_text(teammates_content)

    def _format_teammates(self, team_context: Dict, current_agent_id: str) -> str:
        """Format teammates list for TEAMMATES.md"""
        lines = []
        for agent in team_context.get('agents', []):
            if agent['agent_id'] != current_agent_id:
                leader_marker = " **(Team Leader)**" if agent['agent_id'] == team_context.get('leader_agent') else ""
                lines.append(f"### @{agent['agent_id']}{leader_marker}")
                lines.append(f"**Name:** {agent['name']}")
                if agent.get('personality'):
                    lines.append(f"**Role:** {agent['personality']}")
                lines.append("")
        return "\n".join(lines)

    def _build_system_prompt(
        self,
        agent_dir: Path,
        agent_config,
        team_context: Optional[Dict],
        tool_registry: Optional[ToolRegistry] = None
    ) -> str:
        """Build system prompt from agent directory files"""
        parts = []

        # 🚨 CRITICAL: Add tool guidance FIRST before identity/personality
        # This ensures Claude sees the mandatory tool-use rules before any role-play examples
        if tool_registry and tool_registry.tool_schemas:
            tool_guidance = """
## ⚠️ CRITICAL: YOU MUST USE YOUR REAL TOOLS

You have REAL tools connected to actual APIs. You MUST use them - DO NOT make up data!

**MANDATORY TOOL USE RULES:**

1. **ALWAYS use tools for data retrieval** - NEVER guess or make up information
2. **Calendar requests → get_todays_events()** - Use the tool, don't invent events
3. **Email requests → get_unread_emails()** - Use the tool, don't create fake emails
4. **Briefings → get_daily_briefing()** - Use the tool for real data
5. **NEVER role-play having data** - If you don't call the tool, you DON'T have the data

**Your Available Tools:**
- get_todays_events() - Fetch REAL calendar events
- get_unread_emails() - Fetch REAL unread emails
- get_daily_briefing() - Get REAL daily context
- send_email() - Actually send emails
- create_calendar_event() - Actually create events
- Plus 6 more tools for Drive, search, etc.

**Correct Behavior:**
User: "Show me my calendar"
You: [CALL get_todays_events() tool] → [Display actual results]

**WRONG Behavior (DO NOT DO THIS):**
User: "Show me my calendar"
You: "Here are your meetings: 9am Team Sync, 2pm Review..." ← NEVER DO THIS! You don't have this data unless you called the tool!

**Remember:** You have REAL tools. Use them. Don't pretend. Call the tools first, then show the results.
"""
            parts.append(tool_guidance)

        # NOW add identity/personality (after tool rules are established)
        identity_file = agent_dir / "IDENTITY.md"
        if identity_file.exists():
            parts.append(identity_file.read_text())

        # Add teammates info
        teammates_file = agent_dir / "TEAMMATES.md"
        if teammates_file.exists():
            parts.append(teammates_file.read_text())

        return "\n\n".join(parts)

    async def _invoke_anthropic(self, model: str, system_prompt: str, history: list) -> str:
        """Invoke Anthropic Claude API (without tools - legacy)"""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        # Map model names
        model_map = {
            "sonnet": "claude-sonnet-4-5-20250929",
            "opus": "claude-opus-4-6",
            "haiku": "claude-haiku-4-5-20251001",
        }
        model_id = model_map.get(model, model)

        try:
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=model_id,
                max_tokens=4096,
                system=system_prompt,
                messages=history
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def _invoke_anthropic_with_tools(
        self,
        model: str,
        system_prompt: str,
        history: list,
        tool_registry: Optional[ToolRegistry] = None
    ) -> str:
        """
        Invoke Anthropic Claude API with tool calling support.

        Handles multi-turn tool use conversations.
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        # Map model names
        model_map = {
            "sonnet": "claude-sonnet-4-5-20250929",
            "opus": "claude-opus-4-6",
            "haiku": "claude-haiku-4-5-20251001",
        }
        model_id = model_map.get(model, model)

        # Get tools if available
        tools = tool_registry.get_tool_schemas() if tool_registry else None

        # DEBUG: Log tool availability
        if tool_registry:
            logger.info(f"🔧 Tool registry available with {len(tools) if tools else 0} tools")
            if tools:
                tool_names = [t['name'] for t in tools]
                logger.info(f"🔧 Available tools: {', '.join(tool_names[:5])}{'...' if len(tool_names) > 5 else ''}")
        else:
            logger.info("⚠️ No tool registry provided to agent")

        try:
            # First API call with retry logic
            api_params = {
                "model": model_id,
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": history
            }

            if tools:
                api_params["tools"] = tools
                logger.info(f"✅ Sending {len(tools)} tools to Claude API")
                # DEBUG: Log system prompt excerpt to verify tool guidance is included
                if system_prompt:
                    first_200_chars = system_prompt[:200].replace('\n', ' ')
                    logger.info(f"🔍 System prompt starts with: {first_200_chars}...")
                # DEBUG: Log conversation history length and contents
                logger.info(f"🔍 Conversation history length: {len(history)} messages")
                if history:
                    for idx, msg in enumerate(history[-3:]):  # Last 3 messages
                        role = msg.get('role', 'unknown')
                        content = str(msg.get('content', ''))[:100]
                        logger.info(f"🔍 History[{len(history)-3+idx}]: {role} - {content}...")

            # Retry logic for connection errors
            max_retries = 3
            retry_delay = 1  # Start with 1 second

            for attempt in range(max_retries):
                try:
                    response = await asyncio.to_thread(
                        self.anthropic_client.messages.create,
                        **api_params
                    )
                    break  # Success, exit retry loop

                except Exception as e:
                    error_msg = str(e)
                    # Check if it's a connection/SSL error
                    if "Connection error" in error_msg or "SSL" in error_msg or "ReadError" in error_msg:
                        if attempt < max_retries - 1:
                            logger.warning(f"Connection error on attempt {attempt + 1}/{max_retries}. Retrying in {retry_delay}s...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        else:
                            # Last attempt failed
                            logger.error("All retry attempts failed. Please check your network connection.")
                            logger.error("Troubleshooting steps:")
                            logger.error("  1. Check your internet connection")
                            logger.error("  2. Disable VPN/proxy temporarily")
                            logger.error("  3. Verify your API key is valid")
                            logger.error("  4. Check if you're behind a corporate firewall")
                            raise
                    else:
                        # Not a connection error, raise immediately
                        raise

            # Handle tool use in a loop
            max_tool_iterations = 5
            iteration = 0

            # DEBUG: Log response stop reason
            logger.info(f"🤖 Claude response - stop_reason: {response.stop_reason}")
            if hasattr(response, 'content'):
                content_types = [block.type for block in response.content]
                logger.info(f"🤖 Response content blocks: {content_types}")
                # DEBUG: If end_turn with text, log what Claude said
                if response.stop_reason == "end_turn":
                    for block in response.content:
                        if block.type == "text":
                            logger.info(f"🤖 Claude's text response: {block.text[:200]}...")
                            break

            while response.stop_reason == "tool_use" and iteration < max_tool_iterations:
                iteration += 1
                logger.info(f"Tool use iteration {iteration}")

                # Extract tool uses from response
                tool_uses = [block for block in response.content if block.type == "tool_use"]

                # Add assistant message to history
                history.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Execute tools and collect results
                tool_results = []
                for tool_use in tool_uses:
                    tool_name = tool_use.name
                    tool_input = tool_use.input
                    logger.info(f"Executing tool: {tool_name} with input: {tool_input}")

                    try:
                        # Execute the tool
                        result = await tool_registry.execute_tool(tool_name, tool_input)

                        # Convert result to string if needed
                        if isinstance(result, dict):
                            import json
                            result_content = json.dumps(result, indent=2)
                        elif isinstance(result, list):
                            import json
                            result_content = json.dumps(result, indent=2)
                        else:
                            result_content = str(result)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": result_content
                        })

                        logger.info(f"Tool {tool_name} executed successfully")

                    except Exception as e:
                        logger.error(f"Tool {tool_name} execution failed: {e}")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": f"Error: {str(e)}",
                            "is_error": True
                        })

                # Add tool results to history
                history.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continue conversation with tool results (with retry)
                api_params["messages"] = history

                for attempt in range(max_retries):
                    try:
                        response = await asyncio.to_thread(
                            self.anthropic_client.messages.create,
                            **api_params
                        )
                        break  # Success
                    except Exception as e:
                        error_msg = str(e)
                        if "Connection error" in error_msg or "SSL" in error_msg or "ReadError" in error_msg:
                            if attempt < max_retries - 1:
                                logger.warning(f"Connection error in tool loop. Retrying...")
                                await asyncio.sleep(retry_delay)
                                continue
                            else:
                                raise
                        else:
                            raise

            # Extract final text response
            text_blocks = [block.text for block in response.content if hasattr(block, 'text')]
            final_response = "\n\n".join(text_blocks) if text_blocks else ""

            return final_response

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def _invoke_openai(self, model: str, system_prompt: str, history: list) -> str:
        """Invoke OpenAI API"""
        # TODO: Implement OpenAI support
        raise NotImplementedError("OpenAI provider not yet implemented")

    def _load_history(self, history_file: Path) -> list:
        """Load conversation history from file"""
        import json
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
                # Prune history to prevent token overflow
                return self._prune_history(history)
        except Exception as e:
            logger.warning(f"Could not load history: {e}")
            return []

    def _prune_history(self, history: list, max_messages: int = 10) -> list:
        """
        Prune conversation history to prevent token overflow.

        Keeps only the most recent messages to stay within token limits.
        With tool use, each iteration can add 3-4 messages, so this prevents
        the history from growing to 200k+ tokens.

        Args:
            history: Full conversation history
            max_messages: Maximum number of message pairs to keep

        Returns:
            Pruned history
        """
        if len(history) <= max_messages * 2:
            return history

        # Keep only the most recent messages
        # Always keep pairs (user/assistant) to maintain conversation structure
        pruned = history[-(max_messages * 2):]

        logger.info(f"Pruned conversation history from {len(history)} to {len(pruned)} messages")
        return pruned

    def _save_history(self, history_file: Path, history: list):
        """Save conversation history to file"""
        import json
        try:
            # Prune before saving to keep file size manageable
            pruned_history = self._prune_history(history, max_messages=10)
            with open(history_file, 'w') as f:
                json.dump(pruned_history, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save history: {e}")
