"""Unified Google OAuth authentication for all services.

This module handles OAuth authentication with ALL required Google API scopes
in a single flow, so one token can be used across Gmail, Calendar, and Drive.
"""

import logging
import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)

# ALL Google API scopes needed across all integrations
ALL_SCOPES = [
    # Gmail scopes
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    # Calendar scopes
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    # Drive scopes
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


def get_unified_credentials(
    credentials_path: Optional[str] = None,
    token_path: Optional[str] = None,
    scopes: Optional[list] = None,
) -> Optional[Credentials]:
    """
    Get or create unified Google credentials with all required scopes.

    This function:
    1. Checks for existing token with all scopes
    2. If token expired but has refresh_token, refreshes it
    3. If no valid token, runs OAuth flow to get new one
    4. Saves token for future use

    Args:
        credentials_path: Path to OAuth credentials JSON (from Google Cloud Console)
        token_path: Path to save/load token pickle file
        scopes: List of OAuth scopes (defaults to ALL_SCOPES)

    Returns:
        Valid Credentials object, or None if authentication failed
    """
    # Default paths
    if not credentials_path:
        credentials_path = os.getenv(
            "GOOGLE_OAUTH_CREDENTIALS",
            "google_oauth_credentials.json"
        )

    if not token_path:
        token_path = os.getenv(
            "GOOGLE_TOKEN_PATH",
            "google_token.pickle"
        )

    if not scopes:
        scopes = ALL_SCOPES

    creds = None

    # Try to load existing token
    if os.path.exists(token_path):
        logger.info(f"Loading existing token from {token_path}")
        try:
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

            # Verify token has all required scopes
            if creds and creds.scopes:
                missing_scopes = set(scopes) - set(creds.scopes)
                if missing_scopes:
                    logger.warning(
                        f"Token is missing scopes: {missing_scopes}. "
                        "Will re-authenticate to add them."
                    )
                    creds = None  # Force re-auth
        except Exception as e:
            logger.error(f"Error loading token: {e}")
            creds = None

    # Refresh or create credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired token...")
            try:
                creds.refresh(Request())
                logger.info("✅ Token refreshed successfully")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                creds = None

        # Need to run OAuth flow
        if not creds:
            if not os.path.exists(credentials_path):
                logger.error(
                    f"❌ Credentials file not found: {credentials_path}\n"
                    f"Please download OAuth credentials from Google Cloud Console:\n"
                    f"1. Go to https://console.cloud.google.com/apis/credentials\n"
                    f"2. Create OAuth 2.0 Client ID (Desktop app)\n"
                    f"3. Download JSON and save as '{credentials_path}'"
                )
                return None

            logger.info(f"Running OAuth flow with {len(scopes)} scopes...")
            logger.info(f"Required scopes: {', '.join(scopes)}")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, scopes
                )
                creds = flow.run_local_server(port=0)
                logger.info("✅ OAuth flow completed successfully")
            except Exception as e:
                logger.error(f"❌ OAuth flow failed: {e}")
                return None

        # Save the credentials
        try:
            # Create directory if needed
            token_dir = Path(token_path).parent
            token_dir.mkdir(parents=True, exist_ok=True)

            with open(token_path, "wb") as token:
                pickle.dump(creds, token)
            logger.info(f"✅ Token saved to {token_path}")
        except Exception as e:
            logger.error(f"Failed to save token: {e}")

    if creds and creds.valid:
        logger.info("✅ Valid credentials ready")
        return creds
    else:
        logger.error("❌ Failed to obtain valid credentials")
        return None


def verify_credentials(credentials_path: Optional[str] = None) -> bool:
    """
    Verify that credentials are properly set up and all scopes are granted.

    Returns:
        True if credentials are valid and all scopes granted
    """
    creds = get_unified_credentials(credentials_path)

    if not creds:
        return False

    logger.info("Verifying all required scopes...")

    if creds.scopes:
        granted_scopes = set(creds.scopes)
        required_scopes = set(ALL_SCOPES)

        missing = required_scopes - granted_scopes
        if missing:
            logger.warning(f"Missing scopes: {missing}")
            return False

        extra = granted_scopes - required_scopes
        if extra:
            logger.info(f"Extra scopes granted: {extra}")

        logger.info(f"✅ All {len(required_scopes)} required scopes granted")
        return True
    else:
        logger.warning("Could not verify scopes")
        return True  # Assume OK if we can't check


def reset_credentials(token_path: Optional[str] = None) -> bool:
    """
    Delete existing token to force re-authentication.

    Use this if you need to re-authorize with different scopes
    or if the token is corrupted.

    Returns:
        True if token was deleted
    """
    if not token_path:
        token_path = os.getenv("GOOGLE_TOKEN_PATH", "google_token.pickle")

    if os.path.exists(token_path):
        try:
            os.remove(token_path)
            logger.info(f"✅ Deleted token: {token_path}")
            logger.info("Run your app again to re-authenticate")
            return True
        except Exception as e:
            logger.error(f"Failed to delete token: {e}")
            return False
    else:
        logger.info(f"No token file found at {token_path}")
        return False
