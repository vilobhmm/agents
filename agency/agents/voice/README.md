# 🎙️ Voice Agent System

**Complete voice-enabled multi-agent system for hands-free productivity**

Four specialized voice agents that work together to replace typing, boost productivity, capture ideas, and assist with development—all via voice.

---

## 🤖 The Four Voice Agents

### 1. **Dictation Agent** 📝
> *Replace typing with your voice*

**Purpose:** Transcribe audio to text for any chat interface or application.

**Key Features:**
- Real-time speech-to-text transcription
- Direct integration with Claude, ChatGPT, and other chatbots
- Continuous dictation mode
- Copy to clipboard
- Voice commands for editing
- Multi-language support

**Use cases:**
- Dictate messages to Claude AI
- Transcribe notes while walking
- Voice-to-text for any application
- Accessibility tool for hands-free typing

**[📖 Complete Dictation Agent Guide →](./dictation/README.md)**

---

### 2. **Productivity Voice Agent** 🎯
> *Your AI voice assistant for daily productivity*

**Purpose:** Talks to you, gives daily updates, and executes actions via voice commands.

**Key Features:**
- Morning briefings via voice
- Email and calendar voice summaries
- Voice-activated commands
- Proactive voice notifications
- Natural conversation interface
- Integration with Google services

**Use cases:**
- "Give me my morning briefing"
- "Check my email"
- "What's on my calendar today?"
- "Block 2 hours of focus time"
- "Schedule meeting with John"

**[📖 Complete Productivity Agent Guide →](./productivity/README.md)**

---

### 3. **Ideas Capture Agent** 💡
> *Never lose an idea again*

**Purpose:** Transcribe ideas on-the-go and save to Google Docs or Apple Notes.

**Key Features:**
- Quick voice capture
- Auto-categorization using Claude AI
- Save to Google Docs, Apple Notes, or local files
- Batch capture mode
- Idea organization by topic
- Search through saved ideas

**Use cases:**
- Capture ideas while driving
- Record thoughts during walks
- Voice journaling
- Quick note-taking in meetings
- Brainstorming sessions

**[📖 Complete Ideas Capture Guide →](./ideas_capture/README.md)**

---

### 4. **Developer Co-pilot Agent** 👨‍💻
> *Your thoughtful development partner*

**Purpose:** Voice-based code discussions, reviews, and pair programming.

**Key Features:**
- Voice code discussions with Claude
- Architecture brainstorming
- Code review via voice
- Debugging conversations
- Technical explanations
- Pair programming mode

**Use cases:**
- "How should I structure this API?"
- "Review this code file"
- "Help me debug this error"
- "Explain this algorithm"
- Voice-based pair programming

**[📖 Complete Developer Co-pilot Guide →](./dev_copilot/README.md)**

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install openai anthropic sounddevice soundfile pyperclip

# Set up API keys
export OPENAI_API_KEY=sk-...        # For Whisper STT & TTS
export ANTHROPIC_API_KEY=sk-ant-... # For Claude AI
export ELEVENLABS_API_KEY=...       # Optional: Better TTS
```

### Test Voice Skills

```python
# Test speech-to-text
from agency.voice.voice_skills import transcribe

audio_file = "recording.mp3"
text = await transcribe(audio_file)
print(text)

# Test text-to-speech
from agency.voice.voice_skills import speak

audio_file = await speak("Hello! This is a test.")
# Audio will play automatically
```

---

## 💻 Using Each Agent

### Dictation Agent

```bash
# Dictate to Claude
python -m agency.agents.voice.dictation.dictation_agent 10 claude

# Dictate to clipboard
python -m agency.agents.voice.dictation.dictation_agent 10 clipboard
```

```python
# In code
from agency.agents.voice.dictation.dictation_agent import DictationAgent

agent = DictationAgent()
result = await agent.dictate_to_claude("my_voice.mp3")
print(result["transcription"])  # Ready to send to Claude!
```

---

### Productivity Voice Agent

```bash
# Interactive mode
python -m agency.agents.voice.productivity.productivity_agent

# Options:
# 1 - Morning briefing
# 2 - Listen for command
# 3 - Continuous voice mode
```

```python
# In code
from agency.agents.voice.productivity.productivity_agent import ProductivityVoiceAgent

agent = ProductivityVoiceAgent()

# Morning briefing
result = await agent.morning_briefing(speak_out_loud=True)

# Voice command
result = await agent.listen_for_command(duration=5)
```

---

### Ideas Capture Agent

```bash
# Interactive mode
python -m agency.agents.voice.ideas_capture.ideas_capture_agent

# Options:
# 1 - Quick capture
# 2 - Batch capture (5 ideas)
# 3 - Set target (Google Docs/Apple Notes/Local)
```

```python
# In code
from agency.agents.voice.ideas_capture.ideas_capture_agent import IdeasCaptureAgent

agent = IdeasCaptureAgent()

# Quick capture
result = await agent.quick_capture(duration=30)

# Saved to Google Docs with auto-categorization!
print(result["category"])  # e.g., "project"
print(result["doc_url"])   # Link to Google Doc
```

---

### Developer Co-pilot Agent

```bash
# Interactive mode
python -m agency.agents.voice.dev_copilot.dev_copilot_agent

# Options:
# 1 - Start coding session
# 2 - Discuss code (voice)
# 3 - Review code file
# 4 - Pair programming mode
```

```python
# In code
from agency.agents.voice.dev_copilot.dev_copilot_agent import DeveloperCopilotAgent

agent = DeveloperCopilotAgent()

# Start session
await agent.start_coding_session(topic="API design")

# Discuss code
result = await agent.discuss_code("my_question.mp3")
# Agent speaks the response!

# Code review
result = await agent.review_code("app.py")
```

---

## 🎯 Multi-Agent Workflows

Use the **Voice Coordinator** to orchestrate all agents together:

```bash
python -m agency.agents.voice.voice_coordinator

# Options:
# 1 - Unified voice interface
# 2 - Morning routine workflow
```

### Morning Routine Workflow

```python
from agency.agents.voice.voice_coordinator import VoiceCoordinator

coordinator = VoiceCoordinator()

# Complete morning routine:
# - Voice briefing
# - Email summary
# - Calendar review
# - Priorities suggestion
result = await coordinator.workflow_morning_routine()
```

### Idea-to-Implementation Workflow

```python
# Capture idea → Discuss with copilot → Create task
result = await coordinator.workflow_idea_to_implementation("my_idea.mp3")

# 1. Saves idea to Google Docs
# 2. Discusses implementation with Claude
# 3. Ready to code!
```

---

## 📖 Example Workflows

### Example 1: Voice-Controlled Morning

```bash
# 1. Get morning briefing
🎤 "Give me my morning briefing"
🤖 "Good morning! You have 5 unread emails, 3 are urgent..."

# 2. Check urgent emails
🎤 "Read my urgent emails"
🤖 "Email 1: From Sarah, Budget approval needed..."

# 3. Schedule focus time
🎤 "Block 2 hours of focus time"
🤖 "I've blocked 2 hours on your calendar from 9 AM to 11 AM"
```

---

### Example 2: Capture Ideas While Driving

```bash
# Quick capture mode
🎤 Record: "New feature idea: add real-time collaboration to the editor,
            similar to Google Docs but for code..."

🤖 "Idea captured and saved to Google Docs under 'project' category"

# Later, review and implement
🤖 "Let's discuss how to implement your collaboration feature"
🎤 "Yeah, I'm thinking we could use WebSockets..."
🤖 "Good approach! For WebSockets, I'd suggest..."
```

---

### Example 3: Voice Code Review

```bash
# Start pair programming session
🎤 "Start coding session on API design"
🤖 "Hey! I'm ready to help with your code. What are we working on?"

# Discuss architecture
🎤 "Should I use REST or GraphQL for this API?"
🤖 "Let's think through both options. REST is simpler for CRUD..."

# Review code
🎤 "Review app.py"
🤖 "Let me look at that... I see some good patterns here,
     but there are a few improvements we could make..."
```

---

### Example 4: Dictate to Claude

```bash
# Instead of typing
python -m agency.agents.voice.dictation.dictation_agent 15 claude

🎤 Record: "Hey Claude, I need help refactoring this function
            to make it more readable. Can you suggest improvements?"

✅ Transcription copied to clipboard
📋 Ready to paste into Claude chat!
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Required for all agents
OPENAI_API_KEY=sk-...              # Whisper STT + TTS
ANTHROPIC_API_KEY=sk-ant-...       # Claude AI

# Optional: Better TTS
ELEVENLABS_API_KEY=...

# Optional: Google integration (for Productivity & Ideas agents)
GOOGLE_OAUTH_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.pickle

# Optional: Ideas target
IDEAS_TARGET=google_docs  # or "apple_notes" or "local"
```

### Voice Customization

```python
# Change voice for TTS
agent.voice = "onyx"  # Options: alloy, echo, fable, onyx, nova, shimmer

# Change language for STT
agent.language = "es"  # Spanish
agent.language = "fr"  # French
```

---

## 🛠️ Advanced Usage

### Custom Wake Word (Future)

```python
# Activate on "Hey Assistant"
coordinator.enable_wake_word("hey assistant")

# Now just say "Hey Assistant, check my email"
```

### Voice Pipelines

```python
# Chain multiple agents
result = await coordinator.chain([
    ("productivity", "morning_briefing"),
    ("ideas", "review_recent_ideas"),
    ("copilot", "start_session")
])
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Voice Coordinator                        │
│         (Orchestrates all voice agents)                  │
└────────────────┬────────────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
    ┌────▼────┐    ┌────▼─────┐
    │ Voice   │    │  Voice   │
    │ Skills  │    │  Router  │
    └────┬────┘    └──────────┘
         │
    ┌────┴──────────────────────────────────┐
    │                                        │
┌───▼─────┐  ┌──────────┐  ┌───────────┐  ┌─────────┐
│Dictation│  │Productivity│ │   Ideas   │  │Developer│
│ Agent   │  │   Agent    │ │  Capture  │  │ Copilot │
└─────────┘  └────┬───────┘ └─────┬─────┘  └────┬────┘
                  │               │             │
             ┌────▼──────┐   ┌────▼────┐   ┌────▼─────┐
             │  Google   │   │ Google  │   │  Claude  │
             │ Services  │   │  Docs   │   │   API    │
             └───────────┘   └─────────┘   └──────────┘

Core Technologies:
- STT: OpenAI Whisper API
- TTS: OpenAI TTS / ElevenLabs
- AI: Claude Sonnet 4.5
- Audio: sounddevice, soundfile
```

---

## 🐛 Troubleshooting

### Audio Recording Issues

```bash
# Test microphone
python -c "import sounddevice as sd; print(sd.query_devices())"

# Check default device
python -c "import sounddevice as sd; print(sd.default.device)"
```

### API Errors

```bash
# Test OpenAI Whisper
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@audio.mp3" \
  -F model="whisper-1"

# Test Claude
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":100,"messages":[{"role":"user","content":"Hi"}]}'
```

### Google Integration

```bash
# Re-authenticate
rm google_token.pickle
python -m openclaw.integrations.google_services
```

---

## 📚 Documentation

- **[Voice Skills Reference](../../voice/voice_skills.py)** - Core voice capabilities
- **[Dictation Agent](./dictation/README.md)** - Complete guide
- **[Productivity Agent](./productivity/README.md)** - Complete guide
- **[Ideas Capture Agent](./ideas_capture/README.md)** - Complete guide
- **[Developer Copilot](./dev_copilot/README.md)** - Complete guide

---

## 🎯 Use Cases by Persona

### For Executives
- Morning briefings via voice
- Email and calendar management
- Voice-controlled scheduling
- Hands-free productivity

### For Developers
- Voice-based pair programming
- Code review conversations
- Architecture discussions
- Debug via voice

### For Creators
- Capture ideas on-the-go
- Voice journaling
- Brainstorming sessions
- Content ideation

### For Everyone
- Replace typing with voice
- Accessibility tool
- Multitask while working
- Natural language commands

---

## 💡 Tips & Best Practices

### Recording Quality
- Use a good microphone
- Minimize background noise
- Speak clearly and naturally
- Keep 6-12 inches from mic

### Voice Commands
- Be specific: "Schedule meeting with John tomorrow at 2pm"
- Use natural language: "What should I work on next?"
- Speak at normal pace
- Pause between commands

### Workflows
- Start with morning routine
- Use quick capture frequently
- Pair programming for complex code
- Dictate long messages to save time

---

## 🚀 Next Steps

1. **[Quick Start Guide](../../../examples/voice/README.md)** - Get started
2. **[Try Examples](../../../examples/voice/)** - Working demos
3. **[API Reference](../../voice/voice_skills.py)** - Technical docs
4. **[Customization Guide](#)** - Extend agents

---

**Work hands-free. Think out loud. Code with your voice.** 🎙️✨
