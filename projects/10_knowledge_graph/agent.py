"""Personal Knowledge Graph Builder - Multi-Agent System"""

import logging
from typing import Any, Dict, List

import networkx as nx
from openclaw.core.agent import Agent, AgentConfig
from openclaw.core.orchestrator import Orchestrator
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.slack import SlackIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration


logger = logging.getLogger(__name__)


class ExtractionAgent(Agent):
    """Extracts entities and relationships"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Knowledge Extractor",
            description="I extract entities and relationships from your data.",
        )
        super().__init__(config, api_key)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract knowledge from text"""

        text = input_data.get("text", "")
        source = input_data.get("source", "unknown")

        prompt = f"""Extract entities and relationships from this text:

{text}

Return in this format:

ENTITIES:
- [Entity 1] (Type: person/concept/project/etc.)
- [Entity 2] (Type: ...)

RELATIONSHIPS:
- [Entity 1] -> [relationship] -> [Entity 2]
- ...

INSIGHTS:
- [Key insight or learning]
- ..."""

        extraction = await self.chat(prompt)

        return {
            "source": source,
            "text": text[:200],
            "extraction": extraction,
        }


class GraphBuilderAgent(Agent):
    """Builds and maintains knowledge graph"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Graph Builder",
            description="I build and maintain your knowledge graph.",
        )
        super().__init__(config, api_key)

        self.graph = nx.DiGraph()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add to knowledge graph"""

        extraction = input_data.get("extraction", "")

        # Parse extraction (simplified)
        entities, relationships = self.parse_extraction(extraction)

        # Add to graph
        for entity in entities:
            self.graph.add_node(entity["name"], **entity)

        for rel in relationships:
            self.graph.add_edge(
                rel["source"],
                rel["target"],
                relationship=rel["type"],
            )

        logger.info(
            f"Graph now has {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges"
        )

        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
        }

    def parse_extraction(self, extraction: str) -> tuple:
        """Parse extraction into structured data"""

        # Simplified parsing
        entities = []
        relationships = []

        lines = extraction.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("ENTITIES"):
                current_section = "entities"
            elif line.startswith("RELATIONSHIPS"):
                current_section = "relationships"
            elif line.startswith("-") and current_section == "entities":
                # Parse entity
                entity_text = line.strip("- ")
                if "(" in entity_text:
                    name = entity_text.split("(")[0].strip()
                    entity_type = (
                        entity_text.split("Type:")[1].strip(")")
                        if "Type:" in entity_text
                        else "unknown"
                    )
                    entities.append({"name": name, "type": entity_type})
            elif line.startswith("-") and current_section == "relationships":
                # Parse relationship
                if "->" in line:
                    parts = line.strip("- ").split("->")
                    if len(parts) >= 3:
                        relationships.append(
                            {
                                "source": parts[0].strip(),
                                "type": parts[1].strip(),
                                "target": parts[2].strip(),
                            }
                        )

        return entities, relationships


class QueryEngineAgent(Agent):
    """Answers questions using knowledge graph"""

    def __init__(self, api_key: str = None, graph: nx.DiGraph = None):
        config = AgentConfig(
            name="Query Engine",
            description="I answer questions using your knowledge graph.",
        )
        super().__init__(config, api_key)

        self.graph = graph or nx.DiGraph()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Answer a query"""

        question = input_data.get("question", "")

        # Get graph context
        graph_summary = self.get_graph_summary()

        prompt = f"""Answer this question using the knowledge graph:

Question: {question}

Knowledge Graph Summary:
{graph_summary}

Provide a detailed answer with references to specific nodes and relationships."""

        answer = await self.chat(prompt)

        return {"question": question, "answer": answer}

    def get_graph_summary(self) -> str:
        """Get summary of knowledge graph"""

        summary = f"Nodes: {self.graph.number_of_nodes()}\n"
        summary += f"Edges: {self.graph.number_of_edges()}\n\n"

        # Sample nodes
        summary += "Sample entities:\n"
        for node in list(self.graph.nodes())[:20]:
            node_data = self.graph.nodes[node]
            summary += f"- {node} ({node_data.get('type', 'unknown')})\n"

        return summary


class InsightGeneratorAgent(Agent):
    """Generates insights from knowledge graph"""

    def __init__(self, api_key: str = None, graph: nx.DiGraph = None):
        config = AgentConfig(
            name="Insight Generator",
            description="I generate insights from your knowledge graph.",
        )
        super().__init__(config, api_key)

        self.graph = graph or nx.DiGraph()
        self.whatsapp = WhatsAppIntegration()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weekly insights"""

        # Find central nodes (most connected)
        if self.graph.number_of_nodes() > 0:
            centrality = nx.degree_centrality(self.graph)
            top_nodes = sorted(
                centrality.items(), key=lambda x: x[1], reverse=True
            )[:10]

            # Generate insights
            prompt = f"""Based on this knowledge graph analysis, generate insights:

Most central concepts:
{chr(10).join([f'- {node} (centrality: {score:.2f})' for node, score in top_nodes])}

Provide:
1. What are the main themes in my knowledge base?
2. What connections or patterns are emerging?
3. What areas might need more exploration?
4. Suggestions for learning or projects based on this knowledge"""

            insights = await self.chat(prompt)

            # Send insights
            await self.whatsapp.send_message(
                os.getenv("WHATSAPP_RECIPIENT"),
                f"📊 Weekly Knowledge Insights:\n\n{insights}",
            )

            return {"status": "success", "insights": insights}

        return {"status": "no_data"}


class KnowledgeGraphOrchestrator:
    """Orchestrates knowledge graph building"""

    def __init__(self, api_key: str = None):
        self.graph = nx.DiGraph()

        self.extractor = ExtractionAgent(api_key)
        self.builder = GraphBuilderAgent(api_key)
        self.query_engine = QueryEngineAgent(api_key, self.graph)
        self.insight_gen = InsightGeneratorAgent(api_key, self.graph)

        # Share graph reference
        self.builder.graph = self.graph
        self.query_engine.graph = self.graph
        self.insight_gen.graph = self.graph

        self.orchestrator = Orchestrator(
            [self.extractor, self.builder, self.query_engine, self.insight_gen]
        )

        # Integrations
        self.email = EmailIntegration()
        self.slack = SlackIntegration()
        self.notion = NotionIntegration()

    async def process_all_sources(self):
        """Process all data sources"""

        # Get emails
        emails = await self.email.get_messages(max_results=50)

        for email_data in emails:
            text = f"{email_data.get('subject', '')}\n{email_data.get('body', '')}"
            await self.process_text(text, source="email")

        # Get Slack messages
        # Get Notion pages
        # etc.

        logger.info("Processed all sources")

    async def process_text(self, text: str, source: str = "unknown"):
        """Process text and add to knowledge graph"""

        workflow = [
            {"agent": "Knowledge Extractor", "input": {"text": text, "source": source}},
            {"agent": "Graph Builder", "input": {}},
        ]

        await self.orchestrator.run_sequential(workflow)

    async def answer_question(self, question: str) -> str:
        """Answer a question"""

        result = await self.query_engine.process({"question": question})
        return result.get("answer", "")

    async def generate_weekly_insights(self):
        """Generate weekly insights"""

        await self.insight_gen.process({})
