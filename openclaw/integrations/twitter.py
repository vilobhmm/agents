"""Twitter/X integration - Simplified posting and monitoring"""

import logging
import os
from typing import Dict, List, Optional
import tweepy


logger = logging.getLogger(__name__)


class TwitterIntegration:
    """
    Simplified Twitter/X integration.

    Easy access to:
    - Post tweets and threads
    - Search tweets
    - Monitor mentions
    - Get user timeline
    - Track hashtags
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_token_secret: Optional[str] = None,
        bearer_token: Optional[str] = None,
    ):
        """
        Initialize Twitter integration.

        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_token_secret: Twitter access token secret
            bearer_token: Twitter bearer token (for read-only operations)
        """
        self.api_key = api_key or os.getenv("TWITTER_API_KEY")
        self.api_secret = api_secret or os.getenv("TWITTER_API_SECRET")
        self.access_token = access_token or os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.getenv(
            "TWITTER_ACCESS_TOKEN_SECRET"
        )
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")

        self.client = None
        self.api = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Twitter API"""
        try:
            # API v2 client (for posting)
            if all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
                self.client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                    wait_on_rate_limit=True,
                )
                logger.info("Twitter API v2 authenticated successfully")

                # Also create v1.1 API for additional features
                auth = tweepy.OAuth1UserHandler(
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_token_secret,
                )
                self.api = tweepy.API(auth, wait_on_rate_limit=True)

            elif self.bearer_token:
                # Read-only mode
                self.client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    wait_on_rate_limit=True,
                )
                logger.info("Twitter API authenticated (read-only mode)")
            else:
                logger.warning("Twitter API credentials not found")

        except Exception as e:
            logger.error(f"Error authenticating with Twitter: {e}")

    async def post_tweet(self, text: str) -> Optional[str]:
        """
        Post a single tweet.

        Args:
            text: Tweet content (max 280 characters)

        Returns:
            Tweet ID if successful
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return None

        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data["id"]
            logger.info(f"Posted tweet: {tweet_id}")
            return tweet_id

        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None

    async def post_thread(self, tweets: List[str]) -> Optional[List[str]]:
        """
        Post a thread of tweets.

        Args:
            tweets: List of tweet texts

        Returns:
            List of tweet IDs if successful
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return None

        try:
            tweet_ids = []
            previous_id = None

            for tweet_text in tweets:
                if previous_id:
                    response = self.client.create_tweet(
                        text=tweet_text,
                        in_reply_to_tweet_id=previous_id
                    )
                else:
                    response = self.client.create_tweet(text=tweet_text)

                tweet_id = response.data["id"]
                tweet_ids.append(tweet_id)
                previous_id = tweet_id
                logger.info(f"Posted tweet {len(tweet_ids)}/{len(tweets)}: {tweet_id}")

            logger.info(f"Posted thread with {len(tweet_ids)} tweets")
            return tweet_ids

        except Exception as e:
            logger.error(f"Error posting thread: {e}")
            return None

    async def search_tweets(
        self,
        query: str,
        max_results: int = 10,
        recent: bool = True,
    ) -> List[Dict]:
        """
        Search for tweets.

        Args:
            query: Search query (supports Twitter search operators)
            max_results: Maximum number of tweets (10-100)
            recent: If True, get recent tweets; if False, get all

        Returns:
            List of tweet dictionaries
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return []

        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=["created_at", "author_id", "public_metrics", "text"],
            )

            if not tweets.data:
                return []

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_id": tweet.author_id,
                    "metrics": tweet.public_metrics,
                }
                for tweet in tweets.data
            ]

        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []

    async def get_my_mentions(self, max_results: int = 10) -> List[Dict]:
        """
        Get recent mentions of the authenticated user.

        Args:
            max_results: Maximum number of mentions

        Returns:
            List of mention dictionaries
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return []

        try:
            # Get authenticated user ID
            me = self.client.get_me()
            user_id = me.data.id

            mentions = self.client.get_users_mentions(
                id=user_id,
                max_results=max_results,
                tweet_fields=["created_at", "author_id", "public_metrics", "text"],
            )

            if not mentions.data:
                return []

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "author_id": tweet.author_id,
                }
                for tweet in mentions.data
            ]

        except Exception as e:
            logger.error(f"Error getting mentions: {e}")
            return []

    async def get_user_timeline(
        self, username: str, max_results: int = 10
    ) -> List[Dict]:
        """
        Get recent tweets from a specific user.

        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets

        Returns:
            List of tweet dictionaries
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return []

        try:
            # Get user ID
            user = self.client.get_user(username=username)
            if not user.data:
                logger.error(f"User not found: {username}")
                return []

            user_id = user.data.id

            # Get tweets
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "text"],
            )

            if not tweets.data:
                return []

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "metrics": tweet.public_metrics,
                }
                for tweet in tweets.data
            ]

        except Exception as e:
            logger.error(f"Error getting user timeline: {e}")
            return []

    async def track_hashtag(self, hashtag: str, max_results: int = 20) -> List[Dict]:
        """
        Get recent tweets with a specific hashtag.

        Args:
            hashtag: Hashtag to track (with or without #)
            max_results: Maximum number of tweets

        Returns:
            List of tweet dictionaries
        """
        # Clean hashtag
        if not hashtag.startswith("#"):
            hashtag = f"#{hashtag}"

        return await self.search_tweets(query=hashtag, max_results=max_results)

    async def get_trending_ai_tweets(self, max_results: int = 20) -> List[Dict]:
        """Get trending AI-related tweets"""
        queries = ["#AI", "#MachineLearning", "#LLM", "#GenAI"]
        all_tweets = []

        for query in queries:
            tweets = await self.search_tweets(query=query, max_results=max_results // len(queries))
            all_tweets.extend(tweets)

        # Sort by engagement
        all_tweets.sort(
            key=lambda t: (
                t.get("metrics", {}).get("like_count", 0) +
                t.get("metrics", {}).get("retweet_count", 0) * 2
            ),
            reverse=True
        )

        return all_tweets[:max_results]


# Simple interface functions
async def tweet(text: str) -> bool:
    """Quick function to post a tweet"""
    twitter = TwitterIntegration()
    result = await twitter.post_tweet(text)
    return result is not None


async def tweet_thread(tweets: List[str]) -> bool:
    """Quick function to post a thread"""
    twitter = TwitterIntegration()
    result = await twitter.post_thread(tweets)
    return result is not None


async def search_twitter(query: str, max_results: int = 10) -> List[Dict]:
    """Quick function to search Twitter"""
    twitter = TwitterIntegration()
    return await twitter.search_tweets(query, max_results)


async def get_ai_news() -> List[Dict]:
    """Quick function to get AI news from Twitter"""
    twitter = TwitterIntegration()
    return await twitter.get_trending_ai_tweets(max_results=20)
