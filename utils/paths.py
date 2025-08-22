"""Утилиты работы с путями."""

from pathlib import Path


def build_output_path(src: str) -> str:
    """Создаёт путь для результирующего файла.

    :param src: путь к исходному файлу.
    :return: путь к файлу с суффиксом _transcript.
    """
    return str(Path(src).with_suffix("_transcript.txt"))
