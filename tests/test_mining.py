from datetime import date

from bleedingedge import mining as mn


def _p(y, title, abstract="", cats=("cs.LG",)):
    return {"created": f"{y}-03-01", "title": title, "abstract": abstract, "cats": list(cats)}


def test_words_split_hyphens_and_ngrams_skip_stopwords():
    assert mn.words("Vision-Language-Action Models!") == ["vision-language-action", "models"]
    g = mn.ngrams(mn.words("towards in-context learning for few-shot robots"))
    assert "in-context learning" in g and "few-shot robots" in g and "shot robots" not in g
    assert not any(x.startswith("towards") or x.endswith(" for") for x in g)


def _corpus():
    ps = []
    ps += [_p(2023, f"Segment anything model for task {i}") for i in range(10)]      # new in 2023
    ps += [_p(2023, f"Graph neural networks for case {i}") for i in range(10)]       # old topic
    ps += [_p(2022, "A study", "we use graph neural networks") for _ in range(20)]
    ps += [_p(2023, f"Rare phrase widget {i}") for i in range(3)]                   # too few titles
    ps += [_p(2023, f"Diffusion policy tricks {i}", cats=("cs.RO",)) for i in range(9)]  # test-topic overlap
    ps += [_p(2023, f"Tactile skin sensing {i}", cats=("cs.RO",)) for i in range(9)]
    return ps


def test_mine_keeps_new_recurring_phrases_only():
    rows, dropped = mn.mine(_corpus())
    got = {r["topic"]: r for r in rows}
    assert "segment anything model" in got
    assert "segment anything" not in got and "anything model" not in got  # subsumed by the 3-word phrase
    assert not any("graph neural" in g for g in got)                       # seen 20 times in 2022
    assert not any("rare phrase" in g for g in got)                        # only 3 titles
    assert dropped == ["diffusion policy tricks"] and not any("diffusion" in g for g in got)
    assert got["tactile skin sensing"]["domain"] == "rl_robotics"
    assert got["segment anything model"]["domain"] == "ai_tooling"


def test_mine_ignores_future_papers_when_choosing():
    ps = _corpus() + [_p(2025, f"Late bloomer topic {i}") for i in range(50)]
    rows, _ = mn.mine(ps)
    assert not any("late bloomer" in r["topic"] for r in rows)


def test_phrase_dates_match_title_or_abstract():
    ps = [_p(2024, "x", "uses the Segment Anything model"), _p(2025, "Segment Anything Model v2"), _p(2024, "other")]
    d = mn.phrase_dates(ps, ["segment anything model"])
    assert d["segment anything model"] == [date(2024, 3, 1), date(2025, 3, 1)]

