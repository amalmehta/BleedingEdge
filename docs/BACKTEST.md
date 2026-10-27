# Backtest: would the method have spotted past trends early?

**Verdict: fail, so don't run the weekly brief yet.**

- Criterion (a) passes, but it's in-sample, so it's weak evidence.
- Criterion (b) failed twice, and both times the candidate list could barely score a hit:
  - **First run (2026-10-26):** 6% precision against a 50% bar.
  - **Second run (2026-10-27):** 0 of 3, after the newness fix and a new list of 2023 candidates.
- The precision test needs a different source of candidates before it can say anything. See [the second run](#second-run-2023-candidates-and-a-newness-test).

Run on 2026-10-26 over Jan 2021 – Dec 2025: 65 four-week windows, 3 test topics, 59 candidate topics. The signals were arXiv, new GitHub repos and funding rounds. Citations and lab papers were left out because they wait on API keys. Every count, query URL and chart is in [BacktestResults.md](BacktestResults.md), which is generated. Raw counts are in `data/backtest/Counts.csv`.

## The question

If this detector had run every 4 weeks from 2021, would it have flagged the topics you later wished you'd studied, and would it have done so ≥ 8 weeks before the research crowd arrived?

- **Hypothesis.** Growth in leading signals (papers, new repos, funding), measured both as a sudden burst and as a year-over-year trend, flags a topic before it's crowded.
- **Baseline.** The same detector using arXiv only. If more signals don't beat it, they're not worth collecting.
- **"The crowd arrives".** This is the first window where a topic's 12-week paper count reaches 25% of its eventual peak. It uses hindsight, so it only grades the method and is never fed into it.
- **Metrics.** The spec sets the pass criteria:
  - **(a) Lead.** At least 2 of the 3 test topics are flagged ≥ 8 weeks early.
  - **(b) Precision.** Take the top 10 "early" flags in each 2024 window. At least 50% of them should have the crowd arrive within the next 12 months.

## (a) Lead on the test topics: passes, but in-sample

| Topic | First flag | Crowd arrives | Lead | arXiv-only lead |
|---|---|---|---|---|
| GRPO / RLVR | 30 Dec 2024 (trend) | 21 Apr 2025 | 16 wk | 16 wk |
| Diffusion policies | 29 Jan 2024 (burst) | 20 May 2024 | 16 wk | 16 wk |
| VLAs | 17 Jun 2024 (trend) | 19 May 2025 | 48 wk | 52 wk |

The spec asked for leads at 4, 8 and 12 weeks. All 3 topics pass at all three, because the shortest lead is 16 weeks.

![GRPO](img/backtest-grpo_rlvr.png)
![Diffusion policies](img/backtest-diffusion_policy.png)
![VLAs](img/backtest-vla.png)

**Why this is weak evidence:**

- **The method was redesigned after the first run, which used these same 3 topics.** That run missed VLAs, so I added the trend ratio, changed how consensus is defined and dropped acronyms. Passing on the topics you tuned against is like grading yourself on the practice exam.
- **The search phrases were picked in 2026.** "Vision-language-action" is the name the field settled on. Someone in 2023 might have searched a different term.
- **The arXiv-only baseline does just as well, and slightly better on VLAs.** On these topics, GitHub and funding add no lead. GitHub's lead weight is 0.67, but it never beats arXiv to the flag.

## (b) Precision on the candidates: fails

| Method | Flags in 2024 | Crowd arrived within 12 months | Precision |
|---|---|---|---|
| Full method (tuned weights) | 16 | 1 | 6% |
| Full method (untuned) | 16 | 1 | 6% |
| arXiv only | 77 | 1 | 1% |

The single hit was cross-embodiment learning. It was flagged in Sep 2024 and the crowd arrived in Oct 2024, which is a lead of only 4 weeks.

**Why it failed.** There are two reasons, and they need different fixes.

1. **The test could barely score a hit.** Using the arXiv counts, here is when each of the 59 candidates had its crowd arrive:

   | When the crowd arrived | Candidates |
   |---|---|
   | Never (fewer than 20 papers per 12 weeks at peak) | 29 |
   | 2021, the first year of data, meaning they were established before the window opened | 24 |
   | 2022–23 | 5 |
   | In 2024–25, the only years a 2024 flag could count | **1** |

   So even a perfect detector would have scored about 1 hit, because workshop titles name topics that are already active. The candidate list doesn't test the detector.

2. **The detector did flag the wrong things.** 7 of the 12 topics it flagged had their crowd arrive back in 2021. Examples are tactile sensing, legged locomotion and long-horizon planning. They count as "early" only because they stay small: fewer than 50 papers per 12 weeks. **The "early" rule measures size, not newness.** A small, mature topic with a noisy month looks the same as a new one. The test does get this part right, and it's a real flaw.

## Second run: 2023 candidates and a newness test

**What changed (2026-10-27):**

1. **"Early" now also means new.** A topic must have had fewer than 10 papers in the same 12 weeks two years earlier. The 10 is invented.
2. **New candidate list.** It holds every RL, robotics, agents and ML-tooling workshop at CoRL, RSS, ICRA, NeurIPS, ICML and ICLR 2023: 97 topics in [`data/Candidates2023.csv`](../data/Candidates2023.csv).
   - They were picked by an inclusion rule, not by me.
   - Search phrases are taken word for word from the 2023 titles and calls.
3. **Held-out half.** The list is split in half by a hash of each name:
   - **Dev half:** 40 topics, used here.
   - **Held-out half:** 57 topics. It has not been fetched, so nobody has seen it yet.
4. **Mature topics dropped from the score.** Candidates whose crowd arrived before 2023 are left out of (b).

**Dev-half result:**

| Method | Flags in 2024 | Crowd arrived within 12 months | Precision |
|---|---|---|---|
| Full method (tuned) | 3 | 0 | 0% |
| arXiv only | 15 | 0 | 0% |
| Full method, mature topics left in | 7 | 0 | 0% |

**The newness test worked.** On the old list it cut flags from 16 to 5, and no small mature topic was flagged this time.

**But the test still can't score a hit.** Here is how the 40 dev topics break down:

| How the topic did | Topics |
|---|---|
| Crowd never arrived (fewer than 20 papers per 12 weeks at peak) | 24 |
| Crowd arrived in 2021 | 14 |
| Crowd arrived in 2023 | 2 |
| Crowd arrived in 2024–25, the only years a 2024 flag could count | **0** |

Half of the dev topics peak below 10 papers per 12 weeks. Workshop wording ("variable impedance learning and control", "construction robotics") is too narrow to ever draw a crowd.

The 3 topics flagged were exactly these small niches, and none of them took off. They peaked at 18, 16 and 11 papers per 12 weeks. **So 0 of 3 is a true result, but it's 3 data points.**

**What this says.** Workshop lists are the wrong place to find candidates. A workshop gets organised either after a topic is established or around a niche. Both lists, 156 topics in total, contained only 1 topic whose crowd arrived in 2024–25. That one was cross-embodiment learning, from the first list. A detector can't show precision on a list with almost no positives.

## Other findings

- **README search leaks hindsight.** When GitHub search included README text, 61 "VLA" repos showed up as created in 2021, before the term existed, because README text is what the repo says today. That gave VLAs a fake 96-week lead. GitHub now searches only names and descriptions. Run `--with-readme` to reproduce the comparison; results go to `data/backtest/WithReadme/`.
- **Hacker News can't mark consensus for RL/robotics.** No test topic ever had more than 1 story with ≥ 50 points in a 4-week window. Diffusion policies never got one at all. HN is still counted, but only for comparison.
- **Funding.** Funding scored a lead weight of 0.67 on 3 topics with 15 hand-collected rounds. Diffusion policies had none, so the weight is low-confidence.

## Limits

- The citation and lab-paper signals aren't in yet. They might add lead, and they're the most likely to do so for VLAs, since big labs drove that topic.
- arXiv phrase search matches loosely and only searches titles and abstracts. Counts may be off in either direction, though the error should be consistent across years.
- Deleted GitHub repos are missing. This biases older windows downward.
- 3 test topics is a very small sample. One topic changing its result moves (a) a lot.

## What I'd change next (proposal: not applied)

**Fix 1 was applied:** the 2023 candidates and the held-out half. It didn't make (b) testable. The held-out half stays sealed. Running it now would use up the one clean look on a test that we already know can't score hits.

1. **Replace hand-named candidates with every phrase that was new on arXiv in 2023.**
   - Take every 2–3-word phrase in 2023 cs.RO and cs.LG titles that appeared fewer than 10 times in 2021–22.
   - Keep the ones that recur at least a few times, so one-off phrases drop out.
   - This is the same set of topics the weekly brief would have to search anyway. It contains future winners and duds in their real proportions, and nobody picks them.
   - Cost: one bulk download of arXiv metadata (about 4 GB, the Kaggle snapshot or OAI-PMH) instead of a search API.
2. **Split that list by hash the same way.** The dev half is used for checks, and the other half is run once at the end.
3. **Add citations and lab papers once your keys are in `.env`.** Then re-run.

If you'd rather not build phrase mining: on what's been measured, arXiv growth alone matches the full method. The arXiv-only baseline and the full method tied on all three test topics' lead times, within 4 weeks. A weekly script that lists the fastest-growing new arXiv phrases is the simple product that's left. Phrase mining would also be the first step of that script.

## Reproduce

```bash
uv run python -m bleedingedge.backtest            # dev half
uv run python -m bleedingedge.backtest --holdout  # held-out half: run once, at the end
```

The cached API responses in `data/cache/` make re-runs free and identical. Delete that folder to refetch.
