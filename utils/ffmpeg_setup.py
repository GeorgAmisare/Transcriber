"""Настройка и загрузка статического FFmpeg."""

from __future__ import annotations

import hashlib
import os
import platform
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Tuple

import requests


def _install_dir() -> Path:
    """Возвращает директорию установки FFmpeg."""
    system = platform.system()
    if system == "Windows":
        base = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "Transcriber" / "ffmpeg"
    if system == "Darwin":
        return (
            Path.home() / "Library" / "Application Support" / "Transcriber" / "ffmpeg"
        )
    return Path.home() / ".local" / "share" / "Transcriber" / "ffmpeg"


def _download(url: str, dest: Path, sha256: str) -> None:
    """Скачивает файл и проверяет хэш."""
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        hasher = hashlib.sha256()
        with dest.open("wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
                hasher.update(chunk)
    if hasher.hexdigest() != sha256:
        dest.unlink(missing_ok=True)
        raise RuntimeError("Повреждён архив FFmpeg")


def _extract(archive: Path, folder: Path) -> None:
    """Распаковывает архив в указанную папку."""
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(folder)
    else:
        with tarfile.open(archive) as tf:
            tf.extractall(folder)
    archive.unlink()


def ensure_ffmpeg() -> Tuple[Path, Path]:
    """Гарантирует наличие ffmpeg и ffprobe.

    :return: пути к бинарникам.
    :raises RuntimeError: при ошибках загрузки.
    """
    system = platform.system()
    ext = ".exe" if system == "Windows" else ""
    candidates = [
        shutil.which(f"ffmpeg{ext}"),
        shutil.which(f"ffprobe{ext}"),
    ]
    if all(candidates):
        return Path(candidates[0]), Path(candidates[1])

    install = _install_dir()
    ffmpeg_bin = install / f"ffmpeg{ext}"
    ffprobe_bin = install / f"ffprobe{ext}"
    if ffmpeg_bin.exists() and ffprobe_bin.exists():
        return ffmpeg_bin, ffprobe_bin

    urls = {
        "Windows": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        "Linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
        "Darwin": "https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip",
    }
    url = urls.get(system)
    if not url:
        raise RuntimeError("Неизвестная платформа для установки FFmpeg")

    sha = requests.get(url + ".sha256", timeout=60).text.split()[0]
    install.mkdir(parents=True, exist_ok=True)
    archive = install / Path(url).name
    try:
        _download(url, archive, sha)
        _extract(archive, install)
    except Exception as error:
        shutil.rmtree(install, ignore_errors=True)
        raise RuntimeError("Не удалось установить FFmpeg") from error

    ffmpeg_path = next(install.rglob(f"ffmpeg{ext}"))
    ffprobe_path = next(install.rglob(f"ffprobe{ext}"))
    ffmpeg_path.chmod(0o755)
    ffprobe_path.chmod(0o755)
    return ffmpeg_path, ffprobe_path
