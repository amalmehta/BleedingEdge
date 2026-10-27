# Instructions

How to set up BleedingEdge, run the backtest, and read what it produces. Only the backtest is
built; the weekly brief waits on it passing (see [BACKTEST.md](BACKTEST.md)).

## What you need

- macOS or Linux with Python 3.12 (pinned in `.python-version`)
- [uv](https://docs.astral.sh/uv/), which installs Python and the dependencies for you
- The [GitHub CLI](https://cli.github.com/), signed in with `gh auth login`. The GitHub signal
  borrows that login's token (`gh auth token`), so the backtest stops with an error without it.
- Optional, not used yet: `S2_API_KEY` (Semantic Scholar) and `OPENALEX_API_KEY` for the citation
  and lab signals. Put them in a `.env` file at the repo root, one `NAME=value` per line. `.env`
  is ignored by git; never commit it.

No paid APIs. arXiv, GitHub search and Hacker News (Algolia) are free.

## Set up

```bash
git clone https://github.com/amalmehta/BleedingEdge.git
```

```bash
cd BleedingEdge && uv sync
```

`uv sync` builds `.venv/` from `pyproject.toml` and `uv.lock`, so everyone gets the same versions.

## Check it works

```bash
uv run pytest
```

The tests use saved responses in `tests/fixtures/`, so they need no network and no login.

## Run the backtest

```bash
uv run python -m bleedingedge.backtest
```

This runs the 3 test topics and the dev half of the 2023 candidates, then rewrites
`docs/BacktestResults.md`, the charts in `docs/img/` and the data in `data/backtest/`.
`docs/BACKTEST.md` is written by hand from those, so update it yourself after a run that
changes the numbers. It prints the lead times, lead weights and whether each pass criterion held.

**The first run is slow.** Every API response is cached in `data/cache/`, which is not in the
repo (about 1 GB). From a fresh clone the backtest makes roughly 2,800 GitHub, 300 arXiv and 300
Hacker News calls, spaced out to respect each site's rate limit: about 2 hours. After that, re-runs
take seconds and give the same numbers. Results from a fresh clone can differ slightly from the
committed ones, because the APIs return what they hold today.

Other options:

| Command | What it does |
|---|---|
| `uv run python -m bleedingedge.backtest --tests-only` | Only the 3 test topics: a quicker first run |
| `uv run python -m bleedingedge.backtest --with-readme` | Also searches GitHub READMEs, to reproduce why that was dropped. Writes to `data/backtest/WithReadme/` only |
| `uv run python -m bleedingedge.backtest --holdout` | The held-out half. **Run it once, at the end**: looking at it while tuning turns it into more dev data. Writes to `data/backtest/Holdout/` |

To refresh the data, delete `data/cache/` (or one host's folder inside it) and run again.

## Mine candidate topics from arXiv (in progress)

The next candidate list comes from phrases that were new on arXiv in 2023, so that no one picks
the topics by hand. It takes two steps:

```bash
uv run python -m bleedingedge.sources.arxiv_bulk
```

This harvests arXiv metadata for cs.RO, cs.LG, cs.AI and cs.CL since 2021 into
`data/cache/arxiv_bulk/`. It takes about 3 hours the first time, and it is resumable: stop it and
run it again to carry on from `state.json`.

```bash
uv run python -m bleedingedge.mining
```

Once the harvest is done, this writes `data/CandidatesMined2023.csv` and
`data/backtest/MinedArxivCounts.json`. The backtest doesn't use these yet.

## Read the results

- [BACKTEST.md](BACKTEST.md): the verdict, in words, with misses reported
- [BacktestResults.md](BacktestResults.md): every count, query and chart, generated
- `data/backtest/Counts.csv`: one row per topic, signal and 4-week window, with both growth ratios
- `data/backtest/Summary.json`: lead times, lead weights and pass/fail, machine-readable

## When something goes wrong

- **`gh auth token` fails** (`CalledProcessError`): run `gh auth login`, then try again.
- **It seems stuck**: it's probably waiting between calls, or backing off after a 429 or 5xx
  error. Waits and retries are set in `bleedingedge/http.py`.
- **Odd numbers after editing a topic's phrases**: changed phrases mean new URLs, so they're
  fetched fresh. Old cached responses stay on disk, unused.
