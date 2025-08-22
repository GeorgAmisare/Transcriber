"""Обработка медиафайлов."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


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

    def validate(self, path: str) -> None:
        """Проверяет формат, размер и длительность файла.

        :param path: путь к медиафайлу.
        :raises ValueError: при нарушении ограничений.
        """
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
                    "ffprobe",
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
            )
            return float(result.stdout.strip())
        except (FileNotFoundError, subprocess.SubprocessError, ValueError) as error:
            raise ValueError("Не удалось определить длительность файла") from error

    def extract_audio(self, path: str) -> str:
        """Извлекает аудио из видеофайла.

        :param path: путь к исходному файлу.
        :return: путь к аудиофайлу.
        """
        # Возвращаем путь-заглушку
        return f"{path}.wav"
