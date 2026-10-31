import csv
from datetime import date, timedelta

from bleedingedge import brief
from bleedingedge.windows import counts

DAY = date(2026, 10, 27)


def _p(i, d, title):
    return {"id": f"x{i}", "created": d.isoformat(), "title": title, "abstract": "", "cats": ["cs.RO"]}


def _corpus():
    ps = []
    d = date(2023, 6, 1)
    while d < DAY:  # one filler paper a day, all stopwords, so arXiv's total stays flat
        ps.append(_p(len(ps), d, "on the of a"))
        d += timedelta(days=1)
    for i in range(10):  # new in 2025, then quiet, then a burst in the last 4 weeks
        ps.append(_p(len(ps), date(2025, 3, 1) + timedelta(days=i), f"Magnetic skin gripper {i}"))
    for k, n in ((3, 2), (2, 2), (1, 2), (0, 12)):
        end = DAY - timedelta(days=28 * k)
        ps += [_p(len(ps), end - timedelta(days=j + 1), "magnetic skin gripper again") for j in range(n)]
    return ps


def test_counts_on_a_moved_grid():
    start = date(2026, 1, 5)
    assert counts([date(2026, 1, 5), date(2026, 2, 1), date(2026, 2, 2), date(2025, 12, 31)], start, 2) == [2, 1]


def test_brief_flags_a_new_bursting_phrase_and_skips_recent_picks(tmp_path, monkeypatch):
    for name in ("BRIEFS", "DATA"):
        monkeypatch.setattr(brief, name, tmp_path / name.lower())
    monkeypatch.setattr(brief, "TRENDS", tmp_path / "Trends.csv")
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(brief.arxiv_bulk, "papers", _corpus)
    gh = [DAY - timedelta(days=28 * k + 3) for k in (1, 2, 3)] + [DAY - timedelta(days=j + 1) for j in range(12)]
    monkeypatch.setattr(brief.github, "dates", lambda phrases, start, end: gh)

    out = brief.main(DAY, update=False, log=lambda *_: None)
    text = out.read_text()
    assert "flagged topics" in text and "failed the 50% bar" in text and "<!-- pick:start -->" in text
    assert "**magnetic skin gripper**" in text.split("## Early")[1]
    assert "magnetic skin gripper" in text.split("<!-- pick:end -->")[0]  # on the shortlist
    rows = list(csv.DictReader((tmp_path / "Trends.csv").open()))
    assert [r["early"] for r in rows if r["topic"] == "magnetic skin gripper"] == ["True"]

    # Picked last week: still listed as early, but not offered again as the study pick.
    (tmp_path / "Picks.csv").write_text("date,topic,first_step\n2026-10-20,magnetic skin gripper,x\n")
    text = brief.main(DAY, update=False, log=lambda *_: None).read_text()
    pick = text.split("<!-- pick:start -->")[1].split("<!-- pick:end -->")[0]
    assert "Left out as repeats of recent picks: magnetic skin gripper" in pick
    assert "No early robotics topic this week" in pick
    assert len(list(csv.DictReader((tmp_path / "Trends.csv").open()))) == len(rows)  # re-run replaced its day


def test_rerun_keeps_a_written_pick_and_refreshes_the_rest(tmp_path, monkeypatch):
    for name in ("BRIEFS", "DATA"):
        monkeypatch.setattr(brief, name, tmp_path / name.lower())
    monkeypatch.setattr(brief, "TRENDS", tmp_path / "Trends.csv")
    monkeypatch.setattr(brief, "PICKS", tmp_path / "Picks.csv")
    monkeypatch.setattr(brief.arxiv_bulk, "papers", _corpus)
    monkeypatch.setattr(brief.github, "dates", lambda phrases, start, end: [])

    out = brief.main(DAY, update=False, log=lambda *_: None)
    draft = out.read_text()
    pick = "**Pick: magnetic skin gripper.** Written by the weekly task."
    written = draft.split(brief.PICK_START)[0] + brief.PICK_START + "\n" + pick + "\n" + brief.PICK_END \
        + draft.split(brief.PICK_END)[1].replace("## Early / speculative", "## Early / speculative (stale)")
    out.write_text(written)

    text = brief.main(DAY, update=False, log=lambda *_: None).read_text()
    assert pick in text and "_Not written yet." not in text
    assert "(stale)" not in text  # everything outside the markers is regenerated


def test_keep_pick_replaces_an_unwritten_draft():
    new = f"a\n{brief.PICK_START}\nnew shortlist\n{brief.PICK_END}\nb\n"
    old = f"x\n{brief.PICK_START}\n_Not written yet._ old shortlist\n{brief.PICK_END}\ny\n"
    assert brief.keep_pick(old, new) == new
    assert brief.keep_pick("no markers", new) == new


def test_render_labels_ratios_and_reads_the_all_categories_figure():
    text = brief.render(DAY, 1, [], {}, DAY, [], [], None)
    assert "repo ratios are raw GitHub counts" in text
    assert "scored about random in the backtest (on held-out phrases, 1 of 14 flagged topics took off, 7%, against 6% at random)" in text
