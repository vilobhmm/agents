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

        # Add identity
        identity_file = agent_dir / "IDENTITY.md"
        if identity_file.exists():
            parts.append(identity_file.read_text())

        # Add teammates info
        teammates_file = agent_dir / "TEAMMATES.md"
        if teammates_file.exists():
            parts.append(teammates_file.read_text())

        # Add tool usage instructions if tools are available
        if tool_registry and tool_registry.tool_schemas:
            tool_guidance = """
## Your Tools

You have access to real tools that allow you to take actions. When you need to:
- Check emails, calendar, or Drive - use your tools
- Send emails or schedule meetings - use your tools
- Get briefings or prepare for meetings - use your tools

Use your tools proactively. Don't just describe what you would do - actually do it!

Example:
User: "Give me my morning briefing"
You: [Use get_daily_briefing tool, then present the results in a friendly format]

User: "Schedule a meeting with John tomorrow at 2pm"
You: [Use create_calendar_event tool with the right parameters, then confirm]

Be concise and action-oriented. Execute first, explain second.
"""
            parts.append(tool_guidance)

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

        try:
            # First API call
            api_params = {
                "model": model_id,
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": history
            }

            if tools:
                api_params["tools"] = tools

            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                **api_params
            )

            # Handle tool use in a loop
            max_tool_iterations = 5
            iteration = 0

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

                # Continue conversation with tool results
                api_params["messages"] = history
                response = await asyncio.to_thread(
                    self.anthropic_client.messages.create,
                    **api_params
                )

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
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load history: {e}")
            return []

    def _save_history(self, history_file: Path, history: list):
        """Save conversation history to file"""
        import json
        try:
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save history: {e}")
