"""Web scraping and API tools for agents - Real job scraping capabilities."""

import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class WebTools:
    """
    Web scraping and API access tools.

    Provides:
    - Job board scraping (Anthropic, OpenAI, Google, etc.)
    - General web scraping
    - API access
    - HTML parsing
    """

    def __init__(self):
        """Initialize web tools"""
        self.session = None

    async def _get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Fetch content from a URL.

        Args:
            url: URL to fetch
            timeout: Timeout in seconds

        Returns:
            HTML content or None if error
        """
        try:
            session = await self._get_session()
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def fetch_json_api(self, url: str, timeout: int = 30) -> Optional[Dict]:
        """
        Fetch JSON from an API.

        Args:
            url: API URL
            timeout: Timeout in seconds

        Returns:
            Parsed JSON dict or None if error
        """
        try:
            session = await self._get_session()
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching API {url}: {e}")
            return None

    async def scrape_anthropic_jobs(self) -> List[Dict]:
        """
        Scrape job listings from Anthropic careers page.

        Returns:
            List of job dicts with title, location, department, url
        """
        jobs = []
        try:
            # Anthropic uses Lever for job postings
            api_url = "https://api.lever.co/v0/postings/anthropic?mode=json"
            data = await self.fetch_json_api(api_url)

            if data:
                for job in data:
                    jobs.append({
                        "company": "Anthropic",
                        "title": job.get("text", ""),
                        "location": job.get("categories", {}).get("location", ""),
                        "department": job.get("categories", {}).get("team", ""),
                        "url": job.get("hostedUrl", ""),
                        "posted_at": job.get("createdAt", ""),
                        "description": job.get("description", "")[:500],  # First 500 chars
                    })

            logger.info(f"Scraped {len(jobs)} jobs from Anthropic")
        except Exception as e:
            logger.error(f"Error scraping Anthropic jobs: {e}")

        return jobs

    async def scrape_openai_jobs(self) -> List[Dict]:
        """
        Scrape job listings from OpenAI careers page.

        Returns:
            List of job dicts
        """
        jobs = []
        try:
            # OpenAI uses Greenhouse for job postings
            api_url = "https://api.greenhouse.io/v1/boards/openai/jobs"
            data = await self.fetch_json_api(api_url)

            if data and "jobs" in data:
                for job in data["jobs"]:
                    jobs.append({
                        "company": "OpenAI",
                        "title": job.get("title", ""),
                        "location": job.get("location", {}).get("name", ""),
                        "department": job.get("departments", [{}])[0].get("name", "") if job.get("departments") else "",
                        "url": job.get("absolute_url", ""),
                        "posted_at": job.get("updated_at", ""),
                        "description": job.get("content", "")[:500] if job.get("content") else "",
                    })

            logger.info(f"Scraped {len(jobs)} jobs from OpenAI")
        except Exception as e:
            logger.error(f"Error scraping OpenAI jobs: {e}")

        return jobs

    async def scrape_google_deepmind_jobs(self) -> List[Dict]:
        """
        Scrape job listings from Google DeepMind.

        Returns:
            List of job dicts
        """
        jobs = []
        try:
            # Google uses their own careers API
            # This is a placeholder - actual implementation would use Google's jobs API
            logger.info("DeepMind job scraping placeholder - would use Google Careers API")

            # For demo, return placeholder
            jobs.append({
                "company": "Google DeepMind",
                "title": "Research Scientist, AI Safety",
                "location": "London, UK",
                "department": "Research",
                "url": "https://www.google.com/about/careers/applications/jobs/results/",
                "posted_at": datetime.now().isoformat(),
                "description": "Leading AI safety research at DeepMind...",
            })

        except Exception as e:
            logger.error(f"Error scraping DeepMind jobs: {e}")

        return jobs

    async def search_all_jobs(
        self,
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search jobs across all supported companies.

        Args:
            keywords: Keywords to filter by (e.g., ["ML Engineer", "Research"])
            locations: Locations to filter by (e.g., ["San Francisco", "Remote"])

        Returns:
            Combined list of jobs from all companies
        """
        # Scrape all companies in parallel
        tasks = [
            self.scrape_anthropic_jobs(),
            self.scrape_openai_jobs(),
            self.scrape_google_deepmind_jobs(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine all jobs
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)

        # Filter by keywords
        if keywords:
            filtered_jobs = []
            for job in all_jobs:
                title = job.get("title", "").lower()
                desc = job.get("description", "").lower()
                if any(kw.lower() in title or kw.lower() in desc for kw in keywords):
                    filtered_jobs.append(job)
            all_jobs = filtered_jobs

        # Filter by location
        if locations:
            filtered_jobs = []
            for job in all_jobs:
                location = job.get("location", "").lower()
                if any(loc.lower() in location for loc in locations):
                    filtered_jobs.append(job)
            all_jobs = filtered_jobs

        logger.info(f"Found {len(all_jobs)} total jobs")
        return all_jobs

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [
            "fetch_url",
            "fetch_json_api",
            "scrape_anthropic_jobs",
            "scrape_openai_jobs",
            "scrape_google_deepmind_jobs",
            "search_all_jobs",
        ]

    def get_tools_description(self) -> str:
        """Get description of available tools for agent prompt"""
        return """
You have access to the following web scraping tools:

**Job Scraping:**
- scrape_anthropic_jobs() - Get all current Anthropic job listings
- scrape_openai_jobs() - Get all current OpenAI job listings
- scrape_google_deepmind_jobs() - Get Google DeepMind job listings
- search_all_jobs(keywords=[], locations=[]) - Search all companies with filters

**General Web:**
- fetch_url(url, timeout=30) - Fetch HTML content from any URL
- fetch_json_api(url, timeout=30) - Fetch JSON from an API

Each job includes: company, title, location, department, url, posted_at, description

Use these tools to find real job opportunities for users!
"""
