"""Тесты для окна PyQt5."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QMimeData, QPoint, QUrl, Qt
from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import QApplication

from gui import messages
from gui.window import MainWindow


def _get_app() -> QApplication:
    """Возвращает экземпляр QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_status_transitions() -> None:
    """Проверяет изменение статусов окна."""
    app = _get_app()
    window = MainWindow()
    assert window.status_label.text() == messages.READY_MESSAGE

    window.set_processing()
    assert window.status_label.text() == messages.PROCESSING_MESSAGE

    window.set_done()
    assert window.status_label.text() == messages.DONE_MESSAGE

    window.set_error()
    assert window.status_label.text() == messages.ERROR_MESSAGE


def test_drop_event_emits_file(tmp_path) -> None:
    """Проверяет приём файла и смену статуса на "обработка"."""
    app = _get_app()
    window = MainWindow()
    emitted = []
    window.file_dropped.connect(lambda path: emitted.append(path))

    test_file = tmp_path / "sample.txt"
    test_file.write_text("data")

    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(str(test_file))])
    event = QDropEvent(QPoint(0, 0), Qt.CopyAction, mime, Qt.LeftButton, Qt.NoModifier)

    window.dropEvent(event)

    assert emitted == [str(test_file)]
    assert window.status_label.text() == messages.PROCESSING_MESSAGE

