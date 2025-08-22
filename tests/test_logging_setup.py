"""Тесты для модуля utils.logging_setup."""

from pathlib import Path
import sys
import logging
from unittest.mock import MagicMock

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.logging_setup import setup_logging


def test_setup_logging_default_level(monkeypatch) -> None:
    """Проверяет использование уровня INFO по умолчанию."""
    mock_basic = MagicMock()
    monkeypatch.setattr(logging, "basicConfig", mock_basic)
    setup_logging()
    mock_basic.assert_called_once_with(level=logging.INFO, filename=None)


def test_setup_logging_with_filename(monkeypatch) -> None:
    """Проверяет передачу имени файла в basicConfig."""
    mock_basic = MagicMock()
    monkeypatch.setattr(logging, "basicConfig", mock_basic)
    setup_logging(filename="app.log")
    mock_basic.assert_called_once_with(level=logging.INFO, filename="app.log")
