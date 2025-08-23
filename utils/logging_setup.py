"""Настройка логирования в приложении."""

from __future__ import annotations

import logging
import sys
from typing import Callable, Optional


class GuiLogHandler(logging.Handler):
    """Передаёт сообщения об ошибках в GUI."""

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__(level=logging.ERROR)
        self._callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        """Отправляет сообщение в callback."""
        msg = self.format(record)
        self._callback(msg)


def setup_logging(
    level: int = logging.INFO,
    filename: Optional[str] = None,
    gui_callback: Optional[Callable[[str], None]] = None,
) -> None:
    """Настраивает вывод логов в файл, консоль и GUI.

    :param level: уровень логирования.
    :param filename: путь к файлу логов.
    :param gui_callback: функция для отображения ошибок в интерфейсе.
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

    if gui_callback:
        gui_handler = GuiLogHandler(gui_callback)
        gui_handler.setFormatter(formatter)
        root.addHandler(gui_handler)
