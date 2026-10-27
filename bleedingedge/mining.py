"""Candidate topics mined from arXiv titles, so nobody picks them.

    uv run python -m bleedingedge.mining   # after the bulk harvest; writes data/CandidatesMined2023.csv

A candidate is a 2–3-word phrase that appears in at least MIN_TITLES 2023 titles (cs.RO, cs.LG,
cs.AI, cs.CL) and in fewer than PRIOR_MAX 2021–22 papers (title or abstract). That is the set
a detector running at the start of 2024 could see as "new", winners and duds alike.
Only data up to the end of 2023 picks the candidates; 2024–25 is used only to count and grade.

Phrases are matched on words, with hyphens split, so "vision-language-action" and
"vision language action" count as the same phrase ("in-context" stays whole).
"""
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from .windows import counts

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "CandidatesMined2023.csv"
OUT_COUNTS = ROOT / "data" / "backtest" / "MinedArxivCounts.json"

YEAR = 2023
MIN_TITLES = 8      # invented: recurs enough to be a topic, not a one-off title
PRIOR_MAX = 10      # invented: the same bar as the newness test in "early"
SUBSUME = 0.8       # drop "segment anything" in favour of "segment anything model" if the longer one covers 80% of it

# Words a topic phrase can't start or end with.
STOP = set("""a an the of for in on to and or with without via by from at as into over under using based
towards toward is are be can do does how what when why which we our your its their this that these those
new novel study analysis paper case towards beyond through across between than vs versus not no more less
all any each""".split())

# Phrases that overlap the 3 test topics, which are graded separately in (a).
TEST_OVERLAP = re.compile(r"diffusion polic|vision language action|\bvla\b|verifiable reward|group relative|\bgrpo\b|\brlvr\b")


def words(text: str) -> list[str]:
    """Lowercase words with hyphens split, except compounds with a stopword part
    ("in-context" stays one word, so it can start a phrase)."""
    out = []
    for tok in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower()):
        parts = tok.split("-")
        out.extend([tok] if len(parts) > 1 and any(x in STOP for x in parts) else parts)
    return out


def ngrams(ws: list[str], ns=(2, 3)) -> set[str]:
    out = set()
    for n in ns:
        for i in range(len(ws) - n + 1):
            g = ws[i:i + n]
            if g[0] in STOP or g[-1] in STOP or any(w.isdigit() for w in (g[0], g[-1])):
                continue
            if any(len(w) < 2 for w in g):
                continue
            out.add(" ".join(g))
    return out


def _year(p: dict) -> int:
    return int(p["created"][:4])


def mine(papers: list[dict]) -> tuple[list[dict], list[str]]:
    """Returns (candidates, phrases dropped for overlapping the test topics)."""
    title_df = Counter()
    cats_by = defaultdict(Counter)
    for p in papers:
        if _year(p) != YEAR:
            continue
        for g in ngrams(words(p["title"])):
            title_df[g] += 1
            for c in p["cats"]:
                cats_by[g][c] += 1
    pool = {g for g, n in title_df.items() if n >= MIN_TITLES}

    prior = Counter()
    for p in papers:
        if _year(p) in (YEAR - 2, YEAR - 1):
            for g in ngrams(words(p["title"] + " " + p["abstract"])) & pool:
                prior[g] += 1
    new = {g for g in pool if prior[g] < PRIOR_MAX}

    # A shorter phrase mostly seen inside a longer candidate is the same topic.
    keep = set(new)
    for g in new:
        for h in new:
            if h != g and f" {g} " in f" {h} " and title_df[h] >= SUBSUME * title_df[g]:
                keep.discard(g)
                break

    dropped = sorted(g for g in keep if TEST_OVERLAP.search(g))
    rows = []
    for g in sorted(keep - set(dropped), key=lambda g: (-title_df[g], g)):
        n = title_df[g]
        robot = cats_by[g]["cs.RO"] / n >= 0.3 or re.search(r"\b(robot|reinforcement|policy|policies|manipulation)", g)
        rows.append({"topic": g, "arxiv_phrases": g, "domain": "rl_robotics" if robot else "ai_tooling",
                     "first_year": YEAR, "titles_2023": n, "prior_2021_22": prior[g],
                     "source_urls": "arXiv OAI-PMH bulk metadata (cs.RO, cs.LG, cs.AI, cs.CL)"})
    return rows, dropped


def phrase_dates(papers: list[dict], phrases: list[str]) -> dict[str, list[date]]:
    """Creation dates of papers whose title or abstract contains each phrase (word match)."""
    want = set(phrases)
    out: dict[str, list[date]] = {g: [] for g in phrases}
    for p in papers:
        hits = ngrams(words(p["title"] + " " + p["abstract"])) & want
        if hits:
            d = date.fromisoformat(p["created"])
            for g in hits:
                out[g].append(d)
    return out


def main() -> None:
    from .sources import arxiv_bulk
    papers = arxiv_bulk.papers()
    rows, dropped = mine(papers)
    by_year = Counter(_year(p) for p in papers)
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    OUT_COUNTS.parent.mkdir(parents=True, exist_ok=True)
    dates = phrase_dates(papers, [r["topic"] for r in rows])
    OUT_COUNTS.write_text(json.dumps({g: counts(ds) for g, ds in dates.items()}))
    print(json.dumps({"papers_by_year": dict(sorted(by_year.items())), "candidates": len(rows),
                      "dropped_test_overlap": dropped}, indent=1))


if __name__ == "__main__":
    main()
