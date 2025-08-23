"""Тесты для модуля core.orchestrator."""

from pathlib import Path
import sys
from unittest.mock import Mock
from contextlib import contextmanager

import pytest

# Добавляем корень проекта в путь поиска модулей.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.orchestrator import Orchestrator  # noqa: E402
from utils.paths import build_output_path  # noqa: E402
from core.models import ASRSegment, DiarSegment, Utterance  # noqa: E402


def test_run_pipeline_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет успешный запуск пайплайна и порядок вызовов."""
    src_path = "sample.mp4"
    audio_path = "sample.wav"
    text_segments = [ASRSegment(start=0.0, end=1.0, text="text")]
    speaker_segments = [DiarSegment(start=0.0, end=1.0, speaker="speaker")]
    merged_utterances = [
        Utterance(
            timespan="[00:00:00 — 00:00:01]",
            speaker="speaker",
            text="text",
            words=["text"],
        )
    ]
    expected_path = build_output_path(src_path)
    call_order: list[str] = []

    media_mock = Mock()

    def validate_side_effect(path: str) -> None:
        call_order.append("validate")
        assert path == src_path

    @contextmanager
    def extract_side_effect(path: str):
        call_order.append("extract_audio")
        assert path == src_path
        yield audio_path

    media_mock.validate.side_effect = validate_side_effect
    media_mock.extract_audio.side_effect = extract_side_effect
    monkeypatch.setattr(
        "core.orchestrator.MediaProcessor", Mock(return_value=media_mock)
    )

    def transcribe_side_effect(path: str) -> list[ASRSegment]:
        call_order.append("transcribe")
        assert path == audio_path
        return text_segments

    def diarize_side_effect(path: str) -> list[DiarSegment]:
        call_order.append("diarize")
        assert path == audio_path
        return speaker_segments

    def merge_side_effect(
        ts: list[ASRSegment], ds: list[DiarSegment]
    ) -> list[Utterance]:
        call_order.append("merge")
        assert ts == text_segments
        assert ds == speaker_segments
        return merged_utterances

    def save_side_effect(items: list[Utterance], path: str) -> str:
        call_order.append("save")
        assert items == merged_utterances
        assert path == src_path
        return expected_path

    monkeypatch.setattr(
        "core.orchestrator.transcribe", Mock(side_effect=transcribe_side_effect)
    )
    monkeypatch.setattr(
        "core.orchestrator.diarize", Mock(side_effect=diarize_side_effect)
    )
    monkeypatch.setattr(
        "core.orchestrator.merge", Mock(side_effect=merge_side_effect)
    )
    monkeypatch.setattr(
        "core.orchestrator.save_txt", Mock(side_effect=save_side_effect)
    )

    result = Orchestrator().run(src_path)

    assert result == expected_path
    assert call_order == [
        "validate",
        "extract_audio",
        "transcribe",
        "diarize",
        "merge",
        "save",
    ]
