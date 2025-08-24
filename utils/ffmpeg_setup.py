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


def _find_existing(ext: str) -> tuple[Path | None, Path | None]:
    """Ищет ffmpeg и ffprobe в системе или по переменной окружения."""
    env = os.getenv("FFMPEG_PATH")
    if env:
        ffmpeg = Path(env)
        ffprobe = ffmpeg.with_name(f"ffprobe{ext}")
        if ffmpeg.exists() and ffprobe.exists():
            return ffmpeg, ffprobe
    ffmpeg = shutil.which(f"ffmpeg{ext}")
    ffprobe = shutil.which(f"ffprobe{ext}")
    if ffmpeg and ffprobe:
        return Path(ffmpeg), Path(ffprobe)
    return None, None


def _download_build(system: str, install: Path, ext: str) -> Tuple[Path, Path]:
    """Скачивает и распаковывает статический билд FFmpeg."""
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
    _download(url, archive, sha)
    _extract(archive, install)
    ffmpeg_path = next(install.rglob(f"ffmpeg{ext}"))
    ffprobe_path = next(install.rglob(f"ffprobe{ext}"))
    ffmpeg_path.chmod(0o755)
    ffprobe_path.chmod(0o755)
    return ffmpeg_path, ffprobe_path


def ensure_ffmpeg() -> Tuple[Path, Path]:
    """Возвращает пути к ffmpeg и ffprobe, скачивая при необходимости."""
    system = platform.system()
    ext = ".exe" if system == "Windows" else ""
    ffmpeg, ffprobe = _find_existing(ext)
    if ffmpeg and ffprobe:
        return ffmpeg, ffprobe

    install = _install_dir()
    ffmpeg_bin = install / f"ffmpeg{ext}"
    ffprobe_bin = install / f"ffprobe{ext}"
    if ffmpeg_bin.exists() and ffprobe_bin.exists():
        return ffmpeg_bin, ffprobe_bin

    if os.getenv("CI") or os.getenv("DISABLE_FFMPEG_DOWNLOAD"):
        raise RuntimeError("FFmpeg не найден. Установите его или задайте FFMPEG_PATH")

    try:
        return _download_build(system, install, ext)
    except Exception as error:
        shutil.rmtree(install, ignore_errors=True)
        raise RuntimeError("Не удалось установить FFmpeg") from error
