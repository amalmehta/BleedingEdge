"""The website's data: four JSON files built from the weekly briefs, for the BleedingEdge Radar page.

    uv run python -m bleedingedge.site            # writes site/*.json (gitignored build output)

The page (a private claude.ai dashboard) draws everything from these files, so every number on it
can be traced back here and from here to the repo's data:

  topics.json   one row per topic flagged in any brief (heating or early), with its latest numbers
  series.json   papers and new repos per 4-week window, about 3 years, from the latest brief that
                flagged the topic (only flagged topics have this history saved)
  scores.json   each covered topic's score in every brief since 27 Oct 2026 (data/Trends.csv)
  picks.json    every study pick with its ledger grade (data/Picks.csv) and the brief's own words
  record.json   the backtest's track record the brief leads with, read from the round-2 result files

Each file is {"rows": [...], "meta": [...]}; meta carries this script's text and its inputs, so a
reader can check how a number was made. Nothing here changes a number: it only reshapes.
"""
import csv
import json
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from . import brief as br
from .windows import WINDOW_DAYS

OUT = br.ROOT / "site"
REPO = "https://github.com/amalmehta/BleedingEdge/blob/main"
SMALL = 30          # the brief's "consensus" line: 30+ bulk papers in 12 weeks (backtest.LOCAL_SMALL_MAX)


def briefs() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(br.DATA.glob("20*.json"))]


def picks() -> list[dict]:
    if not br.PICKS.exists():
        return []
    with br.PICKS.open(newline="") as f:
        return list(csv.DictReader(f))


def what_it_is(day: str) -> str:
    """The first sentence of the pick's "What it is" paragraph, as the brief wrote it."""
    path = br.BRIEFS / f"{day}.md"
    if not path.exists():
        return ""
    m = re.search(r"\*\*What it is\.\*\*\s*(.+)", path.read_text())
    if not m:
        return ""
    s = re.split(r"(?<=[.!?])\s+(?=[A-Z\"(])", m[1].strip(), maxsplit=1)[0]
    return s


def _num(v):
    return None if v is None else round(float(v), 3)


def record() -> list[dict]:
    """The same counts brief.record() prints: robotics phrases new in 2024, both halves."""
    flagged = hit = took_off = judged = 0
    for path in (br.LEAD_FROM, br.LEAD_FROM.parent / "Holdout" / "Summary.json"):
        d = json.loads(path.read_text())
        flagged += d["precision"]["tuned"]["topics_flagged"]
        hit += d["precision"]["tuned"]["topics_hit"]
        took_off += d["candidates"]["crowd_in_judged_year_or_later"]
        judged += d["candidates"]["judged"]
    return [{"flagged": flagged, "took_off": hit, "candidates": judged, "took_off_any": took_off}]


def build() -> dict[str, list[dict]]:
    bs = briefs()
    if not bs:
        return {"topics": [], "series": [], "scores": [], "picks": [], "record": record()}
    latest = bs[-1]["date"]
    picked = {p["topic"]: p["date"] for p in picks()}
    seen: dict[str, tuple[dict, dict]] = {}          # topic -> (its latest record, that brief)
    for b in bs:
        for r in b.get("heating", []) + b.get("early", []):
            seen[r["topic"]] = (r, b)
    topics, series = [], []
    for g, (r, b) in sorted(seen.items(), key=lambda kv: (kv[1][1]["date"] != latest, -(kv[1][0].get("score") or 0))):
        day = date.fromisoformat(b["date"])
        early, heating = bool(r.get("early")), bool(r.get("heating"))
        papers, repos = sum(r["arxiv"][-3:]), sum(r.get("github", [])[-3:])
        status = ("Not flagged this week" if b["date"] != latest else "Early" if early
                  else "Consensus" if heating and papers >= SMALL else "Heating")
        topics.append({
            "topic": g, "status": status, "last_flagged": b["date"], "score": _num(r.get("score")),
            "papers_12w": papers, "repos_12w": repos,
            "papers_vs_year_ago": _num(r.get("g_trend_arxiv")), "repos_vs_year_ago": _num(r.get("g_trend_github")),
            "first_flagged": r.get("first_flag") or "", "picked_on": picked.get(g, ""),
            "papers_link": br.arxiv_search_url(g),
            "repos_link": br.github_search_url(g, day - timedelta(days=3 * WINDOW_DAYS), day)})
        start = date.fromisoformat(b["grid_start"])
        for k, n in enumerate(r["arxiv"]):
            end = start + timedelta(days=WINDOW_DAYS * (k + 1) - 1)
            series.append({"topic": g, "window_end": end.isoformat(), "papers": n,
                           "new_repos": r["github"][k] if "github" in r else None})
    covered = set(seen)
    scores = []
    if br.TRENDS.exists():
        with br.TRENDS.open(newline="") as f:
            for r in csv.DictReader(f):
                if r["topic"] in covered and r["score"]:
                    scores.append({"date": r["date"], "topic": r["topic"], "score": _num(r["score"]),
                                   "papers_12w": int(r["arxiv_12w"])})
    prows = [{"date": p["date"], "topic": p["topic"], "what_it_is": what_it_is(p["date"]),
              "first_step": p["first_step"], "brief": f"{REPO}/briefs/{quote(p['date'])}.md",
              "papers_when_picked": int(p["papers_12w"]) if p.get("papers_12w") else None,
              "bar": int(p["bar"]) if p.get("bar") else None, "due": p.get("due") or "",
              "peak_12w": int(p["peak_12w"]) if p.get("peak_12w") else None,
              "status": p.get("status") or "open", "graded_on": p.get("checked_on") or ""}
             for p in picks()]
    return {"topics": topics, "series": series, "scores": scores, "picks": prows, "record": record()}


def write(out: Path = OUT) -> dict[str, Path]:
    out.mkdir(parents=True, exist_ok=True)
    code = Path(__file__).read_text()
    inputs = {"topics": "data/briefs/*.json, data/Picks.csv", "series": "data/briefs/*.json",
              "scores": "data/Trends.csv", "picks": "data/Picks.csv, briefs/*.md",
              "record": "data/backtest/Run2024RO/Summary.json, data/backtest/Run2024RO/Holdout/Summary.json"}
    paths = {}
    for name, rows in build().items():
        p = out / f"{name}.json"
        p.write_text(json.dumps({"rows": rows, "meta": [
            {"label": "site.py", "value": code, "type": "code", "lang": "python"},
            {"label": "Input", "value": inputs[name]},
            {"label": "Built", "value": date.today().isoformat()}]}, ensure_ascii=False))
        paths[name] = p
    return paths


if __name__ == "__main__":
    for name, p in write().items():
        print(f"{p.relative_to(br.ROOT)}: {len(json.loads(p.read_text())['rows'])} rows, {p.stat().st_size // 1024} KB")
