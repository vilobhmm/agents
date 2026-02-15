"""Proactive Context Switcher Agent - Multi-Agent System"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.orchestrator import Orchestrator
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.github import GitHubIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.slack import SlackIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration


logger = logging.getLogger(__name__)


class PatternDetectorAgent(Agent):
    """Detects context changes"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Pattern Detector",
            description="I detect when you switch between projects/contexts.",
        )
        super().__init__(config, api_key)

        self.calendar = CalendarIntegration()
        self.github = GitHubIntegration()
        self.email = EmailIntegration()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect current context"""

        # Check calendar
        upcoming = await self.calendar.get_upcoming_events(hours=2)

        # Check recent commits (if GitHub configured)
        recent_activity = []

        # Check recent emails
        recent_emails = await self.email.get_messages(max_results=5, unread_only=True)

        # Analyze to determine context
        prompt = f"""Analyze this activity to determine the current work context:

Calendar: {upcoming[0].get('summary', '') if upcoming else 'No upcoming events'}

Recent emails: {', '.join([e.get('subject', '') for e in recent_emails[:3]])}

What project/context is the user likely working on?
Return: Project name and confidence (high/medium/low)"""

        response = await self.chat(prompt)

        # Parse context
        context = self.parse_context(response)

        return {"context": context, "confidence": "high"}

    def parse_context(self, response: str) -> str:
        """Parse context from response"""
        # Simplified parsing
        lines = response.strip().split("\n")
        return lines[0] if lines else "Unknown"


class KnowledgeRetrieverAgent(Agent):
    """Retrieves relevant information for context"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Knowledge Retriever",
            description="I retrieve relevant information for your current context.",
        )
        super().__init__(config, api_key)

        self.notion = NotionIntegration()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant information"""

        context = input_data.get("context", "")

        # Search Notion for related pages
        pages = await self.notion.query_database()

        # Filter and rank by relevance
        relevant_info = []

        for page in pages[:10]:
            # In production, use semantic search
            relevant_info.append(
                {
                    "title": page.get("properties", {})
                    .get("Name", {})
                    .get("title", [{}])[0]
                    .get("text", {})
                    .get("content", ""),
                    "id": page.get("id", ""),
                }
            )

        return {"context": context, "relevant_pages": relevant_info}


class ContextAssemblerAgent(Agent):
    """Assembles context packs"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Context Assembler",
            description="I assemble context packs with everything you need.",
        )
        super().__init__(config, api_key)

        self.notion = NotionIntegration()
        self.slack = SlackIntegration()
        self.whatsapp = WhatsAppIntegration()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assemble and deliver context pack"""

        context = input_data.get("context", "")
        relevant_pages = input_data.get("relevant_pages", [])

        # Create context pack in Notion
        context_pack = await self.create_context_pack(context, relevant_pages)

        # Update Slack status
        await self.slack.update_status(f"Working on: {context}")

        # Send WhatsApp notification
        message = f"""Context Switch Detected: {context}

I've prepared a context pack for you:
{context_pack.get('url', '')}

Relevant information:
{chr(10).join(['- ' + p.get('title', '') for p in relevant_pages[:5]])}"""

        await self.whatsapp.send_message(
            os.getenv("WHATSAPP_RECIPIENT"), message
        )

        return {"status": "success", "context_pack": context_pack}

    async def create_context_pack(
        self, context: str, pages: List[Dict]
    ) -> Dict:
        """Create context pack in Notion"""

        children = [
            self.notion.create_heading_block(f"Context: {context}", level=1),
            self.notion.create_text_block(f"Created: {datetime.now().isoformat()}"),
            self.notion.create_heading_block("Relevant Resources", level=2),
        ]

        for page in pages[:10]:
            children.append(
                self.notion.create_bulleted_list_block(page.get("title", ""))
            )

        page_id = await self.notion.create_page(
            properties={
                "Name": {"title": [{"text": {"content": f"Context: {context}"}}]}
            },
            children=children,
        )

        return {"id": page_id, "url": f"https://notion.so/{page_id}"}


class ContextSwitcherOrchestrator:
    """Orchestrates context switching"""

    def __init__(self, api_key: str = None):
        self.detector = PatternDetectorAgent(api_key)
        self.retriever = KnowledgeRetrieverAgent(api_key)
        self.assembler = ContextAssemblerAgent(api_key)

        self.orchestrator = Orchestrator(
            [self.detector, self.retriever, self.assembler]
        )

    async def detect_and_switch(self):
        """Detect context change and prepare"""

        workflow = [
            {"agent": "Pattern Detector", "input": {}},
            {"agent": "Knowledge Retriever", "input": {}},
            {"agent": "Context Assembler", "input": {}},
        ]

        results = await self.orchestrator.run_sequential(workflow)

        logger.info("Context switch handled")
        return results
