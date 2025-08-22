"""Дата-классы проекта."""

from dataclasses import dataclass
from typing import List


@dataclass
class ASRSegment:
    """Сегмент текста из распознавания."""

    start: float
    end: float
    text: str


@dataclass
class DiarSegment:
    """Сегмент с идентификатором спикера."""

    start: float
    end: float
    speaker: str


@dataclass
class Utterance:
    """Готовая реплика."""

    timespan: str
    speaker: str
    text: str
    words: List[str]
