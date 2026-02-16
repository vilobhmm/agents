"""
Tool management for agents.

Converts Python functions/methods into Anthropic tool schemas
and handles tool execution.
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registry for agent tools.

    Manages tool definitions and execution for Anthropic agents.
    """

    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict] = []

    def register_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameter_descriptions: Optional[Dict[str, str]] = None
    ):
        """
        Register a tool function.

        Args:
            func: The function to register
            name: Tool name (defaults to function name)
            description: Tool description
            parameter_descriptions: Descriptions for each parameter
        """
        tool_name = name or func.__name__
        self.tools[tool_name] = func

        # Generate schema
        schema = self._generate_schema(func, tool_name, description, parameter_descriptions)
        self.tool_schemas.append(schema)

        logger.info(f"Registered tool: {tool_name}")

    def _generate_schema(
        self,
        func: Callable,
        name: str,
        description: Optional[str],
        param_descriptions: Optional[Dict[str, str]]
    ) -> Dict:
        """Generate Anthropic tool schema from function"""

        # Get function signature
        sig = inspect.signature(func)

        # Build input schema
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Skip 'self' parameter
            if param_name == 'self':
                continue

            # Determine type
            param_type = self._get_param_type(param)

            # Get description
            param_desc = param_descriptions.get(param_name, "") if param_descriptions else ""

            properties[param_name] = {
                "type": param_type,
                "description": param_desc
            }

            # Check if required (no default value)
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            "name": name,
            "description": description or func.__doc__ or f"Execute {name}",
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }

        return schema

    def _get_param_type(self, param: inspect.Parameter) -> str:
        """Determine JSON schema type from parameter annotation"""
        annotation = param.annotation

        if annotation == inspect.Parameter.empty:
            return "string"  # Default to string

        # Handle type annotations
        if annotation == str:
            return "string"
        elif annotation == int:
            return "integer"
        elif annotation == float:
            return "number"
        elif annotation == bool:
            return "boolean"
        elif hasattr(annotation, '__origin__'):
            # Handle typing annotations (List, Dict, etc.)
            origin = annotation.__origin__
            if origin == list:
                return "array"
            elif origin == dict:
                return "object"

        return "string"  # Default

    async def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a registered tool.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool

        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        func = self.tools[tool_name]

        try:
            # Execute the tool
            if inspect.iscoroutinefunction(func):
                result = await func(**tool_input)
            else:
                result = func(**tool_input)

            logger.info(f"Tool '{tool_name}' executed successfully")
            return result

        except Exception as e:
            logger.error(f"Tool '{tool_name}' execution failed: {e}")
            raise

    def get_tool_schemas(self) -> List[Dict]:
        """Get all tool schemas for Anthropic API"""
        return self.tool_schemas

    def clear(self):
        """Clear all registered tools"""
        self.tools.clear()
        self.tool_schemas.clear()


def create_google_tools_registry() -> ToolRegistry:
    """
    Create tool registry with Google services tools for CC agent.

    Returns:
        ToolRegistry with Google tools
    """
    from agency.tools.google_tools import GoogleTools

    registry = ToolRegistry()
    google_tools = GoogleTools()

    # Wrapper to handle datetime conversion for create_calendar_event
    async def create_event_wrapper(title: str, start: str, end: str, description: str = None):
        """Create calendar event with datetime conversion"""
        from datetime import datetime
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
        return await google_tools.create_calendar_event(title, start_dt, end_dt, description)

    # Register email tools
    registry.register_tool(
        google_tools.get_unread_emails,
        name="get_unread_emails",
        description="Get unread emails from Gmail. Returns a list of emails with subject, sender, and preview.",
        parameter_descriptions={
            "max_results": "Maximum number of emails to return (default 10)"
        }
    )

    registry.register_tool(
        google_tools.search_emails,
        name="search_emails",
        description="Search emails by query or sender. Use this to find specific emails.",
        parameter_descriptions={
            "query": "Search query (e.g., 'meeting agenda', 'budget report')",
            "sender": "Optional: Filter by sender email address"
        }
    )

    registry.register_tool(
        google_tools.send_email,
        name="send_email",
        description="Send an email via Gmail. Use this to send messages to people.",
        parameter_descriptions={
            "to": "Recipient email address",
            "subject": "Email subject line",
            "body": "Email body content"
        }
    )

    # Register calendar tools
    registry.register_tool(
        google_tools.get_todays_events,
        name="get_todays_events",
        description="Get all calendar events scheduled for today. Returns event titles, times, and details.",
        parameter_descriptions={}
    )

    registry.register_tool(
        google_tools.get_upcoming_events,
        name="get_upcoming_events",
        description="Get upcoming calendar events in the next N hours.",
        parameter_descriptions={
            "hours": "Number of hours to look ahead (default 24)"
        }
    )

    registry.register_tool(
        create_event_wrapper,
        name="create_calendar_event",
        description="Create a new calendar event. Use this to schedule meetings or block time. Dates should be in ISO 8601 format.",
        parameter_descriptions={
            "title": "Event title",
            "start": "Start datetime in ISO 8601 format (e.g., '2024-02-16T14:00:00')",
            "end": "End datetime in ISO 8601 format (e.g., '2024-02-16T15:00:00')",
            "description": "Optional event description"
        }
    )

    registry.register_tool(
        google_tools.block_time,
        name="block_time",
        description="Block time on calendar starting now. Use for focus time or lunch breaks.",
        parameter_descriptions={
            "title": "Block title (e.g., 'Focus Time', 'Lunch')",
            "duration_minutes": "Duration in minutes"
        }
    )

    registry.register_tool(
        google_tools.get_next_meeting,
        name="get_next_meeting",
        description="Get information about the next upcoming meeting including attendees and agenda.",
        parameter_descriptions={}
    )

    # Register Drive tools
    registry.register_tool(
        google_tools.search_drive_files,
        name="search_drive_files",
        description="Search for files in Google Drive by name or content.",
        parameter_descriptions={
            "query": "Search query"
        }
    )

    registry.register_tool(
        google_tools.get_recent_files,
        name="get_recent_files",
        description="Get recently modified files from Google Drive.",
        parameter_descriptions={
            "max_results": "Maximum number of files to return (default 20)"
        }
    )

    # Register daily briefing (composite tool)
    registry.register_tool(
        google_tools.get_daily_briefing,
        name="get_daily_briefing",
        description="Get comprehensive daily briefing including unread emails, today's calendar, and recent files. Use this for morning briefings.",
        parameter_descriptions={}
    )

    logger.info(f"Created Google Tools registry with {len(registry.tool_schemas)} tools")

    return registry


def create_job_search_tools_registry() -> ToolRegistry:
    """
    Create tool registry with job search tools for job_hunter agent.

    Returns:
        ToolRegistry with job search tools
    """
    from agency.tools.job_search_tools import JobSearchTools

    registry = ToolRegistry()
    job_tools = JobSearchTools()

    # ===== UNIVERSAL JOB SEARCH (Fully Configurable) =====
    registry.register_tool(
        job_tools.universal_job_search,
        name="universal_job_search",
        description="""
        🌐 UNIVERSAL JOB SEARCH - Search for ANY job, at ANY company, in ANY country!

        This is your PRIMARY job search tool. Use this for ALL job searches unless specifically asked for AI companies only.

        Features:
        - Search ANY role (Software Engineer, Product Manager, Data Scientist, etc.)
        - Search ANY company (TCS, Wipro, Infosys, Google, Microsoft, startups, etc.)
        - Search ANY country (India, USA, France, UK, etc.)
        - Search ANY location (Bangalore, Mumbai, San Francisco, Remote, etc.)
        - Filter by experience level (0-1 years, 2-3 years, 5+ years, etc.)
        - Filter by skills (Java, Python, Machine Learning, PyTorch, React, etc.)

        Returns:
        - LinkedIn Jobs search links (pre-filtered)
        - Indeed search links (global + country-specific)
        - Naukri.com links (for India)
        - Glassdoor links (with company ratings)

        ALL with one-click apply access!

        Examples:
        - Find Java Developer at TCS in India with 2-3 years:
          universal_job_search(role="Java Developer", company="TCS", country="India", experience_level="2-3 years")

        - Find Software Engineer at Wipro:
          universal_job_search(role="Software Engineer", company="Wipro")

        - Find ML Engineer with Python skills:
          universal_job_search(role="ML Engineer", skills="Python, Machine Learning, PyTorch")

        - Find remote Product Manager:
          universal_job_search(role="Product Manager", location="Remote")

        USE THIS TOOL FOR ALL JOB SEARCHES!
        """,
        parameter_descriptions={
            "role": "Job title/role (e.g., 'Software Engineer', 'Product Manager', 'Data Scientist')",
            "company": "Company name (e.g., 'Google', 'TCS', 'Wipro', 'Microsoft') - ANY company!",
            "location": "City/region (e.g., 'Bangalore', 'San Francisco', 'Remote')",
            "country": "Country (e.g., 'India', 'USA', 'France', 'UK')",
            "experience_level": "Experience level (e.g., '2-3 years', '5+ years', 'Entry level')",
            "skills": "Skills comma-separated (e.g., 'Java, Spring Boot' or 'Python, Machine Learning')"
        }
    )

    # ===== LEGACY AI COMPANY SCRAPERS (For AI companies only) =====
    registry.register_tool(
        job_tools.scrape_anthropic_jobs,
        name="scrape_anthropic_jobs",
        description="Scrape current job openings from Anthropic careers page. Returns real-time job listings.",
        parameter_descriptions={
            "role_filter": "Optional: Filter by role keywords (e.g., 'engineer', 'research', 'safety')"
        }
    )

    registry.register_tool(
        job_tools.scrape_openai_jobs,
        name="scrape_openai_jobs",
        description="Scrape current job openings from OpenAI careers page. Returns real-time job listings.",
        parameter_descriptions={
            "role_filter": "Optional: Filter by role keywords"
        }
    )

    registry.register_tool(
        job_tools.scrape_deepmind_jobs,
        name="scrape_deepmind_jobs",
        description="Scrape current job openings from DeepMind careers page. Returns real-time job listings.",
        parameter_descriptions={
            "role_filter": "Optional: Filter by role keywords"
        }
    )

    registry.register_tool(
        job_tools.search_all_companies,
        name="search_all_companies",
        description="Search jobs across all major AI companies (Anthropic, OpenAI, DeepMind, etc.). Returns aggregated results.",
        parameter_descriptions={
            "role_filter": "Optional: Filter by role keywords",
            "location_filter": "Optional: Filter by location (e.g., 'San Francisco', 'Remote')"
        }
    )

    # Register job tracking tools
    registry.register_tool(
        job_tools.track_job,
        name="track_job",
        description="Add a job to your tracking list. Use this to save jobs you're interested in.",
        parameter_descriptions={
            "job": "Job details dictionary (must include at minimum: title, company, job_id)"
        }
    )

    registry.register_tool(
        job_tools.get_tracked_jobs,
        name="get_tracked_jobs",
        description="Get all jobs you're currently tracking. View your saved opportunities.",
        parameter_descriptions={
            "status_filter": "Optional: Filter by status (interested, applied, interviewing, offer, rejected)"
        }
    )

    registry.register_tool(
        job_tools.update_job_status,
        name="update_job_status",
        description="Update the status of a tracked job. Use when you apply, get an interview, receive an offer, etc.",
        parameter_descriptions={
            "job_id": "Unique job identifier",
            "status": "New status (interested, applied, interviewing, offer, rejected)",
            "notes": "Optional notes about the update"
        }
    )

    # Register application tracking tools
    registry.register_tool(
        job_tools.record_application,
        name="record_application",
        description="Record that you submitted an application for a job. Automatically updates job status to 'applied'.",
        parameter_descriptions={
            "job_id": "Job identifier",
            "application_date": "Optional: Date of application (defaults to today)",
            "application_url": "Optional: URL of application portal",
            "referral": "Optional: Name of person who referred you"
        }
    )

    registry.register_tool(
        job_tools.get_applications,
        name="get_applications",
        description="Get all your job applications and their current status.",
        parameter_descriptions={
            "status_filter": "Optional: Filter by status"
        }
    )

    # Register preference tools
    registry.register_tool(
        job_tools.save_preferences,
        name="save_preferences",
        description="Save your job search preferences (roles, locations, companies, etc.). Used to personalize recommendations.",
        parameter_descriptions={
            "preferences": "Dictionary with role_keywords, locations, companies, seniority_level, etc."
        }
    )

    registry.register_tool(
        job_tools.get_preferences,
        name="get_preferences",
        description="Get your saved job search preferences.",
        parameter_descriptions={}
    )

    registry.register_tool(
        job_tools.match_jobs_to_preferences,
        name="match_jobs_to_preferences",
        description="Match a list of jobs to your preferences and rank by fit. Returns jobs sorted by match score.",
        parameter_descriptions={
            "jobs": "List of job dictionaries to evaluate"
        }
    )

    logger.info(f"Created Job Search Tools registry with {len(registry.tool_schemas)} tools")

    return registry
