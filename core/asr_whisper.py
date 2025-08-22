"""Модуль транскрибации."""

from typing import List
import os

from dotenv import load_dotenv

try:
    from huggingface_hub import login as hf_login
except Exception:  # noqa: BLE001
    hf_login = None  # type: ignore[assignment]


load_dotenv()
_HF_TOKEN = os.getenv("HF_TOKEN") or ""
if _HF_TOKEN and hf_login:
    try:
        hf_login(token=_HF_TOKEN)
    except Exception:  # noqa: BLE001
        # Если авторизация не удалась, продолжаем работу без неё.
        pass


def transcribe(path: str) -> List[str]:
    """Выполняет распознавание речи.

    :param path: путь к аудиофайлу.
    :return: список строк с текстом.
    """
    return [f"Транскрибировано из {path}"]
