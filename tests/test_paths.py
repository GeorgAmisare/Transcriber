"""Тесты для модуля utils.paths."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.paths import build_output_path


def test_build_output_path_appends_suffix() -> None:
    """Проверяет добавление суффикса _transcript.txt к имени файла."""
    src = "/tmp/audio.mp3"
    assert build_output_path(src) == "/tmp/audio_transcript.txt"

