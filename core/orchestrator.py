"""Оркестратор приложения."""

from __future__ import annotations

from typing import Callable, Optional

from core.asr_whisper import transcribe
from core.diarization import diarize
from core.media_proc import MediaProcessor
from core.postprocess import merge_results
from core.export_txt import export_txt
from utils.paths import build_output_path


class Orchestrator:
    """Связывает все этапы обработки файла."""

    def __init__(
        self,
        on_done: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Создаёт оркестратор.

        :param on_done: колбэк при успешном завершении.
        :param on_error: колбэк при возникновении ошибки.
        """
        self._on_done = on_done
        self._on_error = on_error

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
        try:
            media = MediaProcessor()
            media.validate(src_path)
            with media.extract_audio(src_path) as audio_path:
                text_segments = transcribe(audio_path)
                speaker_segments = diarize(audio_path)
                merged_lines = merge_results(text_segments, speaker_segments)

                result_path = build_output_path(src_path)
                export_txt(merged_lines, result_path)

            if self._on_done:
                self._on_done(result_path)
            return result_path
        except Exception as error:  # noqa: BLE001
            if self._on_error:
                self._on_error(str(error))
            return None
