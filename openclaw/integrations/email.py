"""Email integration using Gmail API"""

import base64
import logging
import os
import pickle
from datetime import datetime
from email.mime.text import MIMEText
from typing import Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class EmailIntegration:
    """Gmail integration for reading and sending emails"""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        credentials: Optional[Credentials] = None,
    ):
        """
        Initialize Gmail integration.

        Args:
            credentials_path: Path to OAuth credentials JSON (for standalone use)
            token_path: Path to token file (for standalone use)
            credentials: Pre-authenticated Credentials object (for unified auth)
        """
        self.credentials_path = credentials_path or os.getenv(
            "GMAIL_CREDENTIALS_PATH", "credentials.json"
        )
        self.token_path = token_path or os.getenv("GMAIL_TOKEN_PATH", "token.json")
        self.service = None

        # Use pre-authenticated credentials if provided, otherwise authenticate
        if credentials:
            self.service = build("gmail", "v1", credentials=credentials)
            logger.info("Gmail API authenticated successfully (unified auth)")
        else:
            self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)

        # If no valid credentials, login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    logger.warning(
                        f"Credentials file not found: {self.credentials_path}"
                    )
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("gmail", "v1", credentials=creds)
        logger.info("Gmail API authenticated successfully")

    async def get_messages(
        self,
        query: str = "",
        max_results: int = 10,
        unread_only: bool = False,
    ) -> List[Dict]:
        """
        Get messages from Gmail.

        Args:
            query: Gmail search query
            max_results: Maximum number of messages to return
            unread_only: Only return unread messages

        Returns:
            List of message dictionaries
        """
        if not self.service:
            logger.error("Gmail service not initialized")
            return []

        try:
            if unread_only:
                query = f"{query} is:unread" if query else "is:unread"

            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])
            detailed_messages = []

            for msg in messages:
                msg_detail = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="full")
                    .execute()
                )

                headers = msg_detail["payload"]["headers"]
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
                )
                sender = next(
                    (h["value"] for h in headers if h["name"] == "From"), "Unknown"
                )
                date = next((h["value"] for h in headers if h["name"] == "Date"), "")

                # Get message body
                body = ""
                if "parts" in msg_detail["payload"]:
                    for part in msg_detail["payload"]["parts"]:
                        if part["mimeType"] == "text/plain":
                            if "data" in part["body"]:
                                body = base64.urlsafe_b64decode(
                                    part["body"]["data"]
                                ).decode("utf-8")
                                break
                elif "body" in msg_detail["payload"] and "data" in msg_detail["payload"]["body"]:
                    body = base64.urlsafe_b64decode(
                        msg_detail["payload"]["body"]["data"]
                    ).decode("utf-8")

                detailed_messages.append(
                    {
                        "id": msg["id"],
                        "subject": subject,
                        "from": sender,
                        "date": date,
                        "body": body,
                        "snippet": msg_detail.get("snippet", ""),
                    }
                )

            return detailed_messages

        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            return []

    async def send_message(
        self, to: str, subject: str, body: str, html: bool = False
    ) -> bool:
        """
        Send an email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: Whether body is HTML

        Returns:
            True if successful
        """
        if not self.service:
            logger.error("Gmail service not initialized")
            return False

        try:
            if html:
                message = MIMEText(body, "html")
            else:
                message = MIMEText(body)

            message["to"] = to
            message["subject"] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {"raw": raw}

            self.service.users().messages().send(
                userId="me", body=send_message
            ).execute()

            logger.info(f"Email sent to {to}: {subject}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    async def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read"""
        if not self.service:
            return False

        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False

    async def search_emails(
        self, sender: Optional[str] = None, subject: Optional[str] = None, **kwargs
    ) -> List[Dict]:
        """Search emails with filters"""
        query_parts = []

        if sender:
            query_parts.append(f"from:{sender}")
        if subject:
            query_parts.append(f"subject:{subject}")

        query = " ".join(query_parts)
        return await self.get_messages(query=query, **kwargs)
