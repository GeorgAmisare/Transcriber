"""Тесты для модуля postprocess."""

from core.postprocess import merge_results


def test_merge_results_combines_text_and_speakers() -> None:
    """Проверяет объединение текста и спикеров."""
    text = ["фраза"]
    speakers = ["Спикер 1"]
    result = merge_results(text, speakers)
    assert result[0] == "Спикер 1: фраза"
