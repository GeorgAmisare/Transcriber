"""Тесты для модуля export_txt."""

import os
import tempfile

from core.export_txt import export_txt


def test_export_txt_creates_file() -> None:
    """Проверяет создание текстового файла."""
    lines = ["пример"]
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    try:
        result = export_txt(lines, path)
        assert os.path.exists(result)
    finally:
        os.remove(path)
