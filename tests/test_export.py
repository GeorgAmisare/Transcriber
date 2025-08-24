"""Тесты для модуля core.export_txt."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.export_txt import export_txt, save_txt
from core.models import Utterance


def test_export_txt_writes_file(tmp_path) -> None:
    """Проверяет запись строк в файл .txt."""
    lines = ["первая", "вторая"]
    path = tmp_path / "out.txt"
    export_txt(lines, str(path))
    assert path.read_text(encoding="utf-8") == "\n".join(lines)


def test_export_txt_creates_parent_dirs(tmp_path) -> None:
    """Создаёт недостающие директории перед записью."""
    lines = ["строка"]
    path = tmp_path / "nested" / "out.txt"
    export_txt(lines, str(path))
    assert path.read_text(encoding="utf-8") == "\n".join(lines)


def test_save_txt_formats_times_and_utf8(tmp_path) -> None:
    """Проверяет форматирование таймкодов и кодировку UTF-8."""
    utterances = [
        Utterance(
            timespan="[00:00:01 — 00:00:02]",
            speaker="Спикер 1",
            text="Привет",
            words=["Привет"],
        ),
        Utterance(
            timespan="[00:00:03 — 00:00:04]",
            speaker="Спикер 2",
            text="Пока",
            words=["Пока"],
        ),
    ]
    src = tmp_path / "meeting.wav"
    result_path = save_txt(utterances, str(src))
    expected_path = tmp_path / "meeting_transcript.txt"
    assert result_path == str(expected_path)
    content = expected_path.read_text(encoding="utf-8")
    assert content == (
        "[00:00:01 — 00:00:02] Спикер 1: Привет\n"
        "[00:00:03 — 00:00:04] Спикер 2: Пока"
    )


def test_save_txt_creates_file_near_source(tmp_path) -> None:
    """Сохраняет итоговый файл рядом с исходным."""
    src_dir = tmp_path / "папка с пробелом"
    src_dir.mkdir()
    src = src_dir / "видео.mp4"
    src.write_text("", encoding="utf-8")
    utterances = [
        Utterance(
            timespan="[00:00:00 — 00:00:01]",
            speaker="Спикер 1",
            text="Привет",
            words=["Привет"],
        )
    ]
    result = save_txt(utterances, str(src))
    expected = src_dir / "видео_transcript.txt"
    assert result == str(expected)
    assert expected.exists()
