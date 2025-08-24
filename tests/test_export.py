"""Тесты для модулей core.export_txt, export_srt и export_md."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.export_txt import export_txt, save_txt
from core.export_srt import export_srt
from core.export_md import export_md
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


def test_export_srt_writes_file(tmp_path) -> None:
    """Проверяет запись строк в файл .srt."""
    lines = ["первая", "вторая"]
    path = tmp_path / "out.srt"
    export_srt(lines, str(path))
    assert path.read_text(encoding="utf-8") == "\n".join(lines)


def test_export_md_writes_file(tmp_path) -> None:
    """Проверяет запись строк в файл .md."""
    lines = ["первая", "вторая"]
    path = tmp_path / "out.md"
    export_md(lines, str(path))
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
