"""Backtest: would the method have flagged past trends before the consensus did?

    uv run python -m bleedingedge.backtest              # everything
    uv run python -m bleedingedge.backtest --tests-only # the 3 test topics, a quick look
    uv run python -m bleedingedge.backtest --tests-only --with-readme  # README check, to data/backtest/WithReadme
    uv run python -m bleedingedge.backtest --holdout    # the sealed half of the candidates: run once, at the end

Two checks, kept separate so the test topics don't grade themselves:
  (a) lead on the 3 test topics, with every lead weight at its default of 1 (untuned);
  (b) precision on 2023 workshop-title candidates during 2024, with lead weights set from (a).
      The candidates are split in half by a hash of their name. Normal runs fetch and score only
      the dev half; the held-out half is fetched only with --holdout, so it is seen once.
A baseline (arXiv growth alone) runs through the same checks.

"Consensus" here is the research crowd arriving: the first window where a topic's 12-week
arXiv count reaches 25% of its peak. It uses hindsight, but only to grade the method.
"""
import csv
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import scoring as sc
from .http import secret
from .sources import arxiv, funding, github, hackernews
from .windows import END, START, counts, windows

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "backtest"
TOP_N = 10
HORIZON = 13  # windows: "reaches consensus within 12 months"
CANDIDATES = ROOT / "data" / "Candidates2023.csv"
CUTOFF = 2023  # a candidate whose crowd arrived before this year was never new in 2024


def held_out(key: str) -> bool:
    """Fixed half of the candidates, chosen by hash so nobody picks it."""
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % 2 == 1


@dataclass
class Topic:
    key: str
    name: str
    domain: str
    arxiv: list[str]
    hn: list[str]
    github: list[str]
    is_test: bool
    sources: str = ""
    venue: str = ""
    counts: dict[str, list[int]] = field(default_factory=dict)
    gb: dict[str, list] = field(default_factory=dict)       # burst growth ratios
    gt: dict[str, list] = field(default_factory=dict)       # trend growth ratios
    rolled: dict[str, list[int]] = field(default_factory=dict)  # 12-week sums


def _split(s: str) -> list[str]:
    return [p.strip() for p in s.split("|") if p.strip()]


def _full_phrases(phrases: list[str]) -> list[str]:
    """GitHub only: drop bare acronyms like "GRPO", which match unrelated repos."""
    return [p for p in phrases if " " in p or "-" in p]


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def load_topics() -> list[Topic]:
    topics = []
    with (ROOT / "data" / "TestTopics.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            topics.append(Topic(r["key"], r["topic"], r["domain"], _split(r["arxiv_phrases"]),
                                _split(r["hn_phrases"]), _full_phrases(_split(r["github_phrases"])), True))
    if CANDIDATES.exists():
        with CANDIDATES.open(newline="") as f:
            for r in csv.DictReader(f):
                ph = _split(r["arxiv_phrases"])
                topics.append(Topic(_slug(r["topic"]), r["topic"], r["domain"].strip(), ph, ph, _full_phrases(ph),
                                    False, r.get("source_urls", ""), r.get("venue", "")))
    return topics


def fetch(t: Topic, log=print) -> None:
    log(f"  {t.name}: arxiv")
    t.counts["arxiv"] = counts(arxiv.dates(t.arxiv, START, END))
    log(f"  {t.name}: github")
    t.counts["github"] = counts(github.dates(t.github, START, END))
    log(f"  {t.name}: hn")
    t.counts["hn"] = counts(hackernews.dates(t.hn, START, END))
    if t.is_test and funding.rows():
        t.counts["funding"] = counts(funding.dates(t.key, START, END))
    t.gb = {s: sc.growth(c) for s, c in t.counts.items()}
    t.gt = {s: sc.trend(c) for s, c in t.counts.items()}
    t.rolled = {s: sc.rolling(c) for s, c in t.counts.items()}


def available_signals() -> list[str]:
    sig = ["arxiv", "github"]
    if funding.rows():
        sig.append("funding")
    # Citation and lab signals need keys; they are not fetched until the keys exist.
    return sig


def flags(t: Topic, lam: dict[str, float]) -> dict[str, list]:
    w = sc.DOMAIN_WEIGHT.get(t.domain, 0.4)
    n = len(t.counts["arxiv"])
    burst = [sc.heating_up(t.gb, t.counts, lam, w, k, "burst") for k in range(n)]
    trend = [sc.heating_up(t.gt, t.rolled, lam, w, k, "trend") for k in range(n)]
    S = []
    for k in range(n):
        vals = [v for v in (sc.mode_score(t.gb, t.counts, lam, w, k, "burst"),
                            sc.mode_score(t.gt, t.rolled, lam, w, k, "trend")) if v is not None]
        S.append(max(vals) if vals else None)
    heat = [b or tr for b, tr in zip(burst, trend)]
    early = [h and sc.early(t.counts["arxiv"], k) for k, h in enumerate(heat)]
    return {"score": S, "burst": burst, "trend": trend, "heating": heat, "early": early,
            "consensus": sc.consensus_window(t.counts["arxiv"])}


def baseline_flags(t: Topic) -> dict[str, list]:
    """arXiv growth alone, same burst/trend thresholds, ranked by its larger growth ratio."""
    c, gb, gt, r = t.counts["arxiv"], t.gb["arxiv"], t.gt["arxiv"], t.rolled["arxiv"]
    n = len(c)
    burst = [gb[k] is not None and gb[k] >= sc.BURST["g"] and c[k] >= sc.BURST["volume"]["arxiv"] for k in range(n)]
    trend = [gt[k] is not None and gt[k] >= sc.TREND["g"] and r[k] >= sc.TREND["volume"]["arxiv"] for k in range(n)]
    heat = [b or tr for b, tr in zip(burst, trend)]
    early = [h and sc.early(c, k) for k, h in enumerate(heat)]
    S = [max([v for v in (gb[k], gt[k]) if v is not None], default=None) for k in range(n)]
    return {"score": S, "burst": burst, "trend": trend, "heating": heat, "early": early,
            "consensus": sc.consensus_window(c)}


def lead_check(topics: list[Topic], fl: dict[str, dict]) -> list[dict]:
    rows = []
    for t in topics:
        f = fl[t.key]
        h, c = sc.first(f["heating"]), f["consensus"]
        mode = None if h is None else ("burst" if f["burst"][h] else "trend")
        lead = None if h is None or c is None else (c - h) * 4
        hn = sc.first([x > 0 for x in t.counts["hn"]])
        rows.append({"key": t.key, "topic": t.name, "heating_window": h, "mode": mode,
                     "consensus_window": c, "hn_first_story_window": hn,
                     "lead_weeks": lead, "passes": lead is not None and lead >= sc.LEAD_WINDOWS * 4})
    return rows


def precision(topics: list[Topic], fl: dict[str, dict], year: int = 2024) -> dict:
    """Of the top-N early flags in each window of `year`, the share whose research crowd arrives
    within the next 12 months (not before the flag). Pooled over topic-window pairs, and over topics."""
    wins = windows()
    pairs, hits, topics_flagged, topics_hit = 0, 0, set(), set()
    per_window = []
    for k, (ws, _) in enumerate(wins):
        if ws.year != year:
            continue
        flagged = [(fl[t.key]["score"][k], t) for t in topics if fl[t.key]["early"][k]]
        flagged.sort(key=lambda x: -(x[0] or 0))
        top = flagged[:TOP_N]
        h = 0
        for _, t in top:
            c = fl[t.key]["consensus"]
            hit = c is not None and k < c <= k + HORIZON
            h += hit
            topics_flagged.add(t.key)
            if hit:
                topics_hit.add(t.key)
        pairs += len(top)
        hits += h
        per_window.append({"window_start": ws.isoformat(), "flagged": len(top), "hits": h,
                           "topics": [t.key for _, t in top]})
    return {
        "pairs": pairs, "hits": hits, "precision": hits / pairs if pairs else None,
        "topics_flagged": len(topics_flagged), "topics_hit": len(topics_hit),
        "topic_precision": len(topics_hit) / len(topics_flagged) if topics_flagged else None,
        "per_window": per_window,
    }


def run(log=print, tests_only: bool = False, report: bool = True, holdout: bool = False) -> dict:
    topics = [t for t in load_topics() if t.is_test or not tests_only]
    n_all = sum(not t.is_test for t in topics)
    topics = [t for t in topics if t.is_test or held_out(t.key) == holdout]
    tests = [t for t in topics if t.is_test]
    cands = [t for t in topics if not t.is_test]
    log(f"Fetching {len(tests)} test topics and {len(cands)} candidates (cached after the first run)")
    for t in topics:
        fetch(t, log)

    sigs = available_signals()
    untuned = {s: 1.0 for s in sigs}

    # (a) lead on the test topics, untuned
    fl_a = {t.key: flags(t, untuned) for t in tests}
    lead = lead_check(tests, fl_a)

    # lead weights from each signal's own crossing on the test topics
    cons = {t.key: fl_a[t.key]["consensus"] for t in tests}
    crossings = {s: {t.key: sc.signal_crossing(t.counts[s], sc.SIGNAL_FLOOR[s])
                     for t in tests if s in t.counts} for s in sigs}
    lam_raw = sc.lead_weights(crossings, cons)
    tuned = {s: (1.0 if v is None else v) for s, v in lam_raw.items()}

    # (b) precision on candidates in 2024, untuned, tuned and baseline
    # Candidates whose crowd arrived before CUTOFF can't be hits; they are dropped from the
    # criterion, and kept in a stricter "all candidates" line for comparison.
    cutoff_k = next(k for k, (ws, _) in enumerate(windows()) if ws.year >= CUTOFF)
    crowd = {t.key: sc.consensus_window(t.counts["arxiv"]) for t in cands}
    judged = [t for t in cands if crowd[t.key] is None or crowd[t.key] >= cutoff_k]
    reachable = sum(1 for t in judged if crowd[t.key] is not None and windows()[crowd[t.key]][0].year >= 2024)
    prec = {}
    if cands:
        prec["untuned"] = precision(judged, {t.key: flags(t, untuned) for t in judged})
        prec["tuned"] = precision(judged, {t.key: flags(t, tuned) for t in judged})
        prec["baseline_arxiv_only"] = precision(judged, {t.key: baseline_flags(t) for t in judged})
        prec["tuned_all_candidates"] = precision(cands, {t.key: flags(t, tuned) for t in cands})
    lead_base = lead_check(tests, {t.key: baseline_flags(t) for t in tests})

    passes_a = sum(r["passes"] for r in lead) >= 2
    p = prec.get("tuned", {}).get("precision")
    result = {
        "window": [START.isoformat(), END.isoformat()],
        "signals": sigs,
        "missing_signals": [s for s in ("citations", "labs") if s not in sigs],
        "keys_present": {k: bool(secret(k)) for k in ("S2_API_KEY", "OPENALEX_API_KEY")},
        "lead": lead, "lead_baseline": lead_base,
        "crossings": crossings, "consensus": cons,
        "lead_weights_raw": lam_raw, "lead_weights": tuned,
        "precision": prec,
        "passes": {"a_lead": passes_a, "b_precision": p is not None and p >= 0.5},
        "candidates": {"file": CANDIDATES.name, "half": "holdout" if holdout else "dev",
                       "total_both_halves": n_all, "in_this_half": len(cands),
                       "dropped_crowd_before_cutoff": len(cands) - len(judged), "judged": len(judged),
                       "crowd_in_2024_25": reachable},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    _write_counts(topics)
    (OUT / "Summary.json").write_text(json.dumps(result, indent=2))
    if report:
        from .report import write_report
        write_report(result, tests, fl_a)
    return result


def _write_counts(topics: list[Topic]) -> None:
    wins = windows()
    with (OUT / "Counts.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["topic", "is_test", "signal", "window_start", "count", "burst_ratio", "trend_ratio"])
        for t in topics:
            for s, c in t.counts.items():
                for k, (ws, _) in enumerate(wins):
                    gb, gt = t.gb[s][k], t.gt[s][k]
                    w.writerow([t.key, int(t.is_test), s, ws.isoformat(), c[k],
                                "" if gb is None else f"{gb:.3f}", "" if gt is None else f"{gt:.3f}"])


if __name__ == "__main__":
    import sys
    if "--with-readme" in sys.argv:  # README check: also search GitHub READMEs
        github.FIELDS = "name,description,readme"
        OUT = OUT / "WithReadme"
    if "--holdout" in sys.argv:
        OUT = OUT / "Holdout"
    r = run(tests_only="--tests-only" in sys.argv, report="--with-readme" not in sys.argv and "--holdout" not in sys.argv,
            holdout="--holdout" in sys.argv)
    print(json.dumps({k: r[k] for k in ("lead", "lead_weights", "passes")}, indent=2, default=str))
