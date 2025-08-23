"""Утилиты форматирования времени."""

import logging


logger = logging.getLogger(__name__)


def format_ts(seconds: float) -> str:
    """Форматирует секунды в строку HH:MM:SS.

    :param seconds: количество секунд.
    :return: форматированная строка.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    result = f"{hours:02d}:{minutes:02d}:{secs:02d}"
    logger.debug("Форматированное время %s", result)
    return result
