# 🎙️ Voice Agent Examples

**Working examples demonstrating the complete voice agent system**

---

## 📁 Contents

1. **[e2e_voice_demo.py](./e2e_voice_demo.py)** - Complete E2E demonstration of all voice agents

---

## 🚀 E2E Voice Demo

### Overview

**File:** `e2e_voice_demo.py`

A comprehensive demonstration that showcases all 4 voice agents:
- **Dictation Agent** - Voice-to-text transcription
- **Productivity Agent** - Voice assistant for daily productivity
- **Ideas Capture Agent** - Voice-to-notes
- **Developer Copilot** - Voice-based code discussion

Plus the **Voice Coordinator** that orchestrates multi-agent workflows.

---

### Quick Start

```bash
# Set API keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

# Run the demo
python examples/voice/e2e_voice_demo.py
```

---

### What The Demo Shows

```
Demo 1: Core Voice Skills
  ✓ Text-to-Speech (TTS)
  ✓ Speech-to-Text (STT)

Demo 2: Dictation Agent
  ✓ Voice-to-text transcription
  ✓ Integration with chatbots

Demo 3: Productivity Voice Agent
  ✓ Morning briefings
  ✓ Voice commands

Demo 4: Ideas Capture Agent
  ✓ Quick idea capture
  ✓ Auto-categorization
  ✓ Save to Google Docs/Notes

Demo 5: Developer Co-pilot
  ✓ Code discussions with Claude
  ✓ Voice-based code review

Demo 6: Voice Coordinator
  ✓ Multi-agent workflows
  ✓ Unified voice interface
```

---

## 🎯 Try Each Agent

### Dictation Agent

```bash
# Dictate to Claude (10 seconds)
python -m agency.agents.voice.dictation.dictation_agent 10 claude

# Dictate to clipboard
python -m agency.agents.voice.dictation.dictation_agent 10 clipboard

# Dictate to any chatbot
python -m agency.agents.voice.dictation.dictation_agent 10 chatgpt
```

**What it does:**
- Records audio from your microphone
- Transcribes using OpenAI Whisper
- Formats for the target chatbot
- Copies to clipboard or sends directly

---

### Productivity Voice Agent

```bash
# Interactive mode
python -m agency.agents.voice.productivity.productivity_agent

# Options:
# 1 - Morning briefing (spoken out loud)
# 2 - Listen for voice command (5s)
# 3 - Continuous voice mode
```

**Voice commands you can try:**
- "Check my email"
- "What's on my calendar?"
- "Schedule meeting with John"
- "Block 2 hours of focus time"
- "What should I do next?"

---

### Ideas Capture Agent

```bash
# Interactive mode
python -m agency.agents.voice.ideas_capture.ideas_capture_agent

# Options:
# 1 - Quick capture (single idea)
# 2 - Batch capture (5 ideas)
# 3 - Set target (Google Docs / Apple Notes / Local)
```

**What it does:**
- Records your idea (30s max)
- Auto-categorizes using Claude AI
- Saves to your chosen target
- Organizes by category

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
# 5 - Save conversation
```

**What you can discuss:**
- Architecture decisions
- Code quality and patterns
- Debugging strategies
- Technical explanations
- Implementation approaches

---

### Voice Coordinator

```bash
# Interactive mode
python -m agency.agents.voice.voice_coordinator

# Workflows:
# 1 - Unified voice interface
# 2 - Morning routine workflow
```

**Multi-agent workflows:**
- Morning routine (briefing + email + calendar)
- Idea-to-implementation (capture + discuss + plan)
- Code review session (review + capture action items)

---

## 💻 Code Examples

### Basic TTS & STT

```python
from agency.voice.voice_skills import transcribe, speak

# Text-to-speech
audio_file = await speak("Hello! This is a test.")

# Speech-to-text
text = await transcribe("recording.mp3")
print(text)
```

---

### Dictation Agent

```python
from agency.agents.voice.dictation import DictationAgent

agent = DictationAgent()

# Dictate to Claude
result = await agent.dictate_to_claude("my_voice.mp3")
print(result["transcription"])  # Ready to send!

# Copy to clipboard
result = await agent.transcribe_and_copy_to_clipboard("my_voice.mp3")
print(f"Copied: {result['transcription']}")
```

---

### Productivity Agent

```python
from agency.agents.voice.productivity import ProductivityVoiceAgent

agent = ProductivityVoiceAgent()

# Morning briefing (spoken)
result = await agent.morning_briefing(speak_out_loud=True)

# Voice command
result = await agent.listen_for_command(duration=5)
print(f"You said: {result['command']}")
print(f"Action: {result['action']}")
```

---

### Ideas Capture

```python
from agency.agents.voice.ideas_capture import IdeasCaptureAgent

agent = IdeasCaptureAgent()

# Quick capture
result = await agent.quick_capture(duration=30)

print(f"Category: {result['category']}")
print(f"Saved to: {result['saved_to']}")
print(f"URL: {result.get('doc_url', 'N/A')}")
```

---

### Developer Copilot

```python
from agency.agents.voice.dev_copilot import DeveloperCopilotAgent

agent = DeveloperCopilotAgent()

# Start session
await agent.start_coding_session(topic="API design")

# Discuss code (records and responds via voice)
result = await agent.discuss_code("my_question.mp3")

# Code review
result = await agent.review_code("app.py")
# Review is spoken out loud!
```

---

### Voice Coordinator Workflows

```python
from agency.agents.voice.voice_coordinator import VoiceCoordinator

coordinator = VoiceCoordinator()

# Morning routine workflow
result = await coordinator.workflow_morning_routine()

# Idea-to-implementation
result = await coordinator.workflow_idea_to_implementation("idea.mp3")

# Code review session
result = await coordinator.workflow_code_review_session("app.py")
```

---

## 🔧 Configuration

### API Keys

```bash
# Required
export OPENAI_API_KEY=sk-...              # For Whisper STT & TTS
export ANTHROPIC_API_KEY=sk-ant-...       # For Claude AI

# Optional (better TTS)
export ELEVENLABS_API_KEY=...

# Optional (for productivity features)
export GOOGLE_OAUTH_CREDENTIALS_FILE=credentials.json
export GOOGLE_TOKEN_FILE=token.pickle
```

---

### Voice Preferences

```python
# Change TTS voice
agent.voice = "onyx"  # Options: alloy, echo, fable, onyx, nova, shimmer

# Change STT language
agent.language = "es"  # Spanish, French, etc.

# Set ideas target
agent.default_target = "google_docs"  # or "apple_notes" or "local"
```

---

## 🎬 Example Scenarios

### Scenario 1: Morning Routine

```bash
# Run morning routine workflow
python -m agency.agents.voice.voice_coordinator

> 2  # Select morning routine

🎤 "Good morning! Starting your morning routine."
🎤 "You have 5 unread emails, 3 are urgent..."
🎤 "You have 4 events on your calendar today..."
🎤 "I suggest blocking focus time before your first meeting. Should I do that?"

> Record: "Yes"

🎤 "I've blocked 2 hours on your calendar from 9 AM to 11 AM"
🎤 "Your morning routine is complete. Have a great day!"
```

---

### Scenario 2: Capture Idea While Driving

```bash
# Quick capture mode
python -m agency.agents.voice.ideas_capture.ideas_capture_agent

> 1  # Quick capture

🎤 Recording idea (30s max)...

> Record: "New feature idea for the app: add dark mode support with
           automatic switching based on time of day. Could use CSS
           variables for theming and local storage for preferences."

💾 Saving idea...
✅ Idea saved!
   Category: project
   Saved to: google_docs
   Idea: New feature idea for the app: add dark mode support...
```

---

### Scenario 3: Pair Programming

```bash
# Start pair programming
python -m agency.agents.voice.dev_copilot.dev_copilot_agent

> 4  # Pair programming mode

🎤 "Pair programming mode activated. I'm here to help!"

🎤 Listening...

> Record: "How should I handle authentication in this API?"

🤔 Thinking...

🎤 "Great question! For API authentication, I'd suggest using JWT tokens.
     Here's why: they're stateless, scalable, and work well with REST APIs.
     You'd typically implement it like this: generate a token on login,
     include it in the Authorization header, and verify it on each request.
     Want me to walk through the implementation?"
```

---

## 📊 Demo Output Example

```
======================================================================
  🎙️  E2E Voice Agent System Demo
======================================================================

  This demo showcases all 4 voice agents:
  1. Dictation Agent - Voice-to-text transcription
  2. Productivity Agent - Voice assistant for productivity
  3. Ideas Capture Agent - Voice-to-notes
  4. Developer Copilot - Voice-based code discussion
  5. Voice Coordinator - Multi-agent workflows

======================================================================

  Press Enter to start demo...

======================================================================
  DEMO 1: Core Voice Skills
======================================================================

▶ Step 1: Text-to-Speech (TTS)

  → Converting text to speech...
  ✓ Audio file created: /tmp/tts_a3f9e2b1.mp3
  ✓ Voice: alloy
  → Playing audio...

----------------------------------------------------------------------

▶ Step 2: Speech-to-Text (STT) - Using pre-recorded audio

  → Note: In a real demo, you would record live audio
  ✓ Transcription: This is a simulated transcription of audio input.

[... continues through all demos ...]

======================================================================
  DEMO COMPLETE
======================================================================

✅ Demonstrated all voice agents:
   • Core voice skills (TTS, STT)
   • Dictation Agent
   • Productivity Voice Agent
   • Ideas Capture Agent
   • Developer Co-pilot Agent
   • Voice Coordinator

📚 Next steps:
   1. Try each agent individually
   2. Set up Google integration for full features
   3. Configure voice preferences
   4. Build custom workflows

======================================================================
  🎙️  Happy voice-coding!
======================================================================
```

---

## 🐛 Troubleshooting

### No audio output

```bash
# Check speakers/headphones
python -c "import sounddevice as sd; sd.play(sd.rec(44100, samplerate=44100), 44100); sd.wait()"
```

### Microphone not working

```bash
# List audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test recording
python -c "import sounddevice as sd; import soundfile as sf; sd.rec(44100, samplerate=44100, channels=1)"
```

### API errors

```bash
# Test OpenAI API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Claude API
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":100,"messages":[{"role":"user","content":"Hi"}]}'
```

---

## 📚 Learn More

- **[Voice Agents Guide](../../agency/agents/voice/README.md)** - Complete documentation
- **[Voice Skills Reference](../../agency/voice/voice_skills.py)** - Technical reference
- **[Main README](../../README.md)** - Project overview

---

**Work hands-free. Think out loud. Code with your voice.** 🎙️✨
