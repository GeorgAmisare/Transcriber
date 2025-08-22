"""Модуль постобработки."""

from typing import List


def merge_results(text: List[str], speakers: List[str]) -> List[str]:
    """Объединяет транскрибацию и диаризацию.

    :param text: список строк текста.
    :param speakers: список спикеров.
    :return: список готовых строк.
    """
    return [f"{s}: {t}" for s, t in zip(speakers, text)]
