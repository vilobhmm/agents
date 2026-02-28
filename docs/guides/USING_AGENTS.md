# 🤖 Using Agents - Complete Guide

Learn how to interact with your AI agents effectively.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Messaging Agents](#-messaging-agents)
- [Working with Teams](#-working-with-teams)
- [Agent Personalities](#-agent-personalities)
- [Best Practices](#-best-practices)
- [Advanced Usage](#-advanced-usage)

---

## 🚀 Quick Start

### 1. Start Agency

```bash
agency start
```

### 2. Talk to Agents

**Via Telegram:**
```
@cc Good morning briefing
```

**Via CLI:**
```bash
agency send "Good morning briefing" cc
```

---

## 💬 Messaging Agents

### Direct Messaging

**Format:** `@<agent_id> <message>`

```
@cc Good morning briefing
@researcher What's new in AI today?
@job_hunter Find ML Engineer roles
@writer Create blog post about AI agents
```

### Examples by Agent

#### **@cc - Chief Coordinator**
```
@cc Good morning briefing
@cc Schedule meeting with Sarah tomorrow at 2pm
@cc Draft email to John about project update
@cc What's on my calendar today?
@cc Block focus time for 2 hours
```

#### **@job_hunter - Job Search**
```
@job_hunter Find ML Engineer roles at Anthropic
@job_hunter Any new postings at OpenAI?
@job_hunter Show me AI research positions
@job_hunter Track these companies: Anthropic, DeepMind, OpenAI
```

#### **@resume_optimizer - Resume & Applications**
```
@resume_optimizer Tailor my resume for this role: [URL]
@resume_optimizer Write cover letter for Anthropic ML Engineer
@resume_optimizer Review my resume
@resume_optimizer Apply for job [job_id]
```

#### **@networker - Networking**
```
@networker Draft referral request to Sarah at Anthropic
@networker Follow up with John about last week
@networker Thank Mike for the referral
@networker Who can help me at OpenAI?
```

#### **@researcher - Research**
```
@researcher Latest AI research papers
@researcher What's trending on Twitter AI?
@researcher Summarize Anthropic's latest blog post
@researcher Track OpenAI announcements
```

#### **@writer - Content Creation**
```
@writer Create newsletter about AI trends
@writer Write blog post about agents
@writer Draft LinkedIn post about my project
@writer Summarize this article: [URL]
```

#### **@social - Social Media**
```
@social Create Twitter thread about AI agents
@social Post to LinkedIn about my project
@social Write engaging tweet about [topic]
@social Schedule post for tomorrow 10 AM
```

---

## 👥 Working with Teams

### Team Messaging

**Format:** `@<team_id> <message>`

Teams coordinate multiple agents automatically!

#### **@cc_team - Personal Productivity**

```
You: @cc_team Help me prepare for my day

CC (Leader): I'll coordinate the team.
  [@assistant: Checking calendar and tasks]
  [@researcher: Getting latest AI news]
  [@action_taker: Preparing summary]
