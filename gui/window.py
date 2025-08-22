"""Модуль окна приложения."""

from typing import Optional


class MainWindow:
    """Основное окно приложения.

    Отвечает за drag-n-drop файлов и отображение статусов.
    """

    def __init__(self) -> None:
        """Инициализирует окно приложения."""
        self._current_status: Optional[str] = None

    def set_status(self, message: str) -> None:
        """Устанавливает текущий статус.

        :param message: текст статуса.
        """
        self._current_status = message

    def show(self) -> None:
        """Отображает окно."""
        # Заглушка для отображения окна
        self.set_status("Окно отображено")
