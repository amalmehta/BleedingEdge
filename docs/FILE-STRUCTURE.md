# File Structure

What's where. For how the pieces fit together, see [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md).

```
BleedingEdge/
├── BleedingEdge.md          The spec: goals, definitions, decisions and their history
├── README.md                What it is, one chart, links
├── pyproject.toml           Package name, Python version, dependencies
├── uv.lock                  Exact dependency versions (uv sync reads it)
├── .python-version          Python 3.12
├── .gitignore               Keeps out secrets, the cache, the virtualenv and logs
│
├── bleedingedge/            The code: a small package the weekly brief will reuse
│   ├── backtest.py          Entry point: loads topics, fetches, scores, grades, writes results
│   ├── scoring.py           Growth ratios, score, heating-up and consensus flags (no I/O)
│   ├── windows.py           Splits 2021–25 into 4-week windows starting on Mondays
│   ├── http.py              GET with a disk cache, per-host delays, retries; reads .env keys
│   ├── report.py            Writes docs/BacktestResults.md and the charts
│   ├── mining.py            Mines 2023's new arXiv phrases into a candidate list
│   └── sources/             One module per signal, each returning matching item dates
│       ├── arxiv.py         arXiv search API: paper dates per phrase
│       ├── arxiv_bulk.py    Resumable bulk arXiv metadata harvest (OAI-PMH)
│       ├── github.py        GitHub search: new repos whose name or description matches
│       ├── hackernews.py    Hacker News stories via Algolia (comparison only)
│       └── funding.py       Reads the hand-collected funding rounds
│
├── data/
│   ├── TestTopics.csv       The 3 test topics and their search phrases
│   ├── Candidates2023.csv   Precision-check topics from 2023 workshops, dev and held-out halves
│   ├── Candidates2022-24.csv  The first candidate list, kept for comparison
│   ├── Funding.csv          Announced funding rounds, each with a source URL
│   ├── backtest/            Generated: Counts.csv, Summary.json, WithReadme/ comparison
│   └── cache/               Not in git: raw API responses, about 1 GB
│
├── docs/
│   ├── INSTRUCTIONS.md      Setup, running and reading the results
│   ├── FILE-STRUCTURE.md    This file
│   ├── SYSTEM-DESIGN.md     Architecture, components, data, decisions and trade-offs
│   ├── BACKTEST.md          The backtest's verdict, misses and proposed fixes (by hand)
│   ├── BacktestResults.md   Every count, query and chart (generated)
│   ├── PROMPTS.md           Log of the requests that shaped the project
│   └── img/                 Backtest charts, one per test topic (generated)
│
└── tests/                   pytest, offline
    ├── test_*.py            Windows, scoring, sources and mining
    └── fixtures/            Saved API responses the tests read instead of the network
```

## Generated or hand-made

Running the backtest rewrites everything marked *generated*, so edit those through
`bleedingedge/report.py`, not by hand. The CSVs in `data/` (apart from `data/backtest/`) are
hand-made inputs, each row citing its source.

## Not in the repo

| Path | Why | How to get it back |
|---|---|---|
| `.env` | Holds API keys | Create it yourself (see [INSTRUCTIONS.md](INSTRUCTIONS.md)) |
| `data/cache/` | About 1 GB, and APIs change, so it can't be rebuilt exactly | Run the backtest to refetch; back it up separately |
| `.venv/` | Rebuilt from the lock file | `uv sync` |
| `*.log` | Run logs | Written by long runs |
