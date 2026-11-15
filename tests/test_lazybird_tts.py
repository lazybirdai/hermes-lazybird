"""Request and output checks for the Lazybird TTS provider, no network."""

import httpx
import pytest

from lazybird_tts import DEFAULT_VOICE, LazybirdTTS


def fake_post(seen, status=200, content=b"ID3fake"):
    def post(url, **kwargs):
        seen.update(kwargs, url=url)
        return httpx.Response(status, content=content, request=httpx.Request("POST", url))
    return post


def test_synthesize_posts_v2_request(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setenv("LAZYBIRD_API_KEY", "lzb_test")
    monkeypatch.setattr(httpx, "post", fake_post(seen))

    out = LazybirdTTS().synthesize("hi", str(tmp_path / "a.mp3"), voice="v1", speed=1.2)

    assert out == str(tmp_path / "a.mp3")
    assert (tmp_path / "a.mp3").read_bytes() == b"ID3fake"
    assert seen["url"] == "https://api.lazybird.app/v2/generate-speech"
    assert seen["headers"] == {"X-API-Key": "lzb_test", "Accept": "audio/mpeg"}
    assert seen["json"] == {"voiceId": "v1", "text": "hi", "settings": {"speed": 1.2}}


def test_default_voice_and_mp3_for_other_formats(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setenv("LAZYBIRD_API_KEY", "lzb_test")
    monkeypatch.setattr(httpx, "post", fake_post(seen))

    out = LazybirdTTS().synthesize("hi", str(tmp_path / "a.ogg"), format="opus")

    assert out == str(tmp_path / "a.mp3")
    assert seen["json"] == {"voiceId": DEFAULT_VOICE, "text": "hi"}


def test_missing_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("LAZYBIRD_API_KEY", raising=False)
    assert not LazybirdTTS().is_available()
    with pytest.raises(RuntimeError, match="LAZYBIRD_API_KEY"):
        LazybirdTTS().synthesize("hi", str(tmp_path / "a.mp3"))


def test_api_error_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("LAZYBIRD_API_KEY", "lzb_test")
    monkeypatch.setattr(httpx, "post", fake_post({}, 402, b'{"error":"out of credits"}'))
    with pytest.raises(RuntimeError, match="402"):
        LazybirdTTS().synthesize("hi", str(tmp_path / "a.mp3"))
    assert not (tmp_path / "a.mp3").exists()
