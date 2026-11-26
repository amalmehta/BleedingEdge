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
│   ├── notify.py            The Monday desktop notification, missed-brief alert and review reminder
│   ├── ledger.py            Grades each study pick against the test its brief wrote down
│   ├── site.py              Builds the website's data files (site/, not in git)
│   ├── daily.py             Composes the daily email (sent by a scheduled task through Gmail)
│   ├── feedback.py          Records your More/Less votes and replies from the email; mutes and ranks topics
│   ├── harness.py           Hard checks every improver change must pass
│   ├── mining.py            Mines 2023's new arXiv phrases into a candidate list
│   └── sources/             One module per signal, each returning matching item dates
│       ├── arxiv.py         arXiv search API: paper dates per phrase
│       ├── arxiv_bulk.py    Resumable bulk arXiv metadata harvest (OAI-PMH)
│       ├── github.py        GitHub search: new repos whose name or description matches
│       ├── hackernews.py    Hacker News stories via Algolia (comparison only)
│       └── funding.py       Reads the hand-collected funding rounds
│
├── web/radar.html           The BleedingEdge Radar page (stored in a private claude.ai dashboard)
├── site/                    Not in git: the page's data files, rebuilt each Monday
│
├── data/
│   ├── TestTopics.csv       The 3 test topics and their search phrases
│   ├── CandidatesMined2023.csv  Precision-check topics mined from arXiv (backtest reads it)
│   ├── Candidates2023.csv   Earlier precision-check topics, from 2023 workshops
│   ├── Candidates2022-24.csv  The first candidate list, kept for comparison
│   ├── Funding.csv          Announced funding rounds, each with a source URL
│   ├── Opportunities.csv    Opportunities the brief listed
│   ├── Fragments.csv        Mined phrases that aren't topics, skipped by the email, site and Monday shortlist
│   ├── Explainers.json      Plain-language, cited explainers per topic (written by the improver)
│   ├── steps/               Each pick's first step in four Tue–Fri pieces, for the daily email
│   ├── Picks.csv            The study picks, each with its bar, due date and grade (ledger.py fills these)
│   ├── backtest/            Generated: Counts.csv, Summary.json, MinedArxivCounts.json, WithReadme/ comparison
│   └── cache/               Not in git: raw API responses, about 1 GB
│
├── docs/
│   ├── INSTRUCTIONS.md      Setup, running and reading the results
│   ├── FILE-STRUCTURE.md    This file
│   ├── SYSTEM-DESIGN.md     Architecture, components, data, decisions and trade-offs
│   ├── BACKTEST.md          The backtest's verdict, misses and proposed fixes (by hand)
│   ├── BacktestResults.md   Every count, query and chart (generated)
│   ├── IMPROVE.md           The daily improver's rules, backlog and log
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
| `data/private/Applications.csv` | What you applied to; the repo is public | It can't be rebuilt; back it up yourself |
| `data/private/Feedback.csv` | Your votes and replies from the daily email | It can't be rebuilt; back it up yourself, or delete it to reset your feedback |
| `*.log` | Run logs | Written by long runs |
