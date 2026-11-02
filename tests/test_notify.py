import csv
from datetime import date

import pytest

from bleedingedge import brief, notify

DAY = date(2026, 11, 2)
WRITTEN = "# Brief\n<!-- pick:start -->\n**Pick.**\n<!-- pick:end -->\n"


@pytest.fixture
def paths(tmp_path, monkeypatch):
    monkeypatch.setattr(brief, "BRIEFS", tmp_path / "briefs")
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(notify, "OPPORTUNITIES", tmp_path / "Opportunities.csv")
    monkeypatch.setattr(notify, "REVIEW", tmp_path / "TrialReview.md")
    monkeypatch.setattr(notify, "OPPS_ONLY", tmp_path / "briefs" / "opportunities")
    (tmp_path / "briefs").mkdir()
    (tmp_path / "Picks.csv").write_text("date,topic,first_step\n2026-10-27,robot foundation,https://x\n")
    (tmp_path / "TrialReview.md").write_text(
        "| Brief | Study pick | Taste (1–5) | Acted on (y/n) | Notes |\n|---|---|---|---|---|\n"
        "| [2026-10-27](x) | robot foundation |  |  | a note |\n")
    (tmp_path / "briefs" / "2026-10-27.md").write_text(WRITTEN)
    return tmp_path


def _sent(monkeypatch):
    sent = []
    monkeypatch.setattr(notify, "send", sent.append)
    return sent


def test_missing_brief_alerts_even_with_only_if_missing(paths, monkeypatch):
    sent = _sent(monkeypatch)
    notify.main(DAY, only_if_missing=True)
    assert len(sent) == 1 and "No finished brief for 2 Nov" in sent[0]


def test_unwritten_draft_counts_as_missing(paths, monkeypatch):
    sent = _sent(monkeypatch)
    (paths / "briefs" / f"{DAY}.md").write_text(f"{brief.PICK_START}\n_Not written yet._\n{brief.PICK_END}\n")
    notify.main(DAY, only_if_missing=True)
    assert "No finished brief" in sent[0]
    (paths / "briefs" / f"{DAY}.md").write_text(f"{WRITTEN}{brief.OPPS_DRAFT}\n")
    assert not notify.finished(paths / "briefs" / f"{DAY}.md")


def test_finished_brief_gives_the_pick_and_last_weeks_question(paths, monkeypatch):
    sent = _sent(monkeypatch)
    (paths / "briefs" / f"{DAY}.md").write_text(WRITTEN)
    with (paths / "Picks.csv").open("a", newline="") as f:
        csv.writer(f).writerow([DAY, "flow policies", "https://y"])
    (paths / "Opportunities.csv").write_text(f"date,type,name,deadline,url,checked_on\n{DAY},job,A,rolling,https://a,{DAY}\n")
    notify.main(DAY)
    assert "Pick: flow policies." in sent[0] and "1 new opportunity." in sent[0]
    assert "2 hours on robot foundation" in sent[0] and "10 Nov" in sent[0]


def test_finished_brief_is_silent_for_the_later_check(paths, monkeypatch):
    sent = _sent(monkeypatch)
    (paths / "briefs" / f"{DAY}.md").write_text(WRITTEN)
    notify.main(DAY, only_if_missing=True)
    assert sent == []


def test_a_marked_pick_isnt_asked_about_again(paths):
    review = paths / "TrialReview.md"
    review.write_text(review.read_text().replace("|  |  | a note", "| 4 | y | a note"))
    assert notify.last_pick_question(DAY) == ""


def test_no_pick_week_says_so(paths):
    (paths / "briefs" / f"{DAY}.md").write_text(WRITTEN)
    assert notify.message(DAY).startswith("No pick this week. 0 new opportunities.")


def test_after_the_trial_it_expects_the_opportunities_file_then_nothing(paths):
    for d in ("2026-11-02", "2026-11-09", "2026-11-16"):
        (paths / "briefs" / f"{d}.md").write_text(WRITTEN)
    later = date(2026, 11, 23)
    assert notify.expected(later) == paths / "briefs" / "opportunities" / f"{later}.md"
    assert "No finished brief" in notify.message(later)
    (paths / "briefs" / "opportunities").mkdir()
    (paths / "briefs" / "opportunities" / f"{later}.md").write_text("None this week\n")
    assert notify.message(later).startswith("Weekly opportunities are ready")
    assert notify.expected(date(2026, 12, 28)) is None and notify.message(date(2026, 12, 28)) is None


def test_send_passes_text_as_an_argument(monkeypatch):
    calls = []
    monkeypatch.setattr(notify.subprocess, "run", lambda cmd, check: calls.append(cmd))
    notify.send('x" & do shell script "boom')
    assert calls[0][-1] == 'x" & do shell script "boom'
    assert all("boom" not in part for part in calls[0][:-1])
