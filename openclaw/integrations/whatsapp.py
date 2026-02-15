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
