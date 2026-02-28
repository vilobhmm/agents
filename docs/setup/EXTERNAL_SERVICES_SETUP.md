# 🔌 External Services Integration Guide

**Complete setup for connecting OpenClaw to Google, Twitter/X, LinkedIn, ArXiv, and AI news sources**

*Build the ultimate AI intelligence network - Personal. Proactive. Powerful.*

---

## 📋 Overview

This guide connects your Avengers system to:

✅ **Google Services** (Gmail, Calendar, Drive) - Build context from your data
✅ **Twitter/X** - Real-time tech updates, research, posting
✅ **LinkedIn** - Professional content, authority building
✅ **ArXiv** - Latest research papers
✅ **AI News** - OpenAI, Anthropic, DeepMind blogs, trending AI news
✅ **GitHub** - Repository creation, trending projects

**Result:** Your agents have access to everything they need to be truly intelligent and proactive.

---

## 🎯 Service Overview

| Service | Used By | Purpose | Setup Time |
|---------|---------|---------|------------|
| **Google** | Captain America, Hawkeye | Context from Gmail/Calendar/Drive | 10 min |
| **Twitter/X** | Thor, Captain America | Posting, monitoring, research | 5 min |
| **LinkedIn** | Black Widow | Authority posts, networking | 15 min |
| **GitHub** | Hulk, Captain America | Repo creation, trending | 2 min |
| **ArXiv** | Captain America | Research papers | 1 min |
| **OpenAI/Anthropic** | Captain America | Official AI news | Free |
| **Hacker News** | Captain America | Tech trends | Free |

**Total Setup Time:** ~45 minutes for all services

---

# 📧 PART 1: Google Services Integration

## Why Google Integration?

**Gmail:** Understand your context, relationships, commitments
**Calendar:** Know what's coming, prepare briefings, context switching
**Drive:** Access your documents, research, notes

### Step 1: Create Google Cloud Project (10 minutes)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create New Project**
   - Click "Select a project" dropdown (top bar)
   - Click "New Project"
   - Name: `OpenClaw Avengers`
   - Click "Create"

3. **Enable APIs**

   Click "Enable APIs and Services" and enable these:

   - ✅ Gmail API
   - ✅ Google Calendar API
   - ✅ Google Drive API

   For each:
   - Search for the API name
   - Click on it
   - Click "Enable"

### Step 2: Create Service Account

1. **Navigate to Credentials**
   - Left sidebar → "APIs & Services" → "Credentials"

2. **Create Service Account**
   - Click "Create Credentials" → "Service Account"
   - Name: `openclaw-service`
   - Description: `OpenClaw Avengers system access`
   - Click "Create and Continue"

3. **Grant Roles**
   - Role: "Project" → "Editor"
   - Click "Continue"
   - Click "Done"

### Step 3: Create and Download Keys

1. **Create Key**
   - Find your service account in the list
   - Click the email address
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Click "Create"

2. **Save the Key**
   - File downloads automatically (e.g., `openclaw-avengers-abc123.json`)
   - **Move it to your OpenClaw directory:**

   ```bash
   mv ~/Downloads/openclaw-avengers-*.json ~/openclaw/google_credentials.json
   chmod 600 ~/openclaw/google_credentials.json
   ```

### Step 4: Configure OAuth for User Access

**Note:** Service accounts are for server access. For personal data (Gmail/Calendar), you need OAuth.

1. **Create OAuth Consent Screen**
   - APIs & Services → "OAuth consent screen"
   - User Type: "External"
   - Click "Create"

   Fill out:
   - App name: `OpenClaw Avengers`
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"

2. **Add Scopes**
   - Click "Add or Remove Scopes"
   - Add these scopes:
     ```
     https://www.googleapis.com/auth/gmail.readonly
     https://www.googleapis.com/auth/gmail.send
     https://www.googleapis.com/auth/calendar.readonly
     https://www.googleapis.com/auth/calendar.events
     https://www.googleapis.com/auth/drive.readonly
     ```
   - Click "Update"
   - Click "Save and Continue"

3. **Add Test Users**
   - Add your email as a test user
   - Click "Save and Continue"

4. **Create OAuth Client ID**
   - Go to "Credentials" tab
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: `OpenClaw Desktop`
   - Click "Create"

5. **Download OAuth Credentials**
   - Click the download icon (⬇️) next to your OAuth client
   - Save as `google_oauth_credentials.json` in your OpenClaw directory

   ```bash
   mv ~/Downloads/client_secret_*.json ~/openclaw/google_oauth_credentials.json
   ```

### Step 5: Add to .env

```bash
# Google Services
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/openclaw/google_credentials.json
GOOGLE_OAUTH_CREDENTIALS_FILE=/path/to/openclaw/google_oauth_credentials.json
GOOGLE_CALENDAR_ID=primary
```

### Step 6: First-Time OAuth Authorization

Run the OAuth flow once to authorize:

```bash
cd openclaw
python -m projects.11_avengers_system.google_auth_setup
```

This will:
1. Open browser for Google login
2. Ask for permissions
3. Save refresh token to `google_token.pickle`
4. Print "✅ Google authorization successful!"

**Now your agents can access Gmail, Calendar, and Drive!**

---

# 🐦 PART 2: Twitter/X API Setup

## Why Twitter Integration?

**Thor:** Posts insights, builds audience
**Captain America:** Monitors AI trends, tech news in real-time

### Step 1: Apply for Twitter Developer Account (5 minutes)

1. **Go to Twitter Developer Portal**
   - Visit: https://developer.twitter.com/
   - Click "Sign up" or "Developer Portal"
   - Log in with your Twitter account

2. **Apply for Access**
   - Choose "Hobbyist" → "Exploring the API"
   - Or "Making a bot" if that's your main use

   Fill out application:
   - Name: Your name
   - Country: Your country
   - Use case: "Personal AI assistant for content curation and posting"
   - Description: "Building an AI agent system that monitors AI/tech news and posts insights"
   - Click "Next"

3. **Agree to Terms**
   - Read and agree to terms
   - Click "Submit"

4. **Wait for Approval** (usually instant to a few hours)

### Step 2: Create Twitter App

1. **Create Project**
   - In Developer Portal, click "Projects & Apps"
   - Click "Create Project"
   - Name: `OpenClaw Avengers`
   - Click "Next"

2. **Select Use Case**
   - Choose "Making a bot"
   - Click "Next"

3. **Add App Details**
   - App name: `openclaw-bot` (must be unique)
   - Click "Complete"

### Step 3: Get API Keys

1. **API Keys Shown**
   - You'll see API Key, API Secret, Bearer Token
   - **COPY THESE NOW** (you can't see them again)

2. **Save Keys to .env**

```bash
# Twitter/X API (v2)
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

### Step 4: Generate Access Token & Secret

1. **User Authentication Settings**
   - Go to your app settings
   - Find "User authentication settings"
   - Click "Set up"

2. **Configure OAuth**
   - App permissions: "Read and write"
   - Type of App: "Web App"
   - Callback URL: `http://localhost:8080/callback`
   - Website URL: `https://github.com/yourusername` (or your site)
   - Click "Save"

3. **Generate Tokens**
   - Go to "Keys and tokens" tab
   - Under "Access Token and Secret" click "Generate"
   - **COPY THESE NOW**

4. **Add to .env**

```bash
# Add these to Twitter section
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

### Step 5: Verify Setup

```bash
python -m projects.11_avengers_system.verify_twitter
```

Should output:
```
✅ Twitter API connection successful!
✅ Authenticated as: @yourusername
✅ Can read timeline
✅ Can post tweets
```

**Twitter integration complete!**

---

# 💼 PART 3: LinkedIn API Setup

## Why LinkedIn Integration?

**Black Widow:** Posts thought leadership, builds professional authority

**⚠️ Note:** LinkedIn API access is more restricted than other platforms.

### Option A: LinkedIn API (Requires Approval)

1. **Create LinkedIn App**
   - Go to: https://www.linkedin.com/developers/apps
   - Click "Create app"
   - Fill out form:
     - App name: `OpenClaw Avengers`
     - LinkedIn Page: Your company page (required)
     - Privacy policy URL: Your URL
     - App logo: Upload an image
   - Check verification box
   - Click "Create app"

2. **Request API Access**
   - Click "Products" tab
   - Request access to:
     - "Share on LinkedIn"
     - "Sign In with LinkedIn"
   - Fill out use case form
   - Wait for approval (can take days/weeks)

3. **Get Credentials** (once approved)
   - Go to "Auth" tab
   - Copy "Client ID" and "Client Secret"

4. **Add to .env**

```bash
# LinkedIn API
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
```

### Option B: Manual Posting (Immediate)

Use LinkedIn's web interface with automation:

```bash
# No API key needed
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password
```

**Agents will use Selenium to post for you**

### Option C: Third-Party Service

Use services like:
- **Buffer** (buffer.com) - Social media scheduling
- **Hootsuite** (hootsuite.com) - Social media management

Add their API credentials instead.

**For most users:** Start with Option B (manual), upgrade to API later.

---

# 📚 PART 4: Research Sources (ArXiv, Hacker News)

## ArXiv API (Free, No Registration)

ArXiv has a free, open API. No setup needed!

```bash
# Optional: Add your email for polite usage
ARXIV_EMAIL=your@email.com  # Used in API requests user-agent
```

**That's it!** Captain America can now search ArXiv.

## Hacker News API (Free, No Registration)

Hacker News has a free, open API.

```bash
# No credentials needed!
```

**Already works!** Captain America monitors HN automatically.

---

# 📰 PART 5: AI News Sources

## Official Blogs (No API Needed)

These sources are scraped via RSS/web:

### OpenAI Blog
```bash
OPENAI_BLOG_URL=https://openai.com/blog
OPENAI_RSS_URL=https://openai.com/blog/rss.xml
```

### Anthropic Blog
```bash
ANTHROPIC_BLOG_URL=https://www.anthropic.com/news
```

### DeepMind Blog
```bash
DEEPMIND_BLOG_URL=https://deepmind.google/discover/blog/
```

### Additional AI News Sources
```bash
# AI News Aggregators
AIWEEKLY_URL=https://aiweekly.co/
IMPORTAI_URL=https://jack-clark.net/

# Tech News
TECHCRUNCH_AI_URL=https://techcrunch.com/category/artificial-intelligence/
THEVERGE_AI_URL=https://www.theverge.com/ai-artificial-intelligence

# Research
ARXIV_CS_AI_URL=https://arxiv.org/list/cs.AI/recent
ARXIV_CS_LG_URL=https://arxiv.org/list/cs.LG/recent
```

**All added to .env** → Captain America monitors automatically

---

# 🐙 PART 6: GitHub Integration

## Why GitHub?

**Hulk:** Creates demo repositories
**Captain America:** Monitors trending projects, AI repositories

### Step 1: Create Personal Access Token (2 minutes)

1. **Go to GitHub Settings**
   - Click your profile picture → Settings
   - Scroll to "Developer settings" (bottom left)
   - Click "Personal access tokens" → "Tokens (classic)"

2. **Generate New Token**
   - Click "Generate new token" → "Generate new token (classic)"
   - Note: `OpenClaw Avengers System`
   - Expiration: `No expiration` (or 90 days)

3. **Select Scopes**

   Check these boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `gist` (Create gists)
   - ✅ `read:org` (Read org data)

4. **Generate and Copy**
   - Click "Generate token"
   - **COPY THE TOKEN** (starts with `ghp_`)
   - You can't see it again!

### Step 2: Add to .env

```bash
# GitHub
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_github_username
```

### Step 3: Verify

```bash
python -m projects.11_avengers_system.verify_github
```

Should output:
```
✅ GitHub API connection successful!
✅ Authenticated as: yourusername
✅ Can create repositories
✅ Can read trending repos
```

**GitHub integration complete!**

---

# 🔧 PART 7: Complete .env Configuration

Here's your complete `.env` file with all integrations:

```bash
# ============================================
# CORE AI
# ============================================
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ============================================
# TELEGRAM INTERFACE
# ============================================
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF-your-token
TELEGRAM_CHAT_ID=your_chat_id_here

# ============================================
# GOOGLE SERVICES
# ============================================
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/openclaw/google_credentials.json
GOOGLE_OAUTH_CREDENTIALS_FILE=/path/to/openclaw/google_oauth_credentials.json
GOOGLE_TOKEN_FILE=/path/to/openclaw/google_token.pickle
GOOGLE_CALENDAR_ID=primary

# ============================================
# TWITTER / X
# ============================================
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# ============================================
# LINKEDIN
# ============================================
# Option A: LinkedIn API (if approved)
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token

# Option B: Manual posting
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password

# ============================================
# GITHUB
# ============================================
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_github_username

# ============================================
# RESEARCH SOURCES
# ============================================
# ArXiv
ARXIV_EMAIL=your@email.com

# AI News Blogs
OPENAI_BLOG_URL=https://openai.com/blog
OPENAI_RSS_URL=https://openai.com/blog/rss.xml
ANTHROPIC_BLOG_URL=https://www.anthropic.com/news
DEEPMIND_BLOG_URL=https://deepmind.google/discover/blog/

# AI News Aggregators
AIWEEKLY_URL=https://aiweekly.co/
IMPORTAI_URL=https://jack-clark.net/

# Tech News
TECHCRUNCH_AI_URL=https://techcrunch.com/category/artificial-intelligence/
THEVERGE_AI_URL=https://www.theverge.com/ai-artificial-intelligence

# Research ArXiv Categories
ARXIV_CS_AI_URL=https://arxiv.org/list/cs.AI/recent
ARXIV_CS_LG_URL=https://arxiv.org/list/cs.LG/recent
ARXIV_CS_CL_URL=https://arxiv.org/list/cs.CL/recent

# Hacker News
HN_API_URL=https://hacker-news.firebaseio.com/v0

# ============================================
# OPTIONAL: WhatsApp (Alternative to Telegram)
# ============================================
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890
```

---

# 🧪 PART 8: Verify All Integrations

Run the complete verification script:

```bash
python -m projects.11_avengers_system.verify_all_services
```

Expected output:

```
🔍 VERIFYING ALL EXTERNAL SERVICES

✅ Anthropic API: Connected
✅ Telegram Bot: Connected (@your_bot)
✅ Google Gmail: Connected (your@email.com)
✅ Google Calendar: Connected (3 upcoming events)
✅ Google Drive: Connected (125 files accessible)
✅ Twitter API: Connected (@yourusername)
✅ LinkedIn: Configured (manual mode)
✅ GitHub: Connected (yourusername, 45 repos)
✅ ArXiv API: Available
✅ Hacker News API: Available
✅ OpenAI Blog: Accessible
✅ Anthropic Blog: Accessible
✅ DeepMind Blog: Accessible

🎉 ALL SERVICES CONNECTED!

Your Avengers team has full intelligence access.
```

---

# 📊 PART 9: What Each Agent Now Has Access To

### 🧠 **Iron Man** (Chief of Staff)
- Telegram interface
- All agent coordination
- Task management
- Context from all sources

### 🛡 **Captain America** (Research & Intelligence)
**Now monitors:**
- ✅ Twitter AI hashtags (#AI, #ML, #LLM)
- ✅ ArXiv (cs.AI, cs.LG, cs.CL)
- ✅ Hacker News top stories
- ✅ OpenAI blog
- ✅ Anthropic blog
- ✅ DeepMind blog
- ✅ GitHub trending (AI repositories)
- ✅ TechCrunch AI
- ✅ The Verge AI
- ✅ Your Gmail (for context)
- ✅ Your Calendar (upcoming meetings)

**Outputs:**
- Daily intelligence briefings
- Research summaries
- Trend analysis

### ⚡ **Thor** (Twitter Operator)
**Now can:**
- ✅ Post tweets
- ✅ Post threads
- ✅ Monitor mentions
- ✅ Track hashtags
- ✅ Engage with influencers
- ✅ Real-time AI news commentary

**Outputs:**
- 3-5 tweets daily
- Thread breakdowns
- Engagement growth

### 🕷 **Black Widow** (LinkedIn Authority)
**Now can:**
- ✅ Post long-form content
- ✅ Build professional brand
- ✅ Network strategically

**Outputs:**
- 2-3 LinkedIn posts weekly
- Thought leadership
- Professional insights

### 🔨 **Hulk** (GitHub Prototypes)
**Now can:**
- ✅ Create repositories
- ✅ Push code
- ✅ Update READMEs
- ✅ Track trending repos

**Outputs:**
- Weekly demos
- Code prototypes
- GitHub presence

### 🎯 **Hawkeye** (Newsletter Curator)
**Now has access to:**
- ✅ All research sources
- ✅ Gmail for subscribers
- ✅ Drive for drafts
- ✅ Calendar for publishing schedule

**Outputs:**
- Weekly newsletters
- Curated insights
- Original analysis

---

# 🎯 PART 10: Priority Setup Order

**If you're short on time, set up in this order:**

### Tier 1: Essential (15 minutes)
1. ✅ Anthropic API (already done)
2. ✅ Telegram Bot (already done)
3. ✅ GitHub Token (2 min)

**You can use the system NOW with these three.**

### Tier 2: Intelligence (15 minutes)
4. ✅ Twitter API (5 min)
5. ✅ ArXiv (free, 1 min)
6. ✅ HN (free, already works)

**Now Captain America has real intelligence.**

### Tier 3: Context (20 minutes)
7. ✅ Google OAuth (Gmail/Calendar) (15 min)
8. ✅ Blog RSS feeds (5 min)

**Now agents understand YOUR context.**

### Tier 4: Publishing (10+ minutes)
9. ✅ Twitter posting (already done if Step 4 complete)
10. ✅ LinkedIn (manual mode: 2 min, API: 10+ days)

**Now Thor and Black Widow can build your brand.**

---

# 🚨 Troubleshooting

## Google OAuth "Access Blocked"

**Problem:** OAuth screen shows "This app isn't verified"

**Fix:**
1. Click "Advanced"
2. Click "Go to OpenClaw Avengers (unsafe)"
3. This is YOUR app, it's safe
4. Google requires verification for public apps, not needed for personal use

## Twitter API "Forbidden"

**Problem:** API returns 403 errors

**Fix:**
1. Check your app has "Read and Write" permissions
2. Regenerate access token AFTER changing permissions
3. Wait 5 minutes for changes to propagate

## LinkedIn "No API Access"

**Problem:** LinkedIn API products not approved

**Fix:**
- Use Option B (manual posting) for now
- LinkedIn API approval can take weeks
- Most users never need official API for personal use

## GitHub "Not Found"

**Problem:** Can't access repositories

**Fix:**
1. Make sure token has `repo` scope
2. Check GITHUB_USERNAME matches token owner
3. Try regenerating token

## ArXiv "Rate Limited"

**Problem:** Too many requests to ArXiv

**Fix:**
1. Add ARXIV_EMAIL to .env
2. Reduce search frequency
3. ArXiv allows 1 request per 3 seconds

---

# 📈 Next Steps

After setting up services:

1. **Test Each Integration**
   ```bash
   python -m projects.11_avengers_system.test_integrations
   ```

2. **Run First Intelligence Sweep**
   ```bash
   python -m projects.11_avengers_system.captain_america --sweep
   ```

3. **Start Telegram Interface**
   ```bash
   python -m projects.11_avengers_system.telegram_manager
   ```

4. **Ask Iron Man**
   ```
   You: /status
   Iron Man: Shows all agents and their data sources

   You: What's new in AI today?
   Iron Man: Captain America scans all sources and reports back
   ```

---

# 🎉 You Now Have

✅ **Intelligence Network:** 15+ sources feeding Captain America
✅ **Context Engine:** Gmail, Calendar, Drive understanding your life
✅ **Publishing Platform:** Twitter, LinkedIn building your brand
✅ **Build Lab:** GitHub hosting your prototypes
✅ **Research Pipeline:** ArXiv, blogs, news keeping you current

**All controlled via Telegram chat with Iron Man.**

**Multi-agent Agentic - Personal. Proactive. Powerful.**

---

## 📚 Additional Resources

- **Google API Docs:** https://developers.google.com/apis-explorer
- **Twitter API Docs:** https://developer.twitter.com/en/docs
- **LinkedIn API Docs:** https://learn.microsoft.com/en-us/linkedin/
- **GitHub API Docs:** https://docs.github.com/en/rest
- **ArXiv API Docs:** https://arxiv.org/help/api/

**Questions? Check the troubleshooting section or open an issue!**

**Now go build your intelligence empire.** 🚀
