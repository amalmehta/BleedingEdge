import csv
from datetime import date, timedelta

import pytest

from bleedingedge import brief, ledger

PICK = date(2026, 10, 27)


@pytest.fixture
def paths(tmp_path, monkeypatch):
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(brief, "TRENDS", tmp_path / "Trends.csv")
    (tmp_path / "Picks.csv").write_text(f"date,topic,first_step\n{PICK},robot foundation,https://x\n")
    (tmp_path / "Trends.csv").write_text(
        "date,topic,domain,arxiv_4w,arxiv_12w\n"
        f"{PICK},robot foundation,rl_robotics,13,24\n{PICK},tiny,rl_robotics,1,3\n")
    return tmp_path


def _papers(n: int, end: date) -> list[date]:
    """n papers spread over the 12 weeks before end."""
    return [end - timedelta(days=1 + (k * 83) // max(n, 1)) for k in range(n)]


def test_fill_reads_the_bar_the_brief_wrote(paths):
    r = ledger.fill(ledger.read()[0])
    assert (r["papers_12w"], r["bar"], r["due"]) == ("24", "96", "2027-10-27")


def test_small_topics_get_the_floor_of_20(paths):
    r = ledger.fill({c: "" for c in ledger.COLS} | {"date": str(PICK), "topic": "tiny"})
    assert r["bar"] == "20"


def test_open_until_the_bar_is_passed(paths):
    r = ledger.grade(ledger.read()[0], _papers(96, PICK + timedelta(days=100)), PICK + timedelta(days=100))
    assert r["status"] == "open" and r["peak_12w"] == "96"   # 96 doesn't pass a bar of 96


def test_took_off_once_the_peak_passes_the_bar(paths):
    day = PICK + timedelta(days=200)
    r = ledger.grade(ledger.read()[0], _papers(97, day), day + timedelta(days=30))
    assert r["status"] == "took off" and r["peak_12w"] == "97" and r["peak_on"] == str(day)


def test_a_peak_after_the_due_date_doesnt_count(paths):
    late = date(2028, 3, 1)     # all 200 papers fall after the due date, 27 Oct 2027
    r = ledger.grade(ledger.read()[0], _papers(200, late), late)
    assert r["status"] == "didn't take off"


def test_open_on_the_due_date_itself(paths):
    r = ledger.grade(ledger.read()[0], [], date(2027, 10, 27))
    assert r["status"] == "open"


def test_a_pick_missing_from_trends_is_flagged_not_guessed(paths):
    with (paths / "Picks.csv").open("a", newline="") as f:
        csv.writer(f).writerow(["2026-11-02", "unknown phrase", "https://y"])
    r = ledger.grade(ledger.read()[1], [], date(2026, 11, 18))
    assert r["status"] == "no data" and r["bar"] == ""


def test_the_count_excludes_the_day_itself_like_the_brief(paths):
    assert ledger.count_12w([PICK - timedelta(days=84), PICK - timedelta(days=1), PICK], PICK) == 2


def test_rows_appended_by_the_weekly_task_keep_working(paths, monkeypatch):
    ledger.write([ledger.grade(ledger.read()[0], [], date(2026, 11, 18))])
    with (paths / "Picks.csv").open("a", newline="") as f:     # the task appends 3 fields only
        csv.writer(f).writerow(["2026-11-23", "new pick", "https://z"])
    rows = ledger.read()
    assert rows[0]["bar"] == "96" and rows[1]["topic"] == "new pick" and rows[1]["bar"] == ""
    assert brief.recent_picks(date(2026, 12, 1))[-1] == "new pick"


def test_february_29th_rolls_to_the_28th():
    assert ledger.a_year_after(date(2028, 2, 29)) == date(2029, 2, 28)
