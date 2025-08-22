"""Настройка логгирования."""

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO, filename: Optional[str] = None) -> None:
    """Настраивает логирование.

    :param level: уровень логгирования.
    :param filename: файл для записи логов.
    """
    logging.basicConfig(level=level, filename=filename)
