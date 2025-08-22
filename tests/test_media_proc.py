"""Тесты для модуля core.media_proc."""

from pathlib import Path
import sys
import os
import subprocess
from types import SimpleNamespace
import pytest

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.media_proc import MediaProcessor


def test_validate_rejects_unsupported_extension(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет отказ при неподдерживаемом расширении."""
    mp = MediaProcessor()
    # Защищаемся от случайных вызовов внешних команд.
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):
        mp.validate("/tmp/file.txt")


def test_validate_rejects_large_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет отказ при превышении размера файла."""
    mp = MediaProcessor()
    monkeypatch.setattr(os.path, "getsize", lambda _p: mp._MAX_SIZE + 1)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: SimpleNamespace(stdout="0"))
    with pytest.raises(ValueError):
        mp.validate("/tmp/file.mp3")


def test_validate_rejects_long_duration(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет отказ при превышении длительности файла."""
    mp = MediaProcessor()
    monkeypatch.setattr(os.path, "getsize", lambda _p: 1)
    monkeypatch.setattr(
        MediaProcessor, "_probe_duration", lambda self, _p: mp._MAX_DURATION + 1
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: SimpleNamespace(stdout="0"))
    with pytest.raises(ValueError):
        mp.validate("/tmp/file.mp3")


def test_extract_audio_creates_and_cleans(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет создание и удаление временного файла."""
    mp = MediaProcessor()
    created: list[str] = []

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        Path(cmd[-1]).write_bytes(b"0")
        created.append(cmd[-1])
        return SimpleNamespace()

    monkeypatch.setattr(subprocess, "run", fake_run)

    with mp.extract_audio("input.mp4") as tmp_path:
        assert Path(tmp_path).exists()
        assert tmp_path == created[0]

    assert not Path(created[0]).exists()
