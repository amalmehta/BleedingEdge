"""Candidate topics mined from arXiv titles, so nobody picks them.

    uv run python -m bleedingedge.mining              # phrases new in 2023 -> data/CandidatesMined2023.csv
    uv run python -m bleedingedge.mining 2024         # phrases new in 2024
    uv run python -m bleedingedge.mining 2024 --ro    # robotics only: cs.RO titles

A candidate is a 2–3-word phrase that appears in at least MIN_TITLES titles in the year (cs.RO,
cs.LG, cs.AI, cs.CL; cs.RO only with --ro) and in fewer than PRIOR_MAX papers (title or
abstract, all four categories) in the two years before. That is the set a detector running at
the start of the next year could see as "new", winners and duds alike. Only data up to the end
of the year picks the candidates; later years are used only to count and grade.

Phrases are matched on whole words; hyphenated compounds count as one word, so
"vision-language-action" and "vision language action" are different phrases.
"""
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from .windows import counts

ROOT = Path(__file__).resolve().parent.parent
OUT_TOTALS = ROOT / "data" / "backtest" / "ArxivTotals.json"  # all harvested papers per window

YEAR = 2023
MIN_TITLES = 8      # invented: recurs enough to be a topic, not a one-off title (scaled down for --ro)
PRIOR_MAX = 10      # invented: the same bar as the newness test in "early"
SUBSUME = 0.8       # drop "segment anything" in favour of "segment anything model" if the longer one covers 80% of it

# Words a topic phrase can't start or end with.
STOP = set("""a an the of for in on to and or with without via by from at as into over under using based
towards toward is are be can do does how what when why which we our your its their this that these those
new novel study analysis paper case towards beyond through across between than vs versus not no more less
all any each""".split())

# Title boilerplate: can't start a phrase ("leveraging large language ...") or end one ("reasoning in large ...").
START_STOP = set("""leveraging unleashing evaluating evaluation enhancing improving exploring rethinking revisiting
understanding scoping augmented empowering harnessing investigating assessing benchmarking prompting
unlocking making applications learning framework network networks transformer transformers model models
method approach data""".split())
END_STOP = set("""large deep neural review survey efficient enhanced multi zero""".split())
OLD_COMMON = 100    # a 3-word phrase whose 2-word half was this common in 2021–22 is a fragment of an old phrase

# Phrases that overlap the 3 test topics, which are graded separately in (a).
TEST_OVERLAP = re.compile(r"diffusion polic|vision.language.action|\bvla\b|verifiable reward|group relative|\bgrpo\b|\brlvr\b")


def words(text: str) -> list[str]:
    """Lowercase ASCII words; hyphenated compounds stay whole ("few-shot", "fine-tuning"),
    because splitting them made fragments like "shot detection" and "robust fine"."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def ngrams(ws: list[str], ns=(2, 3)) -> set[str]:
    out = set()
    for n in ns:
        for i in range(len(ws) - n + 1):
            g = ws[i:i + n]
            if g[0] in STOP or g[-1] in STOP or g[0] in START_STOP or g[-1] in END_STOP:
                continue
            if any(w.isdigit() and (len(w) == 4 or w in (g[0], g[-1])) for w in g):  # years, numbers at the edges
                continue
            if any(len(w) < 2 for w in g):
                continue
            out.add(" ".join(g))
    return out


def _year(p: dict) -> int:
    return int(p["created"][:4])


def outputs(year: int = YEAR, ro: bool = False) -> tuple[Path, Path]:
    tag = f"{year}{'RO' if ro else ''}"
    return ROOT / "data" / f"CandidatesMined{tag}.csv", ROOT / "data" / "backtest" / f"MinedArxivCounts{tag}.json"


def ro_min_titles(papers: list[dict], year: int) -> int:
    """MIN_TITLES scaled by cs.RO's share of the year's papers, at least 3: the same bar relative to volume."""
    ys = [p for p in papers if _year(p) == year]
    return max(3, round(MIN_TITLES * sum("cs.RO" in p["cats"] for p in ys) / len(ys)))


def mine(papers: list[dict], year: int = YEAR, ro: bool = False, min_titles: int = MIN_TITLES) -> tuple[list[dict], list[str]]:
    """Returns (candidates, phrases dropped for overlapping the test topics)."""
    title_df = Counter()
    cats_by = defaultdict(Counter)
    for p in papers:
        if _year(p) != year or (ro and "cs.RO" not in p["cats"]):
            continue
        for g in ngrams(words(p["title"])):
            title_df[g] += 1
            for c in p["cats"]:
                cats_by[g][c] += 1
    pool = {g for g, n in title_df.items() if n >= min_titles}
    halves = {h for g in pool if g.count(" ") == 2 for h in (g.rsplit(" ", 1)[0], g.split(" ", 1)[1])}

    prior = Counter()
    for p in papers:
        if _year(p) in (year - 2, year - 1):
            for g in ngrams(words(p["title"] + " " + p["abstract"])) & (pool | halves):
                prior[g] += 1
    new = {g for g in pool if prior[g] < PRIOR_MAX
           and not (g.count(" ") == 2 and max(prior[g.rsplit(" ", 1)[0]], prior[g.split(" ", 1)[1]]) >= OLD_COMMON)}

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
        robot = ro or cats_by[g]["cs.RO"] / n >= 0.3 or re.search(r"\b(robot|reinforcement|policy|policies|manipulation)", g)
        rows.append({"topic": g, "arxiv_phrases": g, "domain": "rl_robotics" if robot else "ai_tooling",
                     "first_year": year, "titles_in_year": n, "prior_two_years": prior[g],
                     "source_urls": f"arXiv OAI-PMH bulk metadata ({'cs.RO titles' if ro else 'cs.RO, cs.LG, cs.AI, cs.CL'})"})
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


def main(year: int = YEAR, ro: bool = False) -> None:
    from .sources import arxiv_bulk
    papers = arxiv_bulk.papers()
    min_titles = ro_min_titles(papers, year) if ro else MIN_TITLES
    rows, dropped = mine(papers, year, ro, min_titles)
    by_year = Counter(_year(p) for p in papers)
    out_csv, out_counts = outputs(year, ro)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    out_counts.parent.mkdir(parents=True, exist_ok=True)
    dates = phrase_dates(papers, [r["topic"] for r in rows])
    out_counts.write_text(json.dumps({g: counts(ds) for g, ds in dates.items()}))
    OUT_TOTALS.write_text(json.dumps(counts([date.fromisoformat(p["created"]) for p in papers])))
    print(json.dumps({"year": year, "ro": ro, "min_titles": min_titles,
                      "papers_by_year": dict(sorted(by_year.items())), "candidates": len(rows),
                      "dropped_test_overlap": dropped}, indent=1))


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(int(args[0]) if args else YEAR, "--ro" in sys.argv)
