"""Тесты для модуля diarization."""

from core.diarization import diarize


def test_diarize_returns_speakers() -> None:
    """Проверяет возврат списка спикеров."""
    result = diarize("audio.wav")
    assert "Спикер 1" in result
