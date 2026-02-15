"""Integration modules for external services"""

from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.slack import SlackIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration
from openclaw.integrations.telegram import TelegramIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.github import GitHubIntegration

__all__ = [
    "EmailIntegration",
    "CalendarIntegration",
    "SlackIntegration",
    "WhatsAppIntegration",
    "TelegramIntegration",
    "NotionIntegration",
    "GitHubIntegration",
]
