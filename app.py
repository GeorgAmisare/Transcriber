"""Точка входа приложения."""

import logging
import threading

from PyQt5.QtWidgets import QApplication

from core.orchestrator import Orchestrator
from gui.window import MainWindow
from utils.logging_setup import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    """Создаёт GUI и связывает его с оркестратором."""
    app = QApplication([])
    window = MainWindow()
    setup_logging(
        filename="transcriber.log",
        error_callback=window.set_error,
        status_callback=window.log_signal.emit,
    )
    logger.info("Приложение запущено")
    orchestrator = Orchestrator(on_done=window.set_done)

    def run_in_thread(path: str) -> None:
        """Запускает обработку файла в отдельном потоке."""
        threading.Thread(
            target=orchestrator.run, args=(path,), daemon=True
        ).start()

    window.file_dropped.connect(run_in_thread)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
