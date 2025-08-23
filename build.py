"""Сборка исполняемого файла под Windows с помощью PyInstaller."""

from pathlib import Path

import PyInstaller.__main__


def build() -> None:
    """Упаковывает приложение в один exe-файл."""
    root = Path(__file__).parent
    PyInstaller.__main__.run(
        [
            str(root / "app.py"),
            "--name",
            "transcriber",
            "--onefile",
            "--noconsole",
            "--clean",
        ]
    )


if __name__ == "__main__":
    build()
