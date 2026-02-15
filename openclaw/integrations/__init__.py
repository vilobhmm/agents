"""Integration modules for external services"""

from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.drive import DriveIntegration
from openclaw.integrations.google_services import GoogleServices
from openclaw.integrations.slack import SlackIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration
from openclaw.integrations.telegram import TelegramIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.github import GitHubIntegration
from openclaw.integrations.twitter import TwitterIntegration
from openclaw.integrations.linkedin import LinkedInIntegration

__all__ = [
    "EmailIntegration",
    "CalendarIntegration",
    "DriveIntegration",
    "GoogleServices",
    "SlackIntegration",
    "WhatsAppIntegration",
    "TelegramIntegration",
    "NotionIntegration",
    "GitHubIntegration",
    "TwitterIntegration",
    "LinkedInIntegration",
]
