# 🚀 Quick Integration Guide

**Get started with Google, Twitter/X, and LinkedIn in minutes!**

---

## 🎯 Overview

This guide shows you how to quickly integrate with:

- ✅ **Google Services** (Gmail, Calendar, Drive) - 10 minutes
- ✅ **Twitter/X** - 5 minutes
- ✅ **LinkedIn** - 2 minutes (manual mode)
- ✅ **GitHub** - 2 minutes

**Total Time:** ~20 minutes for all services

---

## 📦 Prerequisites

```bash
# Install required packages
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install tweepy  # For Twitter
pip install requests  # For LinkedIn and GitHub
pip install python-dotenv  # For environment variables
```

---

## 1️⃣ Google Services (10 minutes)

### Quick Setup

1. **Go to Google Cloud Console:** https://console.cloud.google.com/
2. **Create a project** called "OpenClaw"
3. **Enable APIs:**
   - Gmail API
   - Google Calendar API
   - Google Drive API
4. **Create OAuth credentials:**
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Type: "Desktop app"
   - Download as `google_oauth_credentials.json`
5. **Save credentials:**
   ```bash
   mv ~/Downloads/client_secret_*.json ./google_oauth_credentials.json
   ```

### Test It

```python
from openclaw.integrations import GoogleServices

# First run will open browser for auth
google = GoogleServices()

# Get your daily context
context = await google.get_daily_context()
print(f"Unread emails: {context['unread_count']}")
print(f"Events today: {context['events_count']}")
```

✅ **Done!** You can now access Gmail, Calendar, and Drive.

---

## 2️⃣ Twitter/X (5 minutes)

### Quick Setup

1. **Go to:** https://developer.twitter.com/
2. **Create a project** and app
3. **Copy your keys:**
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

4. **Add to `.env`:**
   ```bash
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

### Test It

```python
from openclaw.integrations import TwitterIntegration

twitter = TwitterIntegration()

# Post a tweet
await twitter.post_tweet("Hello from OpenClaw! 🤖")

# Search AI tweets
ai_tweets = await twitter.track_hashtag("#AI", max_results=10)
```

✅ **Done!** You can now post and monitor Twitter.

---

## 3️⃣ LinkedIn (2 minutes - Manual Mode)

### Quick Setup

LinkedIn API requires approval, but you can start immediately with manual mode:

```bash
# No setup needed for manual mode!
```

### Test It

```python
from openclaw.integrations import LinkedInIntegration

linkedin = LinkedInIntegration()

# This will print instructions to post manually
await linkedin.post_update("Excited to share my AI journey! 🚀")
```

The integration will show you the content to post - just copy/paste to LinkedIn!

**Want API access?** See `EXTERNAL_SERVICES_SETUP.md` for details.

✅ **Done!** Manual posting works immediately.

---

## 4️⃣ GitHub (2 minutes)

### Quick Setup

1. **Go to:** https://github.com/settings/tokens
2. **Generate new token (classic)**
3. **Select scopes:** `repo`, `workflow`, `gist`
4. **Copy token** (starts with `ghp_`)

5. **Add to `.env`:**
   ```bash
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_USERNAME=your_username
   ```

### Test It

```python
from openclaw.integrations import GitHubIntegration

github = GitHubIntegration()

# List your repositories
repos = await github.list_repositories()
```

✅ **Done!** GitHub integration ready.

---

## 🧪 Verify All Integrations

Run the verification script:

```bash
python verify_integrations.py
```

Expected output:
```
🔍 VERIFYING ALL EXTERNAL SERVICES
===================================

✅ Anthropic: API key configured
✅ Telegram: Connected (@your_bot)
✅ Gmail: Connected (5 unread emails)
✅ Calendar: Connected (2 events today)
✅ Drive: Connected (15 recent files)
✅ Twitter: Connected (can search tweets)
⚠️  LinkedIn: No API access (manual posting mode)
✅ GitHub: Connected (@yourusername)

🎉 ALL SERVICES CONNECTED!
```

---

## 💡 Quick Examples

### Example 1: Get Daily Context

```python
from openclaw.integrations import GoogleServices

async def morning_briefing():
    google = GoogleServices()
    context = await google.get_daily_context()

    print(f"📧 {context['unread_count']} unread emails")
    print(f"📅 {context['events_count']} events today")
    print(f"📁 {context['recent_files_count']} recent files")
```

### Example 2: Post to All Platforms

```python
from openclaw.integrations import TwitterIntegration, LinkedInIntegration

async def share_insight(message: str):
    # Post to Twitter
    twitter = TwitterIntegration()
    await twitter.post_tweet(message)

    # Post to LinkedIn
    linkedin = LinkedInIntegration()
    await linkedin.post_update(message)
```

### Example 3: Prepare for Meeting

```python
from openclaw.integrations import GoogleServices

async def prep_meeting(meeting_title: str):
    google = GoogleServices()
    prep = await google.prepare_for_meeting(meeting_title)

    print(f"Found {len(prep['related_emails'])} related emails")
    print(f"Found {len(prep['related_files'])} related files")
```

---

## 🎯 Simple Interface Functions

All integrations have quick helper functions:

```python
# Google Services
from openclaw.integrations.google_services import (
    get_my_context,  # Get daily context
    whats_next,      # Next meeting
    prepare_meeting, # Meeting prep
)

# Twitter
from openclaw.integrations.twitter import (
    tweet,          # Post a tweet
    tweet_thread,   # Post a thread
    search_twitter, # Search tweets
    get_ai_news,    # Get AI news
)

# LinkedIn
from openclaw.integrations.linkedin import (
    post_to_linkedin,           # Post update
    share_article_on_linkedin,  # Share article
    post_thought_leadership,    # Thought leadership
)

# Drive
from openclaw.integrations.drive import (
    list_my_files,          # List recent files
    search_drive,           # Search Drive
    download_file_by_name,  # Download file
)
```

### Usage

```python
import asyncio
from openclaw.integrations.google_services import get_my_context
from openclaw.integrations.twitter import tweet

async def main():
    # Get context
    context = await get_my_context()

    # Post to Twitter
    await tweet("Building with AI! 🚀")

asyncio.run(main())
```

---

## 📚 Complete Documentation

For detailed setup, troubleshooting, and advanced features:

- **Full Setup Guide:** `EXTERNAL_SERVICES_SETUP.md`
- **API Documentation:** Check each integration module
- **Examples:** `examples/` directory

---

## 🆘 Troubleshooting

### Google: "Access Blocked"

Click "Advanced" → "Go to OpenClaw (unsafe)" - it's your own app!

### Twitter: "Forbidden"

Regenerate access token AFTER setting "Read and Write" permissions.

### LinkedIn: "No API Access"

Use manual mode (works immediately) or apply for API access (takes weeks).

### GitHub: "Not Found"

Make sure token has `repo` scope and GITHUB_USERNAME is correct.

---

## ✅ You're Done!

You now have:

- ✅ Access to Gmail, Calendar, Drive
- ✅ Twitter posting and monitoring
- ✅ LinkedIn posting (manual mode)
- ✅ GitHub integration
- ✅ Unified interface to all services

**Next Steps:**

1. Run `python verify_integrations.py` to confirm setup
2. Try the example code above
3. Build your AI agents with full service access!

---

## 🚀 Start Building

```python
from openclaw.integrations import GoogleServices, TwitterIntegration

async def ai_assistant():
    # Get your context
    google = GoogleServices()
    context = await google.get_daily_context()

    # Share insights
    twitter = TwitterIntegration()
    await twitter.post_tweet(
        f"Daily snapshot: {context['unread_count']} emails, "
        f"{context['events_count']} meetings today! 🚀"
    )

# Run it
import asyncio
asyncio.run(ai_assistant())
```

**Welcome to the future of personal AI!** 🎉
