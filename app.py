"""Точка входа приложения."""

from PyQt5.QtWidgets import QApplication

from core.orchestrator import Orchestrator
from gui.window import MainWindow


def main() -> None:
    """Создаёт GUI и связывает его с оркестратором."""
    app = QApplication([])
    window = MainWindow()
    orchestrator = Orchestrator(on_done=window.set_done, on_error=window.set_error)
    window.file_dropped.connect(orchestrator.run)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
