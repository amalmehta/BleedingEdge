import json
from datetime import date

import pytest

from bleedingedge import brief, daily

TUE, SAT = date(2026, 11, 24), date(2026, 11, 29)  # SAT: a quiet Sunday, 2 days before "Soon"


def feed(*papers):
    entries = "".join(
        f"<entry><id>http://arxiv.org/abs/{pid}v1</id><title>{title}</title>"
        f"<published>2026-11-22T10:00:00Z</published></entry>" for pid, title in papers)
    return f'<feed xmlns="http://www.w3.org/2005/Atom">{entries}</feed>'


EMPTY = feed()


@pytest.fixture
def paths(tmp_path, monkeypatch):
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(brief, "DATA", tmp_path / "briefs")
    monkeypatch.setattr(daily, "OPPORTUNITIES", tmp_path / "Opportunities.csv")
    monkeypatch.setattr(daily, "OUT", tmp_path / "email.json")
    monkeypatch.setattr(daily, "SEEN", tmp_path / "seen.json")
    monkeypatch.setattr(daily, "STEPS", tmp_path / "steps")
    monkeypatch.setattr(daily, "FRAGMENTS", tmp_path / "Fragments.csv")
    (tmp_path / "briefs").mkdir()
    (tmp_path / "steps").mkdir()
    (tmp_path / "Picks.csv").write_text("date,topic,first_step\n2026-11-23,flow policies,https://arxiv.org/abs/1\n")
    (tmp_path / "briefs" / "2026-11-23.json").write_text(json.dumps({"early": [
        {"topic": "flow policies", "score": 3}, {"topic": "b", "score": 2.5}, {"topic": "c", "score": 2},
        {"topic": "d", "score": 1.8}, {"topic": "e", "score": 1}]}))
    (tmp_path / "steps" / "2026-11-23.json").write_text(json.dumps(
        {"pick": "flow policies", "pieces": {str(TUE): "Read section 1."}}))
    (tmp_path / "Opportunities.csv").write_text(
        "date,type,name,deadline,url,checked_on\n"
        "2026-11-23,fellowship,Soon,2026-12-01,https://a,2026-11-23\n"
        "2026-11-23,job,Rolling,rolling,https://b,2026-11-23\n"
        "2026-11-23,grant,Far,2027-03-01,https://c,2026-11-23\n")
    return tmp_path


def fetch_map(by_phrase):
    return lambda url: next((f for p, f in by_phrase.items() if p.replace(" ", "%20") in url), EMPTY)


def test_watches_the_pick_then_the_top_early_topics(paths):
    assert daily.watched(TUE) == ["flow policies", "b", "c", "d"]


def test_quiet_day_sends_nothing(paths):
    e = daily.compose(SAT, "https://site", lambda url: EMPTY)
    assert e["send"] is False and e["subject"] == ""


def test_tuesday_gets_its_step_and_the_site_link_rides_along(paths):
    e = daily.compose(TUE, "https://site", lambda url: EMPTY)
    assert e["send"] and "today's step" in e["subject"] and "Read section 1." in e["text"]
    assert "https://site" in e["text"]


def test_no_step_on_saturday_even_if_written(paths):
    (paths / "steps" / "2026-11-23.json").write_text(json.dumps({"pieces": {str(SAT): "x"}}))
    assert daily.todays_step(SAT) == ""


def test_deadline_reminders_only_on_14_7_3_1_days(paths):
    assert [r["name"] for r in daily.deadlines(date(2026, 11, 24))] == ["Soon"]      # 7 days
    assert daily.deadlines(date(2026, 11, 25)) == []                                  # 6 days
    assert daily.deadlines(date(2026, 11, 30))[0]["days"] == 1


def test_new_papers_once_and_only_after_a_send(paths):
    f = fetch_map({"flow policies": feed(("2611.00001", "A flow paper"), ("2611.00002", "Another"))})
    e = daily.compose(SAT, "", f)
    assert e["send"] and "2 new papers" in e["subject"] and "(this week's pick)" in e["text"]
    assert daily.compose(SAT, "", f)["send"]          # not sent yet, so still new
    daily.mark_sent()
    assert daily.compose(SAT, "", f)["send"] is False


def test_a_paper_under_two_topics_shows_once(paths):
    f = fetch_map({"flow policies": feed(("2611.00001", "Shared")), "b": feed(("2611.00001", "Shared"))})
    e = daily.compose(SAT, "", f)
    assert e["paper_ids"] == ["2611.00001"] and e["subject"].endswith("1 new paper")


def test_long_lists_are_cut_to_three(paths):
    f = fetch_map({"flow policies": feed(*[(f"2611.0000{i}", f"P{i}") for i in range(5)])})
    e = daily.compose(SAT, "", f)
    assert "and 2 more" in e["text"] and len(e["paper_ids"]) == 5


def test_titles_are_escaped_in_html(paths):
    f = fetch_map({"flow policies": feed(("2611.00001", "x &lt;script&gt;"))})
    assert "<script>" not in daily.compose(SAT, "", f)["html"]


def test_no_pick_still_watches_early_topics(paths):
    (paths / "Picks.csv").write_text("date,topic,first_step\n")
    assert daily.watched(TUE) == ["flow policies", "b", "c", "d"] and daily.todays_step(TUE) == ""


def test_fragments_are_never_watched(paths):
    (paths / "Fragments.csv").write_text("phrase,added,reason\nb,2026-11-19,fragment\n")
    assert daily.watched(TUE) == ["flow policies", "c", "d", "e"]
