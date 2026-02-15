# 🛡⚡ Avengers AI Operating System

**Multi-agent Agentic - Personal. Proactive. Powerful.**

**Six agents. Clear ownership. No overlap. Continuous output.**

A sophisticated multi-agent orchestration system where specialized AI agents work together like the Avengers team. You interact with **Iron Man** (Chief of Staff) via **Telegram** or **WhatsApp**, who coordinates and manages five specialized agents to build your public AI laboratory.

## The Team

### 🧠 Iron Man - Chief of Staff (Your Interface)
**The only agent you talk to**

- Strategic planning and task prioritization
- Delegates work to specialized agents
- Monitors all agent activities
- Provides consolidated status updates
- Makes decisions and sets direction
- Quality control across all outputs

**Role**: Central command and primary interface

### 🛡 Captain America - Research & Intelligence
**Protects signal integrity**

- Runs structured research sweeps 3x daily
- Monitors: X, HackerNews, GitHub Trending, AI blogs, research papers
- Produces clean intelligence reports
- Tracks frontier AI developments
- Filters noise into verified insights

**Output**: Daily intelligence briefings

### ⚡ Thor - X/Twitter Operator
**Converts intelligence into reach**

- Crafts high-impact tweets and threads
- Rapid commentary on AI developments
- Amplifies key insights
- Builds online presence
- Posts 3-5 times daily

**Output**: Twitter engagement and reach

### 🕷 Black Widow - LinkedIn Authority Architect
**Builds professional credibility**

- Deep analysis posts
- Thought leadership content
- Strategic commentary
- Founder/researcher positioning
- Posts 2-3 times weekly

**Output**: Professional authority and reputation

### 🔨 Hulk - Prototype Architect & GitHub Executor
**Builds understanding through execution**

- Converts AI concepts into working code
- Ships to https://github.com/vilobhmm
- Creates runnable prototypes
- Writes clear documentation
- Builds 2-3 prototypes weekly

**Output**: Working code artifacts

### 🎯 Hawkeye - Newsletter & Intelligence Distillation
**Filters everything into clarity**

- Weekly AI digest
- Research summaries
- Prototype highlights
- Clean narrative flow

**Output**: Weekly newsletter

## System Flow

```
Research → Prioritization → Execution → Amplification → Authority → Compounding

1. Captain America gathers frontier intelligence
2. Iron Man prioritizes and delegates
3. Hulk builds working prototypes
4. Thor amplifies on X
5. Black Widow builds authority on LinkedIn
6. Hawkeye distills into newsletter
```

## WhatsApp Control

Interact with Iron Man via WhatsApp to:

### Command Reference

```
status - Get status of all agents
assign <task> - Assign a new task
report <agent> - Get specific agent report
priority <high|medium|low> - Set task priority
sprint - View current sprint
done <task> - Mark task as complete
```

### Example Conversation

```
You: status

Iron Man: 🧠 AVENGERS STATUS

🛡 Captain America: Research complete
   - 15 AI updates tracked today
   - 3 major model releases
   - Report ready

⚡ Thor: Posted 4 tweets today
   - Engagement: 2.3K impressions
   - 1 thread on GPT-4.5 Turbo

🕷 Black Widow: 1 LinkedIn post drafted
   - Topic: RAG systems deep dive
   - Ready for review

🔨 Hulk: 1 prototype in progress
   - Mini RAG implementation
   - 80% complete

🎯 Hawkeye: Newsletter draft 60% done
   - Ships Friday

---

You: assign Build a LoRA fine-tuning demo

Iron Man: ✅ Task assigned to Hulk

Priority: High
Estimated: 2 days
Dependencies: None

I'll keep you updated on progress.

---

You: report hulk

Iron Man: 🔨 HULK STATUS REPORT

Current Task: LoRA fine-tuning demo
Progress: 45%

Recent Completions:
✅ Tiny RAG system (shipped 2 days ago)
✅ RLHF simulation (shipped 5 days ago)

GitHub Activity:
- 3 repos created this week
- 247 lines of code
- All prototypes running

Next: Complete LoRA demo by tomorrow

---

You: What's the most important AI news today?

Iron Man: 🛡 Per Captain America's latest report:

1. 🚨 Anthropic released Claude 4.6 Opus
   - 10x context window
   - New function calling
   - Available now

2. 📄 DeepMind paper on world models
   - Achieves state-of-the-art on MuJoCo
   - Novel training approach

3. 🛠 OpenAI updated GPT-4.5 Turbo
   - 2x faster
   - Better reasoning

⚡ Thor already posted thread on #1
🕷 Black Widow drafting analysis

Want me to assign any tasks based on these?
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Required environment variables:

```bash
# Core
ANTHROPIC_API_KEY=your_key

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890

# Social Media
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_secret
LINKEDIN_ACCESS_TOKEN=your_token

# GitHub
GITHUB_TOKEN=your_token
GITHUB_USERNAME=vilobhmm

# Research Sources
HACKER_NEWS_API_KEY=optional
```

### 3. Start the System

```bash
python -m projects.11_avengers_system.main
```

The system will:
- Initialize all 6 agents
- Start monitoring loops
- Connect to WhatsApp
- Begin automated tasks

### 4. Send WhatsApp Message

Send "start" to your Twilio WhatsApp number to begin interacting with Iron Man.

## Operating Philosophy

### Learn Fast
- Captain America monitors the frontier daily
- Intelligence reports delivered 3x daily

### Build Immediately
- Hulk converts concepts to code within 48 hours
- All prototypes ship to GitHub

### Ship Publicly
- Thor amplifies on X within hours of research
- Black Widow positions on LinkedIn weekly
- Hawkeye publishes newsletter every Friday

### Document Clearly
- Every prototype has README
- Every insight gets written down
- Knowledge compounds over time

### Repeat Relentlessly
- System runs 24/7
- Consistent output
- Continuous improvement

## Agent Schedules

**Captain America** (Research)
- 7:00 AM - Morning research sweep
- 1:00 PM - Midday update
- 7:00 PM - Evening analysis

**Thor** (Twitter)
- Throughout day - Rapid responses
- 8:00 AM - Morning insight
- 12:00 PM - Midday thread
- 5:00 PM - Evening commentary

**Black Widow** (LinkedIn)
- Monday 9:00 AM - Deep analysis post
- Thursday 9:00 AM - Thought leadership

**Hulk** (GitHub)
- Continuous - Prototype development
- Friday 5:00 PM - Weekly shipping deadline

**Hawkeye** (Newsletter)
- Monday - Research compilation
- Wednesday - Draft review
- Friday 8:00 AM - Newsletter publish

**Iron Man** (Orchestration)
- Continuous monitoring
- Instant response via WhatsApp
- 6:00 AM - Morning briefing to you
- 8:00 PM - Evening summary to you

## Output Standards

### Research (Captain America)
- ✅ Source verification
- ✅ Impact assessment
- ✅ Actionable insights
- ✅ Daily reports

### Twitter (Thor)
- ✅ 280 characters of clarity
- ✅ High signal-to-noise
- ✅ Timely and relevant
- ✅ Engagement-worthy

### LinkedIn (Black Widow)
- ✅ Deep analysis (500+ words)
- ✅ Professional tone
- ✅ Strategic positioning
- ✅ Authority building

### Code (Hulk)
- ✅ Runs without errors
- ✅ Minimal but complete
- ✅ Clear documentation
- ✅ Teaches the concept

### Newsletter (Hawkeye)
- ✅ Signal-only content
- ✅ Clean narrative
- ✅ Actionable takeaways
- ✅ Weekly cadence

## Architecture

```
┌─────────────────────────────────────────┐
│         You (via WhatsApp)              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  🧠 Iron Man - Chief Orchestrator       │
│  - Receives your commands               │
│  - Delegates to specialized agents      │
│  - Monitors all activities              │
│  - Reports back to you                  │
└─────────────┬───────────────────────────┘
              │
      ┌───────┴────────┬────────┬─────────┬────────┐
      │                │        │         │        │
      ▼                ▼        ▼         ▼        ▼
┌──────────┐  ┌──────────┐  ┌────────┐  ┌───────┐  ┌────────┐
│🛡 Captain│  │⚡ Thor   │  │🕷 Black│  │🔨 Hulk│  │🎯 Hawk │
│  America │  │          │  │  Widow │  │       │  │  eye   │
│          │  │          │  │        │  │       │  │        │
│ Research │  │ Twitter  │  │LinkedIn│  │GitHub │  │Newsletter│
└──────────┘  └──────────┘  └────────┘  └───────┘  └────────┘
      │                │        │         │        │
      └────────────────┴────────┴─────────┴────────┘
                      │
              Shared Knowledge Base
         (Everything Iron Man can see)
```

## Communication Flow

All agents report to Iron Man. Iron Man reports to you.

### Agent-to-Iron Man
- Status updates every 4 hours
- Completion notifications
- Blocker escalations
- Quality checks

### Iron Man-to-You
- Morning briefing (6 AM)
- Evening summary (8 PM)
- Urgent notifications (real-time)
- On-demand status via WhatsApp

## Example Use Cases

### 1. Daily Research Pipeline
```
6:00 AM - Captain America's morning sweep
7:00 AM - Iron Man briefs you on key developments
9:00 AM - You assign: "Build a demo of that new technique"
9:15 AM - Iron Man delegates to Hulk
11:00 AM - Thor posts thread on the development
2:00 PM - Hulk completes prototype
5:00 PM - Black Widow drafts LinkedIn analysis
8:00 PM - Iron Man shows you everything produced
```

### 2. Sprint Planning
```
You: "Start 2-week sprint on RAG systems"

Iron Man assigns:
- Captain America: Research all RAG papers
- Hulk: Build 3 RAG prototypes
- Thor: Daily updates on RAG developments
- Black Widow: Deep dive post on RAG evolution
- Hawkeye: RAG special edition newsletter

Progress tracked daily via WhatsApp.
```

### 3. Reactive Intelligence
```
News: GPT-5 announced

Captain America: Detects and analyzes
Iron Man: Briefs you immediately
Thor: Thread within 1 hour
Hulk: Explores new capabilities
Black Widow: Strategic analysis
Hawkeye: Includes in weekly digest
```

## Metrics Tracked

Iron Man monitors:
- **Research**: Sources checked, updates tracked, insights generated
- **Twitter**: Tweets posted, impressions, engagement rate
- **LinkedIn**: Posts published, views, reactions
- **GitHub**: Repos created, prototypes shipped, code quality
- **Newsletter**: Open rate, click rate, subscriber growth

Weekly report delivered every Monday.

## Benefits

### For You
- ✅ One interface (WhatsApp with Iron Man)
- ✅ Complete visibility into all activities
- ✅ No micro-management needed
- ✅ Consistent, compounding output
- ✅ Building in public systematically

### For Learning
- ✅ Forced articulation (teaching through content)
- ✅ Immediate prototyping (theory → practice)
- ✅ Knowledge compound effect
- ✅ Public accountability

### For Reach
- ✅ Multi-platform presence
- ✅ Consistent publishing
- ✅ Authority building
- ✅ Network effects

## Troubleshooting

**Issue: Iron Man not responding on WhatsApp**
- Check Twilio credentials
- Verify webhook setup
- Check logs: `tail -f avengers.log`

**Issue: Agents not updating**
- Check individual agent logs
- Verify API credentials
- Check scheduler status

**Issue: GitHub pushes failing**
- Verify GITHUB_TOKEN
- Check repository permissions
- Ensure SSH keys configured

## Advanced Configuration

### Custom Agent Schedules

Edit `config.py`:

```python
AGENT_SCHEDULES = {
    "captain_america": ["0 7 * * *", "0 13 * * *", "0 19 * * *"],
    "thor": "*/30 * * * *",  # Every 30 minutes
    "black_widow": ["0 9 * * 1", "0 9 * * 4"],  # Mon & Thu
    "hulk": "0 */4 * * *",  # Every 4 hours
    "hawkeye": "0 8 * * 5",  # Friday 8 AM
}
```

### Priority Levels

```python
PRIORITY_LEVELS = {
    "urgent": {"response_time": "1 hour", "agents": ["all"]},
    "high": {"response_time": "4 hours", "agents": ["assigned"]},
    "medium": {"response_time": "1 day", "agents": ["assigned"]},
    "low": {"response_time": "1 week", "agents": ["assigned"]},
}
```

## Philosophy

This is not content creation.
This is building an AI laboratory in public.

**Learn fast. Build immediately. Ship publicly. Document clearly. Repeat relentlessly.**

Six agents. One system. Continuous visible output.

---

**Created for**: Building in public, compound learning, authority building

**Managed via**: WhatsApp + Iron Man

**Output**: Daily AI insights, prototypes, content across platforms
