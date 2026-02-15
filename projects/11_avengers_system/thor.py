"""
Thor - X/Twitter Operator Agent

Converts intelligence into high-impact tweets and threads.
Builds online presence through timely, authoritative commentary.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import tweepy
from anthropic import Anthropic

from .coordination import AgentReport, CoordinationHub, Task, coordination_hub

logger = logging.getLogger(__name__)


class ThorAgent:
    """
    Thor - X/Twitter Operator

    Takes research intelligence and crafts:
    - High-impact single tweets
    - Threads
    - Rapid commentary on breaking news

    Tone: Sharp, authoritative, fast-moving
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Thor"
        self.emoji = "⚡"
        self.agent_key = "thor"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub

        # Initialize Twitter client
        self.twitter_client = None
        if all(
            [
                os.getenv("TWITTER_API_KEY"),
                os.getenv("TWITTER_API_SECRET"),
                os.getenv("TWITTER_ACCESS_TOKEN"),
                os.getenv("TWITTER_ACCESS_SECRET"),
            ]
        ):
            try:
                auth = tweepy.OAuth1UserHandler(
                    os.getenv("TWITTER_API_KEY"),
                    os.getenv("TWITTER_API_SECRET"),
                    os.getenv("TWITTER_ACCESS_TOKEN"),
                    os.getenv("TWITTER_ACCESS_SECRET"),
                )

                self.twitter_client = tweepy.API(auth)
                logger.info(f"{self.emoji} Twitter client initialized")

            except Exception as e:
                logger.warning(f"Could not initialize Twitter client: {e}")

        self.tweets_today = []

        logger.info(f"{self.emoji} {self.name} initialized")

    async def create_tweet_from_intel(self, intel: dict) -> Optional[str]:
        """
        Create a tweet from intelligence update

        Args:
            intel: Intelligence update dict from Captain America

        Returns:
            str: Tweet text (or None if skipped)
        """
        # Use Claude to craft tweet
        prompt = f"""You are Thor, an authoritative AI researcher on X/Twitter.

Intelligence update:
Source: {intel.get('source')}
Title: {intel.get('title')}
URL: {intel.get('url')}

Craft a high-impact tweet (max 280 chars) that:
1. Captures the key insight
2. Is authoritative and sharp
3. Drives engagement
4. Includes the URL

Make it thunder. No fluff."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )

        tweet_text = response.content[0].text.strip()

        # Ensure it's within limits
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:276] + "..."

        return tweet_text

    async def create_thread_from_research(
        self, research_report: dict
    ) -> List[str]:
        """
        Create a Twitter thread from research report

        Args:
            research_report: Full research report

        Returns:
            List[str]: Thread tweets
        """
        prompt = f"""You are Thor. Create a Twitter thread about these AI developments:

{research_report.get('summary', '')}

Key updates:
{chr(10).join([f"• {u['title']}" for u in research_report.get('updates', [])[:5]])}

Create 3-5 tweets for a thread:
- Tweet 1: Hook (what's happening)
- Tweet 2-4: Key insights
- Tweet 5: Impact/conclusion

Each tweet max 280 chars. Sharp, authoritative, engaging.
Format: Separate tweets with "---"
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )

        thread_text = response.content[0].text

        # Split into tweets
        tweets = [t.strip() for t in thread_text.split("---")]

        # Ensure each is within limit
        tweets = [t[:280] if len(t) > 280 else t for t in tweets]

        return tweets[:5]  # Max 5 tweets

    async def post_tweet(self, text: str) -> bool:
        """Post a tweet"""
        if not self.twitter_client:
            logger.warning("Twitter client not initialized - tweet not posted")
            logger.info(f"Would post: {text}")
            return False

        try:
            self.twitter_client.update_status(text)
            self.tweets_today.append({"text": text, "timestamp": datetime.now()})

            logger.info(f"{self.emoji} Tweet posted")
            return True

        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False

    async def post_thread(self, tweets: List[str]) -> bool:
        """Post a thread"""
        if not self.twitter_client:
            logger.warning("Twitter client not initialized - thread not posted")
            logger.info(f"Would post thread with {len(tweets)} tweets")
            return False

        try:
            # Post first tweet
            status = self.twitter_client.update_status(tweets[0])
            reply_to_id = status.id

            # Post replies
            for tweet in tweets[1:]:
                status = self.twitter_client.update_status(
                    tweet, in_reply_to_status_id=reply_to_id
                )
                reply_to_id = status.id

            self.tweets_today.extend(
                [{"text": t, "timestamp": datetime.now()} for t in tweets]
            )

            logger.info(f"{self.emoji} Thread posted ({len(tweets)} tweets)")
            return True

        except Exception as e:
            logger.error(f"Error posting thread: {e}")
            return False

    async def process_research_updates(self):
        """
        Check for new research updates and create tweets

        Called periodically (every 30 min)
        """
        # Get recent Captain America reports
        recent_intel = self.coordination.knowledge_base.get_by_source("captain_america")

        # Filter to last hour
        one_hour_ago = datetime.now().replace(microsecond=0)

        new_intel = [
            e
            for e in recent_intel
            if datetime.fromisoformat(e["timestamp"]) > one_hour_ago
        ]

        if not new_intel:
            logger.info(f"{self.emoji} No new intelligence to tweet about")
            return

        # Create tweets from top updates
        for entry in new_intel[:3]:  # Top 3
            if "value" in entry and isinstance(entry["value"], dict):
                report = entry["value"]

                if report.get("updates"):
                    # Create tweet from first update
                    tweet = await self.create_tweet_from_intel(report["updates"][0])

                    if tweet:
                        await self.post_tweet(tweet)

    async def submit_status_report(self):
        """Submit status report"""
        report = AgentReport(
            agent_name=self.agent_key,
            status="Active",
            metrics={
                "tweets_today": len(self.tweets_today),
                "last_tweet": (
                    self.tweets_today[-1]["timestamp"].strftime("%H:%M")
                    if self.tweets_today
                    else "Never"
                ),
            },
            next_action="Monitor for breaking AI news",
        )

        await self.coordination.submit_report(report)
