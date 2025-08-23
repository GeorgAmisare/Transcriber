"""Тесты для модуля core.diarization."""

from pathlib import Path
import sys
import wave
import numpy as np
import pytest

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.diarization import diarize


def _write_wave(path: Path, data: np.ndarray, rate: int = 16000) -> None:
    """Сохраняет массив в wav-файл."""
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes((data * 32767).astype(np.int16).tobytes())


def _sine(freq: float, duration: float, rate: int = 16000) -> np.ndarray:
    """Генерирует синус с заданной частотой."""
    t = np.linspace(0, duration, int(rate * duration), False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


def test_diarize_two_speakers(tmp_path: Path) -> None:
    """Проверяет выделение двух спикеров в записи."""
    audio = np.concatenate([_sine(440, 1), _sine(660, 1)])
    path = tmp_path / "two.wav"
    _write_wave(path, audio)
    segments = diarize(str(path))
    assert [s.speaker for s in segments] == ["speaker_0", "speaker_1"]
    assert pytest.approx(0, abs=0.05) == segments[0].start
    assert pytest.approx(1, abs=0.05) == segments[0].end
    assert pytest.approx(1, abs=0.05) == segments[1].start
    assert pytest.approx(2, abs=0.05) == segments[1].end
