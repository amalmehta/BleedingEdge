import json

import pytest

from bleedingedge import harness

GOOD_WHAT = ("Robots that learn to move their whole body by practising in a computer simulation first, "
             "then carry what they learned into the real world. Researchers test them on walking, "
             "lifting boxes and opening doors.")
GOOD_WHY = ("If it works, the same robot could help in a warehouse one week and a kitchen the next, "
            "without engineers writing new code for each job. That is why many labs are trying it "
            "now, though most results are still early.")


@pytest.fixture
def ex(tmp_path, monkeypatch):
    path = tmp_path / "Explainers.json"
    monkeypatch.setattr(harness, "EXPLAINERS", path)

    def write(**topics):
        path.write_text(json.dumps(topics))
    return write


def entry(what=GOOD_WHAT, why=GOOD_WHY, sources=({"url": "https://arxiv.org/abs/2611.12286", "title": "x"},)):
    return {"what": what, "why": why, "sources": list(sources)}


def test_grade_matches_a_known_example():
    # "The cat sat on the mat." : 6 words, 1 sentence, 6 syllables -> 0.39*6 + 11.8*1 - 15.59 = -1.45
    assert harness.grade("The cat sat on the mat.") == pytest.approx(-1.45, abs=0.01)
    assert harness.grade("Interdisciplinary reinforcement methodologies necessitate considerable computational infrastructure.") > 15


def test_a_good_explainer_passes(ex):
    ex(**{"whole body control": entry()})
    ok, detail = harness.check_explainers(offline=True)
    assert ok, detail


def test_numbers_in_prose_fail_but_not_in_the_topic_name(ex):
    ex(**{"feed-forward 3d": entry(what=GOOD_WHAT + " About 40 papers came out.")})
    ok, detail = harness.check_explainers(offline=True)
    assert not ok and "['40']" in detail and "3" not in detail.split("numbers")[1].split("]")[0].replace("40", "")


def test_missing_sources_and_http_links_fail(ex):
    ex(a=entry(sources=()), b=entry(sources=({"url": "http://example.com", "title": "x"},)))
    ok, detail = harness.check_explainers(offline=True)
    assert not ok and "a: no sources" in detail and "not https" in detail


def test_too_short_fails(ex):
    ex(a=entry(why="Short."))
    ok, detail = harness.check_explainers(offline=True)
    assert not ok and "a/why: 1 words" in detail


def test_hype_is_caught_as_a_whole_word(ex):
    ex(a=entry(why=GOOD_WHY + " A true breakthrough."), b=entry(why=GOOD_WHY.replace("early", "unbroken")))
    ok, detail = harness.check_no_hype(offline=True)
    assert not ok and "explainer: a: 'breakthrough'" in detail and "explainer: b" not in detail


def test_hard_reading_fails(ex):
    hard = ("Contemporaneous methodological interdisciplinarity necessitates substantially "
            "reconceptualized computational infrastructures for embodied generalization. ") * 3
    ex(a=entry(what=hard))
    ok, detail = harness.check_reading_level(offline=True)
    assert not ok and "explainer: a" in detail


def test_the_real_project_passes_offline():
    res = harness.run(offline=True, only=["page_scripts", "site_data", "caveat", "no_hype", "reading_level", "private"])
    assert all(r["passed"] for r in res.values()), res
