"""Модуль постобработки."""

import logging
from typing import List

from .models import ASRSegment, DiarSegment, Utterance
from utils.timing import format_ts


logger = logging.getLogger(__name__)


def merge_results(text: List[str], speakers: List[str]) -> List[str]:
    """Объединяет транскрибацию и диаризацию.

    :param text: список строк текста.
    :param speakers: список спикеров.
    :return: список готовых строк.
    """
    logger.debug("Слияние %d строк", len(text))
    return [f"{s}: {t}" for s, t in zip(speakers, text)]


def _overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    """Вычисляет длительность пересечения двух интервалов."""
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return max(0.0, end - start)


def merge(
    asr_segments: List[ASRSegment], diar_segments: List[DiarSegment]
) -> List[Utterance]:
    """Сопоставляет сегменты распознавания со спикерами.

    Для каждого сегмента из ASR выбирается тот спикер диаризации, чей
    интервал пересекается с ним дольше всего. Если пересечений нет, то
    используется последний определённый спикер либо ``"unknown"``.

    :param asr_segments: сегменты текста из распознавания.
    :param diar_segments: сегменты с идентификатором спикера.
    :return: список готовых реплик.
    """
    logger.debug(
        "Сопоставление %d сегментов ASR и %d сегментов диаризации",
        len(asr_segments),
        len(diar_segments),
    )
    utterances: List[Utterance] = []
    last_speaker = "unknown"

    for seg in asr_segments:
        overlaps = [
            (_overlap(seg.start, seg.end, d.start, d.end), d.speaker)
            for d in diar_segments
            if _overlap(seg.start, seg.end, d.start, d.end) > 0
        ]

        if overlaps:
            # При равенстве длительности берётся первый по времени сегмент.
            _, speaker = max(overlaps, key=lambda item: item[0])
            last_speaker = speaker
        else:
            speaker = last_speaker

        timespan = f"[{format_ts(seg.start)} — {format_ts(seg.end)}]"
        utterances.append(
            Utterance(
                timespan=timespan,
                speaker=speaker,
                text=seg.text,
                words=seg.text.split(),
            )
        )

    return utterances
