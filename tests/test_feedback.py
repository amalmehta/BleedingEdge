from datetime import date

import pytest

from bleedingedge import brief, feedback


@pytest.fixture(autouse=True)
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(feedback, "FEEDBACK", tmp_path / "private" / "Feedback.csv")


def test_link_subjects_parse_and_others_dont():
    assert feedback.parse_subject("BleedingEdge feedback: less · Grasp  Planning") == ("less", "grasp planning")
    assert feedback.parse_subject("Re: BleedingEdge feedback: more · flow policies") == ("more", "flow policies")
    assert feedback.parse_subject("Re: BleedingEdge, 24 Nov: 3 new papers") is None
    assert feedback.parse_subject("BleedingEdge feedback: maybe · x") is None


def test_mailto_round_trips_through_the_subject():
    from urllib.parse import parse_qs, urlparse
    u = urlparse(feedback.mailto("me@example.com", "less", "sim-to-real & co"))
    assert u.path == "me@example.com"
    assert feedback.parse_subject(parse_qs(u.query)["subject"][0]) == ("less", "sim-to-real & co")


def test_same_message_counts_once():
    assert feedback.add("2026-11-24", "m1", "more", "x")
    assert not feedback.add("2026-11-24", "m1", "more", "x")
    assert feedback.net() == {"x": 1}


def test_bad_votes_are_refused():
    with pytest.raises(ValueError):
        feedback.add("2026-11-24", "m1", "love", "x")
    with pytest.raises(ValueError):
        feedback.add("2026-11-24", "m1", "more", "")
    assert feedback.add("2026-11-24", "m1", "note", "", "fewer survey papers please")
    assert feedback.net() == {}


def test_net_votes_mute_unmute_and_boost():
    feedback.add("2026-11-20", "a", "less", "x")
    assert feedback.muted() == {"x"}
    feedback.add("2026-11-22", "b", "more", "x")
    feedback.add("2026-11-23", "c", "more", "x")
    assert feedback.muted() == set() and feedback.wanted() == ["x"]
    assert feedback.boost("x") == 0.5
    assert feedback.boost("x", date(2026, 11, 21)) == 0 and feedback.muted(date(2026, 11, 21)) == {"x"}


def test_shortlist_drops_muted_and_reranks_by_boost_without_changing_scores():
    feedback.add("2026-11-23", "a", "less", "top")
    feedback.add("2026-11-23", "b", "more", "fourth")
    feedback.add("2026-11-23", "c", "more", "fourth")
    cands = [{"topic": t, "score": s} for t, s in [("top", 3), ("second", 2.5), ("third", 2.2), ("fourth", 1.6)]]
    top, n_muted, n_boosted = brief.taste_order(cands, date(2026, 11, 23))
    assert [r["topic"] for r in top] == ["fourth", "second", "third"]
    assert [r["score"] for r in top] == [1.6, 2.5, 2.2] and (n_muted, n_boosted) == (1, 1)
    # votes after the brief's day don't count
    assert brief.taste_order(cands, date(2026, 11, 22))[0][0]["topic"] == "top"
