#!/usr/bin/env python3
"""
Re-authenticate Google Services Script

This script helps you re-authenticate with Google services when you get
"insufficientPermissions" errors. It will:

1. Delete old token with insufficient scopes
2. Run OAuth flow with ALL required scopes
3. Save new token that works with Gmail, Calendar, and Drive

Usage:
    python reauth_google.py
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from openclaw.integrations.unified_auth import (
    get_unified_credentials,
    verify_credentials,
    reset_credentials,
    ALL_SCOPES,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main re-authentication flow"""

    print("=" * 70)
    print("  Google Services Re-Authentication")
    print("=" * 70)
    print()

    print("This script will re-authenticate your Google services with all")
    print("required scopes (Gmail, Calendar, Drive).")
    print()

    print(f"Required OAuth Scopes ({len(ALL_SCOPES)}):")
    for scope in ALL_SCOPES:
        scope_name = scope.split('/')[-1]
        print(f"  • {scope_name}")
    print()

    # Ask user to confirm
    response = input("Delete old token and re-authenticate? (yes/no): ").lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        return

    print()
    print("-" * 70)
    print("Step 1: Deleting old token...")
    print("-" * 70)

    # Delete old token
    if reset_credentials():
        print("✅ Old token deleted")
    else:
        print("⚠️  No old token found (this is OK)")

    print()
    print("-" * 70)
    print("Step 2: Running OAuth flow...")
    print("-" * 70)
    print()
    print("Your browser will open for authentication.")
    print("Please:")
    print("  1. Sign in to your Google account")
    print("  2. Grant ALL permissions requested")
    print("  3. You may see warnings - click 'Advanced' then 'Go to app'")
    print()

    # Run OAuth flow
    creds = get_unified_credentials()

    if not creds:
        print()
        print("❌ Authentication failed!")
        print()
        print("Troubleshooting:")
        print("  1. Ensure 'google_oauth_credentials.json' exists in this directory")
        print("  2. Download it from: https://console.cloud.google.com/apis/credentials")
        print("  3. Enable Gmail, Calendar, and Drive APIs in Google Cloud Console")
        print()
        sys.exit(1)

    print()
    print("-" * 70)
    print("Step 3: Verifying credentials...")
    print("-" * 70)

    # Verify all scopes
    if verify_credentials():
        print("✅ All required scopes granted!")
    else:
        print("⚠️  Some scopes may be missing")
        print("Try running the script again")

    print()
    print("=" * 70)
    print("  ✅ Re-authentication Complete!")
    print("=" * 70)
    print()
    print("You can now use:")
    print("  • python -m agency debug test cc --message 'Give me my morning briefing'")
    print("  • python -m agency debug test job_hunter --message 'Find ML jobs'")
    print()
    print("The new token is saved in: google_token.pickle")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during re-authentication: {e}", exc_info=True)
        print()
        print("❌ Re-authentication failed with error:")
        print(f"   {e}")
        print()
        sys.exit(1)
