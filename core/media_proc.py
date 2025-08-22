"""Обработка медиафайлов."""


class MediaProcessor:
    """Извлекает и нормализует аудио."""

    def extract_audio(self, path: str) -> str:
        """Извлекает аудио из видеофайла.

        :param path: путь к исходному файлу.
        :return: путь к аудиофайлу.
        """
        # Возвращаем путь-заглушку
        return f"{path}.wav"
