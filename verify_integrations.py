#!/usr/bin/env python3
"""
Verify all external service integrations.

This script checks if all external services are properly configured and accessible.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


async def verify_google_services():
    """Verify Google Services (Gmail, Calendar, Drive)"""
    print("\n🔍 Verifying Google Services...")

    try:
        from openclaw.integrations.google_services import GoogleServices

        google = GoogleServices()

        # Test Gmail
        try:
            emails = await google.get_unread_emails(max_results=1)
            print(f"  ✅ Gmail: Connected ({len(emails)} unread emails)")
        except Exception as e:
            print(f"  ❌ Gmail: {e}")

        # Test Calendar
        try:
            events = await google.get_todays_events()
            print(f"  ✅ Calendar: Connected ({len(events)} events today)")
        except Exception as e:
            print(f"  ❌ Calendar: {e}")

        # Test Drive
        try:
            files = await google.list_recent_files(max_results=5)
            print(f"  ✅ Drive: Connected ({len(files)} recent files)")
        except Exception as e:
            print(f"  ❌ Drive: {e}")

        return True

    except Exception as e:
        print(f"  ❌ Google Services: {e}")
        return False


async def verify_twitter():
    """Verify Twitter/X integration"""
    print("\n🐦 Verifying Twitter/X...")

    try:
        from openclaw.integrations.twitter import TwitterIntegration

        twitter = TwitterIntegration()

        if not twitter.client:
            print("  ❌ Twitter: Not configured (missing API credentials)")
            return False

        try:
            # Try to search for a simple query
            tweets = await twitter.search_tweets(query="#AI", max_results=1)
            print(f"  ✅ Twitter: Connected (can search tweets)")
            return True
        except Exception as e:
            print(f"  ❌ Twitter: {e}")
            return False

    except Exception as e:
        print(f"  ❌ Twitter: {e}")
        return False


async def verify_linkedin():
    """Verify LinkedIn integration"""
    print("\n💼 Verifying LinkedIn...")

    try:
        from openclaw.integrations.linkedin import LinkedInIntegration

        linkedin = LinkedInIntegration()

        if linkedin.has_api_access:
            try:
                profile = await linkedin.get_profile()
                if profile:
                    print(f"  ✅ LinkedIn: Connected (API access)")
                    return True
                else:
                    print(f"  ⚠️  LinkedIn: API configured but couldn't get profile")
                    return False
            except Exception as e:
                print(f"  ❌ LinkedIn: {e}")
                return False
        else:
            print(f"  ⚠️  LinkedIn: No API access (manual posting mode)")
            return True

    except Exception as e:
        print(f"  ❌ LinkedIn: {e}")
        return False


async def verify_github():
    """Verify GitHub integration"""
    print("\n🐙 Verifying GitHub...")

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("  ❌ GitHub: No GITHUB_TOKEN found in environment")
        return False

    try:
        import requests

        headers = {"Authorization": f"token {github_token}"}
        response = requests.get("https://api.github.com/user", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("login", "Unknown")
            print(f"  ✅ GitHub: Connected (@{username})")
            return True
        else:
            print(f"  ❌ GitHub: Authentication failed ({response.status_code})")
            return False

    except Exception as e:
        print(f"  ❌ GitHub: {e}")
        return False


async def verify_anthropic():
    """Verify Anthropic API"""
    print("\n🤖 Verifying Anthropic API...")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ❌ Anthropic: No ANTHROPIC_API_KEY found")
        return False

    if api_key.startswith("sk-ant-"):
        print("  ✅ Anthropic: API key configured")
        return True
    else:
        print("  ⚠️  Anthropic: API key format looks incorrect")
        return False


async def verify_telegram():
    """Verify Telegram integration"""
    print("\n💬 Verifying Telegram...")

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token:
        print("  ❌ Telegram: No TELEGRAM_BOT_TOKEN found")
        return False

    if not chat_id:
        print("  ⚠️  Telegram: No TELEGRAM_CHAT_ID found")

    try:
        import requests

        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")

        if response.status_code == 200:
            bot_data = response.json()
            bot_name = bot_data.get("result", {}).get("username", "Unknown")
            print(f"  ✅ Telegram: Connected (@{bot_name})")
            return True
        else:
            print(f"  ❌ Telegram: Authentication failed")
            return False

    except Exception as e:
        print(f"  ❌ Telegram: {e}")
        return False


async def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🔍 VERIFYING ALL EXTERNAL SERVICES")
    print("=" * 60)

    results = {}

    # Core services
    results["Anthropic"] = await verify_anthropic()
    results["Telegram"] = await verify_telegram()

    # Google services
    results["Google"] = await verify_google_services()

    # Social platforms
    results["Twitter"] = await verify_twitter()
    results["LinkedIn"] = await verify_linkedin()

    # Development tools
    results["GitHub"] = await verify_github()

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {service}")

    print("-" * 60)
    print(f"Total: {total} services")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 ALL SERVICES CONNECTED!")
        print("\nYour Avengers system has full intelligence access.")
        return 0
    else:
        print(f"\n⚠️  {failed} service(s) need configuration.")
        print("\nSee EXTERNAL_SERVICES_SETUP.md for setup instructions.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
