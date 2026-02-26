# 📚 Examples & Demos

**Working examples demonstrating Agency capabilities**

This directory contains example scripts and demos showing how to use the Agency system and its agents.

---

## 📁 Directory Structure

```
examples/
├── README.md (this file)
├── feedback/                  # Feedback Management Examples
│   ├── README.md             # Feedback examples guide
│   ├── e2e_feedback_github_demo.py      # E2E demo with real GitHub issues
│   └── feedback_management_demo.py      # Basic feedback workflow demo
└── basic/                    # Basic Agent Examples
    ├── simple_agent.py       # Single agent example
    ├── proactive_agent.py    # Proactive agent example
    └── multi_agent.py        # Multi-agent coordination example
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

---

## 📋 Feedback Management Examples

### 1. **E2E GitHub Feedback Demo** 🎯

**File:** [`feedback/e2e_feedback_github_demo.py`](./feedback/e2e_feedback_github_demo.py)

**What it does:**
- Fetches real issues from `vercel/next.js` GitHub repo
- Uses Claude AI to cluster feedback by theme
- Tracks bugs and generates solutions
- Creates analytics dashboard

**Run:**
```bash
cd /home/user/agents
ANTHROPIC_API_KEY=sk-ant-... python examples/feedback/e2e_feedback_github_demo.py
```

**Workflow:**
1. `/submitfeedback` - Fetch & store real GitHub issues
2. `/clusterfeedback` - Claude clusters by theme + root cause
3. `/trackbugs` - Create tracked bugs from clusters
4. `/generatesolutions` - Generate PRDs + coding prompts
5. `/feedbackreport` - View analytics dashboard

**Expected output:**
```
═══════════════════════════════════════════════════════════════════
  🚀  E2E Feedback Management Demo — Real GitHub Issues + Claude AI
═══════════════════════════════════════════════════════════════════

▶ Step 1: Fetch real GitHub issues as feedback

  → Fetching 15 issues from vercel/next.js...
  ✓ Fetched 15 issues from GitHub
  ✓ Submitted 15 feedback reports

▶ Step 2: Cluster feedback by theme (Claude AI)

  → Calling Claude to analyze feedback and create clusters...
  ✓ Created 3 clusters

  Cluster 1: Build Performance Issues
    └─ 5 feedback items

  Cluster 2: TypeScript Type Errors
    └─ 6 feedback items

  Cluster 3: Routing Problems
    └─ 4 feedback items

...
```

---

### 2. **Basic Feedback Management Demo**

**File:** [`feedback/feedback_management_demo.py`](./feedback/feedback_management_demo.py)

**What it does:**
- Demonstrates basic feedback workflow
- Shows how to use feedback tools directly
- Simple clustering and bug tracking

**Run:**
```bash
python examples/feedback/feedback_management_demo.py
```

---

## 🤖 Basic Agent Examples

### 1. **Simple Agent** 🎯

**File:** [`basic/simple_agent.py`](./basic/simple_agent.py)

**What it does:**
- Shows how to create a basic agent
- Single agent responding to messages
- Minimal setup

**Run:**
```bash
python examples/basic/simple_agent.py
```

---

### 2. **Proactive Agent** ⚡

**File:** [`basic/proactive_agent.py`](./basic/proactive_agent.py)

**What it does:**
- Demonstrates proactive notifications
- Agent runs on schedule
- Sends alerts based on conditions

**Run:**
```bash
python examples/basic/proactive_agent.py
```

---

### 3. **Multi-Agent System** 🤝

**File:** [`basic/multi_agent.py`](./basic/multi_agent.py)

**What it does:**
- Multiple agents working together
- Agent coordination
- Task delegation between agents

**Run:**
```bash
python examples/basic/multi_agent.py
```

---

## 🛠️ Adding Your Own Examples

### Step 1: Create Example File

```bash
# For new category
mkdir -p examples/my_category
cd examples/my_category

# Create example
touch my_example.py
```

### Step 2: Write Example Code

```python
#!/usr/bin/env python3
"""
My Example - Description
========================

What this example demonstrates.

Run:
  python examples/my_category/my_example.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agency.agents.my_agent.my_skills import MySkills

def main():
    """Run the example."""
    print("Starting my example...")

    # Your example logic here
    skills = MySkills()
    result = skills.my_skill(param1="value")

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

### Step 3: Document Example

Add your example to this README with:
- Description
- What it demonstrates
- How to run it
- Expected output

---

## 📖 Example Categories

### Feedback Management
Examples demonstrating the feedback collection → clustering → bug tracking → solution generation pipeline.

**Use cases:**
- Product feedback analysis
- Bug tracking automation
- Customer support insights
- Feature request prioritization

---

### Agent Basics
Simple examples showing core agent functionality.

**Use cases:**
- Learning how agents work
- Building your first agent
- Understanding agent communication
- Testing agent skills

---

## 🔧 Configuration

Most examples require API keys in `.env`:

```env
# Required for Claude AI
ANTHROPIC_API_KEY=sk-ant-...

# Optional for specific examples
GOOGLE_OAUTH_CREDENTIALS_FILE=google_oauth_credentials.json
TELEGRAM_BOT_TOKEN=...
```

---

## 🐛 Troubleshooting

### Import Errors

If you get import errors:

```bash
# Make sure you're running from project root
cd /home/user/agents

# Run with proper path
python examples/feedback/e2e_feedback_github_demo.py
```

### API Key Issues

```bash
# Check your .env file
cat .env | grep ANTHROPIC_API_KEY

# Export directly if needed
export ANTHROPIC_API_KEY=sk-ant-...
```

### Permission Errors

```bash
# Make examples executable
chmod +x examples/feedback/*.py
chmod +x examples/basic/*.py
```

---

## 📚 Learn More

- **[Agent Documentation](../agency/agents/README.md)** - Learn about agents
- **[Getting Started](../GETTING_STARTED.md)** - Complete setup
- **[CLI Commands](../agency/CLI_COMMANDS.md)** - Command reference

---

## 💡 Tips

1. **Start simple** - Begin with `basic/simple_agent.py`
2. **Read the code** - Examples are well-commented
3. **Modify and experiment** - Change parameters and see what happens
4. **Build on examples** - Use them as templates for your own agents
5. **Check logs** - Look at console output to understand what's happening

---

**Learn by doing!** 🚀
