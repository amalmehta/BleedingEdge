"""Charts and tables for the backtest. Regenerated on every run; the narrative in
docs/BACKTEST.md is written by hand from these and links to them."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .sources import arxiv, github, hackernews  # noqa: E402
from .windows import END, START, windows  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMG = DOCS / "img"

INK, MUTED, BG = "#2b2a28", "#8a857d", "#faf7f2"
BLUE, TERRA = "#4a6d8c", "#b8664a"
LABELS = {"arxiv": "arXiv papers", "github": "new GitHub repos", "funding": "funding rounds",
          "hn": "HN stories ≥50 pts", "citations": "citations", "labs": "watch-list lab papers"}


def _chart(t, fl, path: Path) -> None:
    wins = [ws for ws, _ in windows()]
    sigs = [s for s in ("arxiv", "github", "funding", "hn") if s in t.counts]
    fig, axes = plt.subplots(len(sigs), 1, figsize=(8, 1.6 * len(sigs) + 0.6), sharex=True)
    fig.patch.set_facecolor(BG)
    h = next((k for k, f in enumerate(fl["heating"]) if f), None)
    c = fl["consensus"]
    for ax, s in zip(axes, sigs):
        ax.set_facecolor(BG)
        ax.bar(wins, t.counts[s], width=24, color=TERRA if s == "hn" else BLUE, alpha=0.85)
        ax.set_ylabel(LABELS[s], rotation=0, ha="right", va="center", fontsize=8, color=INK)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(colors=MUTED, labelsize=7)
        if h is not None:
            ax.axvline(wins[h], color=BLUE, lw=1, ls="--")
        if c is not None:
            ax.axvline(wins[c], color=TERRA, lw=1, ls="--")
    note = []
    if h is not None:
        note.append(f"blue dashed: first heating-up flag ({wins[h]:%b %Y}, {'burst' if fl['burst'][h] else 'trend'})")
    if c is not None:
        note.append(f"terracotta dashed: research crowd arrives, 25% of peak ({wins[c]:%b %Y})")
    else:
        note.append("research crowd never arrived")
    axes[0].set_title(f"{t.name}: counts per 4-week window", loc="left", fontsize=10, color=INK)
    fig.text(0.01, 0.005, "; ".join(note), fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)


def _w(k):
    return "—" if k is None else f"{windows()[k][0]:%b %Y}"


def _pct(x):
    return "—" if x is None else f"{x:.0%}"


def write_report(result: dict, tests, fl_a) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    for t in tests:
        _chart(t, fl_a[t.key], IMG / f"backtest-{t.key}.png")

    L = ["# Backtest Results (generated)", "",
         f"Window {START:%d %b %Y} – {END:%d %b %Y}, 65 four-week windows. "
         f"Signals used: {', '.join(result['signals'])}. "
         f"Not yet used (need API keys): {', '.join(result['missing_signals']) or 'none'}.", "",
         "All thresholds are invented starting parameters from BleedingEdge.md.", "",
         "## (a) Lead on the test topics (lead weights untuned, all 1)", "",
         "| Topic | First heating-up flag | Research crowd arrives | Lead | ≥ 8 weeks? | arXiv-only baseline lead | First HN story ≥50 pts |",
         "|---|---|---|---|---|---|---|"]
    base = {r["key"]: r for r in result["lead_baseline"]}
    for r in result["lead"]:
        b = base[r["key"]]
        L.append(f"| {r['topic']} | {_w(r['heating_window'])}{' (' + r['mode'] + ')' if r['mode'] else ''} | {_w(r['consensus_window'])} | "
                 f"{'—' if r['lead_weeks'] is None else str(r['lead_weeks']) + ' wk'} | "
                 f"{'yes' if r['passes'] else 'no'} | "
                 f"{'—' if b['lead_weeks'] is None else str(b['lead_weeks']) + ' wk'} | {_w(r['hn_first_story_window'])} |")
    L += ["", f"**Criterion (a): {'passes' if result['passes']['a_lead'] else 'fails'}** "
          "(needs ≥ 2 of 3 topics with a lead of ≥ 8 weeks).", ""]
    for t in tests:
        L.append(f"![{t.name}](img/backtest-{t.key}.png)")
    L += ["", "## Lead weights", "",
          "Share of test topics where the signal on its own rose ≥ 8 weeks before the research crowd arrived. "
          "Topics that never reached consensus can't be judged and are left out.", "",
          "| Signal | First own rise, per test topic | Lead weight |", "|---|---|---|"]
    for s, by_topic in result["crossings"].items():
        raw = result["lead_weights_raw"][s]
        rises = ", ".join(f"{k}: {_w(v)}" for k, v in by_topic.items())
        L.append(f"| {s} | {rises} | {'undetermined (default 1)' if raw is None else f'{raw:.2f}'} |")

    L += ["", "## (b) Precision on 2023 workshop-title candidates, flags in 2024", ""]
    if result["precision"]:
        c = result["candidates"]
        L += [f"From `data/{c['file']}`: {c['total_both_halves']} candidates, split in half by hash. "
              f"This is the **{c['half']}** half ({c['in_this_half']}). {c['dropped_crowd_before_cutoff']} had their crowd "
              f"arrive before 2023, so they could never be new in 2024; they are left out of the criterion and kept "
              f"in the \"tuned all candidates\" line. Of the {c['judged']} judged, {c['crowd_in_2024_25']} had the crowd "
              "arrive in 2024–25, the most a perfect detector could hit.", ""]
        L += ["| Method | Flags (topic-windows) | Reached consensus in 12 months | Precision | Distinct topics flagged | Distinct topic precision |",
              "|---|---|---|---|---|---|"]
        for name, p in result["precision"].items():
            L.append(f"| {name.replace('_', ' ')} | {p['pairs']} | {p['hits']} | {_pct(p['precision'])} | "
                     f"{p['topics_flagged']} | {_pct(p['topic_precision'])} |")
        L += ["", f"**Criterion (b): {'passes' if result['passes']['b_precision'] else 'fails'}** "
              "(needs precision ≥ 50% with tuned lead weights).", ""]
    else:
        L += ["No candidates file yet (data/Candidates.csv).", ""]

    L += ["## Queries behind every count", "",
          "Each test topic's counts come from these queries (first page shown; the code paginates and splits date ranges).", ""]
    for t in tests:
        L.append(f"**{t.name}**")
        for p in t.arxiv:
            L.append(f"- arXiv \"{p}\": {arxiv.query_url(p, START, END)}")
        for p in t.github:
            L.append(f"- GitHub \"{p}\" (2021 slice): https://github.com/search?type=repositories&q="
                     + github.query_url(p, START, START.replace(year=2022, month=1, day=1)).split("q=", 1)[1].split("&", 1)[0])
        for p in t.hn:
            L.append(f"- HN \"{p}\": {hackernews.query_url(p, START, END)}")
        L.append("")
    (DOCS / "BacktestResults.md").write_text("\n".join(L))
