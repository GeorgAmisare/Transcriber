"""Экспорт в формат Markdown."""

from typing import List


def export_md(lines: List[str], path: str) -> str:
    """Сохраняет строки в файл .md.

    :param lines: строки текста.
    :param path: путь к результирующему файлу.
    :return: путь к созданному файлу.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return path
