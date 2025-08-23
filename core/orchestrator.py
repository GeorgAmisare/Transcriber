"""Оркестратор приложения."""

from __future__ import annotations

import logging
from typing import Callable, Optional

from core.asr_whisper import transcribe
from core.diarization import diarize
from core.media_proc import MediaProcessor
from core.postprocess import merge
from core.export_txt import save_txt


logger = logging.getLogger(__name__)


class Orchestrator:
    """Связывает все этапы обработки файла."""

    def __init__(self, on_done: Optional[Callable[[str], None]] = None) -> None:
        """Создаёт оркестратор.

        :param on_done: колбэк при успешном завершении.
        """
        self._on_done = on_done

    def run(self, src_path: str) -> Optional[str]:
        """Запускает пайплайн обработки файла.

        1. Извлекает аудио.
        2. Транскрибирует речь.
        3. Выполняет диаризацию.
        4. Объединяет результаты.
        5. Сохраняет итоговый текст.

        :param src_path: путь к исходному медиафайлу.
        :return: путь к итоговому файлу или ``None`` при ошибке.
        """
        logger.info("Запуск пайплайна для %s", src_path)
        try:
            media = MediaProcessor()
            media.validate(src_path)
            with media.extract_audio(src_path) as audio_path:
                text_segments = transcribe(audio_path)
                speaker_segments = diarize(audio_path)
                utterances = merge(text_segments, speaker_segments)
                result_path = save_txt(utterances, src_path)

            if self._on_done:
                self._on_done(result_path)
            logger.info("Обработка %s завершена", src_path)
            return result_path
        except Exception:  # noqa: BLE001
            logger.exception("Ошибка при обработке %s", src_path)
            return None
