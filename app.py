"""Точка входа приложения."""

import logging

from PyQt5.QtWidgets import QApplication

from core.orchestrator import Orchestrator
from gui.window import MainWindow
from utils.logging_setup import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    """Создаёт GUI и связывает его с оркестратором."""
    app = QApplication([])
    window = MainWindow()
    setup_logging(filename="transcriber.log", gui_callback=window.set_error)
    logger.info("Приложение запущено")
    orchestrator = Orchestrator(on_done=window.set_done)
    window.file_dropped.connect(orchestrator.run)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
