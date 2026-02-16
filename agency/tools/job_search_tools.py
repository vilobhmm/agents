"""
Job Search Tools - REAL job scraping and tracking capabilities.

Provides tools for job_hunter agent to find, track, and manage job applications
using real web scraping APIs.
"""

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

from agency.tools.job_scraper import JobScraper, search_jobs, get_company_jobs
from agency.tools.universal_job_scraper import UniversalJobScraper, search_jobs_universal

logger = logging.getLogger(__name__)


class JobSearchTools:
    """
    Complete job search toolkit with REAL web scraping.

    Features:
    - Real-time job scraping from Anthropic (Lever API), OpenAI (Greenhouse API)
    - Job tracking and application management
    - User preference storage
    - Application deadline monitoring
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize job search tools"""
        self.storage_path = Path(storage_path or os.path.expanduser("~/.agency/job_search"))
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.jobs_file = self.storage_path / "tracked_jobs.json"
        self.applications_file = self.storage_path / "applications.json"
        self.preferences_file = self.storage_path / "preferences.json"

        logger.info("✅ Job Search Tools initialized with REAL scraping")

    # ===== Universal Job Search (Fully Configurable) =====

    async def universal_job_search(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        country: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[str] = None  # Can be comma-separated or single skill
    ) -> List[Dict]:
        """
        Universal job search - FULLY CONFIGURABLE!

        Search for ANY role, at ANY company, in ANY country, with ANY skills.

        Args:
            role: Job title (e.g., "Software Engineer", "Product Manager", "Research Scientist")
            company: Company name (e.g., "Google", "TCS", "Wipro", "Anthropic")
            location: City/region (e.g., "Bangalore", "San Francisco", "Remote")
            country: Country (e.g., "India", "USA", "France", "UK")
            experience_level: Experience (e.g., "2-3 years", "5+ years", "Entry level")
            skills: Skills (e.g., "Java, Spring Boot" or "Python, Machine Learning, PyTorch")

        Returns:
            List of job search links across multiple job boards (LinkedIn, Indeed, Naukri, etc.)

        Examples:
            # Java Developer at TCS in India with 2-3 years experience
            search(role="Java Developer", company="TCS", country="India",
                   experience_level="2-3 years", skills="Java, Spring Boot")

            # Product Manager at Google, remote
            search(role="Product Manager", company="Google", location="Remote")

            # Research Scientist with ML skills
            search(role="Research Scientist", skills="Machine Learning, PyTorch, Python")

            # Any Software Engineer role in France
            search(role="Software Engineer", country="France")

            # Wipro jobs in India
            search(company="Wipro", country="India")
        """
        logger.info(f"🌐 Starting universal job search...")
        logger.info(f"   Parameters: role={role}, company={company}, location={location}, "
                   f"country={country}, exp={experience_level}, skills={skills}")

        try:
            # Parse skills (handle comma-separated string)
            skills_list = None
            if skills:
                if isinstance(skills, str):
                    skills_list = [s.strip() for s in skills.split(',')]
                else:
                    skills_list = skills

            # Use universal scraper
            async with UniversalJobScraper() as scraper:
                jobs = await scraper.universal_search(
                    role=role,
                    company=company,
                    location=location,
                    country=country,
                    experience_level=experience_level,
                    skills=skills_list
                )

            logger.info(f"✅ Universal search found {len(jobs)} job board links")

            # Add tracking metadata
            for job in jobs:
                job["search_date"] = datetime.now().isoformat()
                job["is_real_data"] = True
                job["search_type"] = "universal"

            return jobs

        except Exception as e:
            logger.error(f"❌ Error in universal job search: {e}")
            return []

    # ===== Real Job Scraping Methods =====

    async def scrape_anthropic_jobs(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Scrape REAL Anthropic jobs via Lever API.

        Returns actual job postings with direct application links.
        """
        logger.info("🔍 Fetching REAL Anthropic jobs...")

        try:
            async with JobScraper() as scraper:
                jobs = await scraper.scrape_anthropic(role_filter, location_filter)

            logger.info(f"✅ Found {len(jobs)} real Anthropic jobs")
            return jobs

        except Exception as e:
            logger.error(f"❌ Error scraping Anthropic: {e}")
            return []

    async def scrape_openai_jobs(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Scrape REAL OpenAI jobs via Greenhouse API.

        Returns actual job postings with direct application links.
        """
        logger.info("🔍 Fetching REAL OpenAI jobs...")

        try:
            async with JobScraper() as scraper:
                jobs = await scraper.scrape_openai(role_filter, location_filter)

            logger.info(f"✅ Found {len(jobs)} real OpenAI jobs")
            return jobs

        except Exception as e:
            logger.error(f"❌ Error scraping OpenAI: {e}")
            return []

    async def scrape_deepmind_jobs(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Access DeepMind careers page.

        Note: DeepMind uses JS-heavy site, provides direct link.
        """
        logger.info("🔍 Accessing DeepMind careers...")

        try:
            async with JobScraper() as scraper:
                jobs = await scraper.scrape_deepmind(role_filter, location_filter)

            return jobs

        except Exception as e:
            logger.error(f"❌ Error accessing DeepMind: {e}")
            return []

    async def scrape_meta_jobs(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Access Meta/Facebook AI careers.

        Note: Meta uses interactive search, provides direct link.
        """
        logger.info("🔍 Accessing Meta AI careers...")

        try:
            async with JobScraper() as scraper:
                jobs = await scraper.scrape_meta(role_filter, location_filter)

            return jobs

        except Exception as e:
            logger.error(f"❌ Error accessing Meta: {e}")
            return []

    async def search_all_companies(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None,
        companies: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search REAL jobs across all major AI companies.

        Uses actual APIs (Lever, Greenhouse) to fetch real job postings
        with specific titles, locations, and application links.

        Args:
            role_filter: Keywords for role (e.g., "ML engineer", "researcher")
            location_filter: Location filter (e.g., "San Francisco", "Remote")
            companies: Specific companies (defaults to ["anthropic", "openai", "deepmind", "meta"])

        Returns:
            List of real job postings with:
            - company: Company name
            - title: Exact job title
            - location: Specific location
            - url: Direct link to job posting
            - apply_url: Direct application link
            - posted_date: When job was posted
            - team: Team/department name
            - job_id: Unique identifier
        """
        logger.info(f"🔍 Searching REAL jobs across AI companies...")
        logger.info(f"   Filters: role='{role_filter}', location='{location_filter}'")

        try:
            async with JobScraper() as scraper:
                jobs = await scraper.search_all_companies(
                    role_filter=role_filter,
                    location_filter=location_filter,
                    companies=companies
                )

            logger.info(f"✅ Found {len(jobs)} REAL jobs with application links")

            # Add search metadata
            for job in jobs:
                job["search_date"] = datetime.now().isoformat()
                job["is_real_data"] = True

            return jobs

        except Exception as e:
            logger.error(f"❌ Error searching jobs: {e}")
            return []

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

    async def update_job_status(
        self,
        job_id: str,
        status: str,
        notes: Optional[str] = None
    ) -> bool:
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
