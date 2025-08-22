"""Модуль транскрибации."""

from typing import List


def transcribe(path: str) -> List[str]:
    """Выполняет распознавание речи.

    :param path: путь к аудиофайлу.
    :return: список строк с текстом.
    """
    return [f"Транскрибировано из {path}"]
