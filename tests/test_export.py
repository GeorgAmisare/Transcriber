"""Тесты для модулей core.export_txt, export_srt и export_md."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.export_txt import export_txt
from core.export_srt import export_srt
from core.export_md import export_md


def test_export_txt_writes_file(tmp_path) -> None:
    """Проверяет запись строк в файл .txt."""
    lines = ["первая", "вторая"]
    path = tmp_path / "out.txt"
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
