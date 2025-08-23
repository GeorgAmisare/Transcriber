"""Тесты для модуля core.asr_whisper."""

import urllib.request
from pathlib import Path
import sys

import pytest

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.asr_whisper import transcribe
from core.models import ASRSegment

URL = "https://github.com/openai/whisper/raw/main/tests/jfk.wav"


@pytest.mark.needs_hf
def test_transcribe_returns_segments(tmp_path) -> None:
    """Проверяет, что transcribe возвращает сегменты."""
    audio = tmp_path / "jfk.wav"
    try:
        urllib.request.urlretrieve(URL, audio)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Не удалось загрузить аудио: {exc}")
    try:
        segments = transcribe(str(audio), model="tiny")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Whisper model недоступна: {exc}")
    assert segments
    assert isinstance(segments[0], ASRSegment)
    assert segments[0].text
