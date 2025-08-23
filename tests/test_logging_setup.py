"""Тесты для модуля utils.logging_setup."""

from pathlib import Path
import sys
import logging

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.logging_setup import setup_logging  # noqa: E402


def test_setup_logging_adds_handlers(tmp_path) -> None:
    """Проверяет добавление файлового и консольного обработчиков."""
    log_path = tmp_path / "app.log"
    setup_logging(filename=str(log_path))
    root = logging.getLogger()
    assert any(isinstance(h, logging.StreamHandler) for h in root.handlers)
    assert any(isinstance(h, logging.FileHandler) for h in root.handlers)


def test_gui_handler_receives_error(tmp_path) -> None:
    """Проверяет отправку сообщения в GUI колбэк при ошибке."""
    received: list[str] = []
    setup_logging(gui_callback=received.append)
    logger = logging.getLogger("test")
    logger.error("boom")
    assert received and "boom" in received[0]
