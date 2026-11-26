import pytest

from bleedingedge import daily, feedback


@pytest.fixture(autouse=True)
def _no_real_private_files(tmp_path, monkeypatch):
    """Tests never read your votes in data/private/ or the real fragment list."""
    monkeypatch.setattr(feedback, "FEEDBACK", tmp_path / "private" / "Feedback.csv")
    monkeypatch.setattr(daily, "FRAGMENTS", tmp_path / "Fragments.csv")
