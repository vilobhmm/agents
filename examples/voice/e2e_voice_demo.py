#!/usr/bin/env python3
"""
E2E Voice Agent Demo
====================

Complete demonstration of all voice agents working together.

Run:
    OPENAI_API_KEY=sk-... ANTHROPIC_API_KEY=sk-ant-... python examples/voice/e2e_voice_demo.py

Requirements:
    - OpenAI API key (for Whisper STT and TTS)
    - Anthropic API key (for Claude AI)
    - Microphone for audio input
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrations.voice_core.voice_skills import VoiceSkills
from agents.voice.dictation.dictation_agent import DictationAgent
from agents.voice.productivity.productivity_agent import ProductivityVoiceAgent
from agents.voice.ideas_capture.ideas_capture_agent import IdeasCaptureAgent
from agents.voice.dev_copilot.dev_copilot_agent import DeveloperCopilotAgent
from agents.voice.voice_coordinator import VoiceCoordinator


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_step(step_num, description):
    """Print step description."""
    print(f"\n▶ Step {step_num}: {description}\n")


def print_result(label, value):
    """Print result."""
    print(f"  ✓ {label}: {value}")


async def demo_voice_skills():
    """Demo 1: Core voice skills."""
    print_header("DEMO 1: Core Voice Skills")

    skills = VoiceSkills()

    print_step(1, "Text-to-Speech (TTS)")
    print("  → Converting text to speech...")

    text = "Hello! This is a test of the text-to-speech system. I'm using OpenAI's TTS API."
    result = await skills.synthesize_speech(text, voice="alloy")

    if "audio_file" in result:
        print_result("Audio file created", result["audio_file"])
        print_result("Voice", result["voice"])
        print("  → Playing audio...")
        await skills.stream_audio(result["audio_file"])
    else:
        print(f"  ✗ Error: {result.get('error', 'Unknown error')}")

    print("\n" + "-" * 70)

    print_step(2, "Speech-to-Text (STT) - Using pre-recorded audio")
    print("  → Note: In a real demo, you would record live audio")
    print("  → For now, we'll simulate transcription")

    # Simulated transcription
    simulated_text = "This is a simulated transcription of audio input."
    print_result("Transcription", simulated_text)


async def demo_dictation_agent():
    """Demo 2: Dictation Agent."""
    print_header("DEMO 2: Dictation Agent")

    agent = DictationAgent()

    print_step(1, "Dictation to Clipboard (Simulated)")
    print("  → In a real scenario, you would:")
    print("     1. Record audio via microphone")
    print("     2. Transcribe to text")
    print("     3. Copy to clipboard")
    print("     4. Paste into any application")

    simulated_dictation = "Hey Claude, can you help me refactor this function to be more readable?"
    print_result("Dictated text", simulated_dictation)
    print_result("Target", "Claude AI chat")
    print_result("Status", "Ready to paste!")

    print("\n  💡 Real usage:")
    print("     python -m agency.agents.voice.dictation.dictation_agent 10 claude")


async def demo_productivity_agent():
    """Demo 3: Productivity Voice Agent."""
    print_header("DEMO 3: Productivity Voice Agent")

    agent = ProductivityVoiceAgent()

    print_step(1, "Morning Briefing")
    print("  → Generating morning briefing...")

    # Generate briefing data (without speaking to avoid audio in demo)
    briefing_data = await agent._gather_briefing_data()
    briefing_text = await agent._generate_briefing_text(briefing_data)

    print(f"\n{briefing_text}\n")

    print_step(2, "Voice Commands (Examples)")
    print("  Available voice commands:")
    print("  • 'Check my email' - Get email summary")
    print("  • 'What's on my calendar?' - View today's events")
    print("  • 'Schedule meeting with John' - Schedule meetings")
    print("  • 'Block focus time' - Block calendar for deep work")

    print("\n  💡 Real usage:")
    print("     python -m agency.agents.voice.productivity.productivity_agent")


async def demo_ideas_capture_agent():
    """Demo 4: Ideas Capture Agent."""
    print_header("DEMO 4: Ideas Capture Agent")

    agent = IdeasCaptureAgent()

    print_step(1, "Quick Idea Capture (Simulated)")
    print("  → In a real scenario, you would:")
    print("     1. Record your idea via voice")
    print("     2. Auto-categorize using Claude AI")
    print("     3. Save to Google Docs, Apple Notes, or local file")

    simulated_idea = "New feature idea: add real-time collaboration to the code editor, similar to Google Docs but for code. Could use WebSockets for live updates."

    # Simulate categorization
    category = await agent._auto_categorize_idea(simulated_idea)

    print_result("Idea", simulated_idea[:80] + "...")
    print_result("Auto-category", category)
    print_result("Saved to", agent.default_target)

    # Save to local file
    from datetime import datetime
    save_result = await agent._save_to_local_file(simulated_idea, category, datetime.now())

    print_result("File path", save_result.get("file_path", "N/A"))

    print("\n  💡 Real usage:")
    print("     python -m agency.agents.voice.ideas_capture.ideas_capture_agent")


async def demo_dev_copilot_agent():
    """Demo 5: Developer Co-pilot Agent."""
    print_header("DEMO 5: Developer Co-pilot Agent")

    agent = DeveloperCopilotAgent()

    print_step(1, "Code Discussion with Claude")
    print("  → Simulating voice-based code discussion...")

    question = "How should I structure a REST API for a multi-tenant SaaS application?"

    print(f"  You: {question}")
    print("  → Claude is thinking...")

    # Get response from Claude
    response = await agent._get_claude_response(question)

    print(f"\n  Copilot: {response}\n")

    print_step(2, "Voice-Based Code Review (Example)")
    print("  → In a real scenario, you would:")
    print("     1. Say: 'Review app.py'")
    print("     2. Agent reads and analyzes the code")
    print("     3. Agent speaks the review out loud")
    print("     4. Conversation continues about improvements")

    print("\n  💡 Real usage:")
    print("     python -m agency.agents.voice.dev_copilot.dev_copilot_agent")


async def demo_voice_coordinator():
    """Demo 6: Voice Coordinator."""
    print_header("DEMO 6: Voice Coordinator - Multi-Agent Workflows")

    coordinator = VoiceCoordinator()

    print_step(1, "Morning Routine Workflow")
    print("  The morning routine workflow combines multiple agents:")
    print("  1. Productivity Agent - Morning briefing")
    print("  2. Productivity Agent - Check urgent emails")
    print("  3. Productivity Agent - Review calendar")
    print("  4. Productivity Agent - Block focus time")

    print("\n  💡 Real usage:")
    print("     python -m agency.agents.voice.voice_coordinator")
    print("     Then select: 2 - Morning routine")

    print_step(2, "Idea-to-Implementation Workflow")
    print("  This workflow combines:")
    print("  1. Ideas Capture Agent - Capture the idea")
    print("  2. Developer Copilot - Discuss implementation")
    print("  3. Ideas Capture Agent - Save action items")

    print_step(3, "Unified Voice Interface")
    print("  The coordinator provides a single voice interface:")
    print("  • Say 'dictate to Claude' - Routes to Dictation Agent")
    print("  • Say 'check email' - Routes to Productivity Agent")
    print("  • Say 'capture idea' - Routes to Ideas Capture Agent")
    print("  • Say 'discuss code' - Routes to Developer Copilot")


async def main():
    """Run complete E2E demo."""
    print("\n" + "=" * 70)
    print("  🎙️  E2E Voice Agent System Demo")
    print("=" * 70)

    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set. TTS/STT features will be limited.")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set. Claude AI features will be limited.")

    print("\n  This demo showcases all 4 voice agents:")
    print("  1. Dictation Agent - Voice-to-text transcription")
    print("  2. Productivity Agent - Voice assistant for productivity")
    print("  3. Ideas Capture Agent - Voice-to-notes")
    print("  4. Developer Copilot - Voice-based code discussion")
    print("  5. Voice Coordinator - Multi-agent workflows")
    print("\n" + "=" * 70)

    input("\n  Press Enter to start demo...")

    # Run demos
    await demo_voice_skills()

    input("\n  Press Enter to continue...")
    await demo_dictation_agent()

    input("\n  Press Enter to continue...")
    await demo_productivity_agent()

    input("\n  Press Enter to continue...")
    await demo_ideas_capture_agent()

    input("\n  Press Enter to continue...")
    await demo_dev_copilot_agent()

    input("\n  Press Enter to continue...")
    await demo_voice_coordinator()

    # Summary
    print_header("DEMO COMPLETE")

    print("✅ Demonstrated all voice agents:")
    print("   • Core voice skills (TTS, STT)")
    print("   • Dictation Agent")
    print("   • Productivity Voice Agent")
    print("   • Ideas Capture Agent")
    print("   • Developer Co-pilot Agent")
    print("   • Voice Coordinator")

    print("\n📚 Next steps:")
    print("   1. Try each agent individually (see commands above)")
    print("   2. Set up Google integration for full productivity features")
    print("   3. Configure voice preferences (voice, language)")
    print("   4. Build custom workflows with the coordinator")

    print("\n📖 Documentation:")
    print("   • Voice Agents Guide: agency/agents/voice/README.md")
    print("   • Voice Skills Reference: agency/voice/voice_skills.py")

    print("\n" + "=" * 70)
    print("  🎙️  Happy voice-coding!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
