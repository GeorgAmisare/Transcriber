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
            # Добавляем служебные файлы библиотек Lightning,
            # чтобы exe не падал с FileNotFoundError.
            "--collect-data",
            "lightning_fabric",
            "--collect-data",
            "pytorch_lightning",
        ]
    )


if __name__ == "__main__":
    build()
