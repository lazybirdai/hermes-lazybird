"""Lazybird TTS provider for Hermes: `tts.provider: lazybird`."""

from .lazybird_tts import LazybirdTTS


def register(ctx):
    ctx.register_tts_provider(LazybirdTTS())
