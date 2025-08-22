"""Экспорт в текстовый файл."""

from typing import List


def export_txt(lines: List[str], path: str) -> str:
    """Сохраняет строки в файл .txt.

    :param lines: строки для сохранения.
    :param path: путь к результирующему файлу.
    :return: путь к созданному файлу.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return path
