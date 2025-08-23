"""Тесты для модуля core.diarization."""

from pathlib import Path
import sys

import pytest

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.diarization import diarize


@pytest.mark.needs_hf
def test_diarize_returns_speakers() -> None:
    """Проверяет, что diarize возвращает идентификаторы спикеров."""
    result = diarize("sample.wav")
    assert result == ["Спикер 1", "Спикер 2"]
