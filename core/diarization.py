"""Модуль диаризации."""

from typing import List
import wave
import numpy as np

from .models import DiarSegment


def _dominant_freq(samples: np.ndarray, rate: int) -> float:
    """Возвращает доминирующую частоту фрагмента."""
    spectrum = np.fft.rfft(samples)
    freqs = np.fft.rfftfreq(len(samples), 1 / rate)
    return float(freqs[int(np.argmax(np.abs(spectrum)))])


def diarize(path: str) -> List[DiarSegment]:
    """Определяет спикеров по смене частоты.

    :param path: путь к wav-файлу.
    :return: список сегментов с идентификатором спикера.
    """
    with wave.open(path, "rb") as wav:
        rate = wav.getframerate()
        frames = wav.readframes(wav.getnframes())
    samples = np.frombuffer(frames, dtype=np.int16).astype(float) / 32768.0

    frame_size = int(rate * 0.5)
    threshold = 30.0
    segments: List[DiarSegment] = []
    current_start = 0.0
    prev_freq: float | None = None
    speaker_idx = 0

    for offset in range(0, len(samples) - frame_size + 1, frame_size):
        frame = samples[offset : offset + frame_size]
        freq = _dominant_freq(frame, rate)
        if prev_freq and abs(freq - prev_freq) > threshold:
            end = offset / rate
            segments.append(
                DiarSegment(
                    start=current_start, end=end, speaker=f"speaker_{speaker_idx}"
                )
            )
            current_start = end
            speaker_idx = 1 - speaker_idx
        prev_freq = freq

    segments.append(
        DiarSegment(
            start=current_start,
            end=len(samples) / rate,
            speaker=f"speaker_{speaker_idx}",
        )
    )
    return segments
