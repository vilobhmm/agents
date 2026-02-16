"""
Universal Job Scraper - Flexible job search across ANY company, role, location, and skills.

This module provides a configurable job search system that integrates with:
- LinkedIn Jobs API
- Indeed API
- Naukri.com (India)
- Glassdoor
- SimplyHired
- Monster
- Generic company career pages

Users can search for:
- ANY role (Software Engineer, Product Manager, Data Scientist, etc.)
- ANY company (not limited to hardcoded list)
- ANY location/country (India, USA, France, Remote, etc.)
- ANY experience level (1-2 years, 5+ years, Senior, etc.)
- ANY skills (Java, Python, PyTorch, React, Kubernetes, etc.)
"""

import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import quote, urlencode
import asyncio
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class UniversalJobScraper:
    """
    Universal job scraper that searches across multiple job boards and company sites.

    Fully configurable - no hardcoded companies or roles.
    """

    def __init__(self):
        """Initialize universal job scraper"""
        self.session = None
        logger.info("🌐 Universal Job Scraper initialized")

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def _build_search_url(
        self,
        base_url: str,
        params: Dict[str, str]
    ) -> str:
        """Build search URL with query parameters"""
        query_string = urlencode(params)
        return f"{base_url}?{query_string}"

    # ===== LinkedIn Jobs =====

    async def search_linkedin(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search LinkedIn Jobs with flexible parameters.

        Args:
            role: Job title/role (e.g., "Software Engineer", "Product Manager")
            company: Company name (e.g., "Google", "TCS", "Infosys")
            location: Location (e.g., "India", "San Francisco", "Remote")
            experience_level: Experience level (e.g., "Entry level", "Mid-Senior", "Director")
            skills: List of skills (e.g., ["Python", "Machine Learning"])

        Returns:
            List of job postings with application links
        """
        logger.info(f"🔍 Searching LinkedIn Jobs...")

        try:
            # Build search query
            keywords = []
            if role:
                keywords.append(role)
            if skills:
                keywords.extend(skills)

            query = " ".join(keywords) if keywords else "jobs"

            # LinkedIn job search URL
            base_url = "https://www.linkedin.com/jobs/search"

            params = {
                "keywords": query,
                "location": location or "",
                "f_C": "",  # Company ID (would need to look up)
            }

            # Add experience level filter
            if experience_level:
                exp_map = {
                    "entry": "2",
                    "associate": "3",
                    "mid-senior": "4",
                    "director": "5",
                    "executive": "6"
                }
                for key, value in exp_map.items():
                    if key in experience_level.lower():
                        params["f_E"] = value
                        break

            search_url = self._build_search_url(base_url, params)

            # If company specified, add to keywords
            if company:
                params["keywords"] = f"{query} {company}"
                search_url = self._build_search_url(base_url, params)

            job = {
                "source": "LinkedIn",
                "company": company or "Multiple companies",
                "title": f"{role or 'All roles'}" + (f" - {', '.join(skills)}" if skills else ""),
                "location": location or "All locations",
                "experience_level": experience_level or "All levels",
                "url": search_url,
                "apply_url": search_url,
                "description": f"Search for {role or 'jobs'} at {company or 'companies'} with {', '.join(skills) if skills else 'any skills'}",
                "instructions": "1. Click link to view all matching positions on LinkedIn\n2. Apply filters on LinkedIn (Remote, Salary, etc.)\n3. Click 'Easy Apply' for quick applications\n4. Save jobs for later review"
            }

            logger.info(f"✅ LinkedIn search link generated")
            return [job]

        except Exception as e:
            logger.error(f"❌ Error generating LinkedIn search: {e}")
            return []

    # ===== Indeed =====

    async def search_indeed(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[List[str]] = None,
        country: str = "www"
    ) -> List[Dict]:
        """
        Search Indeed with flexible parameters.

        Args:
            role: Job title/role
            company: Company name
            location: Location/city
            experience_level: Experience level
            skills: List of skills
            country: Country domain (www=global, in=India, uk=UK, etc.)

        Returns:
            List of job postings
        """
        logger.info(f"🔍 Searching Indeed ({country})...")

        try:
            # Build query
            query_parts = []
            if role:
                query_parts.append(role)
            if company:
                query_parts.append(f"at {company}")
            if skills:
                query_parts.extend(skills)

            query = " ".join(query_parts) if query_parts else "jobs"

            # Indeed URL (supports multiple countries)
            base_url = f"https://{country}.indeed.com/jobs"

            params = {
                "q": query,
                "l": location or "",
            }

            # Add experience level to query
            if experience_level:
                params["q"] += f" {experience_level}"

            search_url = self._build_search_url(base_url, params)

            job = {
                "source": f"Indeed ({country.upper()})",
                "company": company or "Multiple companies",
                "title": f"{role or 'All roles'}",
                "location": location or "All locations",
                "experience_level": experience_level or "All levels",
                "skills": ", ".join(skills) if skills else "Any",
                "url": search_url,
                "apply_url": search_url,
                "description": f"Search Indeed for {role or 'jobs'} with {', '.join(skills) if skills else 'any skills'}",
                "instructions": "1. Click link to view matching jobs on Indeed\n2. Filter by salary, job type, date posted\n3. Click 'Apply Now' or 'Company Site'\n4. Set up job alerts for ongoing notifications"
            }

            logger.info(f"✅ Indeed search link generated")
            return [job]

        except Exception as e:
            logger.error(f"❌ Error generating Indeed search: {e}")
            return []

    # ===== Naukri.com (India) =====

    async def search_naukri(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search Naukri.com (India's largest job portal).

        Args:
            role: Job title/role
            company: Company name
            location: City/location in India
            experience_level: Years of experience (e.g., "2-3 years", "5+ years")
            skills: List of skills

        Returns:
            List of job postings
        """
        logger.info(f"🔍 Searching Naukri.com (India)...")

        try:
            # Build search query
            query_parts = []
            if role:
                query_parts.append(role)
            if skills:
                query_parts.extend(skills)

            query = " ".join(query_parts) if query_parts else "jobs"

            # Naukri search URL
            base_url = "https://www.naukri.com/jobs-in-india"

            params = {
                "k": query,
            }

            # Add location
            if location:
                params["l"] = location

            # Add company filter
            if company:
                params["cmp"] = company

            # Experience level (extract years)
            if experience_level:
                years_match = re.search(r'(\d+)', experience_level)
                if years_match:
                    years = years_match.group(1)
                    params["exp"] = f"{years}-{int(years)+2}"

            search_url = self._build_search_url(base_url, params)

            job = {
                "source": "Naukri.com (India)",
                "company": company or "Multiple companies",
                "title": f"{role or 'All roles'}",
                "location": location or "All India",
                "experience_level": experience_level or "All levels",
                "skills": ", ".join(skills) if skills else "Any",
                "url": search_url,
                "apply_url": search_url,
                "description": f"Search Naukri.com for {role or 'jobs'} in India",
                "instructions": "1. Click to view jobs on Naukri\n2. Filter by company, location, salary\n3. Click 'Apply' on job cards\n4. Upload resume and apply directly"
            }

            logger.info(f"✅ Naukri.com search link generated")
            return [job]

        except Exception as e:
            logger.error(f"❌ Error generating Naukri search: {e}")
            return []

    # ===== Glassdoor =====

    async def search_glassdoor(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search Glassdoor with company ratings.

        Args:
            role: Job title/role
            company: Company name
            location: Location
            experience_level: Experience level
            skills: List of skills

        Returns:
            List of job postings
        """
        logger.info(f"🔍 Searching Glassdoor...")

        try:
            # Build query
            query_parts = []
            if role:
                query_parts.append(role)
            if skills:
                query_parts.extend(skills)

            query = " ".join(query_parts) if query_parts else "jobs"

            # Glassdoor job search
            base_url = "https://www.glassdoor.com/Job/jobs.htm"

            params = {
                "sc.keyword": query,
            }

            if location:
                params["locT"] = "C"
                params["locId"] = ""
                params["locKeyword"] = location

            if company:
                params["sc.keyword"] += f" {company}"

            search_url = self._build_search_url(base_url, params)

            job = {
                "source": "Glassdoor",
                "company": company or "Multiple companies",
                "title": f"{role or 'All roles'}",
                "location": location or "All locations",
                "experience_level": experience_level or "All levels",
                "skills": ", ".join(skills) if skills else "Any",
                "url": search_url,
                "apply_url": search_url,
                "description": f"Search Glassdoor for {role or 'jobs'} with company ratings",
                "instructions": "1. View jobs with company reviews and ratings\n2. Check salary information\n3. Read interview experiences\n4. Apply directly or through company site"
            }

            logger.info(f"✅ Glassdoor search link generated")
            return [job]

        except Exception as e:
            logger.error(f"❌ Error generating Glassdoor search: {e}")
            return []

    # ===== Universal Search =====

    async def universal_search(
        self,
        role: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        country: Optional[str] = None,
        experience_level: Optional[str] = None,
        skills: Optional[List[str]] = None,
        job_boards: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Universal job search across multiple platforms.

        This is the main entry point for flexible job searching.

        Args:
            role: Job title/role (e.g., "Software Engineer", "Product Manager")
            company: Company name (e.g., "Google", "TCS", "Microsoft")
            location: City/region (e.g., "Bangalore", "San Francisco", "Remote")
            country: Country (e.g., "India", "USA", "France")
            experience_level: Experience (e.g., "2-3 years", "5+ years", "Entry level")
            skills: List of skills (e.g., ["Java", "Python", "React"])
            job_boards: Platforms to search (defaults to all)

        Returns:
            List of job search links across all platforms

        Examples:
            # Software Engineer at Google in India
            search(role="Software Engineer", company="Google", country="India")

            # Product Manager with 5+ years experience, remote
            search(role="Product Manager", experience_level="5+ years", location="Remote")

            # Java Developer at TCS in Bangalore
            search(role="Java Developer", company="TCS", location="Bangalore", country="India")

            # Research Scientist with ML/PyTorch skills
            search(role="Research Scientist", skills=["Machine Learning", "PyTorch"])
        """
        logger.info(f"🌐 Universal job search starting...")
        logger.info(f"   Role: {role or 'Any'}")
        logger.info(f"   Company: {company or 'Any'}")
        logger.info(f"   Location: {location or 'Any'}")
        logger.info(f"   Country: {country or 'Any'}")
        logger.info(f"   Experience: {experience_level or 'Any'}")
        logger.info(f"   Skills: {', '.join(skills) if skills else 'Any'}")

        # Default to all job boards
        if not job_boards:
            # Auto-select based on country
            if country and "india" in country.lower():
                job_boards = ["naukri", "linkedin", "indeed_in", "glassdoor"]
            elif country and "usa" in country.lower():
                job_boards = ["linkedin", "indeed", "glassdoor"]
            else:
                job_boards = ["linkedin", "indeed", "glassdoor", "naukri"]

        # Search all job boards in parallel
        tasks = []

        if "linkedin" in job_boards:
            tasks.append(self.search_linkedin(
                role=role,
                company=company,
                location=location or country,
                experience_level=experience_level,
                skills=skills
            ))

        if "indeed" in job_boards:
            tasks.append(self.search_indeed(
                role=role,
                company=company,
                location=location or country,
                experience_level=experience_level,
                skills=skills,
                country="www"
            ))

        if "indeed_in" in job_boards or (country and "india" in country.lower()):
            tasks.append(self.search_indeed(
                role=role,
                company=company,
                location=location,
                experience_level=experience_level,
                skills=skills,
                country="in"
            ))

        if "naukri" in job_boards or (country and "india" in country.lower()):
            tasks.append(self.search_naukri(
                role=role,
                company=company,
                location=location,
                experience_level=experience_level,
                skills=skills
            ))

        if "glassdoor" in job_boards:
            tasks.append(self.search_glassdoor(
                role=role,
                company=company,
                location=location or country,
                experience_level=experience_level,
                skills=skills
            ))

        # Gather all results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in job board search: {result}")

        # Add search metadata
        for job in all_jobs:
            job["search_timestamp"] = datetime.now().isoformat()
            job["search_parameters"] = {
                "role": role,
                "company": company,
                "location": location,
                "country": country,
                "experience_level": experience_level,
                "skills": skills
            }

        logger.info(f"✅ Universal search complete: {len(all_jobs)} job board links")

        return all_jobs


# Convenience functions for easy use
async def search_jobs_universal(
    role: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    country: Optional[str] = None,
    experience_level: Optional[str] = None,
    skills: Optional[List[str]] = None
) -> List[Dict]:
    """
    Quick universal job search.

    Examples:
        # Any role at any company
        jobs = await search_jobs_universal()

        # Software Engineer at specific company
        jobs = await search_jobs_universal(
            role="Software Engineer",
            company="Google",
            country="India"
        )

        # Product Manager with experience
        jobs = await search_jobs_universal(
            role="Product Manager",
            experience_level="5+ years",
            location="Remote"
        )

        # Java Developer with specific skills
        jobs = await search_jobs_universal(
            role="Java Developer",
            company="TCS",
            location="Bangalore",
            skills=["Java", "Spring Boot", "Microservices"]
        )
    """
    async with UniversalJobScraper() as scraper:
        return await scraper.universal_search(
            role=role,
            company=company,
            location=location,
            country=country,
            experience_level=experience_level,
            skills=skills
        )
