"""Экспорт в формат SRT."""

import logging
from typing import List


logger = logging.getLogger(__name__)


def export_srt(lines: List[str], path: str) -> str:
    """Сохраняет строки в файл .srt.

    :param lines: строки субтитров.
    :param path: путь к результирующему файлу.
    :return: путь к созданному файлу.
    """
    logger.info("Сохранение SRT в %s", path)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return path
