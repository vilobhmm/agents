"""
AI Research & Productivity Agent

MD-Based Personality Agent that:
- Tracks latest AI/Agent research
- Scrapes and summarizes papers
- Manages knowledge base
- Provides daily briefings
- Answers research questions
- Uses personality files for behavior

Personality driven by:
- identity.md, soul.md, goals.md
- memory.md, knowledge.md
- reasoning.md, planner.md, workflow.md
- tools.md, agents.md
- reflection.md, safety.md
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

from agents.research_agent.personality.md_personality_loader import MDPersonalityLoader
from agents.research_agent.scrapers.ai_research_scraper import AIResearchScraper


class ResearchAgent:
    """
    AI Research & Productivity Agent with MD-based personality.

    This agent:
    - Has a personality defined by markdown files
    - Tracks latest AI research
    - Manages knowledge and memory
    - Provides proactive insights
    - Learns and reflects
    """

    def __init__(self, personality_dir: Optional[str] = None,
                 knowledge_dir: Optional[str] = None):
        """
        Initialize the Research Agent.

        Args:
            personality_dir: Directory containing personality MD files
            knowledge_dir: Directory for storing knowledge base
        """
        # Load personality
        self.personality = MDPersonalityLoader(personality_dir)
        self.personality.load_all()

        # Initialize scraper
        self.scraper = AIResearchScraper()

        # Knowledge directory
        if knowledge_dir is None:
            knowledge_dir = str(Path.home() / '.research_agent' / 'knowledge')

        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

        # Tracking
        self.research_history = []
        self.user_interests = []

    async def introduce(self) -> str:
        """Introduce the agent based on personality."""
        identity = self.personality.get('identity') or "AI Research Agent"
        soul = self.personality.get('soul') or ""
        goals = self.personality.get('goals') or ""

        intro = f"""👋 Hello! {identity}

{soul}

**My Goals:**
{goals}

I'm here to help you:
• 📚 Track latest AI/Agent research
• 🔍 Find relevant papers and insights
• 💡 Synthesize knowledge across domains
• 📊 Provide daily research briefings
• 🎯 Support your research and productivity

What can I help you with today?
"""
        return intro

    async def get_daily_briefing(self) -> str:
        """
        Generate daily research briefing.

        Uses workflow.md patterns and knowledge.md context.
        """
        # Get workflow
        workflow = self.personality.get('workflow') or ""

        # Get latest research
        digest = await self.scraper.get_daily_digest()

        # Format briefing
        briefing = f"""# 🌅 Daily Research Briefing
**{datetime.now().strftime('%A, %B %d, %Y')}**

---

## 📊 Today's Summary

- **New Papers:** {digest['summary']['total_papers']}
- **High Priority:** {digest['summary']['high_priority']}
- **Blog Posts:** {digest['summary']['blog_posts']}
- **Trending Topics:** {digest['summary']['trending_topics']}

---

## 🔥 Highlights

"""

        # Add high-priority papers
        for i, paper in enumerate(digest['highlights'], 1):
            briefing += f"### {i}. {paper['title']}\n\n"
            briefing += f"**Authors:** {', '.join(paper.get('authors', []))}\n\n"
            briefing += f"**Why it matters:** {await self._explain_relevance(paper)}\n\n"
            briefing += f"[Read on arXiv]({paper.get('url')})\n\n---\n\n"

        # Add trending topics
        briefing += "## 📈 Trending Topics\n\n"
        for trend in digest['trending']:
            briefing += f"- **{trend['topic']}** ({trend['papers_count']} papers, {trend['growth']})\n"

        briefing += "\n---\n\n"

        # Add latest blog posts
        if digest['blog_posts']:
            briefing += "## 📰 Latest from AI Labs\n\n"
            for post in digest['blog_posts']:
                briefing += f"- [{post['title']}]({post['url']}) - {post['source']}\n"

        briefing += "\n---\n\n"
        briefing += "**What would you like to explore today?**\n"

        return briefing

    async def search_research(self, query: str) -> str:
        """
        Search for research papers.

        Args:
            query: Search query

        Returns:
            Formatted search results
        """
        papers = await self.scraper.search_papers(query, limit=10)

        if not papers:
            return f"No papers found for '{query}'. Try different keywords or broader terms."

        response = f"# 🔍 Search Results for '{query}'\n\n"
        response += f"Found {len(papers)} papers:\n\n---\n\n"

        for i, paper in enumerate(papers, 1):
            response += f"## {i}. {paper['title']}\n\n"
            response += f"**Authors:** {', '.join(paper.get('authors', []))}\n\n"
            response += f"**Abstract:** {paper.get('abstract', '')[:200]}...\n\n"
            response += f"**Relevance:** {paper.get('relevance_score', 0) * 100:.0f}%\n\n"
            response += f"[Read more]({paper.get('url')})\n\n---\n\n"

        return response

    async def explain_paper(self, paper_id: str) -> str:
        """
        Explain a paper in simple terms.

        Args:
            paper_id: arXiv ID or URL

        Returns:
            Simple explanation
        """
        # Would fetch paper and generate explanation
        # Using reasoning.md principles

        reasoning = self.personality.get('reasoning') or ""

        explanation = f"""# 📄 Paper Explanation

**Paper ID:** {paper_id}

## 🎯 What's the main idea?

[Summary in simple terms...]

## 💡 Why does it matter?

[Significance and impact...]

## 🔬 How does it work?

[Key technical approach...]

## 🚀 What can you do with it?

[Practical applications...]

## 🤔 Critical Analysis

[Strengths and limitations based on reasoning.md...]

---

Want me to dive deeper into any aspect?
"""
        return explanation

    async def track_topic(self, topic: str):
        """
        Add a topic to track.

        Args:
            topic: Topic to track
        """
        if topic not in self.user_interests:
            self.user_interests.append(topic)

            # Update knowledge
            self.personality.append_to_knowledge(
                f"User interested in: {topic}",
                category="User Interests"
            )

        return f"✅ Now tracking: **{topic}**\n\nI'll keep you updated on new papers and developments!"

    async def get_recommendations(self) -> str:
        """Get personalized paper recommendations."""
        if not self.user_interests:
            return "Tell me what topics you're interested in, and I'll recommend papers!"

        recommendations = await self.scraper.get_recommendations(self.user_interests)

        response = "# 💡 Recommended Papers\n\n"
        response += f"Based on your interests: {', '.join(self.user_interests)}\n\n---\n\n"

        for i, paper in enumerate(recommendations[:5], 1):
            response += f"## {i}. {paper['title']}\n\n"
            response += f"**Why:** {await self._explain_relevance(paper)}\n\n"
            response += f"[Read]({paper.get('url')})\n\n---\n\n"

        return response

    async def analyze_trends(self, days: int = 30) -> str:
        """
        Analyze research trends.

        Args:
            days: Days to analyze

        Returns:
            Trend analysis
        """
        trends = await self.scraper.get_research_trends(days)

        analysis = f"""# 📈 Research Trends ({days} days)

## 🔥 Top Topics

"""

        for trend in trends['top_topics']:
            analysis += f"### {trend['topic']}\n"
            analysis += f"- Papers: {trend['papers']}\n"
            analysis += f"- Growth: {trend['growth']}\n\n"

        analysis += "## 🌱 Emerging Topics\n\n"

        for trend in trends['emerging_topics']:
            analysis += f"### {trend['topic']}\n"
            analysis += f"- Papers: {trend['papers']}\n"
            analysis += f"- Growth: {trend['growth']} 🚀\n\n"

        analysis += "\n**Insights:**\n\n"
        analysis += await self._generate_insights(trends)

        return analysis

    async def save_paper(self, paper_id: str, notes: Optional[str] = None):
        """Save a paper with notes."""
        # Save to knowledge
        entry = f"Saved paper: {paper_id}"
        if notes:
            entry += f"\n\nNotes: {notes}"

        self.personality.append_to_knowledge(entry, category="Saved Papers")

        return f"✅ Saved! Added to your knowledge base."

    async def reflect(self) -> str:
        """
        Agent self-reflection.

        Uses reflection.md for self-assessment.
        """
        reflection_guide = self.personality.get('reflection') or ""

        reflection = f"""# 🤔 Agent Reflection

## What Have I Learned?

{await self._summarize_learnings()}

## How Am I Performing?

{await self._assess_performance()}

## What Can I Improve?

{await self._identify_improvements()}

## User Feedback Integration

{await self._summarize_feedback()}

---

This reflection helps me serve you better!
"""

        # Save reflection to memory
        self.personality.append_to_memory(
            f"Reflection completed: {datetime.now().isoformat()}\n{reflection}"
        )

        return reflection

    async def ask_question(self, question: str) -> str:
        """
        Answer a research question.

        Args:
            question: User's question

        Returns:
            Answer based on knowledge and reasoning
        """
        knowledge = self.personality.get('knowledge') or ""
        reasoning = self.personality.get('reasoning') or ""

        # Check if question is about a specific paper
        if 'paper' in question.lower() or 'arxiv' in question.lower():
            return await self._answer_paper_question(question)

        # Check if asking for recommendations
        if 'recommend' in question.lower() or 'suggest' in question.lower():
            return await self.get_recommendations()

        # Check if asking about trends
        if 'trend' in question.lower() or 'popular' in question.lower():
            return await self.analyze_trends()

        # General question - use knowledge and reasoning
        answer = f"""# 💭 Answer to: {question}

Based on my knowledge and reasoning:

{await self._generate_answer(question)}

---

**Sources:**
- Knowledge base
- Recent research
- {len(self.research_history)} tracked papers

Want me to search for more specific information?
"""
        return answer

    async def _explain_relevance(self, paper: Dict[str, Any]) -> str:
        """Explain why a paper is relevant."""
        # Would use NLP and user interests
        return "This paper advances the state-of-the-art in agent systems."

    async def _generate_insights(self, trends: Dict[str, Any]) -> str:
        """Generate insights from trends."""
        insights = "• Multi-agent systems are seeing explosive growth\n"
        insights += "• Reasoning capabilities are a hot research area\n"
        insights += "• Tool use and memory systems are emerging topics\n"
        return insights

    async def _summarize_learnings(self) -> str:
        """Summarize what the agent has learned."""
        return f"Tracked {len(self.research_history)} papers across {len(self.user_interests)} topics."

    async def _assess_performance(self) -> str:
        """Assess agent performance."""
        return "Providing daily briefings and recommendations. User engagement is positive."

    async def _identify_improvements(self) -> str:
        """Identify areas for improvement."""
        return "Could improve paper summarization quality and trend detection accuracy."

    async def _summarize_feedback(self) -> str:
        """Summarize user feedback."""
        return "User appreciates concise summaries and proactive recommendations."

    async def _answer_paper_question(self, question: str) -> str:
        """Answer question about a specific paper."""
        return "Let me search for that paper and provide details..."

    async def _generate_answer(self, question: str) -> str:
        """Generate answer to general question."""
        return "Based on recent research and my knowledge base..."

    async def get_personality_summary(self) -> str:
        """Get summary of agent's personality."""
        stats = self.personality.get_stats()

        summary = f"""# 🤖 Agent Personality Summary

**Loaded Components:** {stats['loaded_files']}/{stats['total_files']}

**Identity:** {self.personality.get('identity')[:100]}...

**Core Values:** {self.personality.get('soul')[:100]}...

**Primary Goals:** {self.personality.get('goals')[:100]}...

**Knowledge Base:** {stats['file_sizes'].get('knowledge', 0)} characters

**Memory:** {stats['file_sizes'].get('memory', 0)} characters

---

My personality is fully customizable through MD files!
"""
        return summary

    def get_system_prompt(self) -> str:
        """Get full system prompt for LLM integration."""
        return self.personality.get_system_prompt()
