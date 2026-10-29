"""The weekly robotics brief: the round-2 backtest method, applied to this week's data.

    uv run python -m bleedingedge.brief                 # brief for today; tops up arXiv first
    uv run python -m bleedingedge.brief 2026-10-27 --no-update

Trial scope (decided 2026-10-27, a bar lowered after the backtest failed; see BleedingEdge.md):
robotics only. Candidates are phrases new in the last complete year, mined from cs.RO titles,
exactly as backtested (phrases new in 2024, flagged during 2025). Phrases that only appeared
this year wait until next year's list, as they did in the backtest.

Windows are 4 weeks long and end on the run date, so each weekly brief sees a fresh last
window. Writes briefs/YYYY-MM-DD.md (the study pick is left for the weekly task to write),
briefs/img/YYYY-MM-DD.png, data/briefs/YYYY-MM-DD.json and rows in data/Trends.csv.
"""
import csv
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode

from . import backtest as bt
from . import mining as mn
from . import scoring as sc
from .sources import arxiv_bulk, github
from .windows import WINDOW_DAYS, counts

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = ROOT / "briefs"
DATA = ROOT / "data" / "briefs"
TRENDS = ROOT / "data" / "Trends.csv"
PICKS = ROOT / "data" / "Picks.csv"
LEAD_FROM = ROOT / "data" / "backtest" / "Run2024RO" / "Summary.json"  # lead weights as backtested

TRIAL_START = date(2026, 10, 27)
N = 40              # windows of history: enough for the trend (1 year) and newness (2 years) checks
SHOW = 5            # items per section ("readable in 15 minutes")
SHORTLIST = 3       # candidates offered to the weekly task for the study pick
NO_REPEAT = 3       # a pick can't repeat any of the last 3
PICK_START, PICK_END = "<!-- pick:start -->", "<!-- pick:end -->"  # the weekly task writes between these

def record() -> str:
    """The backtest record, read from the round-2 robotics results (both halves; the method was
    fixed before either was run), so the brief can't drift from what the backtest found."""
    flagged = hit = took_off = judged = 0
    for path in (LEAD_FROM, LEAD_FROM.parent / "Holdout" / "Summary.json"):
        d = json.loads(path.read_text())
        flagged += d["precision"]["tuned"]["topics_flagged"]
        hit += d["precision"]["tuned"]["topics_hit"]
        took_off += d["candidates"]["crowd_in_judged_year_or_later"]
        judged += d["candidates"]["judged"]
    return (f"In a backtest on robotics phrases new in 2024, **{hit} of {flagged} flagged topics "
            f"({hit / flagged:.0%}) took off within a year**. Picking at random would have found {took_off} of {judged} "
            f"({took_off / judged:.0%}). It caught {hit} of the {took_off} that took off. "
            "That failed the 50% bar set before testing. This trial runs on a bar lowered after seeing that result, "
            f"so treat every flag below as roughly a 1-in-{round(flagged / hit) if hit else '∞'} bet. "
            "[Details](../docs/BACKTEST.md#round-2-results)")


def grid(day: date) -> tuple[date, list[tuple[date, date]]]:
    start = day - timedelta(days=WINDOW_DAYS * N)
    return start, [(start + timedelta(days=WINDOW_DAYS * k), start + timedelta(days=WINDOW_DAYS * (k + 1)))
                   for k in range(N)]


def arxiv_search_url(phrase: str) -> str:
    return "https://arxiv.org/search/?" + urlencode({"query": f'"{phrase}"', "searchtype": "all"})


def github_search_url(phrase: str, start: date, end: date) -> str:
    q = f'"{phrase}" in:name,description created:{start:%Y-%m-%d}..{end - timedelta(days=1):%Y-%m-%d}'
    return "https://github.com/search?" + urlencode({"q": q, "type": "repositories"})


def recent_picks(day: date) -> list[str]:
    if not PICKS.exists():
        return []
    with PICKS.open(newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["date"] < day.isoformat()]
    return [r["topic"] for r in rows[-NO_REPEAT:]]


def score_topics(papers: list[dict], day: date, log=print) -> tuple[list[dict], date, list]:
    """Mine last year's cs.RO phrases, count them on the brief's grid and flag them at the last window."""
    year = day.year - 1
    rows, _ = mn.mine(papers, year, ro=True, min_titles=mn.ro_min_titles(papers, year))
    start, wins = grid(day)
    log(f"{len(rows)} candidates: cs.RO phrases new in {year}")
    phrases = [r["topic"] for r in rows]
    dates = mn.phrase_dates(papers, phrases)
    total = counts([date.fromisoformat(p["created"]) for p in papers], start, N)
    lam = json.loads(LEAD_FROM.read_text())["lead_weights"]
    k = N - 1
    out = []
    for r in rows:
        g = r["topic"]
        t = bt.Topic(bt._slug(g), g, "rl_robotics", [g], [], [g], False, local=True)
        t.counts["arxiv"] = counts(dates[g], start, N)
        gb = sc.relative(sc.growth(t.counts["arxiv"]), sc.growth(total))
        gt = sc.relative(sc.trend(t.counts["arxiv"]), sc.trend(total))
        rec = {"topic": g, "titles_last_year": r["titles_in_year"], "arxiv": t.counts["arxiv"],
               "g_burst_arxiv": gb[k], "g_trend_arxiv": gt[k]}
        # Heating up needs 2 rising signals, so a topic whose arXiv count isn't rising now can't be
        # flagged now. GitHub is only fetched for the rest (one search per topic, rate-limited).
        if (gb[k] or 0) >= sc.BURST["g"] or (gt[k] or 0) >= sc.TREND["g"]:
            log(f"  {g}: github")
            t.counts["github"] = counts(github.dates([g], start, day), start, N)
            t.gb = {"arxiv": gb, "github": sc.growth(t.counts["github"])}
            t.gt = {"arxiv": gt, "github": sc.trend(t.counts["github"])}
            t.rolled = {s: sc.rolling(c) for s, c in t.counts.items()}
            f = bt.flags(t, lam)
            first = sc.first(f["heating"])
            rec |= {"github": t.counts["github"], "g_burst_github": t.gb["github"][k],
                    "g_trend_github": t.gt["github"][k], "score": f["score"][k],
                    "mode": "burst" if f["burst"][k] else "trend" if f["trend"][k] else None,
                    "heating": f["heating"][k], "early": f["early"][k],
                    "first_flag": wins[first][1].isoformat() if first is not None else None}
        out.append(rec)
    return out, start, wins


def examples(papers: list[dict], phrases: list[str], day: date, n: int = 3) -> dict[str, list[dict]]:
    """The most recent papers per phrase (title or abstract), cs.RO first: the concrete way in."""
    want = set(phrases)
    found: dict[str, list[dict]] = {g: [] for g in phrases}
    for p in papers:
        if p["created"] >= day.isoformat():
            continue
        for g in mn.ngrams(mn.words(p["title"] + " " + p["abstract"])) & want:
            found[g].append(p)
    return {g: [{"id": p["id"], "title": p["title"], "created": p["created"], "url": f"https://arxiv.org/abs/{p['id']}"}
                for p in sorted(ps, key=lambda p: ("cs.RO" in p["cats"], p["created"]), reverse=True)[:n]]
            for g, ps in found.items()}


def append_trends(day: date, recs: list[dict]) -> None:
    cols = ["date", "topic", "domain", "arxiv_4w", "arxiv_12w", "g_burst_arxiv", "g_trend_arxiv",
            "github_4w", "github_12w", "g_burst_github", "g_trend_github", "score", "heating", "early"]
    old = []
    if TRENDS.exists():
        with TRENDS.open(newline="") as f:
            old = [r for r in csv.DictReader(f) if r["date"] != day.isoformat()]  # a re-run replaces its day
    rnd = lambda v: "" if v is None else round(v, 3)
    new = [{"date": day.isoformat(), "topic": r["topic"], "domain": "rl_robotics",
            "arxiv_4w": r["arxiv"][-1], "arxiv_12w": sum(r["arxiv"][-3:]),
            "g_burst_arxiv": rnd(r["g_burst_arxiv"]), "g_trend_arxiv": rnd(r["g_trend_arxiv"]),
            "github_4w": r["github"][-1] if "github" in r else "",
            "github_12w": sum(r["github"][-3:]) if "github" in r else "",
            "g_burst_github": rnd(r.get("g_burst_github")), "g_trend_github": rnd(r.get("g_trend_github")),
            "score": rnd(r.get("score")), "heating": r.get("heating", False), "early": r.get("early", False)}
           for r in recs]
    with TRENDS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(old + new)


def chart(path: Path, recs: list[dict], wins: list, span: int = 26) -> None:
    """Small multiples, one per early topic: papers per 4-week window over the last 2 years.
    One hue and a shared y-axis, so the panels compare by height and the title names each."""
    from .report import BG, BLUE, INK, MUTED, plt
    mids = [s + timedelta(days=WINDOW_DAYS // 2) for s, _ in wins][-span:]
    fig, axes = plt.subplots(len(recs), 1, figsize=(7, 1.1 * len(recs) + 0.5), sharex=True, sharey=True, squeeze=False)
    fig.patch.set_facecolor(BG)
    for ax, r in zip(axes[:, 0], recs):
        ax.set_facecolor(BG)
        ax.bar(mids, r["arxiv"][-span:], width=22, color=BLUE)
        ax.set_title(r["topic"], loc="left", fontsize=8, color=INK, pad=2)
        ax.tick_params(colors=MUTED, labelsize=7)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(MUTED)
    fig.suptitle("arXiv papers per 4-week window (bulk count)", x=0.01, ha="left", fontsize=9, color=INK)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)


def _ratio(v: float | None) -> str:
    return "—" if v is None else f"{v:.1f}×"


def _row(r: dict, start: date, day: date) -> str:
    g = r["topic"]
    last4 = day - timedelta(days=WINDOW_DAYS)
    why = (f"burst: papers {_ratio(r['g_burst_arxiv'])}, new repos {_ratio(r['g_burst_github'])} vs the 12 weeks before"
           if r["mode"] == "burst" else
           f"trend: papers {_ratio(r['g_trend_arxiv'])}, new repos {_ratio(r['g_trend_github'])} vs a year ago")
    return (f"| **{g}** | {r['score']:.2f} | {why} | [{sum(r['arxiv'][-3:])}]({arxiv_search_url(g)}) "
            f"| [{sum(r['github'][-3:])}]({github_search_url(g, day - timedelta(days=3 * WINDOW_DAYS), day)}) "
            f"| {r['first_flag']} |")


def render(day: date, week: int, recs: list[dict], ex: dict, start: date, shortlist: list[dict],
           skipped: list[str], img: str | None) -> str:
    early = [r for r in recs if r.get("early")][:SHOW]
    consensus = [r for r in recs if r.get("heating") and sum(r["arxiv"][-3:]) >= bt.LOCAL_SMALL_MAX][:SHOW]
    head = "| Topic | Score | Why flagged | Papers, 12 wk | New repos, 12 wk | First flagged (window ending) |\n|---|---|---|---|---|---|"
    L = [f"# Robotics brief, {day:%-d %b %Y}", "",
         f"Week {week} of 4 of the trial. Robotics only (phrases from cs.RO titles).", "",
         f"> **Track record, read first.** {record()}", "",
         "## Study this next", "", PICK_START,
         "_Not written yet. The weekly task writes this section from the shortlist below "
         "(prompts/WeeklyBrief.md)._", ""]
    for r in shortlist:
        L.append(f"- **{r['topic']}** (score {r['score']:.2f}). Recent papers: "
                 + "; ".join(f"[{p['title']}]({p['url']}) ({p['created']})" for p in ex[r["topic"]]))
    if skipped:
        L.append(f"- Left out as repeats of recent picks: {', '.join(skipped)}")
    if not shortlist:
        L.append("- No early robotics topic this week. Say so; don't force a pick.")
    L += [PICK_END, "", "## Early / speculative", "",
          "Confidence for every row: **low** (see the track record above). "
          "Score = weighted log₂ growth of papers and new repos (1 = doubling). Ratios are relative to arXiv's own growth.", ""]
    L += [head] + [_row(r, start, day) for r in early] if early else ["None this week."]
    if img and early:
        L += ["", f"![4-week paper counts for this week's early topics]({img})"]
    L += ["", "## Consensus is moving", "",
          f"Heating up with {bt.LOCAL_SMALL_MAX} or more papers in 12 weeks: no longer early.", ""]
    L += [head] + [_row(r, start, day) for r in consensus] if consensus else ["None this week."]
    L += ["", "## Not covered in this trial", "",
          "Tools rising and fading, companies heating up, AI tooling and the wider field. "
          "Outside robotics the method scored below random in the backtest (6% on held-out phrases), "
          "so this trial leaves them out rather than print flags known to be noise.", "",
          "## How this was made", "",
          f"- Candidates: {len(recs)} two- and three-word phrases in cs.RO titles in {day.year - 1} that were rare in the two years before "
          "(`bleedingedge/mining.py`). Mined by rule, not picked.",
          f"- Paper counts: arXiv bulk metadata (cs.RO, cs.LG, cs.AI, cs.CL; title or abstract) to {day - timedelta(days=1):%-d %b %Y}. "
          "The linked arXiv searches count differently (the bulk count is about 0.6× arXiv search); they are there to read the papers. "
          "The newest days are thin because arXiv announces papers a day or two late.",
          "- New repos: GitHub repository search on name and description, linked per row.",
          "- Thresholds are invented starting points, unchanged from the backtest. Every row is in `data/Trends.csv`.",
          "- No buy, sell or hold advice, ever."]
    return "\n".join(L) + "\n"


def keep_pick(old: str, new: str) -> str:
    """`new` with the pick section taken from `old`, so a re-run doesn't erase a pick the weekly
    task already wrote. Kept only once written: a draft still holding the placeholder is replaced."""
    if PICK_START not in old or PICK_END not in old:
        return new
    pick = old.split(PICK_START, 1)[1].split(PICK_END, 1)[0]
    if "_Not written yet." in pick:
        return new
    head, rest = new.split(PICK_START, 1)
    return head + PICK_START + pick + PICK_END + rest.split(PICK_END, 1)[1]


def main(day: date, update: bool = True, log=print) -> Path:
    if update:
        arxiv_bulk.update(log)
    papers = arxiv_bulk.papers()
    recs, start, wins = score_topics(papers, day, log)
    recs.sort(key=lambda r: -(r.get("score") or -99))
    picks = recent_picks(day)
    early = [r for r in recs if r.get("early")]
    shortlist = [r for r in early if r["topic"] not in picks][:SHORTLIST]
    skipped = [r["topic"] for r in early[:SHORTLIST + len(picks)] if r["topic"] in picks]
    show = {r["topic"] for r in early[:SHOW]} | {r["topic"] for r in shortlist}
    ex = examples(papers, sorted(show), day)
    BRIEFS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    img = None
    if early:
        (BRIEFS / "img").mkdir(exist_ok=True)
        chart(BRIEFS / "img" / f"{day}.png", early[:SHOW], wins)
        img = f"img/{day}.png"
    week = 1 + sum(1 for p in BRIEFS.glob("20*.md") if TRIAL_START.isoformat() <= p.stem < day.isoformat())
    out = BRIEFS / f"{day}.md"
    text = render(day, week, recs, ex, start, shortlist, skipped, img)
    out.write_text(keep_pick(out.read_text(), text) if out.exists() else text)
    append_trends(day, recs)
    (DATA / f"{day}.json").write_text(json.dumps({
        "date": day.isoformat(), "week": week, "grid_start": start.isoformat(), "candidates": len(recs),
        "screened": sum(1 for r in recs if "github" in r), "recent_picks": picks,
        "shortlist": [r | {"papers": ex[r["topic"]]} for r in shortlist],
        "early": [r | {"papers": ex.get(r["topic"], [])} for r in early],
        "heating": [r for r in recs if r.get("heating")]}, indent=1))
    log(f"wrote {out.name}: {len(early)} early, shortlist {[r['topic'] for r in shortlist]}")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(date.fromisoformat(args[0]) if args else date.today(), "--no-update" not in sys.argv)
