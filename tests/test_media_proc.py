"""Тесты для модуля media_proc."""

from core.media_proc import MediaProcessor


def test_extract_audio_returns_wav_path() -> None:
    """Проверяет генерацию пути аудиофайла."""
    processor = MediaProcessor()
    result = processor.extract_audio("video.mp4")
    assert result.endswith(".wav")
