"""Тесты для модуля utils.timing."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.timing import format_ts


def test_format_ts_basic() -> None:
    """Проверяет базовое форматирование временной метки."""
    assert format_ts(3661) == "01:01:01"
