"""Настройка логирования в приложении."""

from __future__ import annotations

import logging
import sys
from typing import Callable, Optional


class GuiLogHandler(logging.Handler):
    """Передаёт сообщения логгера в GUI."""

    def __init__(self, callback: Callable[[str], None], level: int) -> None:
        super().__init__(level=level)
        self._callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        """Отправляет сообщение в callback."""
        msg = record.getMessage()
        self._callback(msg)


def setup_logging(
    level: int = logging.INFO,
    filename: Optional[str] = None,
    error_callback: Optional[Callable[[str], None]] = None,
    status_callback: Optional[Callable[[str], None]] = None,
) -> None:
    """Настраивает вывод логов в файл, консоль и GUI.

    :param level: уровень логирования.
    :param filename: путь к файлу логов.
    :param error_callback: функция для отображения ошибок в интерфейсе.
    :param status_callback: функция для отображения статусов в интерфейсе.
    """
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    root.addHandler(stream)

    if filename:
        file_handler = logging.FileHandler(filename, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    if status_callback:
        status_handler = GuiLogHandler(status_callback, level=logging.INFO)
        root.addHandler(status_handler)

    if error_callback:
        error_handler = GuiLogHandler(error_callback, level=logging.ERROR)
        root.addHandler(error_handler)
