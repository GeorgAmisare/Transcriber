"""Модуль транскрибации."""

import logging
import os
from typing import List

from dotenv import load_dotenv

try:
    from huggingface_hub import login as hf_login
except Exception:  # noqa: BLE001
    hf_login = None  # type: ignore[assignment]

import whisper

from core.models import ASRSegment


logger = logging.getLogger(__name__)


load_dotenv()
_HF_TOKEN = os.getenv("HF_TOKEN") or ""
if _HF_TOKEN and hf_login:
    try:
        hf_login(token=_HF_TOKEN)
    except Exception:  # noqa: BLE001
        # Если авторизация не удалась, продолжаем работу без неё.
        pass


def transcribe(wav_path: str, model: str = "small") -> List[ASRSegment]:
    """Выполняет распознавание речи.

    :param wav_path: путь к WAV-файлу.
    :param model: название модели Whisper (по умолчанию ``small``).
    :return: список сегментов с началом, концом и текстом.
    """
    logger.info("Запуск распознавания модели %s", model)
    asr = whisper.load_model(model)
    result = asr.transcribe(wav_path)
    return [
        ASRSegment(
            start=float(seg["start"]),
            end=float(seg["end"]),
            text=seg["text"].strip(),
        )
        for seg in result.get("segments", [])
    ]
