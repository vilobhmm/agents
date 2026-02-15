"""Code Review Companion Agent"""

import logging
from typing import Any, Dict, List

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.github import GitHubIntegration
from openclaw.integrations.telegram import TelegramIntegration


logger = logging.getLogger(__name__)


class CodeReviewAgent(Agent):
    """Code Review Companion Agent"""

    def __init__(self, api_key: str = None, repos: List[str] = None):
        config = AgentConfig(
            name="Code Review Companion",
            description="I monitor PRs, analyze code changes, and provide review suggestions.",
            proactive=True,
        )

        super().__init__(config, api_key)

        self.github = GitHubIntegration()
        self.telegram = TelegramIntegration()
        self.repos = repos or []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Scanning for open pull requests")

        all_prs = []
        for repo in self.repos:
            prs = await self.github.get_pull_requests(repo, state="open")
            all_prs.extend([(repo, pr) for pr in prs])

        if not all_prs:
            logger.info("No open PRs found")
            return {"status": "no_prs"}

        # Review each PR
        reviews = []
        for repo, pr in all_prs:
            review = await self.review_pr(repo, pr)
            if review:
                reviews.append(review)

        # Send daily digest
        if reviews:
            await self.send_digest(reviews)

        return {"status": "success", "prs_reviewed": len(reviews)}

    async def review_pr(self, repo: str, pr: Dict) -> Dict:
        """Review a pull request"""
        pr_number = pr["number"]
        logger.info(f"Reviewing PR #{pr_number} in {repo}")

        # Get PR files
        files = await self.github.get_pr_files(repo, pr_number)

        # Analyze changes
        analysis = await self.analyze_code_changes(pr, files)

        # Generate review comments
        suggestions = await self.generate_suggestions(pr, files, analysis)

        return {
            "repo": repo,
            "pr_number": pr_number,
            "title": pr["title"],
            "author": pr["author"],
            "analysis": analysis,
            "suggestions": suggestions,
        }

    async def analyze_code_changes(self, pr: Dict, files: List[Dict]) -> str:
        """Analyze code changes using Claude"""

        # Prepare file changes summary
        files_summary = []
        for f in files[:10]:  # Limit to first 10 files
            files_summary.append(
                f"- {f['filename']}: +{f['additions']} -{f['deletions']}"
            )

        files_text = "\n".join(files_summary)

        prompt = f"""Analyze this pull request:

**Title:** {pr['title']}
**Description:** {pr.get('body', 'No description')}

**Files Changed:**
{files_text}

Provide:
1. Overview of changes
2. Potential issues or concerns
3. Areas needing careful review"""

        analysis = await self.chat(prompt)
        return analysis

    async def generate_suggestions(
        self, pr: Dict, files: List[Dict], analysis: str
    ) -> List[str]:
        """Generate review suggestions"""

        prompt = f"""Based on this analysis, provide 3-5 specific, constructive review suggestions:

{analysis}

Focus on:
- Code quality improvements
- Potential bugs or edge cases
- Best practices
- Testing recommendations

Return only the suggestions as a bulleted list."""

        response = await self.chat(prompt)

        # Parse suggestions
        lines = response.strip().split("\n")
        suggestions = [
            line.strip("- •*").strip()
            for line in lines
            if line.strip() and any(c.isalpha() for c in line)
        ]

        return suggestions[:5]

    async def send_digest(self, reviews: List[Dict]):
        """Send daily PR review digest"""

        digest = "Code Review Digest:\n\n"

        for review in reviews:
            digest += f"*{review['repo']} PR #{review['pr_number']}*\n"
            digest += f"Title: {review['title']}\n"
            digest += f"Author: {review['author']}\n"
            digest += f"\nAnalysis:\n{review['analysis'][:300]}...\n"

            if review.get("suggestions"):
                digest += "\nSuggestions:\n"
                for sugg in review["suggestions"][:3]:
                    digest += f"- {sugg}\n"

            digest += "\n---\n\n"

        await self.telegram.send_message(digest)
        logger.info("Sent PR review digest")
