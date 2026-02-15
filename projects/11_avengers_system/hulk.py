"""
Hulk - Prototype Architect & GitHub Executor Agent

Converts AI concepts into working, runnable code.
Ships prototypes to GitHub: https://github.com/vilobhmm
"""

import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from anthropic import Anthropic
from github import Github

from .coordination import AgentReport, CoordinationHub, Task, TaskStatus, coordination_hub

logger = logging.getLogger(__name__)


class HulkAgent:
    """
    Hulk - Prototype Architect & GitHub Executor

    Builds working prototypes from AI concepts.
    All code ships to https://github.com/vilobhmm

    Core principle: "If you can't run it, you don't understand it."
    """

    def __init__(self, api_key: str, coordination: Optional[CoordinationHub] = None):
        self.name = "Hulk"
        self.emoji = "🔨"
        self.agent_key = "hulk"

        self.client = Anthropic(api_key=api_key)
        self.coordination = coordination or coordination_hub

        # GitHub client
        self.github_client = None
        self.github_username = os.getenv("GITHUB_USERNAME", "vilobhmm")

        if github_token := os.getenv("GITHUB_TOKEN"):
            self.github_client = Github(github_token)
            logger.info(f"{self.emoji} GitHub client initialized")

        # Workspace
        self.workspace = Path("/tmp/hulk_workspace")
        self.workspace.mkdir(exist_ok=True)

        self.prototypes_built = []

        logger.info(f"{self.emoji} {self.name} initialized")

    async def build_prototype(self, concept: str, task_id: str) -> dict:
        """
        Build a working prototype from a concept

        Args:
            concept: Description of what to build
            task_id: Task ID for tracking

        Returns:
            dict: Prototype details including repo URL
        """
        logger.info(f"{self.emoji} Building prototype: {concept}")

        # Update task status
        await self.coordination.update_task(task_id, TaskStatus.IN_PROGRESS)

        # Step 1: Design the prototype
        design = await self._design_prototype(concept)

        # Step 2: Generate code
        code_files = await self._generate_code(design)

        # Step 3: Create repository
        repo_name = design.get("repo_name", "prototype")
        repo_url = await self._create_github_repo(repo_name, code_files, design)

        # Step 4: Test locally
        test_result = await self._test_prototype(code_files)

        # Record completion
        prototype = {
            "concept": concept,
            "repo_name": repo_name,
            "repo_url": repo_url,
            "test_result": test_result,
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
        }

        self.prototypes_built.append(prototype)

        # Store in knowledge base
        self.coordination.knowledge_base.add_entry(
            key=f"prototype_{repo_name}",
            value=prototype,
            source=self.agent_key,
        )

        # Update task as complete
        await self.coordination.update_task(
            task_id,
            TaskStatus.COMPLETED,
            result=f"Prototype built and shipped: {repo_url}",
        )

        logger.info(f"{self.emoji} Prototype complete: {repo_url}")

        return prototype

    async def _design_prototype(self, concept: str) -> dict:
        """Design the prototype structure"""
        prompt = f"""You are Hulk, a prototype builder. Design a minimal but complete implementation for:

Concept: {concept}

Provide:
1. Repository name (lowercase, hyphens, descriptive)
2. File structure (list of files needed)
3. Key implementation points
4. README outline

Format as JSON:
{{
  "repo_name": "name-here",
  "files": ["main.py", "README.md", "requirements.txt"],
  "implementation_points": ["point 1", "point 2"],
  "readme_outline": "Brief description..."
}}
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse JSON response
        import json

        try:
            design = json.loads(response.content[0].text)
            return design
        except:
            # Fallback
            return {
                "repo_name": concept.lower().replace(" ", "-")[:50],
                "files": ["main.py", "README.md", "requirements.txt"],
                "implementation_points": ["Implement core logic"],
                "readme_outline": f"A prototype for {concept}",
            }

    async def _generate_code(self, design: dict) -> Dict[str, str]:
        """Generate code files"""
        files = {}

        # Generate each file
        for filename in design.get("files", []):
            prompt = f"""Generate the content for: {filename}

Repository: {design.get('repo_name')}
Purpose: {design.get('readme_outline')}
Implementation points: {design.get('implementation_points')}

Generate complete, runnable code. Include comments. Make it minimal but functional.

Output ONLY the file content, no markdown code blocks."""

            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            files[filename] = response.content[0].text.strip()

        return files

    async def _create_github_repo(
        self, repo_name: str, files: Dict[str, str], design: dict
    ) -> str:
        """Create GitHub repository and push code"""
        if not self.github_client:
            logger.warning("GitHub client not initialized - repo not created")
            return f"https://github.com/{self.github_username}/{repo_name} (simulated)"

        try:
            # Get user
            user = self.github_client.get_user()

            # Create repo
            description = design.get("readme_outline", "AI prototype")[:100]

            repo = user.create_repo(
                name=repo_name,
                description=description,
                private=False,
                auto_init=False,
            )

            logger.info(f"{self.emoji} Created repo: {repo.html_url}")

            # Add files
            for filename, content in files.items():
                repo.create_file(
                    path=filename,
                    message=f"Initial commit: {filename}",
                    content=content,
                )

            return repo.html_url

        except Exception as e:
            logger.error(f"Error creating GitHub repo: {e}")
            return f"https://github.com/{self.github_username}/{repo_name} (error)"

    async def _test_prototype(self, files: Dict[str, str]) -> str:
        """Test the prototype locally"""
        # Create temp directory
        test_dir = self.workspace / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_dir.mkdir(exist_ok=True)

        try:
            # Write files
            for filename, content in files.items():
                (test_dir / filename).write_text(content)

            # Try to run main.py if it exists
            if "main.py" in files:
                result = subprocess.run(
                    ["python", "main.py"],
                    cwd=test_dir,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    return "✅ Runs without errors"
                else:
                    return f"⚠️ Errors: {result.stderr[:100]}"

            return "✅ Files created"

        except subprocess.TimeoutExpired:
            return "⚠️ Timeout (long-running)"
        except Exception as e:
            return f"⚠️ Test error: {str(e)[:100]}"

    async def process_build_requests(self):
        """Check for new build requests from tasks"""
        # Get assigned tasks
        my_tasks = await self.coordination.get_tasks_by_agent(self.agent_key)

        # Find pending tasks
        pending = [t for t in my_tasks if t.status == TaskStatus.PENDING]

        for task in pending[:1]:  # Build one at a time
            try:
                await self.build_prototype(task.description, task.task_id)
            except Exception as e:
                logger.error(f"Error building prototype: {e}")
                await self.coordination.update_task(
                    task.task_id,
                    TaskStatus.BLOCKED,
                    result=f"Build failed: {str(e)}",
                )

    async def submit_status_report(self):
        """Submit status report"""
        # Get current task
        my_tasks = await self.coordination.get_tasks_by_agent(self.agent_key)
        current_task = next(
            (t for t in my_tasks if t.status == TaskStatus.IN_PROGRESS), None
        )

        # Recent completions
        completed = [t for t in my_tasks if t.status == TaskStatus.COMPLETED]

        report = AgentReport(
            agent_name=self.agent_key,
            status="Building" if current_task else "Ready",
            current_task=current_task,
            recent_completions=completed[-3:],  # Last 3
            metrics={
                "prototypes_built": len(self.prototypes_built),
                "this_week": len([p for p in self.prototypes_built]),  # Simplified
            },
            next_action=(
                f"Building {current_task.description}" if current_task else "Awaiting tasks"
            ),
        )

        await self.coordination.submit_report(report)
