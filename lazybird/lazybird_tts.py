"""Lazybird text-to-speech (https://www.lazybird.app) as a Hermes TTS provider.

``POST https://api.lazybird.app/v2/generate-speech`` with the key in ``X-API-Key`` and
``{voiceId, text, settings}`` in the body answers with MP3 bytes. API reference:
https://www.lazybird.app/docs/api-reference
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import httpx

from agent.secret_scope import get_secret
from agent.tts_provider import TTSProvider

API_URL = "https://api.lazybird.app/v2/generate-speech"
DEFAULT_VOICE = "tgJ2Hes6DauwTg8kFrRPLN"  # Elyssia, an official Lazybird voice
TIMEOUT_SECONDS = 300.0


class LazybirdTTS(TTSProvider):
    """Lazybird voices; ``tts.voice`` is a voice id from https://www.lazybird.app/voices or your own clone."""

    @property
    def name(self) -> str:
        return "lazybird"

    @property
    def display_name(self) -> str:
        return "Lazybird"

    @property
    def voice_compatible(self) -> bool:
        # MP3 out; the gateway converts it to Opus for voice bubbles
        return True

    def is_available(self) -> bool:
        return bool(get_secret("LAZYBIRD_API_KEY"))

    def default_voice(self) -> Optional[str]:
        return DEFAULT_VOICE

    def get_setup_schema(self) -> dict[str, Any]:
        return {
            "name": "Lazybird",
            "badge": "",
            "tag": "tts",
            "env_vars": [{
                "key": "LAZYBIRD_API_KEY",
                "prompt": "Lazybird API key",
                "url": "https://www.lazybird.app/platform",
            }],
        }

    def synthesize(
        self, text: str, output_path: str, *, voice: Optional[str] = None,
        model: Optional[str] = None, speed: Optional[float] = None,
        format: str = "mp3", **extra: Any,
    ) -> str:
        key = get_secret("LAZYBIRD_API_KEY")
        if not key:
            raise RuntimeError("LAZYBIRD_API_KEY is not set; create a key at https://www.lazybird.app/platform")
        payload: dict[str, Any] = {"voiceId": voice or DEFAULT_VOICE, "text": text}
        if speed is not None:
            payload["settings"] = {"speed": speed}
        response = httpx.post(
            API_URL,
            json=payload,
            headers={"X-API-Key": key, "Accept": "audio/mpeg"},
            timeout=TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"Lazybird TTS failed ({response.status_code}): {response.text[:300]}")
        # the API returns MP3 only; any other requested format gets the closest one
        path = Path(output_path).with_suffix(".mp3")
        path.write_bytes(response.content)
        return str(path)
