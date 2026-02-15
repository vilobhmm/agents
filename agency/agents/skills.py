"""
Agent skills - Pre-built capabilities for agents to use.

These skills integrate with external services (Google, Twitter, LinkedIn, etc.)
and can be called by agents to perform actions.
"""

import asyncio
import logging
from typing import Dict, List, Optional

# Import integrations
try:
    from openclaw.integrations import (
        GoogleServices,
        TwitterIntegration,
        LinkedInIntegration,
        GitHubIntegration,
    )
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    INTEGRATIONS_AVAILABLE = False
    logging.warning("Integrations not available. Install openclaw integrations first.")


logger = logging.getLogger(__name__)


class ResearchSkills:
    """Skills for research agents"""

    def __init__(self):
        if INTEGRATIONS_AVAILABLE:
            self.twitter = TwitterIntegration()

    async def get_ai_news_from_twitter(self, max_results: int = 20) -> List[Dict]:
        """Get trending AI news from Twitter"""
        if not INTEGRATIONS_AVAILABLE:
            return []

        try:
            tweets = await self.twitter.get_trending_ai_tweets(max_results)
            return tweets
        except Exception as e:
            logger.error(f"Error getting AI news from Twitter: {e}")
            return []

    async def search_twitter(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Twitter for specific topics"""
        if not INTEGRATIONS_AVAILABLE:
            return []

        try:
            tweets = await self.twitter.search_tweets(query, max_results)
            return tweets
        except Exception as e:
            logger.error(f"Error searching Twitter: {e}")
            return []

    async def track_hashtag(self, hashtag: str, max_results: int = 20) -> List[Dict]:
        """Track a specific hashtag"""
        if not INTEGRATIONS_AVAILABLE:
            return []

        try:
            tweets = await self.twitter.track_hashtag(hashtag, max_results)
            return tweets
        except Exception as e:
            logger.error(f"Error tracking hashtag: {e}")
            return []


class SocialSkills:
    """Skills for social media agents"""

    def __init__(self):
        if INTEGRATIONS_AVAILABLE:
            self.twitter = TwitterIntegration()
            self.linkedin = LinkedInIntegration()

    async def post_tweet(self, text: str) -> bool:
        """Post a tweet"""
        if not INTEGRATIONS_AVAILABLE:
            logger.info(f"[SIMULATION] Would post tweet: {text}")
            return True

        try:
            result = await self.twitter.post_tweet(text)
            return result is not None
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False

    async def post_thread(self, tweets: List[str]) -> bool:
        """Post a Twitter thread"""
        if not INTEGRATIONS_AVAILABLE:
            logger.info(f"[SIMULATION] Would post thread: {len(tweets)} tweets")
            return True

        try:
            result = await self.twitter.post_thread(tweets)
            return result is not None
        except Exception as e:
            logger.error(f"Error posting thread: {e}")
            return False

    async def post_to_linkedin(self, text: str) -> bool:
        """Post to LinkedIn"""
        if not INTEGRATIONS_AVAILABLE:
            logger.info(f"[SIMULATION] Would post to LinkedIn: {text}")
            return True

        try:
            result = await self.linkedin.post_update(text)
            return result is not None
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False

    async def share_article_on_linkedin(self, url: str, commentary: str) -> bool:
        """Share an article on LinkedIn"""
        if not INTEGRATIONS_AVAILABLE:
            logger.info(f"[SIMULATION] Would share on LinkedIn: {url}")
            return True

        try:
            result = await self.linkedin.post_article_share(url, commentary)
            return result is not None
        except Exception as e:
            logger.error(f"Error sharing article: {e}")
            return False


class ContextSkills:
    """Skills for understanding user context"""

    def __init__(self):
        if INTEGRATIONS_AVAILABLE:
            self.google = GoogleServices()

    async def get_daily_context(self) -> Dict:
        """Get user's daily context from Google services"""
        if not INTEGRATIONS_AVAILABLE:
            return {
                "unread_emails": [],
                "todays_events": [],
                "recent_files": [],
            }

        try:
            context = await self.google.get_daily_context()
            return context
        except Exception as e:
            logger.error(f"Error getting daily context: {e}")
            return {}

    async def get_next_meeting(self) -> Optional[Dict]:
        """Get information about next meeting"""
        if not INTEGRATIONS_AVAILABLE:
            return None

        try:
            meeting_info = await self.google.get_next_meeting_info()
            return meeting_info
        except Exception as e:
            logger.error(f"Error getting next meeting: {e}")
            return None

    async def search_drive(self, query: str) -> List[Dict]:
        """Search Google Drive"""
        if not INTEGRATIONS_AVAILABLE:
            return []

        try:
            files = await self.google.search_files(query)
            return files
        except Exception as e:
            logger.error(f"Error searching Drive: {e}")
            return []


class GitHubSkills:
    """Skills for GitHub operations"""

    def __init__(self):
        if INTEGRATIONS_AVAILABLE:
            self.github = GitHubIntegration()

    async def search_repositories(self, query: str) -> List[Dict]:
        """Search GitHub repositories"""
        if not INTEGRATIONS_AVAILABLE:
            return []

        try:
            # Assuming GitHubIntegration has a search method
            # Implement based on actual integration
            return []
        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")
            return []


# Example usage in agent system prompts:
RESEARCHER_TOOLS_GUIDE = """
## Available Research Tools

You have access to these research capabilities:

### Twitter/X Research
- `get_ai_news_from_twitter()` - Get trending AI news
- `search_twitter(query)` - Search for specific topics
- `track_hashtag(hashtag)` - Track hashtag conversations

### Context Awareness
- `get_daily_context()` - Get user's emails, calendar, files
- `get_next_meeting()` - Get upcoming meeting info
- `search_drive(query)` - Search user's Google Drive

To use these tools, mention them in your response and I'll execute them for you.
"""

SOCIAL_TOOLS_GUIDE = """
## Available Social Media Tools

You can perform these social media actions:

### Twitter/X
- `post_tweet(text)` - Post a single tweet (max 280 chars)
- `post_thread(tweets)` - Post a Twitter thread

### LinkedIn
- `post_to_linkedin(text)` - Post an update
- `share_article_on_linkedin(url, commentary)` - Share article with your take

Let me know what you'd like to post and I'll handle it!
"""
