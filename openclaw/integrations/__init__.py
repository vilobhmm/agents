"""Integration modules for external services

Import integrations directly from their modules to avoid loading all dependencies:
    from openclaw.integrations.google_services import GoogleServices
    from openclaw.integrations.slack import SlackIntegration
    etc.
"""

def __getattr__(name):
    """Lazy import integrations to avoid loading all dependencies at once"""
    import importlib

    # Map of integration names to their modules
    _module_map = {
        'EmailIntegration': 'email',
        'CalendarIntegration': 'calendar',
        'DriveIntegration': 'drive',
        'GoogleServices': 'google_services',
        'SlackIntegration': 'slack',
        'WhatsAppIntegration': 'whatsapp',
        'TelegramIntegration': 'telegram',
        'NotionIntegration': 'notion',
        'GitHubIntegration': 'github',
        'TwitterIntegration': 'twitter',
        'LinkedInIntegration': 'linkedin',
    }

    if name in _module_map:
        module = importlib.import_module(f'openclaw.integrations.{_module_map[name]}')
        return getattr(module, name)

    raise AttributeError(f"module 'openclaw.integrations' has no attribute '{name}'")

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
