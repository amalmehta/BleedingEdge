# The improver: one better thing a day, by pull request

A scheduled task, **BleedingEdge improver**, runs every morning. It makes one improvement to what readers see (the website, the daily email, the plain-language explainers), checks it with the harness and three fresh-eyes reviewers, and opens a pull request. Nothing reaches the site or your inbox until you merge it. The next run ships what you merged.

**Who it's for (your answer, 2026-11-19):** friends and family who are curious but not technical, and students learning AI or robotics. The goal is that they get hooked, without lowering quality: every claim stays cited, and the brief's record (flags score about chance) is never softened.

## What it may change

- `web/radar.html`: the page's words, layout and charts.
- `bleedingedge/daily.py`: the email's words and layout only (not what makes an email send).
- `bleedingedge/site.py`: what the page is given, as long as it only reshapes data.
- `data/Explainers.json`: plain-language explainers (format below).
- Tests for any of these, and this file's Log.

## What it must never change

- How topics are found, scored or flagged: `mining.py`, `scoring.py`, `backtest.py`, `brief.py`'s method, thresholds or weights. The pick ledger is a year-long test of a fixed method; changing the method breaks it.
- The ledger's rules (`ledger.py`), `data/Picks.csv`, `data/Trends.csv`, `data/Opportunities.csv`, `data/briefs/`, `briefs/`, `data/private/`.
- The track-record line on the page and in the email, other than making it clearer. Never softer.
- Scheduled tasks, settings, dependencies (`pyproject.toml`, `uv.lock`) or `.gitignore`. Propose those in the PR body instead.
- Anything on `main` directly. It never merges, never force-pushes, never rewrites history.

## Explainers (`data/Explainers.json`)

```json
{"<topic exactly as in the brief>": {
  "what": "In plain words: what it is. 25-90 words.",
  "why": "Why it might matter to someone outside the field. 25-90 words.",
  "sources": [{"url": "https://arxiv.org/abs/2611.12286", "title": "VLA-MOPD"}],
  "written": "YYYY-MM-DD"}}
```

- Written from the papers themselves: read the abstracts of the topic's recent papers (in `data/briefs/<latest>.json`) before writing.
- No numbers in the prose: numbers live in the data, which the page shows beside it.
- Every factual claim traceable to a listed source. If a claim isn't in a source, cut it.
- Honest about uncertainty: "researchers are trying", not "this will". The harness rejects hype words.
- Grade 10 reading level or below, checked by the harness.

## Each run, in order

1. **Fix what's broken first.** Run `uv run python -m bleedingedge.harness` on `main`, and read the dashboard's `check` and `runs` documents (in `data/users/me`). If either fails, that is today's change.
2. **Ship what you merged.** If `main` has changes to `web/radar.html`, `site.py` or `data/Explainers.json` since the last deploy (`data/cache/improver/deployed.txt` holds that commit), deploy them (steps in the task's instructions) and record the new commit.
3. **One open PR at a time.** If an improver PR is still open, don't start another. If you left comments on it, address them on that branch. Otherwise stop for the day.
4. **Pick one improvement**, in this order:
   - an explainer for this week's pick, if it has none;
   - explainers for the early topics without one, highest score first, up to 3 per PR;
   - the top item under Backlog below;
   - the clearest problem the fresh-eyes reviewers found last time (see Log).
5. **Make it** on a branch `improve/YYYY-MM-DD`, small (under about 300 changed lines).
6. **Check it:** `uv run python -m bleedingedge.harness` must pass. Then three reviewers, each a fresh subagent given only the changed reader-facing text and its sources:
   - a curious friend who doesn't work in tech: what lost them, what made them want to read on;
   - a student learning AI: what they'd still need explained;
   - a robotics researcher: anything wrong, overstated or not supported by the cited abstracts.
   Fix what they find (at most two rounds), then re-run the harness.
7. **Open the PR**, with: what changed and for which reader; the harness output; each reviewer's notes, and what you changed because of them; what you couldn't check (the page's own check only runs once the page is opened after deploy).
8. **Log it** below in the PR: date, PR, one line.

## Signals it learns from

- Which PRs you merge, and which you close unmerged. Read your comments on both before choosing.
- The dashboard's `check` after each deploy.
- Your pick marks on the site (taste, 2+ hours).
- **Not available:** what friends open on the page. The page type keeps each viewer's saved data private to them and lets only editors write shared data, so their visits can't be counted. A small companion page with its own shared store could do it; that's a proposal for you, not something the improver builds.

## What you've said

- 2026-11-19: everyday people should get hooked, not just people in the field, without reducing quality at all. Email and site should be easier to read.

## Backlog

Add ideas here; the improver takes the top one when no explainer is due.

- A one-line "why this week" on the pick card, in plain words, from the pick's explainer.
- In the email, the pick's plain-language "why it might matter" under its papers.
- A short "how to read this page" for first-time visitors, folded by default.

## Log

- 2026-11-19: improver set up (harness, explainers, this file). No runs yet.
- 2026-11-19: improve/2026-11-19. Explainers for this week's pick (physical intelligence) and the two top early topics (embodied manipulation, long-horizon embodied). Reviewers: titles like "embodied" and "long-horizon" still lose non-technical readers, so a plainer display name per topic is worth trying.
- 2026-11-20: improve/2026-11-20. Explainers for the next two early topics (policies learn, humanoid manipulation); the rest of this week's early topics have no papers in the brief to write from. Reviewers: the topic name "policies learn" reads as broken English to a non-technical reader, which makes the plainer display name per topic more pressing.
