"""Тесты для модуля utils.paths."""

from pathlib import Path
import sys

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.paths import build_output_path


def test_build_output_path_appends_suffix() -> None:
    """Проверяет добавление суффикса _transcript.txt к имени файла."""
    src = Path("/tmp/audio.mp3")
    expected = src.with_name(f"{src.stem}_transcript.txt")
    # Нормализуем обе стороны как Path, чтобы абстрагироваться от разделителей
    assert Path(build_output_path(str(src))) == expected


def test_build_output_path_is_absolute(tmp_path, monkeypatch) -> None:
    """Убеждается, что возвращается абсолютный путь."""
    monkeypatch.chdir(tmp_path)
    src = Path("meeting.mp3")
    result = Path(build_output_path(str(src)))
    assert result.is_absolute()
    assert result == (tmp_path / "meeting_transcript.txt").resolve()


def test_build_output_path_resolves_symlink(tmp_path) -> None:
    """Возвращает путь внутри реального каталога, а не ссылки."""
    target = tmp_path / "real"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target)
    src = link / "audio.mp3"
    src.touch()
    result = Path(build_output_path(str(src)))
    assert result.parent.resolve() == target.resolve()
