"""Configuration for Personal Research Assistant"""

from dataclasses import dataclass
from typing import List


@dataclass
class ResearchAssistantConfig:
    """Configuration for the Research Assistant"""

    # Schedule
    fetch_schedule: str = "0 2 * * *"  # 2 AM daily
    briefing_schedule: str = "0 8 * * *"  # 8 AM daily

    # Processing
    max_articles_per_day: int = 10
    summary_style: str = "bullet_points"  # concise, detailed, bullet_points

    # Reading blocks
    create_reading_blocks: bool = True
    reading_block_duration: int = 60  # minutes
    reading_block_time: str = "19:00"  # 7 PM

    # Sources
    sources: List[str] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = ["pocket", "instapaper"]

    # Notion
    notion_page_template: str = """
# {title}

**Source:** {source}
**Date:** {date}
**URL:** {url}

## Summary

{summary}

## Key Takeaways

{key_points}

## Notes

*Add your notes here*
"""

    # Briefing template
    briefing_template: str = """
Good morning! Here's your research briefing for {date}:

{articles_summary}

I've also created Notion pages for each article and blocked {reading_time} minutes on your calendar at {reading_block_time} for deep reading.

Have a productive day!
"""
