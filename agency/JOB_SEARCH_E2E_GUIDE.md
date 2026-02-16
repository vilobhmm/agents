# 💼 Job Search Agent - Complete E2E Guide

**Automate Your Entire Job Hunt** with the Job Search Team!

Find roles, optimize applications, get referrals - all automated.

---

## 🎯 What is the Job Search Team?

A **multi-agent team** that handles your entire job search:

**👥 The Team:**
- **@job_hunter** - Finds relevant opportunities
- **@resume_optimizer** - Tailors resume & applies
- **@networker** - Gets referrals & follows up
- **@coordinator** - Manages the workflow

**🎯 What it does:**
- 🔍 Scrapes career pages (Anthropic, OpenAI, DeepMind, Google, Meta, etc.)
- 📊 Filters by role, level, location
- 📝 Tailors resume for each position
- 🤝 Reaches out for referrals
- 📧 Tracks applications & follows up
- ⏰ Monitors deadlines

---

## 🚀 Quick Start (10 Minutes)

### Step 1: Start Agency

```bash
agency start
```

### Step 2: Find Jobs

**Via Telegram:**
```
@job_hunter Find ML Engineer roles at Anthropic and OpenAI
```

**Via CLI:**
```bash
agency send "Find ML Engineer roles at Anthropic" job_hunter
```

### Step 3: Get Tailored Resume

```
@resume_optimizer Tailor my resume for this role: [job URL]
```

### Step 4: Get Referrals

```
@networker Who can refer me to Anthropic?
```

---

## 💬 Using the Job Search Team

### 1. Finding Jobs

#### **Single Company**
```
@job_hunter Find ML Engineer roles at Anthropic
```

**Response:**
```
Job Hunter: Found 5 ML Engineer positions at Anthropic:

1. 🎯 **Senior ML Engineer - Agents**
   📍 San Francisco, CA
   💼 Senior level
   🔗 https://anthropic.com/careers/123
   ⭐ 95% match to your profile
   📅 Posted 2 days ago

2. **ML Research Engineer**
   📍 Remote
   💼 Mid-Senior level
   🔗 https://anthropic.com/careers/124
   ⭐ 92% match

3. **Applied AI Engineer**
   📍 San Francisco, CA or Remote
   💼 Senior level
   🔗 https://anthropic.com/careers/125
   ⭐ 88% match

Want me to:
1. Get more details
2. Tailor resume for top match
3. Find referral contacts
```

---

#### **Multiple Companies**
```
@job_hunter Search for ML Engineer at Anthropic, OpenAI, DeepMind
```

**Response:**
```
Job Hunter: Found 15 roles across 3 companies:

**Anthropic (5 roles)**
- Senior ML Engineer - Agents (95% match)
- ML Research Engineer (92% match)
- Applied AI Engineer (88% match)
...

**OpenAI (6 roles)**
- Research Engineer - Reasoning (94% match)
- Applied ML Engineer (90% match)
...

**DeepMind (4 roles)**
- Research Scientist - RL (89% match)
- ML Engineer - Robotics (87% match)
...

Top 3 recommendations:
1. Anthropic - Senior ML Engineer (95%)
2. OpenAI - Research Engineer (94%)
3. Anthropic - ML Research Engineer (92%)
```

---

#### **Track Companies**
```
@job_hunter Monitor these companies: Anthropic, OpenAI, DeepMind, Cohere
```

**Result:**
Job Hunter will automatically check daily and notify you of new postings!

---

### 2. Optimizing Resume

#### **Tailor for Specific Job**
```
You: @resume_optimizer Tailor my resume for Anthropic Senior ML Engineer

Resume Optimizer: I'll optimize your resume for this role.

[Analyzes job description]

Key requirements identified:
- Deep learning experience (PyTorch/JAX)
- LLM training & fine-tuning
- Production ML systems
- Research background

[Reviews your resume]

Optimization plan:
✏️ Highlight your LLM work at current company
✏️ Emphasize PyTorch expertise
✏️ Add metrics for production systems
✏️ Feature research publications

Creating tailored version...
✅ Resume optimized (95% match → 98% match!)

Saved as: resume_anthropic_senior_ml.pdf

Want me to:
1. Review changes
2. Create cover letter
3. Apply now
```

---

#### **Generic Optimization**
```
@resume_optimizer Review my resume for ML Engineer roles
```

**Result:**
- ATS optimization
- Keyword analysis
- Format improvements
- Impact quantification

---

### 3. Getting Referrals

#### **Find Referral Contacts**
```
You: @networker Who can refer me to Anthropic?

Networker: Checking your network for Anthropic connections...

Found 3 potential referrals:

1. 👤 **Sarah Chen**
   💼 Senior ML Engineer at Anthropic
   🤝 Connected on LinkedIn
   📧 sarah.chen@anthropic.com
   🔗 Worked together at PreviousCo (2020)
   ⭐ Strong connection

2. **Mike Johnson**
   💼 Research Scientist at Anthropic
   🤝 Friend from Stanford
   📧 mike@anthropic.com
   ⭐ Good connection

3. **Emily Davis**
   💼 Recruiter at Anthropic
   🤝 Met at AI conference
   ⭐ Medium connection

Recommended approach: Start with Sarah (strongest connection)

Want me to draft referral request to Sarah?
```

---

#### **Draft Referral Request**
```
You: Yes, draft request to Sarah

Networker: Here's a personalized referral request:

---
Subject: Catching up + Anthropic opportunity

Hi Sarah,

Hope you're doing well! It's been great seeing your work at
Anthropic - the Claude releases have been incredible.

I'm reaching out because I noticed Anthropic is hiring for a
Senior ML Engineer role (Agents team), and I'd love to learn
more about it. Given our work together at PreviousCo on the
recommendation system, I think my background in LLM deployment
and production ML could be a good fit.

Would you be open to a quick chat about the role and team?
And if you think it's a match, I'd really appreciate a referral!

Always happy to return the favor however I can.

Best,
[Your name]
---

Want me to:
1. Send it now
2. Revise anything
3. Schedule for later
```

---

#### **Follow Up**
```
You: @networker Follow up with Sarah (sent referral request 1 week ago)

Networker: Here's a gentle follow-up:

---
Hi Sarah,

Hope you had a great week! I wanted to follow up on my email
from last week about the Anthropic ML Engineer role.

I know you're busy, so no pressure at all - just wanted to keep
it on your radar if you have a chance to chat or pass along my
resume.

Thanks again!
[Your name]
---

Send now?
```

---

### 4. Complete Team Workflow

#### **Full Job Search Automation**
```
You: @job_search Find and apply for ML Engineer roles

Coordinator: I'll run the complete job search workflow.

[Delegates to team]

Job Hunter: Searching top AI companies...
  ✅ Found 15 relevant roles
  ✅ Filtered by match score
  ✅ Top 5 selected

Resume Optimizer: Tailoring resume...
  ✅ Optimized for top 5 roles
  ✅ 5 custom resumes created
  ✅ Cover letters drafted

Networker: Finding referral contacts...
  ✅ 8 potential referrals identified
  ✅ 3 strong connections
  ✅ Referral requests drafted

Coordinator: Here's your complete package:

📊 **Jobs Found: 15**
  Top 5 recommendations (90%+ match):
  1. Anthropic - Senior ML Engineer
  2. OpenAI - Research Engineer
  3. DeepMind - ML Research Scientist
  4. Cohere - ML Engineer
  5. Anthropic - Applied AI Engineer

📝 **Resume Package: 5 tailored resumes**
  All optimized for ATS
  Custom cover letters included
  Match scores: 95-98%

🤝 **Referrals: 8 contacts identified**
  3 strong connections ready to reach out
  5 requests drafted and ready

📧 **Next Steps:**
  Option 1: Apply to all 5 (auto-submit)
  Option 2: Review before applying
  Option 3: Send referral requests first

What would you like to do?
```

---

## 📊 Tracking Applications

### View All Applications

```
@job_hunter Show my applications

Job Hunter: Here's your application status:

**Applied (5)**
✅ Anthropic - Senior ML Engineer
  📅 Applied: Jan 10
  🤝 Referred by Sarah Chen
  📊 Status: Under review

✅ OpenAI - Research Engineer
  📅 Applied: Jan 11
  🤝 Direct application
  📊 Status: Pending

...

**In Progress (3)**
🚧 DeepMind - ML Research Scientist
  📝 Resume tailored, ready to apply

...

**Watching (10)**
👀 Google - Research Scientist
  📅 Posted: Jan 12
  ⭐ 94% match
  💡 Action: Find referral
```

---

### Follow-Up Reminders

```
@networker Show follow-ups needed

Networker: You have 3 pending follow-ups:

1. ⏰ Sarah at Anthropic
   Last contact: 1 week ago
   Action: Follow up on referral

2. ⏰ Mike at OpenAI
   Last contact: 3 days ago
   Action: Thank for referral

3. ⏰ Anthropic Recruiter
   Last contact: 2 weeks ago
   Action: Check application status

Want me to draft follow-up messages?
```

---

## 🎯 Advanced Features

### Custom Job Filters

```
@job_hunter Find roles matching:
- Title: ML Engineer or Research Scientist
- Level: Senior or Staff
- Location: San Francisco or Remote
- Companies: Anthropic, OpenAI, DeepMind, Cohere
- Min salary: $200k
- Posted within: 7 days
```

---

### Automated Daily Updates

Set up daily job alerts:

```bash
# Add to crontab (9 AM every day)
0 9 * * * /home/user/agents/agency_bin send "Any new ML Engineer jobs?" job_hunter
```

**Result:**
```
Job Hunter (9 AM daily): Good morning!

New jobs found today:
1. 🆕 Anthropic - ML Engineer (Platform)
   Posted: Today
   ⭐ 96% match
   [Details...]

Want me to:
1. Tailor resume
2. Find referral
3. Apply now
```

---

### Interview Preparation

```
@resume_optimizer Prepare me for Anthropic interview

Resume Optimizer: Here's your interview prep:

**About Anthropic:**
- Mission: AI safety & research
- Focus: Claude (LLM)
- Team size: ~150 people
- Funding: $7.3B

**Role Analysis:**
Key requirements you match:
✅ Deep learning (your: 5 years)
✅ PyTorch (your: expert)
✅ Production ML (your: 3 systems)

Talking points for YOUR experience:
1. LLM fine-tuning project (quantify impact)
2. Production ML pipeline (scale/performance)
3. Research publications (cite specific papers)

**Likely Questions:**
1. "Tell me about your LLM experience"
   → Talk about [specific project]

2. "How do you handle model deployment?"
   → Discuss [your production system]

3. "Experience with safety/alignment?"
   → Mention [relevant work]

**Questions to Ask:**
1. How does the agents team approach [X]?
2. What's the deployment process like?
3. How do you measure success?

Want me to do a mock interview?
```

---

## 📝 Real-World Examples

### Example 1: Career Pivot

```
You: I want to transition from software engineering to ML engineering

Coordinator: I'll help with your career transition.

[Analyzes your background]

Your transferable skills:
✅ Python programming (5 years)
✅ System design experience
✅ Production experience
✅ Data structures & algorithms

Gaps to address:
📚 Formal ML training
📚 Deep learning projects
📚 Research background

Action plan:
1. Find ML roles that value software engineering
2. Highlight transferable skills in resume
3. Target "Applied ML Engineer" positions
4. Emphasize production/systems experience

Let me find suitable roles...

[Shows 10 "Applied ML Engineer" positions]

These roles value your software background!
Want to proceed with applications?
```

---

### Example 2: Bulk Apply

```
You: @job_search Apply to all top matches (95%+)

Coordinator: Running bulk application workflow...

Job Hunter: 8 roles with 95%+ match
Resume Optimizer: 8 custom resumes created
Networker: 5 referral contacts found

Applying...
✅ 1/8 Anthropic - Senior ML (referred by Sarah)
✅ 2/8 OpenAI - Research Eng (direct)
✅ 3/8 DeepMind - ML Scientist (referred by Mike)
...
✅ 8/8 Complete!

**Application Summary:**
- 8 applications submitted
- 3 with referrals
- 5 direct applications
- All custom-tailored
- All tracked for follow-up

I'll monitor these and notify you of updates!
```

---

### Example 3: Referral Chain

```
You: @networker Get referral for OpenAI Research Engineer role

Networker: Starting referral outreach...

Primary contact: Mike (Research Scientist at OpenAI)
  ✅ Drafted personalized request
  ✅ Sent

Backup contacts:
- Emily (knows Mike, can introduce)
- John (OpenAI alum, can advise)

Mike responded! ✅
"Happy to refer you! Send me your resume."

Next steps:
1. Send tailored resume to Mike
2. Follow up in 2 days
3. Track referral status

Want me to send the resume to Mike?
```

---

## ⚙️ Configuration

### Customize Job Preferences

Edit in `agency/templates/agents.json`:

```json
{
  "job_hunter": {
    "preferences": {
      "target_companies": [
        "Anthropic", "OpenAI", "DeepMind",
        "Cohere", "Adept", "Inflection"
      ],
      "target_roles": [
        "ML Engineer", "Research Scientist",
        "Applied ML", "Research Engineer"
      ],
      "locations": ["San Francisco", "Remote"],
      "min_match_score": 85,
      "check_frequency": "daily"
    }
  }
}
```

---

## 🎓 Tips & Best Practices

### Tip 1: Start Broad, Then Refine

```
# Day 1: Explore
@job_hunter Find ML Engineer roles at top AI labs

# Day 2: Filter
@job_hunter Show only 90%+ matches in San Francisco

# Day 3: Apply
@job_search Apply to top 5
```

---

### Tip 2: Leverage Referrals

Applications with referrals are **10x more likely** to get interviews!

Always check for referral contacts first:
```
@networker Who can refer me to [company]?
```

---

### Tip 3: Tailor Everything

Generic resumes get rejected. Always tailor:
```
@resume_optimizer Tailor for each role in my pipeline
```

---

### Tip 4: Follow Up

Don't forget to follow up!
```
# Set reminder
@networker Remind me to follow up with Sarah in 1 week
```

---

## 🐛 Troubleshooting

### Not Finding Enough Jobs?

```
# Broaden search
@job_hunter Include mid-level positions
@job_hunter Search related roles: "ML", "AI", "Research"
@job_hunter Expand to more companies
```

### Low Match Scores?

```
# Improve resume
@resume_optimizer Optimize my resume for ML roles
@resume_optimizer Add keywords for [target role]
```

### No Referral Contacts?

```
# Expand network
@networker Find indirect connections to [company]
@networker Suggest networking events
@networker Find alumni at [company]
```

---

## 📚 See Also

- [CLI Commands](CLI_COMMANDS.md) - All commands
- [CC Agent Guide](CC_AGENT_GUIDE.md) - Productivity agent
- [Agency README](../README.md) - Main guide

---

**Land your dream job with AI agents!** 🚀💼