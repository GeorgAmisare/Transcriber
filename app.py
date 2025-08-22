"""Точка входа приложения."""

from core.orchestrator import Orchestrator


def main() -> None:
    """Запускает основной процесс приложения."""
    orchestrator = Orchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
