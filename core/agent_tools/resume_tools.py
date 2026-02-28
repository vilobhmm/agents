"""
Resume Optimizer Tools - Tailor resumes to job descriptions with Google Drive integration.

Provides tools for resume_optimizer agent to:
- Access resumes from Google Drive
- Analyze job descriptions for key requirements
- Generate tailored resume versions
- Save updated resumes back to Drive
- Track resume versions for different applications
"""

import logging
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class ResumeTools:
    """
    Resume optimization and management toolkit.

    Features:
    - Google Drive integration for resume storage
    - Job description analysis
    - ATS keyword optimization
    - Resume tailoring suggestions
    - Version tracking
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize resume tools"""
        self.storage_path = Path(storage_path or os.path.expanduser("~/.agency/resume"))
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.versions_file = self.storage_path / "resume_versions.json"
        self.templates_file = self.storage_path / "resume_templates.json"

        logger.info("✅ Resume Tools initialized")

    # ===== Google Drive Integration =====

    async def find_resume_in_drive(
        self,
        google_services,
        filename_pattern: str = "resume"
    ) -> List[Dict]:
        """
        Find resume files in Google Drive.

        Args:
            google_services: GoogleServices instance
            filename_pattern: Pattern to search for (e.g., "resume", "CV")

        Returns:
            List of matching Drive files with metadata
        """
        logger.info(f"🔍 Searching Google Drive for: {filename_pattern}")

        try:
            # Search Drive for resume files
            files = await google_services.search_files(filename_pattern)

            # Filter for document types (docs, pdf, docx)
            resume_types = [
                "application/vnd.google-apps.document",  # Google Docs
                "application/pdf",  # PDF
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # DOCX
                "application/msword",  # DOC
            ]

            resumes = [
                f for f in files
                if f.get("mimeType") in resume_types
            ]

            logger.info(f"✅ Found {len(resumes)} resume files in Drive")

            return resumes

        except Exception as e:
            logger.error(f"❌ Error searching Drive: {e}")
            return []

    async def download_resume_from_drive(
        self,
        google_services,
        file_id: str,
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Download resume from Google Drive.

        Args:
            google_services: GoogleServices instance
            file_id: Drive file ID
            output_path: Optional local path to save

        Returns:
            File bytes if no output_path, None otherwise
        """
        logger.info(f"⬇️  Downloading resume from Drive: {file_id}")

        try:
            result = await google_services.download_file(file_id, output_path)

            if output_path:
                logger.info(f"✅ Resume saved to: {output_path}")
                return None
            else:
                logger.info(f"✅ Resume downloaded ({len(result)} bytes)")
                return result

        except Exception as e:
            logger.error(f"❌ Error downloading resume: {e}")
            return None

    # ===== Job Description Analysis =====

    def analyze_job_description(self, job_description: str) -> Dict:
        """
        Analyze job description to extract key requirements.

        Args:
            job_description: Full job description text

        Returns:
            Dictionary with:
            - required_skills: List of required skills
            - preferred_skills: List of preferred skills
            - experience_years: Required years of experience
            - education: Required education
            - key_responsibilities: Main responsibilities
            - keywords: ATS keywords to include
        """
        logger.info("📊 Analyzing job description...")

        analysis = {
            "required_skills": [],
            "preferred_skills": [],
            "experience_years": None,
            "education": [],
            "key_responsibilities": [],
            "keywords": [],
            "technologies": [],
        }

        # Extract skills
        skill_patterns = [
            r"(?:required|must have|proficiency in)[\s:]+([^.\n]+)",
            r"experience with ([^,.\n]+)",
            r"knowledge of ([^,.\n]+)",
        ]

        for pattern in skill_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            analysis["required_skills"].extend(matches)

        # Extract preferred skills
        preferred_patterns = [
            r"(?:preferred|nice to have|bonus)[\s:]+([^.\n]+)",
            r"(?:a plus|advantage)[\s:]+([^.\n]+)",
        ]

        for pattern in preferred_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            analysis["preferred_skills"].extend(matches)

        # Extract years of experience
        experience_match = re.search(
            r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
            job_description,
            re.IGNORECASE
        )
        if experience_match:
            analysis["experience_years"] = int(experience_match.group(1))

        # Extract education requirements
        education_patterns = [
            r"((?:Bachelor|Master|PhD|Ph\.?D\.?)'?s?\s+(?:degree)?[\s\w]+)",
            r"(BS|MS|PhD)\s+in\s+([\w\s]+)",
        ]

        for pattern in education_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            analysis["education"].extend([m if isinstance(m, str) else " ".join(m) for m in matches])

        # Extract common tech keywords for ATS
        tech_keywords = [
            "Python", "Java", "JavaScript", "C++", "Go", "Rust",
            "Machine Learning", "ML", "AI", "Deep Learning",
            "PyTorch", "TensorFlow", "Kubernetes", "Docker",
            "AWS", "GCP", "Azure", "SQL", "NoSQL",
            "React", "Node.js", "Git", "CI/CD",
            "Distributed Systems", "Scalability", "Performance",
        ]

        for keyword in tech_keywords:
            if keyword.lower() in job_description.lower():
                analysis["technologies"].append(keyword)

        # Deduplicate and clean
        analysis["required_skills"] = list(set([s.strip() for s in analysis["required_skills"] if s]))
        analysis["preferred_skills"] = list(set([s.strip() for s in analysis["preferred_skills"] if s]))
        analysis["education"] = list(set([e.strip() for e in analysis["education"] if e]))
        analysis["keywords"] = analysis["technologies"]

        logger.info(f"✅ Extracted {len(analysis['required_skills'])} required skills, "
                   f"{len(analysis['technologies'])} tech keywords")

        return analysis

    def generate_resume_suggestions(
        self,
        current_resume: str,
        job_analysis: Dict
    ) -> Dict:
        """
        Generate suggestions for tailoring resume to job.

        Args:
            current_resume: Current resume text
            job_analysis: Result from analyze_job_description()

        Returns:
            Dictionary with:
            - skills_to_highlight: Skills to emphasize
            - keywords_to_add: ATS keywords to include
            - sections_to_expand: Resume sections to expand
            - missing_skills: Skills from JD not in resume
            - match_score: 0-100 score of how well resume matches
        """
        logger.info("💡 Generating resume suggestions...")

        suggestions = {
            "skills_to_highlight": [],
            "keywords_to_add": [],
            "sections_to_expand": [],
            "missing_skills": [],
            "match_score": 0,
        }

        resume_lower = current_resume.lower()

        # Check which required skills are in resume
        matching_skills = []
        missing_skills = []

        for skill in job_analysis["required_skills"]:
            if skill.lower() in resume_lower:
                matching_skills.append(skill)
                suggestions["skills_to_highlight"].append(skill)
            else:
                missing_skills.append(skill)

        suggestions["missing_skills"] = missing_skills

        # Check which keywords are missing (for ATS)
        missing_keywords = []
        for keyword in job_analysis["keywords"]:
            if keyword.lower() not in resume_lower:
                missing_keywords.append(keyword)

        suggestions["keywords_to_add"] = missing_keywords

        # Calculate match score
        total_requirements = len(job_analysis["required_skills"]) + len(job_analysis["keywords"])
        if total_requirements > 0:
            matched = len(matching_skills) + (len(job_analysis["keywords"]) - len(missing_keywords))
            suggestions["match_score"] = int((matched / total_requirements) * 100)
        else:
            suggestions["match_score"] = 50  # Default if can't determine

        # Suggest sections to expand
        if missing_skills:
            suggestions["sections_to_expand"].append("Skills - Add: " + ", ".join(missing_skills[:3]))

        if job_analysis["experience_years"]:
            suggestions["sections_to_expand"].append(
                f"Experience - Emphasize {job_analysis['experience_years']}+ years"
            )

        if missing_keywords:
            suggestions["sections_to_expand"].append(
                "Summary - Include keywords: " + ", ".join(missing_keywords[:5])
            )

        logger.info(f"✅ Match score: {suggestions['match_score']}% | "
                   f"Missing {len(missing_skills)} skills, {len(missing_keywords)} keywords")

        return suggestions

    async def create_tailored_resume_prompt(
        self,
        job_title: str,
        company: str,
        job_analysis: Dict,
        suggestions: Dict
    ) -> str:
        """
        Create a prompt for the resume_optimizer agent to tailor the resume.

        Args:
            job_title: Target job title
            company: Target company
            job_analysis: Job description analysis
            suggestions: Resume suggestions

        Returns:
            Formatted prompt for the agent
        """
        prompt = f"""
Tailor resume for: {job_title} at {company}

## Job Requirements Analysis

**Required Skills:**
{self._format_list(job_analysis["required_skills"])}

**Key Technologies:**
{self._format_list(job_analysis["technologies"])}

**Experience Required:** {job_analysis["experience_years"]} years

## Current Resume Match

**Match Score:** {suggestions["match_score"]}%

**Skills to Highlight:**
{self._format_list(suggestions["skills_to_highlight"])}

**Missing Skills (add if applicable):**
{self._format_list(suggestions["missing_skills"])}

**ATS Keywords to Include:**
{self._format_list(suggestions["keywords_to_add"])}

## Recommended Changes

{self._format_list(suggestions["sections_to_expand"])}

## Instructions

Please review the user's resume and suggest specific changes to:
1. Highlight relevant experience for this role
2. Include missing ATS keywords naturally
3. Emphasize accomplishments that match job requirements
4. Quantify impact where possible (metrics, percentages, scale)
5. Tailor summary/objective to this specific role

Ask user if they want to proceed with these changes.
"""
        return prompt

    # ===== Version Tracking =====

    async def save_resume_version(
        self,
        job_id: str,
        company: str,
        job_title: str,
        resume_file_id: Optional[str] = None,
        changes_made: Optional[List[str]] = None
    ) -> bool:
        """
        Track resume version for a specific application.

        Args:
            job_id: Unique job identifier
            company: Company name
            job_title: Job title
            resume_file_id: Google Drive file ID (if applicable)
            changes_made: List of changes made to tailor resume

        Returns:
            Success boolean
        """
        try:
            versions = self._load_json(self.versions_file, [])

            version = {
                "job_id": job_id,
                "company": company,
                "job_title": job_title,
                "resume_file_id": resume_file_id,
                "changes_made": changes_made or [],
                "created_date": datetime.now().isoformat(),
            }

            versions.append(version)
            self._save_json(self.versions_file, versions)

            logger.info(f"✅ Saved resume version for: {job_title} at {company}")
            return True

        except Exception as e:
            logger.error(f"❌ Error saving resume version: {e}")
            return False

    async def get_resume_versions(self, company: Optional[str] = None) -> List[Dict]:
        """
        Get tracked resume versions.

        Args:
            company: Optional filter by company

        Returns:
            List of resume versions
        """
        versions = self._load_json(self.versions_file, [])

        if company:
            versions = [v for v in versions if v.get("company") == company]

        return versions

    # ===== Utility Methods =====

    def _format_list(self, items: List[str]) -> str:
        """Format list for display"""
        if not items:
            return "- (none)"
        return "\n".join([f"- {item}" for item in items[:10]])  # Limit to 10 items

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
