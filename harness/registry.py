"""
Agent Registry — Catalog of every agent in the repository.

Holds a static manifest of all known agents with their module paths,
class names, categories, and optional deterministic methods that can
be used for smoke-testing without external service dependencies.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AgentEntry:
    """A single agent in the registry."""
    name: str                          # Human-readable name
    module_path: str                   # Dotted import path (e.g. "agents.cc.cc_skills")
    class_name: str                    # Class to instantiate
    category: str                      # Grouping: core, voice, research, productivity, base
    description: str = ""              # Short description
    deterministic_methods: List[str] = field(default_factory=list)  # Methods safe to call without external deps
    init_kwargs: Dict = field(default_factory=dict)  # Optional kwargs to pass to __init__


class AgentRegistry:
    """
    Central registry of all agents in the repository.

    Uses a hard-coded manifest rather than reflection because agents
    do not share a common base class, and this is more reliable.
    """

    @staticmethod
    def get_all_agents() -> List[AgentEntry]:
        """Return the full agent manifest."""
        return [
            # ── CC Agent ──────────────────────────────────────────
            AgentEntry(
                name="CC Skills (Chief Coordinator)",
                module_path="agents.cc.cc_skills",
                class_name="CCSkills",
                category="productivity",
                description="Morning briefings, email management, calendar coordination",
                deterministic_methods=["_get_greeting"],
            ),
            AgentEntry(
                name="CC Action Taker",
                module_path="agents.cc.cc_skills",
                class_name="ActionTakerSkills",
                category="productivity",
                description="Send emails, schedule meetings, block focus time",
            ),

            # ── Job Search Agents ─────────────────────────────────
            AgentEntry(
                name="Job Search Skills",
                module_path="agents.job_search.job_search_skills",
                class_name="JobSearchSkills",
                category="productivity",
                description="Scrape career pages, parse listings, track applications",
                deterministic_methods=["_get_sample_jobs"],
            ),
            AgentEntry(
                name="Resume Skills",
                module_path="agents.job_search.job_search_skills",
                class_name="ResumeSkills",
                category="productivity",
                description="Analyze job requirements, tailor resumes, cover letters",
            ),
            AgentEntry(
                name="Networking Skills",
                module_path="agents.job_search.job_search_skills",
                class_name="NetworkingSkills",
                category="productivity",
                description="Draft referral requests, follow-ups, thank-you notes",
            ),

            # ── Feedback Agent ────────────────────────────────────
            AgentEntry(
                name="Feedback Skills",
                module_path="agents.feedback.feedback_skills",
                class_name="FeedbackSkills",
                category="core",
                description="Cluster feedback, track bugs, generate solutions, reports",
            ),

            # ── Voice Agents ─────────────────────────────────────
            AgentEntry(
                name="Voice Coordinator",
                module_path="agents.voice.voice_coordinator",
                class_name="VoiceCoordinator",
                category="voice",
                description="Orchestrates all voice-based agents and workflows",
            ),
            AgentEntry(
                name="Dictation Agent",
                module_path="agents.voice.dictation.dictation_agent",
                class_name="DictationAgent",
                category="voice",
                description="Voice-to-text transcription",
            ),
            AgentEntry(
                name="Productivity Voice Agent",
                module_path="agents.voice.productivity.productivity_agent",
                class_name="ProductivityVoiceAgent",
                category="voice",
                description="Voice assistant for daily task management",
            ),
            AgentEntry(
                name="Ideas Capture Agent",
                module_path="agents.voice.ideas_capture.ideas_capture_agent",
                class_name="IdeasCaptureAgent",
                category="voice",
                description="Voice-to-Google Docs/Notes idea capture",
            ),
            AgentEntry(
                name="Dev Copilot Agent",
                module_path="agents.voice.dev_copilot.dev_copilot_agent",
                class_name="DeveloperCopilotAgent",
                category="voice",
                description="Voice-based pair programming assistant",
            ),

            # ── Co-Scientist Agents ──────────────────────────────
            AgentEntry(
                name="Co-Scientist Agent",
                module_path="agents.co_scientist.co_scientist_agent",
                class_name="CoScientistAgent",
                category="research",
                description="Research partner: literature reviews, experiment design",
            ),
            AgentEntry(
                name="AI Agents Co-Scientist",
                module_path="agents.co_scientist.ai_agents_co_scientist",
                class_name="AIAgentsCoScientist",
                category="research",
                description="AI-focused research and startup partner",
            ),

            # ── Time Tracker Agents ──────────────────────────────
            AgentEntry(
                name="Time Tracker Coordinator",
                module_path="agents.time_tracker.coordinator",
                class_name="TimeTrackerCoordinator",
                category="productivity",
                description="Orchestrates activity monitoring, categorization, analytics",
            ),
            AgentEntry(
                name="Activity Monitor Agent",
                module_path="agents.time_tracker.activity_monitor.activity_monitor_agent",
                class_name="ActivityMonitorAgent",
                category="productivity",
                description="Tracks and logs user activities",
            ),
            AgentEntry(
                name="Categorizer Agent",
                module_path="agents.time_tracker.categorizer.categorizer_agent",
                class_name="CategorizerAgent",
                category="productivity",
                description="Auto-categorizes tracked activities",
            ),
            AgentEntry(
                name="Analytics Agent",
                module_path="agents.time_tracker.analytics.analytics_agent",
                class_name="AnalyticsAgent",
                category="productivity",
                description="Analyzes time-tracking data for insights",
            ),
            AgentEntry(
                name="Reporter Agent",
                module_path="agents.time_tracker.reporter.reporter_agent",
                class_name="ReporterAgent",
                category="productivity",
                description="Generates daily/weekly time reports",
            ),

            # ── Base Skills ──────────────────────────────────────
            AgentEntry(
                name="Research Skills",
                module_path="agents.base.skills",
                class_name="ResearchSkills",
                category="base",
                description="Twitter/X research capabilities",
            ),
            AgentEntry(
                name="Social Skills",
                module_path="agents.base.skills",
                class_name="SocialSkills",
                category="base",
                description="Twitter and LinkedIn posting",
            ),
            AgentEntry(
                name="Context Skills",
                module_path="agents.base.skills",
                class_name="ContextSkills",
                category="base",
                description="Daily context from Google services",
            ),
            AgentEntry(
                name="GitHub Skills",
                module_path="agents.base.skills",
                class_name="GitHubSkills",
                category="base",
                description="GitHub repository operations",
            ),

            # ── Core Framework ───────────────────────────────────
            AgentEntry(
                name="Agent Invoker",
                module_path="core.agent",
                class_name="AgentInvoker",
                category="core",
                description="Invokes AI agents via Anthropic/OpenAI APIs",
            ),
        ]

    @staticmethod
    def get_by_category(category: str) -> List[AgentEntry]:
        """Return agents in a given category."""
        return [a for a in AgentRegistry.get_all_agents() if a.category == category]

    @staticmethod
    def get_categories() -> List[str]:
        """Return all unique categories."""
        return sorted(set(a.category for a in AgentRegistry.get_all_agents()))
