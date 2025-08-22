"""Тесты для модулей export_srt и export_md."""

import os
import tempfile

from core.export_md import export_md
from core.export_srt import export_srt


def _check_export(func, suffix: str) -> None:
    lines = ["пример"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        path = tmp.name
    try:
        result = func(lines, path)
        assert os.path.exists(result)
    finally:
        os.remove(path)


def test_export_srt_creates_file() -> None:
    """Проверяет создание SRT-файла."""
    _check_export(export_srt, ".srt")


def test_export_md_creates_file() -> None:
    """Проверяет создание MD-файла."""
    _check_export(export_md, ".md")
