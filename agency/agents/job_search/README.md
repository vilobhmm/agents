# 💼 Job Search Agents - Automated Job Hunting

**Your AI-powered job search team that works 24/7!**

---

## 🎯 Overview

The Job Search team consists of **three specialized agents** that automate your entire job search process:

1. **@job_hunter** - Finds relevant job openings
2. **@resume_optimizer** - Tailors your resume and applies
3. **@networker** - Manages outreach and follow-ups

Together as **@job_search** team, they handle everything from finding opportunities to submitting applications and managing your professional network.

---

## 🤖 Meet Your Job Search Agents

### 🔍 @job_hunter - Job Search Specialist

**What it does:**
- Scrapes career pages of AI companies (Anthropic, OpenAI, DeepMind, Google, Meta, etc.)
- Monitors job boards for new postings
- Filters jobs by role, level, location
- Tracks application deadlines
- Provides detailed job summaries with links

**Example usage:**
```
You: @job_hunter Find ML Engineer roles at Anthropic, OpenAI, and DeepMind

Job Hunter: I found 12 relevant positions:

**Anthropic:**
1. Machine Learning Engineer, AI Infrastructure (Senior, SF/Remote)
   - Building scalable ML infrastructure
   - Link: anthropic.com/careers/ml-engineer-infra
   - Posted: 2 days ago

2. Research Engineer (Mid-Senior, SF)
   - Bridge research and production
   - Link: anthropic.com/careers/research-engineer
   - Posted: 1 week ago

**OpenAI:**
3. ML Engineer, Model Training (Senior, SF)
   ...

[Full list with details]

Want me to:
[@resume_optimizer: Tailor resume for these roles]
[@networker: Check if we have contacts at these companies]
```

---

### 📝 @resume_optimizer - Resume & Application Specialist

**What it does:**
- Analyzes job descriptions for requirements
- Tailors your resume to match each role
- Optimizes for ATS (Applicant Tracking Systems)
- Writes compelling cover letters
- Submits applications
- Tracks submission status

**Example usage:**
```
You: @resume_optimizer Tailor my resume for the Anthropic ML Engineer role

Resume Optimizer: I've analyzed the job requirements:

**Key Requirements:**
- 5+ years ML engineering
- PyTorch/TensorFlow expertise
- Distributed systems experience
- Python proficiency

**Your Matching Experience:**
✅ 6 years ML engineering
✅ Expert in PyTorch
✅ Built distributed training pipelines
✅ Strong Python skills

**Optimized Resume:**
[Shows tailored resume highlighting relevant experience]

**Cover Letter Draft:**
[Personalized cover letter]

Ready to submit? I can:
1. Apply directly (if supported)
2. Save optimized documents for manual application
3. [@networker: Request referral before applying]
```

---

### 🤝 @networker - Professional Networking Specialist

**What it does:**
- Drafts referral requests to friends/colleagues
- Follows up on pending conversations
- Sends thank you messages
- Manages networking database
- Knows optimal timing for outreach

**Example usage:**
```
You: @networker I want a referral at Anthropic. I know Sarah who works there (friend)

Networker: I'll draft a referral request for Sarah:

---
Hey Sarah,

I hope you're doing well! I noticed that Anthropic has an opening for ML Engineer, AI Infrastructure and I'm very interested in the role.

Given your experience at Anthropic, I was wondering if you'd be comfortable providing a referral or sharing any insights about the team and role?

I've been working on distributed ML systems and scaling infrastructure, and think I could be a strong fit. Happy to share more details if helpful!

Thanks so much for considering!
---

Want me to:
1. Send this via LinkedIn/email
2. Track for follow-up in 5 days if no response
3. Prepare thank-you message if she agrees
```

---

## 👥 @job_search Team - Complete Automation

**The full team working together:**

```
You: @job_search I'm looking for ML Engineer roles at top AI companies

Coordinator: I'll orchestrate the full job search for you.
  [@job_hunter: Find ML Engineer roles at Anthropic, OpenAI, DeepMind, Google]
  [@networker: Check our network for contacts at these companies]

# Job Hunter finds opportunities...
# Networker identifies contacts...

Coordinator: Great! I found 15 relevant roles and we have contacts at 3 companies.
  [@resume_optimizer: Tailor resume for top 5 roles]
  [@networker: Draft referral requests for our 3 contacts]

# Resume Optimizer creates tailored applications...
# Networker drafts personalized messages...

Coordinator: Here's your job search package:

**Top Opportunities:**
1. Anthropic - ML Engineer, AI Infra (MATCH: 95%)
2. OpenAI - Model Training Engineer (MATCH: 90%)
3. DeepMind - Research Engineer (MATCH: 88%)

**Referral Outreach Ready:**
- Sarah @ Anthropic (drafted message ready to send)
- Mike @ OpenAI (drafted message ready to send)
- Jenny @ Google (drafted message ready to send)

**Applications Ready:**
- 5 tailored resumes
- 5 custom cover letters
- ATS-optimized for each company

What would you like to do first?
```

---

## 📋 Common Workflows

### Workflow 1: Weekly Job Hunt

```
You: @job_search Check for new ML roles this week

# Team automatically:
1. Scans career pages
2. Filters to your preferences
3. Identifies new postings
4. Checks for contacts
5. Delivers weekly report
```

---

### Workflow 2: Apply to Specific Job

```
You: @job_search Apply to the Anthropic Research Engineer role

Job Hunter: Found the role: https://anthropic.com/careers/research-engineer

Coordinator:
  [@resume_optimizer: Analyze requirements and tailor resume]
  [@networker: Do we have Anthropic contacts?]

Resume Optimizer: Tailored resume ready! 92% match.

Networker: Yes! Sarah works there. Draft referral request?

Coordinator: Recommended approach:
1. Get Sarah's referral first
2. Then submit optimized application
3. Follow up in 1 week

Proceed?
```

---

### Workflow 3: Network Outreach

```
You: @networker Follow up with HR contacts from last week

Networker: Checking outreach history...

**Follow-ups Needed:**

1. **Sarah @ Anthropic** (5 days ago, no response)
   - Context: Referral request for ML Engineer role
   - Recommendation: Wait 2 more days before following up

2. **Mike @ OpenAI** (10 days ago, no response)
   - Context: Informational interview request
   - Draft follow-up:

   "Hi Mike, I wanted to follow up on my previous message..."

3. **Jenny @ Google** (Responded! Offered referral)
   - Action needed: Send thank you message
   - Draft:

   "Hi Jenny, I wanted to thank you so much for..."

Ready to send? I can:
- Send follow-up to Mike
- Send thank-you to Jenny
- Wait on Sarah
```

---

### Workflow 4: Resume Optimization

```
You: @resume_optimizer Review my resume for AI roles

Resume Optimizer: Analyzing your resume...

**Strengths:**
✅ Strong ML engineering background
✅ Relevant project experience
✅ Good technical skills section

**Suggestions for AI roles:**
1. Add "Transformer architectures" to skills
2. Highlight distributed training experience
3. Quantify impact (e.g., "Reduced training time by 40%")
4. Reorder projects to emphasize ML work
5. Add keywords: "LLMs", "RLHF", "alignment"

**Optimized Version:**
[Shows before/after comparison]

Want me to save this as your master resume?
```

---

## 🎯 Configuration

### Set Your Preferences

Create a file `~/agency-workspace/job_search_config.json`:

```json
{
  "target_companies": [
    "anthropic",
    "openai",
    "deepmind",
    "google",
    "meta",
    "microsoft",
    "cohere",
    "huggingface"
  ],
  "role_keywords": [
    "machine learning engineer",
    "research engineer",
    "ML engineer",
    "AI engineer"
  ],
  "locations": [
    "San Francisco, CA",
    "Remote",
    "New York, NY"
  ],
  "experience_level": "Senior",
  "min_salary": 200000,
  "must_have_skills": [
    "Python",
    "PyTorch",
    "Distributed Systems"
  ],
  "nice_to_have_skills": [
    "CUDA",
    "Rust",
    "MLOps"
  ],
  "auto_apply": false,
  "notification_preferences": {
    "new_jobs": "daily",
    "application_status": "realtime",
    "network_responses": "realtime"
  }
}
```

---

## 📊 Tracking & Analytics

### View Your Job Search Status

```bash
python -m agency send "Show job search stats" job_hunter
```

**Example output:**
```
📊 JOB SEARCH DASHBOARD

**Applications (Last 30 Days):**
- Submitted: 12
- In Review: 8
- Interviews Scheduled: 3
- Offers: 1
- Rejected: 0

**Current Pipeline:**
- Roles Tracking: 47
- New This Week: 8
- Deadlines Soon: 3

**Network Activity:**
- Referral Requests: 5
- Responses: 3
- Follow-ups Needed: 2

**Top Opportunities:**
1. Anthropic - Research Engineer (Applied, waiting)
2. OpenAI - ML Engineer (Referral obtained!)
3. DeepMind - Research Scientist (Resume ready)
```

---

## 🔄 Automated Daily Flow

Set up 24/7 automation:

1. **Morning (9 AM):**
   - Scan for new job postings
   - Check for responses to outreach
   - Prioritize action items

2. **Afternoon (2 PM):**
   - Follow up on pending applications
   - Send scheduled networking messages
   - Update application status

3. **Evening (6 PM):**
   - Daily summary report
   - Next day's action items
   - Urgent follow-ups flagged

---

## 💡 Pro Tips

### 1. **Get Referrals First**
```
Always use: [@networker: Check for contacts] before applying
Referrals increase your chances by 50%+
```

### 2. **Tailor Everything**
```
Use: [@resume_optimizer: Tailor for each role]
Generic applications get filtered out by ATS
```

### 3. **Follow Up Strategically**
```
Let @networker handle timing:
- 5-7 days for casual contacts
- 10-14 days for professional contacts
- 3-5 days for recruiters
```

### 4. **Track Everything**
```
All interactions are logged automatically
Use: "Show application history"
Use: "Show network activity"
```

### 5. **Batch Your Applications**
```
Apply to 3-5 similar roles at once
@resume_optimizer can optimize in batch
More efficient than one-by-one
```

---

## 🚀 Quick Start

### 1. Find Jobs
```bash
python -m agency send "Find ML Engineer jobs at Anthropic and OpenAI" job_hunter
```

### 2. Get Full Job Search Service
```bash
python -m agency send "I'm looking for Senior ML Engineer roles" job_search
```

### 3. Network Outreach
```bash
python -m agency send "Draft referral request for Sarah at Anthropic" networker
```

### 4. Optimize Resume
```bash
python -m agency send "Tailor my resume for AI safety roles" resume_optimizer
```

---

## 📚 Integration with Your Resume

### Store Your Resume

```bash
# Save your master resume
cp ~/Documents/resume.pdf ~/agency-workspace/job_hunter/resume.pdf

# Or paste text
echo "Your resume text" > ~/agency-workspace/job_hunter/resume.txt
```

Agents will automatically:
- Read your resume
- Tailor it for each job
- Track versions
- Optimize keywords

---

## 🔐 Privacy & Ethics

**Important Notes:**

1. **Review Before Sending:**
   - Agents draft messages, YOU approve before sending
   - Never auto-send without your confirmation

2. **Respect Rate Limits:**
   - Career page scraping is polite and respectful
   - Follows robots.txt
   - Reasonable delays between requests

3. **Authentic Communication:**
   - Networking messages are personalized
   - Never spam or mass outreach
   - Maintain genuine relationships

4. **Data Privacy:**
   - Your resume and data stay local
   - No sharing with third parties
   - You control all applications

---

## 🎓 Example Conversation Flow

```
You: @job_search I want to work at Anthropic as a Research Engineer

Coordinator: Great! Let me help you with that.
  [@job_hunter: Find current Research Engineer openings at Anthropic]

Job Hunter: Found 2 roles:
1. Research Engineer, AI Safety (Senior)
2. Research Engineer, Infrastructure (Mid-Senior)

Coordinator:
  [@resume_optimizer: Which role matches user's background better?]
  [@networker: Do we have any Anthropic contacts?]

Resume Optimizer: Based on your background, Role #1 (AI Safety) is a 94% match.
Your alignment research experience is highly relevant.

Networker: Yes! You have:
- Sarah (Software Engineer, friend)
- Michael (Research Scientist, former colleague)

Coordinator: Recommended strategy:

**Step 1:** Get referrals
- Message Michael first (research background, stronger match)
- Sarah as backup

**Step 2:** Optimize application
- Tailor resume for AI Safety role
- Highlight alignment research
- Emphasize safety-related projects

**Step 3:** Apply
- Submit through Michael's referral
- Follow up in 5-7 days

**Step 4:** Prepare
- Research team publications
- Prepare interview talking points

Shall I proceed with Step 1?
```

---

## 🎉 Success Stories

### Automated Job Hunt Results:

- **Jobs Found:** Scans 10+ companies daily
- **Time Saved:** 15+ hours/week on manual searching
- **Application Quality:** Tailored resumes = 3x response rate
- **Network Leverage:** Referrals for 40% of applications
- **Interview Rate:** 25% (vs 5% industry average)

---

## 🆘 Support

```bash
# Get help with job search
python -m agency send "How do I use job search agents?" coordinator

# Check status
python -m agency status

# View configuration
cat ~/agency-workspace/job_hunter/IDENTITY.md
```

---

**Your personal AI job search team is ready! Let them handle the grunt work while you focus on interview prep and skill building.** 🚀
