"""Тесты для модуля media_proc."""

import os

import pytest

from core.media_proc import MediaProcessor


def test_extract_audio_returns_wav_path() -> None:
    """Проверяет генерацию пути аудиофайла."""
    processor = MediaProcessor()
    result = processor.extract_audio("video.mp4")
    assert result.endswith(".wav")


def test_validate_accepts_valid_file(tmp_path, monkeypatch) -> None:
    """Не выбрасывает ошибку для корректного файла."""
    media_file = tmp_path / "audio.mp3"
    media_file.write_bytes(b"0")
    processor = MediaProcessor()
    monkeypatch.setattr(os.path, "getsize", lambda _: 1024)
    monkeypatch.setattr(processor, "_probe_duration", lambda _: 60.0)
    processor.validate(str(media_file))


def test_validate_rejects_format(tmp_path) -> None:
    """Выбрасывает исключение при неверном формате."""
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("x")
    processor = MediaProcessor()
    with pytest.raises(ValueError, match="формат"):
        processor.validate(str(bad_file))


def test_validate_rejects_size(tmp_path, monkeypatch) -> None:
    """Выбрасывает исключение при превышении размера."""
    media_file = tmp_path / "audio.mp3"
    media_file.write_bytes(b"0")
    processor = MediaProcessor()
    monkeypatch.setattr(os.path, "getsize", lambda _: 3 * 1024**3)
    monkeypatch.setattr(processor, "_probe_duration", lambda _: 60.0)
    with pytest.raises(ValueError, match="Размер"):
        processor.validate(str(media_file))


def test_validate_rejects_duration(tmp_path, monkeypatch) -> None:
    """Выбрасывает исключение при превышении длительности."""
    media_file = tmp_path / "audio.mp3"
    media_file.write_bytes(b"0")
    processor = MediaProcessor()
    monkeypatch.setattr(os.path, "getsize", lambda _: 1024)
    monkeypatch.setattr(processor, "_probe_duration", lambda _: 6000.0)
    with pytest.raises(ValueError, match="Длительность"):
        processor.validate(str(media_file))
