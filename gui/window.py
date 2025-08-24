"""Окно приложения на базе PyQt5."""

from __future__ import annotations

import logging
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from gui import messages


logger = logging.getLogger(__name__)


class MainWindow(QWidget):
    """Основное окно приложения.

    Отвечает за drag-n-drop файлов и отображение статусов.
    """

    file_dropped = pyqtSignal(str)
    """Сигнал, испускаемый при успешном переносе файла."""
    log_signal = pyqtSignal(str)
    """Сигнал с новым сообщением логгера."""

    def __init__(self) -> None:
        """Создаёт окно и настраивает интерфейс."""
        super().__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("Транскрибатор")
        self.setMinimumSize(300, 300)

        self._is_processing = False

        self._status_label = QLabel(messages.READY_MESSAGE)
        self._status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self._status_label)
        self.setLayout(layout)

        self.log_signal.connect(self.update_log)

    @property
    def status_label(self) -> QLabel:
        """Возвращает виджет с текстом статуса."""
        return self._status_label

    def set_waiting(self) -> None:
        """Отображает ожидание загрузки файла."""
        self._is_processing = False
        self._status_label.setText(messages.READY_MESSAGE)

    def set_processing(self) -> None:
        """Отображает процесс обработки файла."""
        self._is_processing = True
        self._status_label.setText(messages.PROCESSING_MESSAGE)

    def set_done(self, result_path: Optional[str] = None) -> None:
        """Отображает успешное завершение обработки.

        :param result_path: путь к итоговому файлу.
        """
        self._is_processing = False
        message = messages.DONE_MESSAGE
        if result_path:
            message = f"{message}: {result_path}\nВы можете загрузить новую запись."
        self._status_label.setText(message)

    def set_error(self, message: Optional[str] = None) -> None:
        """Отображает сообщение об ошибке.

        :param message: текст ошибки; по умолчанию стандартное сообщение.
        """
        self._is_processing = False
        self._status_label.setText(message or messages.ERROR_MESSAGE)

    def update_log(self, message: str) -> None:
        """Обновляет статус последним сообщением логгера."""
        if self._is_processing:
            self._status_label.setText(f"{messages.PROCESSING_MESSAGE} {message}")

    # Реализация drag-n-drop -------------------------------------------------
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        """Принимает перетаскиваемый объект, если это файл."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        """Обрабатывает отпускание файла на окне."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            logger.info("Получен файл %s", file_path)
            self.set_processing()
            self.file_dropped.emit(file_path)
