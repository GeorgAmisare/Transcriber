"""Тесты для окна PyQt5."""

import os
import sys
import pytest

# Запускаем PyQt5 в безголовом режиме, чтобы не требовался дисплей.
os.environ["QT_QPA_PLATFORM"] = "minimal"

# PyQt5 нестабилен на Python 3.13, поэтому тесты пропускаются.
if sys.version_info >= (3, 13):  # pragma: no cover
    pytest.skip("PyQt5 не поддерживает Python 3.13", allow_module_level=True)

try:
    from PyQt5.QtCore import QMimeData, QPoint, QUrl, Qt
    from PyQt5.QtGui import QDropEvent
    from PyQt5.QtWidgets import QApplication
except ImportError:  # pragma: no cover
    pytest.skip("PyQt5 is required for these tests", allow_module_level=True)

from gui import messages  # noqa: E402
from gui.window import MainWindow  # noqa: E402


def _get_app() -> QApplication:
    """Возвращает экземпляр QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(["", "-platform", "minimal"])
    return app


def test_status_transitions() -> None:
    """Проверяет изменение статусов окна."""
    _get_app()
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
    _get_app()
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
