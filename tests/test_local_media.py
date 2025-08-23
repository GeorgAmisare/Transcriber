"""Проверяет локальные медиафайлы в каталоге tests/data."""

import os
from pathlib import Path

import pytest

from core.media_proc import MediaProcessor


def _collect_media() -> list[Path]:
    """Возвращает список поддерживаемых медиафайлов."""
    data_dir = Path(__file__).resolve().parent / "data"
    mp = MediaProcessor()
    return [
        p
        for p in data_dir.iterdir()
        if p.is_file() and p.suffix.lower() in mp._SUPPORTED_EXTENSIONS
    ]


@pytest.mark.skipif(bool(os.getenv("CI")), reason="Медиафайлы не хранятся в CI")
def test_all_local_media_files_valid() -> None:
    """Проверяет, что все локальные медиафайлы проходят валидацию."""
    files = _collect_media()
    if not files:
        pytest.fail(
            "В каталоге tests/data/ нет медиафайлов для тестов.",
            pytrace=False,
        )
    mp = MediaProcessor()
    for path in files:
        mp.validate(str(path))
