"""Тесты для модуля core.postprocess."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.postprocess import merge_results


def test_merge_results_equal_lengths() -> None:
    """Проверяет объединение списков одинаковой длины."""
    text = ["Привет", "Пока"]
    speakers = ["Спикер 1", "Спикер 2"]
    assert merge_results(text, speakers) == [
        "Спикер 1: Привет",
        "Спикер 2: Пока",
    ]


def test_merge_results_ignores_extra_items() -> None:
    """Проверяет игнорирование лишних элементов при разной длине списков."""
    text = ["Раз", "Два", "Три"]
    speakers = ["Спикер 1", "Спикер 2"]
    assert merge_results(text, speakers) == [
        "Спикер 1: Раз",
        "Спикер 2: Два",
    ]

