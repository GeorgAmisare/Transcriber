"""Модуль диаризации на основе pyannote.audio."""

from __future__ import annotations

import logging
import os
from typing import List

from pyannote.audio import Pipeline

from .models import DiarSegment


logger = logging.getLogger(__name__)

_PIPELINE: Pipeline | None = None


def _load_pipeline() -> Pipeline:
    """Загружает пайплайн с использованием токена HF_TOKEN."""

    global _PIPELINE
    if _PIPELINE is None:
        token = os.getenv("HF_TOKEN")
        _PIPELINE = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=token
        )
    return _PIPELINE


def diarize(path: str) -> List[DiarSegment]:
    """Определяет спикеров в аудиофайле.

    :param path: путь к wav-файлу.
    :return: список сегментов с идентификатором спикера.
    """

    logger.info("Диаризация файла %s", path)
    pipeline = _load_pipeline()
    diarization = pipeline(path)
    segments: List[DiarSegment] = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        segments.append(
            DiarSegment(
                start=float(segment.start),
                end=float(segment.end),
                speaker=str(speaker),
            )
        )
    return segments
