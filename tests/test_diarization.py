"""Тесты для модуля core.diarization."""

from pathlib import Path
import sys
import wave
from unittest.mock import patch

import numpy as np
import pytest
from pyannote.core import Annotation, Segment

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

import core.diarization as dia


def _write_silence(path: Path, duration: float, rate: int = 16000) -> None:
    """Создаёт wav-файл с тишиной."""

    data = np.zeros(int(rate * duration), dtype=np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(data.tobytes())


class DummyPipeline:
    """Пайплайн, возвращающий два сегмента."""

    def __call__(self, path: str) -> Annotation:  # pragma: no cover
        annotation = Annotation()
        annotation[Segment(0, 1)] = "speaker_0"
        annotation[Segment(1, 2)] = "speaker_1"
        return annotation


@patch(
    "core.diarization.Pipeline.from_pretrained",
    return_value=DummyPipeline(),
)
def test_diarize_two_speakers(mock_pipeline, tmp_path: Path) -> None:
    """Проверяет получение сегментов от пайплайна pyannote."""

    dia._PIPELINE = None
    path = tmp_path / "audio.wav"
    _write_silence(path, 2)
    segments = dia.diarize(str(path))
    assert [s.speaker for s in segments] == ["speaker_0", "speaker_1"]
    assert pytest.approx(0, abs=0.01) == segments[0].start
    assert pytest.approx(1, abs=0.01) == segments[0].end
    assert pytest.approx(1, abs=0.01) == segments[1].start
    assert pytest.approx(2, abs=0.01) == segments[1].end
