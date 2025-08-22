"""Тесты для оркестратора."""

from core.orchestrator import Orchestrator


def test_run_passes_error_message(tmp_path):
    """Передаёт текст ошибки в колбэк GUI."""
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("x")

    messages = []
    orchestrator = Orchestrator(on_error=messages.append)

    result = orchestrator.run(str(bad_file))

    assert result is None
    assert messages and "формат" in messages[0]
