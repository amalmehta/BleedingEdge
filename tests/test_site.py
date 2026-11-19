import json

import pytest

from bleedingedge import brief, site

GRID = "2023-10-23"


def _rec(topic, score, early, heating=True, papers=(1, 2, 3)):
    arxiv = [0] * 37 + list(papers)
    return {"topic": topic, "arxiv": arxiv, "github": [1] * 40, "score": score, "early": early,
            "heating": heating, "g_trend_arxiv": 3.0, "g_trend_github": 2.0, "first_flag": "2026-06-01"}


@pytest.fixture
def paths(tmp_path, monkeypatch):
    monkeypatch.setattr(brief, "DATA", tmp_path / "data_briefs")
    monkeypatch.setattr(brief, "BRIEFS", tmp_path / "briefs")
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(brief, "TRENDS", tmp_path / "Trends.csv")
    (tmp_path / "data_briefs").mkdir()
    (tmp_path / "briefs").mkdir()
    old = _rec("old topic", 2.0, True)
    small = _rec("small new", 2.5, True)
    big = _rec("big crowd", 4.0, False, papers=(10, 10, 15))
    mature = _rec("small mature", 1.5, False)
    (tmp_path / "data_briefs" / "2026-11-09.json").write_text(json.dumps(
        {"date": "2026-11-09", "grid_start": GRID, "heating": [old], "early": [old]}))
    (tmp_path / "data_briefs" / "2026-11-16.json").write_text(json.dumps(
        {"date": "2026-11-16", "grid_start": GRID, "heating": [big, small, mature], "early": [small]}))
    (tmp_path / "Picks.csv").write_text(
        "date,topic,first_step,papers_12w,bar,due,peak_12w,peak_on,status,checked_on\n"
        "2026-11-16,small new,https://arxiv.org/abs/1,6,24,2027-11-16,7,2026-11-17,open,2026-11-18\n")
    (tmp_path / "briefs" / "2026-11-16.md").write_text(
        "**What it is.** Robots that learn small things. A second sentence that is left out.\n")
    (tmp_path / "Trends.csv").write_text(
        "date,topic,arxiv_12w,score\n2026-11-16,small new,6,2.5\n2026-11-16,unflagged,3,\n2026-11-16,elsewhere,9,1.2\n")
    return tmp_path


def test_status_follows_the_brief_rules(paths):
    t = {r["topic"]: r for r in site.build()["topics"]}
    assert t["small new"]["status"] == "Early"
    assert t["big crowd"]["status"] == "Consensus"       # 35 papers in 12 weeks: past the line of 30
    assert t["small mature"]["status"] == "Heating"
    assert t["old topic"]["status"] == "Not flagged this week" and t["old topic"]["last_flagged"] == "2026-11-09"


def test_this_weeks_topics_come_first_by_score(paths):
    assert [r["topic"] for r in site.build()["topics"]] == ["big crowd", "small new", "small mature", "old topic"]


def test_series_windows_end_the_day_before_the_brief(paths):
    s = [r for r in site.build()["series"] if r["topic"] == "small new"]
    assert len(s) == 40 and s[0]["window_end"] == "2023-11-19" and s[-1]["window_end"] == "2026-11-15"
    assert s[-1]["papers"] == 3 and s[-1]["new_repos"] == 1


def test_picks_carry_the_brief_words_and_the_grade(paths):
    p = site.build()["picks"][0]
    assert p["what_it_is"] == "Robots that learn small things."
    assert (p["bar"], p["peak_12w"], p["status"]) == (24, 7, "open")
    assert p["brief"].endswith("/briefs/2026-11-16.md")
    assert next(r for r in site.build()["topics"] if r["topic"] == "small new")["picked_on"] == "2026-11-16"


def test_scores_only_for_covered_topics_with_a_score(paths):
    assert [r["topic"] for r in site.build()["scores"]] == ["small new"]


def test_written_files_carry_their_code_and_inputs(paths, tmp_path):
    out = site.write(tmp_path / "site")
    d = json.loads(out["topics"].read_text())
    assert d["meta"][0]["label"] == "site.py" and "def build" in d["meta"][0]["value"]
    assert set(out) == {"topics", "series", "scores", "picks", "record"}


def test_record_matches_the_brief(paths):
    r = site.record()[0]
    assert f"**{r['took_off']} of {r['flagged']} flagged topics" in brief.record()


def test_fragments_are_left_out_unless_picked(paths, monkeypatch):
    from bleedingedge import daily
    (paths / "Fragments.csv").write_text("phrase,added,reason\nbig crowd,2026-11-19,x\nsmall new,2026-11-19,x\n")
    monkeypatch.setattr(daily, "FRAGMENTS", paths / "Fragments.csv")
    topics = [r["topic"] for r in site.build()["topics"]]
    assert "big crowd" not in topics and "small new" in topics      # a pick always stays


def test_explainers_ride_along_with_their_topic(paths, monkeypatch):
    monkeypatch.setattr(brief, "ROOT", paths)
    (paths / "data").mkdir()
    (paths / "data" / "Explainers.json").write_text(json.dumps({"small new": {
        "what": "W", "why": "Y", "sources": [{"url": "https://arxiv.org/abs/1", "title": "t"}]}}))
    t = {r["topic"]: r for r in site.build()["topics"]}
    assert (t["small new"]["plain_what"], t["small new"]["plain_why"]) == ("W", "Y")
    assert t["small new"]["plain_sources"][0]["title"] == "t" and t["big crowd"]["plain_what"] == ""
