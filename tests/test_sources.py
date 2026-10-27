import json
from datetime import date
from pathlib import Path

from bleedingedge.sources import arxiv, funding, github, hackernews

FIX = Path(__file__).parent / "fixtures"


def test_arxiv_parse_real_page():
    total, items = arxiv.parse((FIX / "arxiv_page.xml").read_text())
    assert total == 6 and len(items) == 3
    assert "2303.04137" in items  # Chi et al., Diffusion Policy; version suffix stripped
    assert items["2303.04137"] == date(2023, 3, 7)


def test_arxiv_parse_empty():
    assert arxiv.parse((FIX / "arxiv_empty.xml").read_text()) == (0, {})


def test_arxiv_query_url_has_phrase_and_dates():
    url = arxiv.query_url("diffusion policy", date(2021, 1, 4), date(2025, 12, 29))
    assert "%22diffusion%20policy%22" in url and "202101040000" in url and "202512292359" in url


def test_hn_parse_real_page():
    data = json.loads((FIX / "hn_page.json").read_text())
    total, items = hackernews.parse(data)
    assert total >= len(items) == 3
    assert all(isinstance(d, date) for d in items.values())
    assert hackernews.parse({}) == (0, {})


def test_hn_query_is_exact_title_phrase():
    url = hackernews.query_url("GRPO", date(2021, 1, 4), date(2025, 12, 29))
    assert "typoTolerance=false" in url and "restrictSearchableAttributes=title" in url
    assert "%22GRPO%22" in url and "points%3E%3D50" in url


def test_github_parse_real_page():
    data = json.loads((FIX / "github_page.json").read_text())
    total, items = github.parse(data)
    assert total >= len(items) == 3
    assert all(date(2023, 1, 1) <= d <= date(2023, 3, 31) for d in items.values())


def test_github_query_end_is_inclusive_day_before():
    url = github.query_url("diffusion policy", date(2023, 1, 1), date(2024, 1, 1))
    assert "2023-01-01..2023-12-31" in url.replace("%3A", ":").replace("..", "..")


def test_funding_filters_topic_and_range(tmp_path):
    p = tmp_path / "Funding.csv"
    p.write_text(
        "topic,company,announced,amount_usd,round,source_url,note\n"
        "vla,A,2024-03-12,70000000,Seed,https://x,\n"
        "vla,B,2026-01-05,,Series A,https://y,\n"
        "grpo_rlvr,C,2025-02-01,,Seed,https://z,\n"
    )
    assert funding.dates("vla", date(2021, 1, 4), date(2025, 12, 29), p) == [date(2024, 3, 12)]
    assert funding.dates("vla", date(2021, 1, 4), date(2025, 12, 29), tmp_path / "missing.csv") == []


def test_arxiv_bulk_parse_keeps_categories_and_dates(monkeypatch):
    from datetime import date
    from bleedingedge.sources import arxiv_bulk
    xml = (FIX / "oai_page.xml").read_text()
    recs, token = arxiv_bulk.parse(xml)
    assert recs == []  # all 3 were created before 2021
    assert token and "skip" in token
    monkeypatch.setattr(arxiv_bulk, "SINCE", date(2020, 1, 1))
    recs, _ = arxiv_bulk.parse(xml)
    # 2020-12-30 cs.LG paper kept; the cs.DM/math paper dropped by category
    assert [r["id"] for r in recs] == ["1706.09520"]
    assert recs[0]["created"] == "2020-12-30" and "  " not in recs[0]["title"]
