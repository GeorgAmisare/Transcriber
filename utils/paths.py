"""Утилиты работы с путями."""

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def build_output_path(src: str) -> str:
    """Создаёт путь для результирующего файла.

    :param src: путь к исходному файлу.
    :return: путь к файлу с суффиксом _transcript.
    """
    path = Path(src)
    result = path.with_name(f"{path.stem}_transcript.txt")
    logger.debug("Итоговый путь %s", result)
    return str(result)
