"""
Configuration for Avengers System
"""

import os

# Agent Schedules (cron format)
AGENT_SCHEDULES = {
    "captain_america": {
        "research_sweeps": "0 7,13,19 * * *",  # 7 AM, 1 PM, 7 PM
        "status_reports": "0 */4 * * *",  # Every 4 hours
    },
    "thor": {
        "process_updates": "*/30 * * * *",  # Every 30 minutes
        "status_reports": "0 */4 * * *",
    },
    "black_widow": {
        "weekly_posts": "0 9 * * 1,4",  # Monday & Thursday 9 AM
        "status_reports": "0 */4 * * *",
    },
    "hulk": {
        "build_requests": "0 */2 * * *",  # Every 2 hours
        "status_reports": "0 */4 * * *",
    },
    "hawkeye": {
        "newsletter": "0 8 * * 5",  # Friday 8 AM
        "status_reports": "0 */4 * * *",
    },
    "iron_man": {
        "morning_briefing": "0 6 * * *",  # 6 AM
        "evening_summary": "0 20 * * *",  # 8 PM
    },
}

# Priority response times
PRIORITY_LEVELS = {
    "urgent": {"response_time_hours": 1, "notify_immediately": True},
    "high": {"response_time_hours": 4, "notify_immediately": False},
    "medium": {"response_time_hours": 24, "notify_immediately": False},
    "low": {"response_time_hours": 168, "notify_immediately": False},  # 1 week
}

# Agent capabilities
AGENT_CAPABILITIES = {
    "captain_america": [
        "research",
        "intelligence gathering",
        "monitoring",
        "analysis",
    ],
    "thor": ["twitter", "social media", "rapid commentary", "engagement"],
    "black_widow": ["linkedin", "thought leadership", "professional content"],
    "hulk": ["prototyping", "coding", "github", "implementation"],
    "hawkeye": ["newsletter", "curation", "summarization", "distillation"],
}

# Research sources
RESEARCH_SOURCES = {
    "hacker_news": "https://hn.algolia.com/api/v1/search?tags=story&query=AI",
    "github_trending": "https://api.github.com/search/repositories?q=language:python+topic:ai&sort=stars",
    "arxiv": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate",
    "openai_blog": "https://openai.com/blog/rss",
}

# GitHub settings
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "vilobhmm")
GITHUB_REPO_PREFIX = "ai-"  # Prefix for prototype repos

# Social media settings
TWITTER_POST_FREQUENCY = 30  # minutes
LINKEDIN_POST_FREQUENCY = 3  # days

# Newsletter settings
NEWSLETTER_SEND_DAY = "friday"
NEWSLETTER_SEND_HOUR = 8

# WhatsApp settings
WHATSAPP_WEBHOOK_PORT = int(os.getenv("PORT", 5000))
