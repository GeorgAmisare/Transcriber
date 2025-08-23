"""Тесты для модуля core.postprocess."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.postprocess import merge, merge_results
from core.models import ASRSegment, DiarSegment, Utterance
from utils.timing import format_ts


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


def test_merge_assigns_speaker_by_longest_overlap() -> None:
    """Выбирает спикера с наибольшим пересечением интервалов."""
    asr = [ASRSegment(start=0.0, end=10.0, text="фраза")]
    diar = [
        DiarSegment(start=0.0, end=4.0, speaker="A"),
        DiarSegment(start=4.0, end=10.0, speaker="B"),
    ]

    result = merge(asr, diar)
    assert result == [
        Utterance(
            timespan=f"[{format_ts(0.0)} — {format_ts(10.0)}]",
            speaker="B",
            text="фраза",
            words=["фраза"],
        )
    ]


def test_merge_prefers_first_on_equal_overlap() -> None:
    """При равном пересечении выбирается первый по времени спикер."""
    asr = [ASRSegment(start=2.0, end=8.0, text="текст")]
    diar = [
        DiarSegment(start=0.0, end=5.0, speaker="X"),
        DiarSegment(start=5.0, end=10.0, speaker="Y"),
    ]

    result = merge(asr, diar)
    assert result[0].speaker == "X"
