# LeetCode Skill Submission Guide

Complete guide for submitting the LeetCode skill to Claude Skill Hub, Claude Code repository, and OpenClaw.

## 📦 What's Been Prepared

All submission packages are ready in this repository:

### 1. Skill Hub Package (`.skill-hub/leetcode/`)
- ✅ `package.json` - Skill metadata
- ✅ `README.md` - User documentation
- ✅ `SKILL.md` - Skill definition
- ✅ `SUBMISSION.md` - Submission checklist

### 2. MCP Server (`mcp-servers/leetcode/`)
- ✅ `server.py` - Full MCP server implementation
- ✅ `test_server.py` - Complete test suite
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Technical documentation
- ✅ `INTEGRATION.md` - Setup guide
- ✅ `mcp-config.json` - Configuration example

### 3. Skills Module (`agents/base/leetcode_skills.py`)
- ✅ Python API for OpenClaw agents
- ✅ Async methods for all tools
- ✅ Helper functions and convenience methods

### 4. Examples (`examples/leetcode_example.py`)
- ✅ 7 complete usage examples
- ✅ Interview prep agent demo
- ✅ Study plan generator

### 5. PR Templates (`.github/`)
- ✅ `PULL_REQUEST_CLAUDE.md` - Claude Code PR
- ✅ `PULL_REQUEST_OPENCLAW.md` - OpenClaw PR

---

## 🚀 Submission Instructions

### Step 1: Submit to Claude Skill Hub

**Option A: GitHub-based Submission**

If Claude has a skill hub repository (e.g., `anthropics/claude-skills`):

```bash
# 1. Fork the skills repository
# 2. Create a new branch
git checkout -b add-leetcode-skill

# 3. Copy the skill package
cp -r .skill-hub/leetcode/ path/to/skills-repo/skills/leetcode/

# 4. Commit
git add skills/leetcode/
git commit -m "Add LeetCode skill for coding interview practice"

# 5. Push and create PR
git push origin add-leetcode-skill
# Then create PR on GitHub
```

**Option B: Direct Submission**

If there's a submission form or email:

1. **Package the skill:**
```bash
cd .skill-hub
tar -czf leetcode-skill.tar.gz leetcode/
```

2. **Submit with details:**
   - **Skill Name:** LeetCode
   - **Category:** Development / Education
   - **Description:** Practice coding interviews with LeetCode problems
   - **Package:** `leetcode-skill.tar.gz`
   - **Repository:** https://github.com/vilobhmm/agents

**Option C: Claude Community Forums**

Post in Claude community with:
- Link to this repository
- Skill description from `.skill-hub/leetcode/README.md`
- Installation instructions
- Demo video or screenshots

---

### Step 2: Submit to Claude Code Repository

**If there's an official Anthropic/Claude Code repository:**

```bash
# 1. Fork the repository
# Visit: https://github.com/anthropics/claude-code (or similar)
# Click "Fork"

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/claude-code.git
cd claude-code

# 3. Create a feature branch
git checkout -b add-leetcode-mcp-server

# 4. Add the MCP server
mkdir -p servers/leetcode
cp -r /path/to/agents/mcp-servers/leetcode/* servers/leetcode/

# 5. Add the skill definition
mkdir -p skills/leetcode
cp /path/to/agents/.skill-hub/leetcode/SKILL.md skills/leetcode/

# 6. Commit
git add servers/leetcode/ skills/leetcode/
git commit -m "Add LeetCode MCP server and skill"

# 7. Push
git push origin add-leetcode-mcp-server

# 8. Create Pull Request
# Go to GitHub and create PR using .github/PULL_REQUEST_CLAUDE.md as template
```

**PR Details:**
- **Title:** Add LeetCode MCP Server and Skill
- **Body:** Copy from `.github/PULL_REQUEST_CLAUDE.md`
- **Base branch:** `main` (or `master`)
- **Head branch:** `add-leetcode-mcp-server`

---

### Step 3: Create PR for OpenClaw Repository

**This repository already has everything - just create the PR:**

```bash
# The branch already exists and is pushed
# Visit: https://github.com/vilobhmm/agents/pulls

# Or use GitHub CLI if available:
gh pr create \
  --base main \
  --head claude/openclaw-weekend-projects-st5pW \
  --title "Add LeetCode Integration: MCP Server, Skills, and Examples" \
  --body-file .github/PULL_REQUEST_OPENCLAW.md
```

**Manual PR Creation:**

1. Go to: https://github.com/vilobhmm/agents/compare
2. Set base: `main`
3. Set compare: `claude/openclaw-weekend-projects-st5pW`
4. Click "Create pull request"
5. Title: "Add LeetCode Integration: MCP Server, Skills, and Examples"
6. Body: Copy from `.github/PULL_REQUEST_OPENCLAW.md`
7. Click "Create pull request"

---

## 📋 Pre-Submission Checklist

### Code Quality
- [x] All tests passing (`python mcp-servers/leetcode/test_server.py`)
- [x] No syntax errors
- [x] Type hints included
- [x] Error handling implemented
- [x] Logging configured

### Documentation
- [x] README.md complete
- [x] INTEGRATION.md with setup guide
- [x] SKILL.md with examples
- [x] Code comments
- [x] API documentation

### Security
- [x] No hardcoded credentials
- [x] Input validation
- [x] Safe error messages
- [x] Public API only
- [x] No PII collection

### Functionality
- [x] MCP server works
- [x] All 5 tools functional
- [x] Multi-language support
- [x] Error cases handled
- [x] Examples run successfully

### Compatibility
- [x] Python 3.8+
- [x] MCP protocol compliant
- [x] Cross-platform (Linux, macOS, Windows)
- [x] No breaking changes

---

## 🎯 Submission Timeline

**Immediate:**
1. ✅ Create PR for OpenClaw (this repo)
2. ✅ All code committed and pushed

**Next Steps:**
1. Submit to Claude Skill Hub (when hub available)
2. Submit to Claude Code repository (if accepting contributions)
3. Post in Claude community forums
4. Share on social media

---

## 📧 Contact Information

**Repository:** https://github.com/vilobhmm/agents
**Branch:** claude/openclaw-weekend-projects-st5pW
**Maintainer:** OpenClaw Team (@vilobhmm)

**Submission URLs:**
- OpenClaw PR: https://github.com/vilobhmm/agents/pull/new/claude/openclaw-weekend-projects-st5pW
- Claude Skill Hub: (Check https://claude.ai or Anthropic documentation)
- Claude Code: (Check https://github.com/anthropics for official repos)

---

## 🎬 Demo & Marketing

### Demo Video Script

```
1. Show today's daily challenge
   "/leetcode what's today's daily challenge?"

2. Get a classic problem
   "Show me the two-sum problem"

3. Search for problems
   "Find 5 medium array problems"

4. Get progressive hints
   "I'm stuck on two-sum, give me a hint"

5. Show statistics
   "What's the acceptance rate for problem 42?"
```

### Social Media Posts

**Twitter/X:**
```
🚀 Just built a LeetCode skill for @AnthropicAI Claude Code!

✅ Practice coding interviews in Claude
✅ Daily challenges
✅ Progressive hints
✅ No LeetCode login needed

Check it out: [link to repo]

#ClaudeAI #LeetCode #CodingInterview
```

**LinkedIn:**
```
Excited to share a new tool for technical interview prep!

I built a LeetCode integration for Claude Code that lets you:
- Practice coding problems with AI assistance
- Get daily challenges
- Search by topic and difficulty
- Receive progressive hints

Built with the Model Context Protocol (MCP) and fully open source.

[Link to repo + demo]
```

### Blog Post Outline

1. **Introduction**
   - Why coding interview prep is hard
   - How AI can help

2. **Features**
   - 5 MCP tools
   - No login required
   - Progressive hints

3. **How It Works**
   - MCP server architecture
   - LeetCode GraphQL API
   - Claude integration

4. **Getting Started**
   - Installation
   - Configuration
   - First problem

5. **Use Cases**
   - Students
   - Professionals
   - Educators
   - Agent builders

6. **Technical Details**
   - Code walkthrough
   - Design decisions
   - Future plans

---

## 🔗 Useful Links

**Documentation:**
- Main README: `mcp-servers/leetcode/README.md`
- Integration Guide: `mcp-servers/leetcode/INTEGRATION.md`
- Submission Info: `.skill-hub/leetcode/SUBMISSION.md`

**Code:**
- MCP Server: `mcp-servers/leetcode/server.py`
- Skills Module: `agents/base/leetcode_skills.py`
- Examples: `examples/leetcode_example.py`

**Templates:**
- Claude PR: `.github/PULL_REQUEST_CLAUDE.md`
- OpenClaw PR: `.github/PULL_REQUEST_OPENCLAW.md`

---

## ✅ Quick Commands

### Test Everything
```bash
# Test MCP server
cd mcp-servers/leetcode
python test_server.py

# Run examples
cd ../../examples
python leetcode_example.py

# Verify skill file
cat ~/.claude/skills/leetcode/SKILL.md
```

### Package for Distribution
```bash
# Create tarball
tar -czf leetcode-skill-v1.0.0.tar.gz \
  mcp-servers/leetcode/ \
  agents/base/leetcode_skills.py \
  examples/leetcode_example.py \
  .skill-hub/leetcode/

# Create zip
zip -r leetcode-skill-v1.0.0.zip \
  mcp-servers/leetcode/ \
  agents/base/leetcode_skills.py \
  examples/leetcode_example.py \
  .skill-hub/leetcode/
```

### Create OpenClaw PR
```bash
# Visit this URL in your browser:
# https://github.com/vilobhmm/agents/compare/main...claude/openclaw-weekend-projects-st5pW

# Or use these commands:
git checkout claude/openclaw-weekend-projects-st5pW
git push -u origin claude/openclaw-weekend-projects-st5pW

# Then create PR on GitHub with .github/PULL_REQUEST_OPENCLAW.md as body
```

---

## 🎉 You're Ready!

Everything is prepared and ready for submission:

1. ✅ **Code** - Fully functional and tested
2. ✅ **Documentation** - Complete and comprehensive
3. ✅ **Examples** - 7 working examples
4. ✅ **PR Templates** - Ready to copy/paste
5. ✅ **Skill Package** - Ready for distribution
6. ✅ **Tests** - All passing

**Next step:** Choose your submission path above and go! 🚀

---

**Questions?** Open an issue at: https://github.com/vilobhmm/agents/issues

**Good luck with your submissions!** 🎯
