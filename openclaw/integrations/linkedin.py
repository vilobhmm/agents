"""LinkedIn integration - Simplified posting and networking"""

import logging
import os
from typing import Dict, List, Optional
import requests


logger = logging.getLogger(__name__)


class LinkedInIntegration:
    """
    Simplified LinkedIn integration.

    Features:
    - Post updates
    - Share articles
    - Get profile info
    - Post thought leadership content

    Note: LinkedIn API access is restricted. This supports both:
    - Official API (requires approval)
    - Alternative posting methods
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """
        Initialize LinkedIn integration.

        Args:
            access_token: LinkedIn access token (if you have API access)
            client_id: LinkedIn client ID
            client_secret: LinkedIn client secret
        """
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.client_id = client_id or os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("LINKEDIN_CLIENT_SECRET")

        self.api_url = "https://api.linkedin.com/v2"
        self.has_api_access = bool(self.access_token)

        if self.has_api_access:
            logger.info("LinkedIn API initialized with official access")
        else:
            logger.info("LinkedIn API initialized (no API access - manual mode)")

    async def post_update(
        self,
        text: str,
        visibility: str = "PUBLIC",
    ) -> Optional[str]:
        """
        Post a text update to LinkedIn.

        Args:
            text: Post content
            visibility: Post visibility (PUBLIC, CONNECTIONS)

        Returns:
            Post ID if successful
        """
        if not self.has_api_access:
            logger.warning(
                "No LinkedIn API access. Use manual posting or get API approval."
            )
            return await self._manual_post_guide(text)

        try:
            # Get user profile URN
            profile = await self.get_profile()
            if not profile:
                logger.error("Could not get LinkedIn profile")
                return None

            person_urn = profile["id"]

            # Create post
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }

            post_data = {
                "author": f"urn:li:person:{person_urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                },
            }

            response = requests.post(
                f"{self.api_url}/ugcPosts",
                headers=headers,
                json=post_data,
            )
            response.raise_for_status()

            post_id = response.headers.get("X-RestLi-Id")
            logger.info(f"Posted LinkedIn update: {post_id}")
            return post_id

        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return None

    async def post_article_share(
        self,
        article_url: str,
        commentary: str,
        visibility: str = "PUBLIC",
    ) -> Optional[str]:
        """
        Share an article with commentary.

        Args:
            article_url: URL of the article to share
            commentary: Your commentary on the article
            visibility: Post visibility

        Returns:
            Post ID if successful
        """
        if not self.has_api_access:
            logger.warning("No LinkedIn API access")
            return await self._manual_post_guide(f"{commentary}\n\n{article_url}")

        try:
            profile = await self.get_profile()
            if not profile:
                return None

            person_urn = profile["id"]

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }

            post_data = {
                "author": f"urn:li:person:{person_urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": commentary},
                        "shareMediaCategory": "ARTICLE",
                        "media": [
                            {
                                "status": "READY",
                                "originalUrl": article_url,
                            }
                        ],
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                },
            }

            response = requests.post(
                f"{self.api_url}/ugcPosts",
                headers=headers,
                json=post_data,
            )
            response.raise_for_status()

            post_id = response.headers.get("X-RestLi-Id")
            logger.info(f"Shared article on LinkedIn: {post_id}")
            return post_id

        except Exception as e:
            logger.error(f"Error sharing article: {e}")
            return None

    async def get_profile(self) -> Optional[Dict]:
        """Get authenticated user's profile information"""
        if not self.has_api_access:
            logger.warning("No LinkedIn API access")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
            }

            response = requests.get(
                f"{self.api_url}/me",
                headers=headers,
            )
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"Error getting profile: {e}")
            return None

    async def _manual_post_guide(self, content: str) -> Optional[str]:
        """
        Provide guidance for manual posting when API access is not available.

        Args:
            content: The content to post

        Returns:
            None (prints instructions)
        """
        logger.info("=" * 60)
        logger.info("LINKEDIN MANUAL POST")
        logger.info("=" * 60)
        logger.info("\nContent to post:")
        logger.info("-" * 60)
        logger.info(content)
        logger.info("-" * 60)
        logger.info("\nTo post this to LinkedIn:")
        logger.info("1. Go to https://www.linkedin.com")
        logger.info("2. Click 'Start a post'")
        logger.info("3. Copy the content above")
        logger.info("4. Paste and click 'Post'")
        logger.info("=" * 60)
        return None

    async def create_thought_leadership_post(
        self,
        topic: str,
        insights: List[str],
        cta: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a formatted thought leadership post.

        Args:
            topic: Main topic/title
            insights: List of key insights (2-5 points)
            cta: Optional call-to-action

        Returns:
            Post ID if successful
        """
        # Format post
        post_lines = [f"💡 {topic}", ""]

        for i, insight in enumerate(insights, 1):
            post_lines.append(f"{i}. {insight}")

        post_lines.append("")

        if cta:
            post_lines.append(cta)
        else:
            post_lines.append("What are your thoughts? 💭")

        post_text = "\n".join(post_lines)

        return await self.post_update(post_text)


# Simple interface functions
async def post_to_linkedin(text: str) -> bool:
    """Quick function to post to LinkedIn"""
    linkedin = LinkedInIntegration()
    result = await linkedin.post_update(text)
    return result is not None


async def share_article_on_linkedin(url: str, commentary: str) -> bool:
    """Quick function to share an article"""
    linkedin = LinkedInIntegration()
    result = await linkedin.post_article_share(url, commentary)
    return result is not None


async def post_thought_leadership(
    topic: str,
    insights: List[str],
    cta: Optional[str] = None,
) -> bool:
    """Quick function to post thought leadership content"""
    linkedin = LinkedInIntegration()
    result = await linkedin.create_thought_leadership_post(topic, insights, cta)
    return result is not None
