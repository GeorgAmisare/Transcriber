"""Тесты для модулей core.asr_whisper и core.diarization."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.asr_whisper import transcribe
from core.diarization import diarize


def test_transcribe_returns_text() -> None:
    """Проверяет, что transcribe возвращает список строк."""
    result = transcribe("sample.wav")
    assert result == ["Транскрибировано из sample.wav"]


def test_diarize_returns_speakers() -> None:
    """Проверяет, что diarize возвращает идентификаторы спикеров."""
    result = diarize("sample.wav")
    assert result == ["Спикер 1", "Спикер 2"]

