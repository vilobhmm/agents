"""
Core Voice Skills - Speech-to-Text, Text-to-Speech, Audio Processing

Provides foundational voice capabilities for all voice agents.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List, BinaryIO
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class VoiceSkills:
    """Core voice capabilities using multiple providers."""

    def __init__(self):
        """Initialize voice skills with available providers."""
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

        # Check available providers
        self.stt_provider = self._detect_stt_provider()
        self.tts_provider = self._detect_tts_provider()

        logger.info(f"Voice skills initialized: STT={self.stt_provider}, TTS={self.tts_provider}")

    def _detect_stt_provider(self) -> str:
        """Detect available speech-to-text provider."""
        if self.openai_api_key:
            return "openai_whisper"
        elif self.anthropic_api_key:
            return "anthropic"
        return "none"

    def _detect_tts_provider(self) -> str:
        """Detect available text-to-speech provider."""
        if self.elevenlabs_api_key:
            return "elevenlabs"
        elif self.openai_api_key:
            return "openai_tts"
        return "none"

    async def transcribe_audio(
        self,
        audio_file: str,
        language: str = "en",
        prompt: Optional[str] = None
    ) -> Dict:
        """
        Transcribe audio file to text.

        Args:
            audio_file: Path to audio file (mp3, wav, m4a, etc.)
            language: Language code (default: en)
            prompt: Optional prompt to guide transcription

        Returns:
            {
                "text": "transcribed text",
                "language": "en",
                "duration": 12.5,
                "confidence": 0.98
            }
        """
        if self.stt_provider == "openai_whisper":
            return await self._transcribe_openai_whisper(audio_file, language, prompt)
        elif self.stt_provider == "anthropic":
            return await self._transcribe_anthropic(audio_file, language, prompt)
        else:
            logger.error("No STT provider available")
            return {"error": "No STT provider configured"}

    async def _transcribe_openai_whisper(
        self,
        audio_file: str,
        language: str,
        prompt: Optional[str]
    ) -> Dict:
        """Transcribe using OpenAI Whisper API."""
        try:
            import openai

            client = openai.OpenAI(api_key=self.openai_api_key)

            with open(audio_file, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language=language,
                    prompt=prompt,
                    response_format="verbose_json"
                )

            return {
                "text": transcript.text,
                "language": transcript.language or language,
                "duration": transcript.duration,
                "confidence": 0.95,  # Whisper doesn't provide confidence
                "provider": "openai_whisper"
            }
        except Exception as e:
            logger.error(f"OpenAI Whisper transcription failed: {e}")
            return {"error": str(e)}

    async def _transcribe_anthropic(
        self,
        audio_file: str,
        language: str,
        prompt: Optional[str]
    ) -> Dict:
        """Transcribe using Anthropic (placeholder for future support)."""
        logger.warning("Anthropic audio transcription not yet available")
        return {"error": "Anthropic STT not yet available"}

    async def synthesize_speech(
        self,
        text: str,
        voice: str = "alloy",
        speed: float = 1.0,
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Convert text to speech.

        Args:
            text: Text to synthesize
            voice: Voice ID or name
            speed: Speech speed (0.25 to 4.0)
            output_file: Optional path to save audio file

        Returns:
            {
                "audio_file": "path/to/audio.mp3",
                "duration": 5.2,
                "voice": "alloy",
                "provider": "openai_tts"
            }
        """
        if self.tts_provider == "openai_tts":
            return await self._synthesize_openai_tts(text, voice, speed, output_file)
        elif self.tts_provider == "elevenlabs":
            return await self._synthesize_elevenlabs(text, voice, speed, output_file)
        else:
            logger.error("No TTS provider available")
            return {"error": "No TTS provider configured"}

    async def _synthesize_openai_tts(
        self,
        text: str,
        voice: str,
        speed: float,
        output_file: Optional[str]
    ) -> Dict:
        """Synthesize using OpenAI TTS."""
        try:
            import openai

            client = openai.OpenAI(api_key=self.openai_api_key)

            # Generate speech
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=speed
            )

            # Save to file
            if not output_file:
                output_file = f"/tmp/tts_{os.urandom(8).hex()}.mp3"

            response.stream_to_file(output_file)

            return {
                "audio_file": output_file,
                "duration": len(text) / 150 * speed,  # Approximate
                "voice": voice,
                "provider": "openai_tts"
            }
        except Exception as e:
            logger.error(f"OpenAI TTS failed: {e}")
            return {"error": str(e)}

    async def _synthesize_elevenlabs(
        self,
        text: str,
        voice: str,
        speed: float,
        output_file: Optional[str]
    ) -> Dict:
        """Synthesize using ElevenLabs."""
        try:
            import requests

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "speed": speed
                }
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            if not output_file:
                output_file = f"/tmp/tts_{os.urandom(8).hex()}.mp3"

            with open(output_file, "wb") as f:
                f.write(response.content)

            return {
                "audio_file": output_file,
                "duration": len(text) / 150 * speed,
                "voice": voice,
                "provider": "elevenlabs"
            }
        except Exception as e:
            logger.error(f"ElevenLabs TTS failed: {e}")
            return {"error": str(e)}

    async def detect_speech_activity(self, audio_file: str) -> Dict:
        """
        Detect speech activity in audio file.

        Returns:
            {
                "has_speech": true,
                "speech_segments": [
                    {"start": 0.5, "end": 5.2},
                    {"start": 6.0, "end": 10.3}
                ],
                "total_speech_duration": 9.0
            }
        """
        # Placeholder - would use VAD (Voice Activity Detection)
        logger.info(f"Detecting speech in {audio_file}")
        return {
            "has_speech": True,
            "speech_segments": [{"start": 0.0, "end": 10.0}],
            "total_speech_duration": 10.0
        }

    async def record_audio(
        self,
        duration: Optional[int] = None,
        stop_on_silence: bool = True,
        output_file: Optional[str] = None
    ) -> str:
        """
        Record audio from microphone.

        Args:
            duration: Max recording duration in seconds (None = until silence)
            stop_on_silence: Stop recording on silence detection
            output_file: Path to save recording

        Returns:
            Path to recorded audio file
        """
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np

            sample_rate = 16000

            logger.info(f"Recording audio (duration={duration}, stop_on_silence={stop_on_silence})")

            if duration:
                # Fixed duration recording
                recording = sd.rec(
                    int(duration * sample_rate),
                    samplerate=sample_rate,
                    channels=1,
                    dtype='float32'
                )
                sd.wait()
            else:
                # Record until silence (simplified)
                logger.warning("Continuous recording not fully implemented, using 10s default")
                recording = sd.rec(
                    int(10 * sample_rate),
                    samplerate=sample_rate,
                    channels=1,
                    dtype='float32'
                )
                sd.wait()

            if not output_file:
                output_file = f"/tmp/recording_{os.urandom(8).hex()}.wav"

            sf.write(output_file, recording, sample_rate)
            logger.info(f"Recording saved to {output_file}")

            return output_file
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            raise

    async def stream_audio(self, audio_file: str) -> None:
        """Stream audio file for playback."""
        try:
            import sounddevice as sd
            import soundfile as sf

            data, sample_rate = sf.read(audio_file)
            sd.play(data, sample_rate)
            sd.wait()
        except Exception as e:
            logger.error(f"Audio playback failed: {e}")
            raise


# Convenience functions for common operations
async def transcribe(audio_file: str, language: str = "en") -> str:
    """Quick transcribe helper."""
    skills = VoiceSkills()
    result = await skills.transcribe_audio(audio_file, language)
    return result.get("text", "")


async def speak(text: str, voice: str = "alloy") -> str:
    """Quick text-to-speech helper."""
    skills = VoiceSkills()
    result = await skills.synthesize_speech(text, voice)
    return result.get("audio_file", "")


async def record_and_transcribe(duration: int = 10) -> str:
    """Record audio and transcribe it."""
    skills = VoiceSkills()
    audio_file = await skills.record_audio(duration=duration)
    result = await skills.transcribe_audio(audio_file)
    return result.get("text", "")
