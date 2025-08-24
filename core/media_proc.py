"""Обработка медиафайлов."""

from __future__ import annotations

import logging
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterator

from utils.ffmpeg_setup import ensure_ffmpeg


logger = logging.getLogger(__name__)

# Флаг скрывает окна консоли при запуске подпроцессов на Windows.
_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class MediaProcessor:
    """Извлекает и нормализует аудио."""

    _MAX_SIZE = 2 * 1024**3
    _MAX_DURATION = 90 * 60
    _SUPPORTED_EXTENSIONS = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".wmv",
        ".webm",
        ".flv",
        ".m4v",
        ".ts",
        ".mts",
        ".mp3",
        ".wav",
        ".aac",
        ".m4a",
        ".wma",
        ".ogg",
        ".oga",
        ".flac",
        ".amr",
        ".aiff",
        ".aifc",
        ".opus",
        ".caf",
    }

    def __init__(self) -> None:
        """Ищет бинарники FFmpeg."""
        self._ffmpeg, self._ffprobe = ensure_ffmpeg()

    def validate(self, path: str) -> None:
        """Проверяет формат, размер и длительность файла.

        :param path: путь к медиафайлу.
        :raises ValueError: при нарушении ограничений.
        """
        logger.debug("Проверка файла %s", path)
        extension = Path(path).suffix.lower()
        if extension not in self._SUPPORTED_EXTENSIONS:
            raise ValueError("Недопустимый формат файла")

        size = os.path.getsize(path)
        if size > self._MAX_SIZE:
            raise ValueError("Размер файла превышает 2 ГБ")

        duration = self._probe_duration(path)
        if duration > self._MAX_DURATION:
            raise ValueError("Длительность файла превышает 90 минут")

    def _probe_duration(self, path: str) -> float:
        """Возвращает длительность файла в секундах.

        :param path: путь к медиафайлу.
        :raises ValueError: если длительность не удалось определить.
        """
        try:
            result = subprocess.run(
                [
                    str(self._ffprobe),
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    path,
                ],
                capture_output=True,
                text=True,
                check=True,
                creationflags=_NO_WINDOW,
            )
            duration = float(result.stdout.strip())
            logger.debug("Длительность файла %s секунд", duration)
            return duration
        except (FileNotFoundError, subprocess.SubprocessError, ValueError) as error:
            raise ValueError("Не удалось определить длительность файла") from error

    @contextmanager
    def extract_audio(self, path: str) -> Iterator[str]:
        """Возвращает путь к временному PCM-файлу и удаляет его."""
        with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        cmd = [
            str(self._ffmpeg),
            "-y",
            "-i",
            path,
            "-ac",
            "1",
            "-ar",
            "16000",
            "-vn",
            "-f",
            "wav",
            "-sample_fmt",
            "s16",
            tmp_path,
        ]
        logger.info("Извлечение аудио из %s", path)
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=_NO_WINDOW,
            )
            yield tmp_path
        finally:
            try:
                os.remove(tmp_path)
                logger.debug("Удалён временный файл %s", tmp_path)
            except OSError:
                pass
