# 🤖 CC Multi-Agent System - Complete User Guide

## What is CC?

**CC (Chief Coordinator)** is your AI productivity copilot that connects to your Gmail, Google Calendar, and Google Drive to help you stay on top of your day. Think of it as having a personal assistant who knows your schedule, reads your emails, and helps you stay organized.

---

## 🎯 What Can CC Do?

### 1. **📧 Email Management**

**Read and Summarize Emails:**
```bash
python -m agency debug test cc --message "What are my unread emails?"
python -m agency debug test cc --message "Summarize emails from Sarah"
python -m agency debug test cc --message "Any urgent emails I need to respond to?"
```

**Search Emails:**
```bash
python -m agency debug test cc --message "Find emails about the Q4 budget"
python -m agency debug test cc --message "Show me emails from John about the project"
```

**Send Emails:**
```bash
python -m agency debug test cc --message "Send an email to sarah@company.com saying I'll be 10 minutes late to the meeting"
python -m agency debug test cc --message "Draft a response to John's email about the deadline"
```

**Example Output:**
```
📧 Inbox Summary:

You have 5 unread emails:

1. Sarah Martinez - "Q4 Budget Review" (2 hours ago)
   Priority: HIGH - Needs response by EOD
   Summary: Requesting your input on Q4 budget allocation...

2. LinkedIn - "You appeared in 3 searches" (yesterday)
   Priority: LOW - Informational
```

---

### 2. **📅 Calendar Management**

**View Schedule:**
```bash
python -m agency debug test cc --message "What's on my calendar today?"
python -m agency debug test cc --message "Show me my meetings this week"
python -m agency debug test cc --message "When is my next meeting?"
```

**Create Events:**
```bash
python -m agency debug test cc --message "Schedule a meeting with team tomorrow at 2pm for 1 hour"
python -m agency debug test cc --message "Block 30 minutes for lunch at noon"
python -m agency debug test cc --message "Create a 1:1 with John next Tuesday at 10am"
```

**Check Availability:**
```bash
python -m agency debug test cc --message "Am I free tomorrow afternoon?"
python -m agency debug test cc --message "Find a 30-minute slot this week for a meeting"
```

**Example Output:**
```
📅 Today's Schedule:

9:00 AM - 9:30 AM: Daily Standup
   Location: Zoom
   Attendees: Team

2:00 PM - 3:00 PM: Interview - Anthropic
   Location: Video call
   ⚡ IMPORTANT: Resume sent, check email for prep materials

5:00 PM - 5:30 PM: 1:1 with Manager
```

---

### 3. **📁 Google Drive Access**

**Search Files:**
```bash
python -m agency debug test cc --message "Find my resume in Drive"
python -m agency debug test cc --message "Show me recent documents about the project"
python -m agency debug test cc --message "Where is the Q4 budget spreadsheet?"
```

**Recent Files:**
```bash
python -m agency debug test cc --message "What files did I work on today?"
python -m agency debug test cc --message "Show me my recent documents"
```

**Example Output:**
```
📁 Recent Drive Activity:

1. Resume_Software_Engineer_2024.pdf
   Last modified: Today at 3:45 PM

2. Q4_Budget_Proposal.xlsx
   Last modified: Yesterday

3. Project_Plan_v2.docx
   Last modified: 2 days ago
```

---

### 4. **🌅 Morning Briefing**

**Get Daily Summary:**
```bash
python -m agency debug test cc --message "Give me my morning briefing"
python -m agency debug test cc --message "What should I know about today?"
python -m agency debug test cc --message "Prepare me for the day"
```

**Example Output:**
```
☀️ Good Morning! Here's your briefing for Feb 16, 2024

📧 INBOX (5 unread - 2 urgent)
• Sarah - Q4 Budget review - NEEDS RESPONSE BY EOD
• Manager - 1:1 agenda for today - Review before 5pm meeting

📅 CALENDAR (3 meetings today)
• 9:00 AM: Daily standup (Zoom)
• 2:00 PM: Interview with Anthropic ⚡ HIGH PRIORITY
• 5:00 PM: 1:1 with Manager

📁 DRIVE (Recent activity)
• Resume updated yesterday - ready for applications
• Budget spreadsheet edited by Finance team

🎯 TOP PRIORITIES:
1. Respond to Sarah's budget email
2. Prepare for 2pm interview
3. Review 1:1 agenda before 5pm

⏰ TIME CHECK:
• You have 2 hours before your first meeting
• Interview prep materials are in email from Anthropic
```

---

### 5. **🎯 Meeting Preparation**

**Prepare for Meetings:**
```bash
python -m agency debug test cc --message "Prepare me for my 2pm meeting with Anthropic"
python -m agency debug test cc --message "What do I need to know for today's interview?"
python -m agency debug test cc --message "Find emails about the standup meeting"
```

**Example Output:**
```
📊 Meeting Prep: Interview with Anthropic (2:00 PM)

📧 RELATED EMAILS (3):
1. Recruiter email with interview details
2. Job description for Research Engineer role
3. Team info and interviewer bios

📁 RELEVANT DOCS:
1. Your Resume (updated yesterday)
2. Anthropic research papers (saved last week)

💡 KEY POINTS:
• Interview format: Technical + behavioral (1 hour)
• Interviewer: Dr. Smith (Safety Research team)
• Focus areas: ML safety, RLHF, model alignment
• Your talking points: Previous safety work at [company]

✅ YOU'RE READY:
• Resume sent ✓
• Interview link received ✓
• Zoom link: [provided in email]
```

---

### 6. **⚡ Quick Actions**

**Time Blocking:**
```bash
python -m agency debug test cc --message "Block 2 hours for deep work tomorrow morning"
python -m agency debug test cc --message "Hold my calendar for 30 minutes this afternoon"
```

**Email Quick Replies:**
```bash
python -m agency debug test cc --message "Reply to Sarah that I'll review by EOD"
python -m agency debug test cc --message "Send a quick thank you to John for the referral"
```

**Priority Alerts:**
```bash
python -m agency debug test cc --message "What needs my attention right now?"
python -m agency debug test cc --message "Any deadlines coming up?"
```

---

### 7. **🔔 Proactive Assistance**

CC is **proactive** - it doesn't just wait for you to ask. It will:

- **Alert on urgent items:** "You have an urgent email from your manager"
- **Remind about deadlines:** "Sarah's budget request needs response by EOD"
- **Suggest actions:** "Your calendar is packed - should I block lunch?"
- **Prepare context:** "Your 2pm meeting is in 30 minutes - here's what you need to know"
- **Track patterns:** "You usually take breaks at 11am - should I block time?"

---

## 💼 Real-World Usage Examples

### Example 1: Starting Your Day
```bash
# Morning routine
python -m agency debug test cc --message "Good morning! What's my day looking like?"

# CC responds with:
# - Unread emails with priorities
# - Today's meetings with context
# - Action items that need attention
# - Suggested priorities
```

### Example 2: Before a Meeting
```bash
python -m agency debug test cc --message "I have an interview with Anthropic in 30 minutes. Help me prepare."

# CC responds with:
# - Interview details from email
# - Related documents from Drive
# - Previous communications
# - Key talking points
# - Zoom link and logistics
```

### Example 3: Email Triage
```bash
python -m agency debug test cc --message "Which emails need my immediate attention?"

# CC responds with:
# - Urgent emails flagged
# - Deadlines highlighted
# - Suggested responses
# - Items that can wait
```

### Example 4: Calendar Management
```bash
python -m agency debug test cc --message "My calendar is too packed. What can I move?"

# CC responds with:
# - Overview of schedule
# - Meetings that could be rescheduled
# - Suggested time blocks for focus work
# - Conflicts to resolve
```

---

## 🚀 How to Use CC

### Basic Setup (One-Time)

1. **Re-authenticate Google Services** (if you haven't already):
```bash
cd ~/agents  # or wherever your agents directory is
python reauth_google.py
```

2. **Grant Permissions:**
- Sign in to your Google account
- Grant ALL permissions (Gmail, Calendar, Drive)
- Click "Advanced" → "Go to app" if you see "App not verified"

### Using CC

**Command Format:**
```bash
python -m agency debug test cc --message "YOUR QUESTION OR REQUEST HERE"
```

**Examples:**
```bash
# Morning briefing
python -m agency debug test cc --message "Give me my morning briefing"

# Check emails
python -m agency debug test cc --message "What are my unread emails?"

# Check calendar
python -m agency debug test cc --message "What's on my schedule today?"

# Search Drive
python -m agency debug test cc --message "Find my resume in Drive"

# Send email
python -m agency debug test cc --message "Send an email to john@company.com thanking him for the referral"

# Create meeting
python -m agency debug test cc --message "Schedule a 1:1 with Sarah tomorrow at 2pm for 30 minutes"
```

---

## 🎓 Pro Tips

### 1. **Be Conversational**
CC understands natural language. Talk to it like you'd talk to a human assistant:
- ✅ "What's on my plate today?"
- ✅ "Help me prep for my 2pm"
- ✅ "Any urgent stuff in my inbox?"

### 2. **Chain Requests**
CC remembers context, so you can follow up:
```
You: "Show me emails from Sarah"
CC: [Shows emails]
You: "Draft a response to the budget one"
CC: [Drafts response]
```

### 3. **Use Time References**
CC understands natural time references:
- "today", "tomorrow", "this week"
- "in 30 minutes", "at 2pm"
- "next Tuesday", "end of day"

### 4. **Ask for Help**
Not sure what CC can do?
```bash
python -m agency debug test cc --message "What can you help me with?"
```

---

## ⚠️ Limitations

### What CC Can Do:
- ✅ Read Gmail messages
- ✅ Search emails
- ✅ Send emails
- ✅ View calendar events
- ✅ Create calendar events
- ✅ Search Google Drive files
- ✅ Access file metadata
- ✅ Provide intelligent summaries

### What CC Cannot Do (Yet):
- ❌ Edit Google Docs content directly
- ❌ Delete emails or calendar events
- ❌ Share Drive files
- ❌ Access other people's calendars (unless shared with you)
- ❌ Book external meeting rooms

---

## 🔧 Troubleshooting

### Issue: "Insufficient permissions" error
**Solution:** Run `python reauth_google.py` and grant all permissions

### Issue: "Credentials file not found"
**Solution:** Download OAuth credentials from Google Cloud Console

### Issue: CC doesn't see my emails/calendar
**Solution:**
1. Delete `google_token.pickle`
2. Run `python reauth_google.py`
3. Make sure you grant ALL permissions

### Issue: CC is slow to respond
**Solution:** This is normal - CC is reading your emails/calendar in real-time

---

## 📊 CC Multi-Agent System

CC is part of a larger multi-agent system. Here's how it works with other agents:

### 🎯 **Job Hunter** → Search for jobs with real links
```bash
python -m agency debug test job_hunter --message "Find Java developer jobs at Infosys, TCS, Accenture in India"
```

### 📄 **Resume Optimizer** → Tailor resume to jobs
```bash
python -m agency debug test resume_optimizer --message "Optimize my resume for the Infosys Java role"
```

### 🤝 **Networker** → Manage contacts and outreach
```bash
python -m agency debug test networker --message "Draft a LinkedIn message to John asking for a referral"
```

### 🎯 **CC Coordinates Everything**
CC can work with these agents to help you:
1. Get morning briefing with job alerts
2. Prepare interview materials from Drive
3. Send thank-you emails after interviews
4. Schedule follow-up reminders

---

## 🎉 Get Started Now!

1. **Re-authenticate** (if you haven't):
```bash
python reauth_google.py
```

2. **Try your first briefing**:
```bash
python -m agency debug test cc --message "Give me my morning briefing"
```

3. **Explore what CC can do**:
```bash
python -m agency debug test cc --message "What can you help me with today?"
```

---

**CC is your productivity copilot. Let it help you stay ahead of your day!** 🚀
