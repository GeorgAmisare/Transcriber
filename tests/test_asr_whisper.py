"""Тесты для модуля asr_whisper."""

from core.asr_whisper import transcribe


def test_transcribe_returns_text() -> None:
    """Проверяет возврат текста."""
    result = transcribe("audio.wav")
    assert "audio.wav" in result[0]
