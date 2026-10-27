"""Scale factor for "small": local (bulk, 4 categories, whole words) vs arXiv search counts,
on neutral phrases that are neither test topics nor candidates. Also writes ArxivTotals.json.

    uv run python -m bleedingedge.calibrate   # result of the 2026-10-27 run: data/backtest/calibration/SmallBar.txt

"model predictive control" counts 0 locally because the miner never starts a phrase with
"model"; it is left out of the median.
"""
import json, statistics
from datetime import date
from bleedingedge import mining as mn
from bleedingedge.sources import arxiv, arxiv_bulk
from bleedingedge.windows import START, END, counts
NEUTRAL = ["imitation learning", "model predictive control", "graph neural networks", "offline reinforcement learning",
           "motion planning", "knowledge distillation", "federated learning", "domain adaptation",
           "contrastive learning", "neural radiance fields", "diffusion policy", "verifiable rewards"]
ps = arxiv_bulk.papers()
json.dump(counts([date.fromisoformat(p["created"]) for p in ps]), open(mn.OUT_TOTALS, "w"))
loc = mn.phrase_dates(ps, NEUTRAL)
rows = []
for p in NEUTRAL:
    api = len(arxiv.dates([p], START, END))
    l = sum(START <= d < END for d in loc[p])
    rows.append((p, l, api, round(l / api, 2) if api else None))
    print(rows[-1], flush=True)
print("median ratio", statistics.median(r[3] for r in rows if r[3]))
