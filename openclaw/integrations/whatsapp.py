"""WhatsApp integration using Twilio"""

import logging
import os
from typing import Optional

from twilio.rest import Client


logger = logging.getLogger(__name__)


class WhatsAppIntegration:
    """WhatsApp messaging via Twilio"""

    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        from_number: Optional[str] = None,
    ):
        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = from_number or os.getenv("TWILIO_WHATSAPP_FROM")

        if not all([self.account_sid, self.auth_token, self.from_number]):
            logger.warning("Twilio credentials not fully configured")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio WhatsApp client initialized")

    async def send_message(self, to: str, message: str) -> bool:
        """
        Send a WhatsApp message.

        Args:
            to: Recipient phone number (format: whatsapp:+1234567890)
            message: Message text

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return False

        try:
            # Ensure proper format
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"

            msg = self.client.messages.create(
                body=message, from_=self.from_number, to=to
            )

            logger.info(f"WhatsApp message sent to {to}: {msg.sid}")
            return True

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False

    async def send_media(self, to: str, message: str, media_url: str) -> bool:
        """
        Send a WhatsApp message with media.

        Args:
            to: Recipient phone number
            message: Message text
            media_url: URL of media to send

        Returns:
            True if successful
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return False

        try:
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"

            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to,
                media_url=[media_url],
            )

            logger.info(f"WhatsApp media message sent to {to}: {msg.sid}")
            return True

        except Exception as e:
            logger.error(f"Error sending WhatsApp media: {e}")
            return False

    async def send_briefing(
        self, to: str, title: str, sections: list[dict], footer: Optional[str] = None
    ) -> bool:
        """
        Send a formatted briefing message

        Args:
            to: Recipient number
            title: Briefing title
            sections: List of dicts with 'title' and 'content'
            footer: Optional footer text

        Returns:
            bool: True if successful
        """
        # Format briefing
        message = f"*{title}*\n\n"

        for section in sections:
            message += f"*{section['title']}*\n"
            message += f"{section['content']}\n\n"

        if footer:
            message += f"_{footer}_"

        return await self.send_message(to, message)

    async def send_notification(
        self, to: str, emoji: str, title: str, body: str, urgent: bool = False
    ) -> bool:
        """
        Send a formatted notification

        Args:
            to: Recipient number
            emoji: Emoji for notification type
            title: Notification title
            body: Notification body
            urgent: Mark as urgent

        Returns:
            bool: True if successful
        """
        prefix = "🚨 *URGENT*\n\n" if urgent else ""
        message = f"{prefix}{emoji} *{title}*\n\n{body}"

        return await self.send_message(to, message)

    async def send_list(self, to: str, title: str, items: list[str]) -> bool:
        """
        Send a formatted list message

        Args:
            to: Recipient number
            title: List title
            items: List items

        Returns:
            bool: True if successful
        """
        message = f"*{title}*\n\n"

        for i, item in enumerate(items, 1):
            message += f"{i}. {item}\n"

        return await self.send_message(to, message)
