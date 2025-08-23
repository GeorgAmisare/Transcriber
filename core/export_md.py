"""Экспорт в формат Markdown."""

import logging
from typing import List


logger = logging.getLogger(__name__)


def export_md(lines: List[str], path: str) -> str:
    """Сохраняет строки в файл .md.

    :param lines: строки текста.
    :param path: путь к результирующему файлу.
    :return: путь к созданному файлу.
    """
    logger.info("Сохранение Markdown в %s", path)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return path
