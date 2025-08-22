"""Оркестратор приложения."""

from core.media_proc import MediaProcessor
from core.asr_whisper import transcribe
from core.diarization import diarize
from core.postprocess import merge_results


class Orchestrator:
    """Связывает все этапы обработки файла."""

    def run(self) -> None:
        """Запускает пайплайн обработки."""
        # Заглушка пайплайна
        media = MediaProcessor()
        audio_path = media.extract_audio("input")
        text_segments = transcribe(audio_path)
        speaker_segments = diarize(audio_path)
        merge_results(text_segments, speaker_segments)
