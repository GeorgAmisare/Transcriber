"""Утилиты форматирования времени."""


def format_ts(seconds: float) -> str:
    """Форматирует секунды в строку HH:MM:SS.

    :param seconds: количество секунд.
    :return: форматированная строка.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
