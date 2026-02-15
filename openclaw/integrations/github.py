"""GitHub integration"""

import logging
import os
from typing import Dict, List, Optional

from github import Github, GithubException


logger = logging.getLogger(__name__)


class GitHubIntegration:
    """GitHub API integration"""

    def __init__(
        self,
        token: Optional[str] = None,
        username: Optional[str] = None,
    ):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.username = username or os.getenv("GITHUB_USERNAME")

        if not self.token:
            logger.warning("GitHub token not provided")
            self.client = None
        else:
            self.client = Github(self.token)
            logger.info("GitHub client initialized")

    async def get_pull_requests(
        self, repo_name: str, state: str = "open"
    ) -> List[Dict]:
        """
        Get pull requests for a repository.

        Args:
            repo_name: Repository name (format: owner/repo)
            state: PR state (open, closed, all)

        Returns:
            List of PR dictionaries
        """
        if not self.client:
            logger.error("GitHub client not initialized")
            return []

        try:
            repo = self.client.get_repo(repo_name)
            prs = repo.get_pulls(state=state)

            pr_list = []
            for pr in prs:
                pr_list.append(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "author": pr.user.login,
                        "created_at": pr.created_at,
                        "updated_at": pr.updated_at,
                        "url": pr.html_url,
                        "body": pr.body,
                    }
                )

            return pr_list

        except GithubException as e:
            logger.error(f"Error fetching pull requests: {e}")
            return []

    async def get_pr_files(self, repo_name: str, pr_number: int) -> List[Dict]:
        """Get files changed in a PR"""
        if not self.client:
            logger.error("GitHub client not initialized")
            return []

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            files = pr.get_files()

            file_list = []
            for file in files:
                file_list.append(
                    {
                        "filename": file.filename,
                        "status": file.status,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "changes": file.changes,
                        "patch": file.patch if hasattr(file, "patch") else None,
                    }
                )

            return file_list

        except GithubException as e:
            logger.error(f"Error fetching PR files: {e}")
            return []

    async def create_pr_comment(
        self, repo_name: str, pr_number: int, comment: str
    ) -> bool:
        """
        Create a comment on a PR.

        Args:
            repo_name: Repository name
            pr_number: PR number
            comment: Comment text

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("GitHub client not initialized")
            return False

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment)

            logger.info(f"Created comment on PR #{pr_number}")
            return True

        except GithubException as e:
            logger.error(f"Error creating PR comment: {e}")
            return False

    async def get_repo_info(self, repo_name: str) -> Optional[Dict]:
        """Get repository information"""
        if not self.client:
            logger.error("GitHub client not initialized")
            return None

        try:
            repo = self.client.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "url": repo.html_url,
            }

        except GithubException as e:
            logger.error(f"Error fetching repo info: {e}")
            return None

    async def search_code(
        self, query: str, repo_name: Optional[str] = None
    ) -> List[Dict]:
        """
        Search code in repositories.

        Args:
            query: Search query
            repo_name: Optional repository to search in

        Returns:
            List of code search results
        """
        if not self.client:
            logger.error("GitHub client not initialized")
            return []

        try:
            if repo_name:
                query = f"{query} repo:{repo_name}"

            results = self.client.search_code(query)

            code_list = []
            for result in results[:20]:  # Limit to 20 results
                code_list.append(
                    {
                        "name": result.name,
                        "path": result.path,
                        "repository": result.repository.full_name,
                        "url": result.html_url,
                    }
                )

            return code_list

        except GithubException as e:
            logger.error(f"Error searching code: {e}")
            return []

    async def get_user_repos(self, username: Optional[str] = None) -> List[Dict]:
        """Get repositories for a user"""
        if not self.client:
            logger.error("GitHub client not initialized")
            return []

        user = username or self.username
        if not user:
            logger.error("No username provided")
            return []

        try:
            user_obj = self.client.get_user(user)
            repos = user_obj.get_repos()

            repo_list = []
            for repo in repos:
                repo_list.append(
                    {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "private": repo.private,
                        "url": repo.html_url,
                        "updated_at": repo.updated_at,
                    }
                )

            return repo_list

        except GithubException as e:
            logger.error(f"Error fetching user repos: {e}")
            return []
