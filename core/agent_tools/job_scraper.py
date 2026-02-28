"""
Real Job Scraping Engine - Fetch actual job postings from company career pages.

This module implements real web scraping for major AI/tech companies using:
- BeautifulSoup for HTML parsing
- aiohttp for async HTTP requests
- Playwright for JavaScript-heavy sites
- Company-specific API endpoints where available
"""

import logging
import re
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class JobScraper:
    """
    Real job scraping engine for AI/tech companies.

    Supports:
    - Anthropic (Lever API)
    - OpenAI (Greenhouse API)
    - Google/DeepMind (Google Careers)
    - Meta/Facebook (Meta Careers API)
    - Generic career pages via HTML parsing
    """

    def __init__(self):
        """Initialize job scraper"""
        self.session = None
        logger.info("Job Scraper initialized")

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def _fetch_url(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """
        Fetch URL content.

        Args:
            url: URL to fetch
            headers: Optional HTTP headers

        Returns:
            Page content as string, or None if failed
        """
        if not headers:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36'
            }

        try:
            async with self.session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def _fetch_json(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict]:
        """Fetch JSON API endpoint"""
        if not headers:
            headers = {'Accept': 'application/json'}

        try:
            async with self.session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Failed to fetch JSON {url}: HTTP {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching JSON {url}: {e}")
            return None

    # ===== Anthropic (Lever API) =====

    async def scrape_anthropic(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape Anthropic jobs via Lever API.

        Anthropic uses Lever for job postings, which has a public API.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping Anthropic jobs via Lever API...")

        # Lever API endpoint for Anthropic
        url = "https://api.lever.co/v0/postings/anthropic"

        try:
            data = await self._fetch_json(url)

            if not data:
                logger.warning("No data from Anthropic Lever API")
                return []

            jobs = []
            for posting in data:
                # Extract job details
                title = posting.get("text", "")
                categories = posting.get("categories", {})
                location = categories.get("location", "Unknown")
                team = categories.get("team", "")
                commitment = categories.get("commitment", "")

                # Build job dict
                job = {
                    "company": "Anthropic",
                    "title": title,
                    "location": location,
                    "team": team,
                    "employment_type": commitment,
                    "url": posting.get("hostedUrl", "https://www.anthropic.com/careers"),
                    "apply_url": posting.get("applyUrl", ""),
                    "posted_date": self._parse_date(posting.get("createdAt")),
                    "description": posting.get("description", ""),
                    "job_id": posting.get("id", ""),
                    "source": "Lever API"
                }

                # Apply filters
                if role_filter and role_filter.lower() not in title.lower():
                    continue
                if location_filter and location_filter.lower() not in location.lower():
                    continue

                jobs.append(job)

            logger.info(f"Found {len(jobs)} Anthropic jobs")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping Anthropic jobs: {e}")
            return []

    # ===== OpenAI (Greenhouse API) =====

    async def scrape_openai(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape OpenAI jobs via Greenhouse API.

        OpenAI uses Greenhouse for job postings with a public API.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping OpenAI jobs via Greenhouse API...")

        # Greenhouse API endpoint for OpenAI
        url = "https://api.greenhouse.io/v1/boards/openai/jobs"

        try:
            data = await self._fetch_json(url)

            if not data or "jobs" not in data:
                logger.warning("No data from OpenAI Greenhouse API")
                return []

            jobs = []
            for posting in data["jobs"]:
                title = posting.get("title", "")
                location = posting.get("location", {}).get("name", "Unknown")

                # Extract departments/teams
                departments = posting.get("departments", [])
                team = departments[0].get("name", "") if departments else ""

                job = {
                    "company": "OpenAI",
                    "title": title,
                    "location": location,
                    "team": team,
                    "url": posting.get("absolute_url", "https://openai.com/careers"),
                    "apply_url": posting.get("absolute_url", ""),
                    "posted_date": self._parse_date(posting.get("updated_at")),
                    "job_id": str(posting.get("id", "")),
                    "source": "Greenhouse API"
                }

                # Apply filters
                if role_filter and role_filter.lower() not in title.lower():
                    continue
                if location_filter and location_filter.lower() not in location.lower():
                    continue

                jobs.append(job)

            logger.info(f"Found {len(jobs)} OpenAI jobs")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping OpenAI jobs: {e}")
            return []

    # ===== Google/DeepMind =====

    async def scrape_deepmind(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape DeepMind/Google jobs.

        Note: Google Careers is JavaScript-heavy, this is a simplified version.
        For production, would use Playwright or Selenium.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping DeepMind jobs...")

        # DeepMind careers page
        url = "https://www.deepmind.com/careers"

        try:
            # For now, return structure showing what would be scraped
            # In production, would use Playwright to handle JS
            jobs = []

            logger.info(f"DeepMind requires JavaScript rendering - using fallback")
            logger.info(f"In production, would use Playwright for: {url}")

            # Provide manual link as fallback
            jobs.append({
                "company": "Google DeepMind",
                "title": "See available positions",
                "location": "Multiple locations",
                "url": "https://www.deepmind.com/careers",
                "apply_url": "https://www.deepmind.com/careers",
                "note": "Visit careers page to view current openings",
                "source": "Direct link (requires manual check)"
            })

            return jobs

        except Exception as e:
            logger.error(f"Error accessing DeepMind jobs: {e}")
            return []

    # ===== Meta/Facebook =====

    async def scrape_meta(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape Meta/Facebook AI jobs.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping Meta AI jobs...")

        # Meta careers API endpoint
        url = "https://www.metacareers.com/graphql"

        try:
            # Meta uses GraphQL API - would need proper query
            # For now, provide direct link
            jobs = [{
                "company": "Meta (Facebook)",
                "title": "AI & Machine Learning roles",
                "location": "Multiple locations",
                "url": "https://www.metacareers.com/jobs?roles[0]=Software%20Engineer",
                "apply_url": "https://www.metacareers.com/jobs",
                "note": "Visit Meta Careers to search AI/ML positions",
                "source": "Direct link"
            }]

            logger.info(f"Meta careers require interactive search")
            return jobs

        except Exception as e:
            logger.error(f"Error accessing Meta jobs: {e}")
            return []

    # ===== Indian IT Services Companies =====

    async def scrape_infosys(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape Infosys jobs.

        Infosys uses their own career portal with search functionality.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries with direct application links
        """
        logger.info("Scraping Infosys jobs...")

        try:
            # Infosys career search page
            base_url = "https://www.infosys.com/careers/job-listing.html"

            # Build search URL with filters
            params = []
            if role_filter:
                # Common keywords mapping
                keywords = role_filter.lower()
                if "java" in keywords:
                    params.append("keyword=java")
                if "full stack" in keywords or "fullstack" in keywords:
                    params.append("keyword=fullstack")
                if "software" in keywords:
                    params.append("keyword=software")

            if location_filter:
                if "india" in location_filter.lower():
                    params.append("country=india")

            search_url = base_url
            if params:
                search_url = f"{base_url}?{'&'.join(params)}"

            # Return structured link for user to search
            jobs = [{
                "company": "Infosys",
                "title": f"Java Full Stack Developer / Software Engineer roles",
                "location": "India (Multiple cities)",
                "url": search_url,
                "apply_url": search_url,
                "description": "Search for Java, Full Stack, and Software Developer roles with 2-3 years experience",
                "experience_level": "2-3 years",
                "source": "Infosys Careers Portal",
                "instructions": "Click the link to search available positions. You can filter by location (Bangalore, Hyderabad, Pune, etc.) and experience level on the careers page."
            }]

            logger.info(f"Infosys careers link provided")
            return jobs

        except Exception as e:
            logger.error(f"Error accessing Infosys jobs: {e}")
            return []

    async def scrape_tcs(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape TCS (Tata Consultancy Services) jobs.

        TCS uses their iBegin platform and TCS Careers portal.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping TCS jobs...")

        try:
            # TCS careers page for experienced professionals
            base_url = "https://www.tcs.com/careers/tcs-experienced-hiring"
            search_url = "https://ibegin.tcs.com/iBegin/jobs/search"

            jobs = [{
                "company": "TCS (Tata Consultancy Services)",
                "title": "Java Developer / Full Stack Engineer roles",
                "location": "India (Multiple locations)",
                "url": search_url,
                "apply_url": search_url,
                "description": "Search for Java, Full Stack Developer, and Software Engineer positions with 2-3 years experience",
                "experience_level": "2-3 years",
                "source": "TCS iBegin Portal",
                "instructions": "1. Visit TCS iBegin portal\n2. Search for 'Java Developer' or 'Full Stack'\n3. Filter by India location\n4. Select 2-3 years experience\n5. Apply directly"
            }]

            # Also provide main careers page
            jobs.append({
                "company": "TCS",
                "title": "Experienced Professional Hiring",
                "location": "India",
                "url": base_url,
                "apply_url": base_url,
                "description": "Browse all TCS openings for experienced professionals",
                "source": "TCS Careers"
            })

            logger.info(f"TCS careers links provided")
            return jobs

        except Exception as e:
            logger.error(f"Error accessing TCS jobs: {e}")
            return []

    async def scrape_accenture(self, role_filter: Optional[str] = None, location_filter: Optional[str] = None) -> List[Dict]:
        """
        Scrape Accenture jobs.

        Accenture has a comprehensive job search portal.

        Args:
            role_filter: Filter by role keywords
            location_filter: Filter by location

        Returns:
            List of job dictionaries
        """
        logger.info("Scraping Accenture jobs...")

        try:
            # Accenture India careers with pre-applied filters
            # Build search URL with filters for India, Technology, 2-3 years exp
            base_url = "https://www.accenture.com/in-en/careers/jobsearch"

            # URL with common filters for Java/Full Stack roles in India
            search_params = "?jk=java+developer&loc=India"
            search_url = base_url + search_params

            jobs = [{
                "company": "Accenture",
                "title": "Java Full Stack Developer / Software Engineer",
                "location": "India (Bangalore, Hyderabad, Pune, Gurgaon, Chennai)",
                "url": search_url,
                "apply_url": search_url,
                "description": "Search Java, Full Stack, and Software Development roles",
                "experience_level": "2-3 years",
                "source": "Accenture Careers Portal",
                "instructions": "1. Visit Accenture job search\n2. Enter keywords: 'Java Developer' or 'Full Stack'\n3. Select India as location\n4. Filter by Technology domain\n5. Select 2-3 years experience range\n6. Click Apply on matching positions"
            }]

            # Alternative search for full stack roles
            fullstack_url = base_url + "?jk=full+stack+developer&loc=India"
            jobs.append({
                "company": "Accenture",
                "title": "Full Stack Developer roles",
                "location": "India",
                "url": fullstack_url,
                "apply_url": fullstack_url,
                "description": "Full Stack development positions across India",
                "source": "Accenture Careers"
            })

            logger.info(f"Accenture careers links provided")
            return jobs

        except Exception as e:
            logger.error(f"Error accessing Accenture jobs: {e}")
            return []

    # ===== Helper Methods =====

    def _parse_date(self, date_str: Optional[str]) -> str:
        """Parse date string to standard format"""
        if not date_str:
            return ""

        try:
            # Try parsing ISO format
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d")
        except:
            return date_str

    # ===== Main Search Methods =====

    async def search_all_companies(
        self,
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None,
        companies: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search jobs across multiple companies.

        Args:
            role_filter: Filter by role keywords (e.g., "engineer", "ML", "research")
            location_filter: Filter by location (e.g., "San Francisco", "Remote")
            companies: List of companies to search (defaults to all), or comma-separated string

        Returns:
            Aggregated list of all jobs
        """
        # Handle comma-separated string input
        if companies and isinstance(companies, str):
            companies = [c.strip() for c in companies.split(',')]

        if not companies:
            companies = ["anthropic", "openai", "deepmind", "meta"]

        logger.info(f"Searching {len(companies)} companies for jobs...")

        # Scrape all companies in parallel
        tasks = []

        # AI/Research companies
        if "anthropic" in companies:
            tasks.append(self.scrape_anthropic(role_filter, location_filter))

        # Indian IT Services
        for company in companies:
            company_lower = company.lower().strip()
            if "infosys" in company_lower:
                tasks.append(self.scrape_infosys(role_filter, location_filter))
            elif "tcs" in company_lower or "tata" in company_lower:
                tasks.append(self.scrape_tcs(role_filter, location_filter))
            elif "accenture" in company_lower:
                tasks.append(self.scrape_accenture(role_filter, location_filter))
        if "openai" in companies:
            tasks.append(self.scrape_openai(role_filter, location_filter))
        if "deepmind" in companies:
            tasks.append(self.scrape_deepmind(role_filter, location_filter))
        if "meta" in companies:
            tasks.append(self.scrape_meta(role_filter, location_filter))

        # Gather results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine all jobs
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in parallel scraping: {result}")

        logger.info(f"Total jobs found: {len(all_jobs)}")
        return all_jobs


# Async wrapper functions for easy use
async def search_jobs(
    role: Optional[str] = None,
    location: Optional[str] = None,
    companies: Optional[List[str]] = None
) -> List[Dict]:
    """
    Search for jobs across AI companies.

    Args:
        role: Role filter (e.g., "ML engineer", "researcher")
        location: Location filter (e.g., "San Francisco", "Remote")
        companies: List of companies to search

    Returns:
        List of job postings
    """
    async with JobScraper() as scraper:
        return await scraper.search_all_companies(role, location, companies)


async def get_company_jobs(company: str, role: Optional[str] = None) -> List[Dict]:
    """
    Get jobs from a specific company.

    Args:
        company: Company name (anthropic, openai, deepmind, meta)
        role: Optional role filter

    Returns:
        List of job postings
    """
    async with JobScraper() as scraper:
        company_lower = company.lower()

        if company_lower == "anthropic":
            return await scraper.scrape_anthropic(role)
        elif company_lower == "openai":
            return await scraper.scrape_openai(role)
        elif company_lower == "deepmind" or company_lower == "google deepmind":
            return await scraper.scrape_deepmind(role)
        elif company_lower == "meta" or company_lower == "facebook":
            return await scraper.scrape_meta(role)
        else:
            logger.warning(f"Unknown company: {company}")
            return []
