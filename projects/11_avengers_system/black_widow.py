"""
Black Widow - LinkedIn Authority Architect Agent

Builds professional credibility through strategic thought leadership content.
Plays the long game for authority building.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import requests
from anthropic import Anthropic

from .coordination import AgentReport, CoordinationHub, Task, TaskStatus, coordination_hub

logger = logging.getLogger(__name__)


class BlackWidowAgent:
    """
    Black Widow - LinkedIn Authority Architect

    Creates strategic LinkedIn content:
    - Deep analysis posts (500+ words)
    - Thought leadership
    - Professional positioning
    - Strategic commentary

    Tone: Composed, high-signal, strategic
    Posts 2-3 times weekly
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Black Widow"
        self.emoji = "🕷"
        self.agent_key = "black_widow"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub

        # LinkedIn credentials
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

        if self.linkedin_token:
            logger.info(f"{self.emoji} LinkedIn client configured")

        self.posts_drafted = []
        self.posts_published = []

        logger.info(f"{self.emoji} {self.name} initialized")

    async def create_deep_analysis_post(self, topic: str, research_data: dict) -> str:
        """
        Create a deep analysis LinkedIn post

        Args:
            topic: Topic to analyze
            research_data: Research intelligence from Captain America

        Returns:
            str: LinkedIn post text
        """
        # Use Claude to create analysis
        prompt = f"""You are Black Widow, a strategic AI thought leader on LinkedIn.

Topic: {topic}

Research data:
{research_data}

Create a deep analysis post (500-800 words) that:

1. Opening: Hook with a strategic insight
2. Analysis: Deep dive into the topic
   - What's happening
   - Why it matters
   - Strategic implications
3. Professional perspective: How this affects practitioners
4. Conclusion: Forward-looking statement

Tone: Composed, authoritative, strategic
Style: Professional, high-signal, builds authority
Format: Clear paragraphs, use line breaks for readability

Output the post text only."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        post_text = response.content[0].text.strip()

        # Store draft
        draft = {
            "topic": topic,
            "text": post_text,
            "status": "drafted",
            "timestamp": datetime.now(),
        }

        self.posts_drafted.append(draft)

        return post_text

    async def create_thought_leadership_post(self, insights: List[str]) -> str:
        """
        Create thought leadership post from insights

        Args:
            insights: List of insights to weave into post

        Returns:
            str: LinkedIn post text
        """
        insights_text = "\n".join([f"• {i}" for i in insights])

        prompt = f"""You are Black Widow. Create a thought leadership LinkedIn post.

Key insights to incorporate:
{insights_text}

Create a post (400-600 words) that:

1. Start with a contrarian or strategic observation
2. Build on the insights
3. Provide a unique perspective
4. End with actionable implications

Make readers feel they gained strategic clarity.
Tone: Authoritative but not arrogant, strategic, insightful.

Output the post text only."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text.strip()

    async def publish_to_linkedin(self, post_text: str) -> bool:
        """
        Publish post to LinkedIn

        Args:
            post_text: Post content

        Returns:
            bool: Success status
        """
        if not self.linkedin_token:
            logger.warning("LinkedIn not configured - post not published")
            logger.info(f"Would publish:\n{post_text[:200]}...")
            return False

        try:
            # LinkedIn API endpoint
            url = "https://api.linkedin.com/v2/ugcPosts"

            headers = {
                "Authorization": f"Bearer {self.linkedin_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }

            # Get person URN (would need to be stored)
            person_urn = "urn:li:person:YOUR_PERSON_ID"  # Placeholder

            data = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 201:
                logger.info(f"{self.emoji} LinkedIn post published")

                self.posts_published.append(
                    {"text": post_text[:100], "timestamp": datetime.now()}
                )

                return True
            else:
                logger.error(f"LinkedIn API error: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error publishing to LinkedIn: {e}")
            return False

    async def weekly_post_generation(self):
        """
        Generate weekly posts (runs Monday and Thursday)
        """
        # Get research intelligence from last few days
        recent_intel = self.coordination.knowledge_base.get_by_source("captain_america")

        if not recent_intel:
            logger.info(f"{self.emoji} No intelligence for post generation")
            return

        # Extract key topics
        topics = []
        for entry in recent_intel[-10:]:  # Last 10 entries
            if "value" in entry and isinstance(entry["value"], dict):
                report = entry["value"]

                if "summary" in report:
                    topics.append(report["summary"])

        # Create analysis post
        if topics:
            combined_research = "\n\n".join(topics[:3])  # Top 3

            post = await self.create_deep_analysis_post(
                topic="Recent AI Developments", research_data=combined_research
            )

            # Store in knowledge base
            self.coordination.knowledge_base.add_entry(
                key=f"linkedin_post_{datetime.now().isoformat()}",
                value={"post": post, "status": "ready"},
                source=self.agent_key,
            )

            logger.info(f"{self.emoji} LinkedIn post drafted and ready for review")

    async def submit_status_report(self):
        """Submit status report"""
        report = AgentReport(
            agent_name=self.agent_key,
            status="Active",
            metrics={
                "posts_drafted": len(self.posts_drafted),
                "posts_published": len(self.posts_published),
                "this_week": len([p for p in self.posts_published]),  # Simplified
            },
            next_action="Weekly post on Monday",
        )

        await self.coordination.submit_report(report)
