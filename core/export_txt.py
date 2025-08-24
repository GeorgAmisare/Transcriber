"""Экспорт в текстовый файл."""

import logging
from pathlib import Path
from typing import List

from .models import Utterance
from utils.paths import build_output_path


logger = logging.getLogger(__name__)


def export_txt(lines: List[str], path: str) -> str:
    """Сохраняет строки в файл .txt.

    :param lines: строки для сохранения.
    :param path: путь к результирующему файлу.
    :return: путь к созданному файлу.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Сохранение текста в %s", output_path)

    with output_path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines))
        file.flush()

    return str(output_path)


def save_txt(utterances: List[Utterance], base_path: str) -> str:
    """Формирует строки и сохраняет реплики в файл .txt.

    :param utterances: список готовых реплик.
    :param base_path: путь к исходному файлу, на основе которого создаётся
        имя результирующего файла.
    :return: путь к созданному файлу.
    """
    lines = [f"{u.timespan} {u.speaker}: {u.text}" for u in utterances]
    path = build_output_path(base_path)
    return export_txt(lines, path)
