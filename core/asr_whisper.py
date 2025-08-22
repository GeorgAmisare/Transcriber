"""Модуль транскрибации."""

from typing import List
import os

from dotenv import load_dotenv
from huggingface_hub import login as hf_login


load_dotenv()
_token = os.getenv("HF_TOKEN")
if _token:
    hf_login(token=_token)


def transcribe(path: str) -> List[str]:
    """Выполняет распознавание речи.

    :param path: путь к аудиофайлу.
    :return: список строк с текстом.
    """
    return [f"Транскрибировано из {path}"]
