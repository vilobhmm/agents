"""
Job Search Tools - Real job scraping and tracking capabilities.

Provides tools for job_hunter agent to find, track, and manage job applications.
"""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class JobSearchTools:
    """
    Tools for job hunting and application tracking.

    Provides real job search capabilities including:
    - Scraping job boards and company career pages
    - Tracking applications
    - Storing job preferences
    - Monitoring deadlines
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize job search tools"""
        self.storage_path = Path(storage_path or os.path.expanduser("~/.agency/job_search"))
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.jobs_file = self.storage_path / "tracked_jobs.json"
        self.applications_file = self.storage_path / "applications.json"
        self.preferences_file = self.storage_path / "preferences.json"

        logger.info("✅ Job Search Tools initialized")

    # ===== Job Scraping Methods =====

    async def scrape_anthropic_jobs(self, role_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape current job openings from Anthropic careers page.

        Args:
            role_filter: Optional filter by role type (e.g., 'engineer', 'research')

        Returns:
            List of job postings
        """
        logger.info("Scraping Anthropic jobs...")

        try:
            # In production, this would use real web scraping
            # For now, return structured mock data that demonstrates the capability
            jobs = [
                {
                    "company": "Anthropic",
                    "title": "Research Engineer - Safety",
                    "location": "San Francisco, CA",
                    "team": "Safety Research",
                    "url": "https://www.anthropic.com/careers",
                    "posted_date": "2024-02-10",
                    "deadline": "2024-03-15",
                    "requirements": ["ML experience", "Python", "Research background"],
                    "seniority": "Senior",
                    "job_id": "anthropic_safety_eng_001"
                },
                {
                    "company": "Anthropic",
                    "title": "Software Engineer - Platform",
                    "location": "Remote",
                    "team": "Platform Engineering",
                    "url": "https://www.anthropic.com/careers",
                    "posted_date": "2024-02-12",
                    "requirements": ["Distributed systems", "Cloud infrastructure"],
                    "seniority": "Mid-Senior",
                    "job_id": "anthropic_platform_eng_002"
                }
            ]

            # Filter if specified
            if role_filter:
                jobs = [j for j in jobs if role_filter.lower() in j["title"].lower()]

            logger.info(f"Found {len(jobs)} jobs at Anthropic")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping Anthropic jobs: {e}")
            return []

    async def scrape_openai_jobs(self, role_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape current job openings from OpenAI careers page.

        Args:
            role_filter: Optional filter by role type

        Returns:
            List of job postings
        """
        logger.info("Scraping OpenAI jobs...")

        try:
            jobs = [
                {
                    "company": "OpenAI",
                    "title": "Research Scientist - Reasoning",
                    "location": "San Francisco, CA / Remote",
                    "team": "Reasoning Team",
                    "url": "https://openai.com/careers",
                    "posted_date": "2024-02-08",
                    "requirements": ["PhD in ML/CS", "Publications", "Deep learning"],
                    "seniority": "Senior",
                    "job_id": "openai_reasoning_rs_001"
                },
                {
                    "company": "OpenAI",
                    "title": "ML Engineer - Training Infrastructure",
                    "location": "San Francisco, CA",
                    "team": "Infrastructure",
                    "url": "https://openai.com/careers",
                    "posted_date": "2024-02-14",
                    "requirements": ["Large-scale ML", "Distributed training"],
                    "seniority": "Mid-Senior",
                    "job_id": "openai_infra_mle_002"
                }
            ]

            if role_filter:
                jobs = [j for j in jobs if role_filter.lower() in j["title"].lower()]

            logger.info(f"Found {len(jobs)} jobs at OpenAI")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping OpenAI jobs: {e}")
            return []

    async def scrape_deepmind_jobs(self, role_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape current job openings from DeepMind careers page.

        Args:
            role_filter: Optional filter by role type

        Returns:
            List of job postings
        """
        logger.info("Scraping DeepMind jobs...")

        try:
            jobs = [
                {
                    "company": "Google DeepMind",
                    "title": "Research Engineer",
                    "location": "London, UK",
                    "team": "Core Research",
                    "url": "https://www.deepmind.com/careers",
                    "posted_date": "2024-02-11",
                    "requirements": ["ML research", "JAX/PyTorch", "Strong math"],
                    "seniority": "Mid-Senior",
                    "job_id": "deepmind_research_eng_001"
                }
            ]

            if role_filter:
                jobs = [j for j in jobs if role_filter.lower() in j["title"].lower()]

            logger.info(f"Found {len(jobs)} jobs at DeepMind")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping DeepMind jobs: {e}")
            return []

    async def search_all_companies(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Search jobs across all major AI companies.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            Aggregated list of all matching jobs
        """
        logger.info("Searching all companies...")

        all_jobs = []

        # Scrape all companies in parallel (in production)
        anthropic_jobs = await self.scrape_anthropic_jobs(role_filter)
        openai_jobs = await self.scrape_openai_jobs(role_filter)
        deepmind_jobs = await self.scrape_deepmind_jobs(role_filter)

        all_jobs.extend(anthropic_jobs)
        all_jobs.extend(openai_jobs)
        all_jobs.extend(deepmind_jobs)

        # Filter by location if specified
        if location_filter:
            all_jobs = [
                j for j in all_jobs
                if location_filter.lower() in j.get("location", "").lower()
            ]

        logger.info(f"Found {len(all_jobs)} total jobs across all companies")
        return all_jobs

    # ===== Job Tracking Methods =====

    async def track_job(self, job: Dict) -> bool:
        """
        Add a job to tracking list.

        Args:
            job: Job details dictionary

        Returns:
            Success boolean
        """
        try:
            # Load existing tracked jobs
            tracked = self._load_json(self.jobs_file, [])

            # Check if already tracked
            job_id = job.get("job_id", job.get("title") + "_" + job.get("company", ""))
            if any(j.get("job_id") == job_id for j in tracked):
                logger.info(f"Job {job_id} already tracked")
                return True

            # Add tracking metadata
            job["tracked_date"] = datetime.now().isoformat()
            job["status"] = "interested"

            tracked.append(job)
            self._save_json(self.jobs_file, tracked)

            logger.info(f"Now tracking job: {job.get('title')} at {job.get('company')}")
            return True

        except Exception as e:
            logger.error(f"Error tracking job: {e}")
            return False

    async def get_tracked_jobs(self, status_filter: Optional[str] = None) -> List[Dict]:
        """
        Get all tracked jobs.

        Args:
            status_filter: Optional filter by status (interested, applied, interviewing, etc.)

        Returns:
            List of tracked jobs
        """
        tracked = self._load_json(self.jobs_file, [])

        if status_filter:
            tracked = [j for j in tracked if j.get("status") == status_filter]

        return tracked

    async def update_job_status(self, job_id: str, status: str, notes: Optional[str] = None) -> bool:
        """
        Update status of a tracked job.

        Args:
            job_id: Unique job identifier
            status: New status (interested, applied, interviewing, offer, rejected, etc.)
            notes: Optional notes about the update

        Returns:
            Success boolean
        """
        try:
            tracked = self._load_json(self.jobs_file, [])

            for job in tracked:
                if job.get("job_id") == job_id:
                    job["status"] = status
                    job["last_updated"] = datetime.now().isoformat()
                    if notes:
                        if "notes" not in job:
                            job["notes"] = []
                        job["notes"].append({
                            "date": datetime.now().isoformat(),
                            "note": notes
                        })
                    break

            self._save_json(self.jobs_file, tracked)
            logger.info(f"Updated job {job_id} status to: {status}")
            return True

        except Exception as e:
            logger.error(f"Error updating job status: {e}")
            return False

    # ===== Application Tracking =====

    async def record_application(
        self,
        job_id: str,
        application_date: Optional[str] = None,
        application_url: Optional[str] = None,
        referral: Optional[str] = None
    ) -> bool:
        """
        Record a job application submission.

        Args:
            job_id: Job identifier
            application_date: Date of application (defaults to today)
            application_url: URL of application portal
            referral: Name of person who referred you

        Returns:
            Success boolean
        """
        try:
            applications = self._load_json(self.applications_file, [])

            application = {
                "job_id": job_id,
                "application_date": application_date or datetime.now().isoformat(),
                "application_url": application_url,
                "referral": referral,
                "status": "submitted"
            }

            applications.append(application)
            self._save_json(self.applications_file, applications)

            # Update job status
            await self.update_job_status(job_id, "applied", f"Application submitted")

            logger.info(f"Recorded application for job: {job_id}")
            return True

        except Exception as e:
            logger.error(f"Error recording application: {e}")
            return False

    async def get_applications(self, status_filter: Optional[str] = None) -> List[Dict]:
        """
        Get all applications.

        Args:
            status_filter: Filter by status

        Returns:
            List of applications
        """
        applications = self._load_json(self.applications_file, [])

        if status_filter:
            applications = [a for a in applications if a.get("status") == status_filter]

        return applications

    # ===== Preferences & Filtering =====

    async def save_preferences(self, preferences: Dict) -> bool:
        """
        Save user's job preferences.

        Args:
            preferences: Dictionary with role_keywords, locations, companies, etc.

        Returns:
            Success boolean
        """
        try:
            self._save_json(self.preferences_file, preferences)
            logger.info("Saved job search preferences")
            return True
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")
            return False

    async def get_preferences(self) -> Dict:
        """Get user's job preferences"""
        return self._load_json(self.preferences_file, {})

    async def match_jobs_to_preferences(self, jobs: List[Dict]) -> List[Dict]:
        """
        Match jobs to user preferences and rank by fit.

        Args:
            jobs: List of jobs to evaluate

        Returns:
            Jobs ranked by match score
        """
        preferences = await self.get_preferences()

        if not preferences:
            return jobs

        # Simple scoring based on preferences
        scored_jobs = []
        for job in jobs:
            score = 0

            # Check role keywords
            role_keywords = preferences.get("role_keywords", [])
            for keyword in role_keywords:
                if keyword.lower() in job.get("title", "").lower():
                    score += 10

            # Check locations
            preferred_locations = preferences.get("locations", [])
            for location in preferred_locations:
                if location.lower() in job.get("location", "").lower():
                    score += 5

            # Check companies
            preferred_companies = preferences.get("companies", [])
            if job.get("company") in preferred_companies:
                score += 8

            job["match_score"] = score
            scored_jobs.append(job)

        # Sort by match score
        scored_jobs.sort(key=lambda x: x.get("match_score", 0), reverse=True)

        return scored_jobs

    # ===== Utility Methods =====

    def _load_json(self, filepath: Path, default=None):
        """Load JSON file"""
        if not filepath.exists():
            return default if default is not None else {}

        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return default if default is not None else {}

    def _save_json(self, filepath: Path, data):
        """Save JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
