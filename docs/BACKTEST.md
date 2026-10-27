# Backtest: would the method have spotted past trends early?

**Verdict: fail, so don't run the weekly brief yet.** Criterion (a) passes, but it's in-sample, so it's weak evidence. Criterion (b) fails at 6% precision against a 50% bar. Part of that failure comes from the method, and part comes from a candidate list that can't test it. Details and the proposed fix are below.

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

## Other findings

- **README search leaks hindsight.** When GitHub search included README text, 61 "VLA" repos showed up as created in 2021, before the term existed, because README text is what the repo says today. That gave VLAs a fake 96-week lead. GitHub now searches only names and descriptions. Run `--with-readme` to reproduce the comparison; results go to `data/backtest/WithReadme/`.
- **Hacker News can't mark consensus for RL/robotics.** No test topic ever had more than 1 story with ≥ 50 points in a 4-week window. Diffusion policies never got one at all. HN is still counted, but only for comparison.
- **Funding.** Funding scored a lead weight of 0.67 on 3 topics with 15 hand-collected rounds. Diffusion policies had none, so the weight is low-confidence.

## Limits

- The citation and lab-paper signals aren't in yet. They might add lead, and they're the most likely to do so for VLAs, since big labs drove that topic.
- arXiv phrase search matches loosely and only searches titles and abstracts. Counts may be off in either direction, though the error should be consistent across years.
- Deleted GitHub repos are missing. This biases older windows downward.
- 3 test topics is a very small sample. One topic changing its result moves (a) a lot.

## What I'd change (proposal: not applied)

1. **Rebuild the candidate list so (b) can score a hit.** Use topics that were new in 2023, taken from 2023 sources as written then: arXiv listing titles, workshop calls and lab blog posts. That would put both winners and duds inside the window. Remove anything whose crowd arrived before 2023.
2. **Add a newness test to "early".** For example, the topic's 12-week paper count was under 10 two years earlier. This is an invented number, and the backtest would check it. It would stop flags on small mature topics like tactile sensing.
3. **Add citations and lab papers once your keys are in `.env`.** Then re-run.
4. **Then judge (b) again, once.** If it still fails, the honest answer is that arXiv growth alone (the baseline) is as good as this gets. A simpler weekly script that lists the fastest-growing arXiv phrases may be the whole product.

Before deciding, consider this: if the method only passes after a third redesign, (b) stops being an out-of-sample check too. One way to keep it honest is to set aside half the new candidates and look at them only once, at the end.

## Reproduce

```bash
uv run python -m bleedingedge.backtest
```

The cached API responses in `data/cache/` make re-runs free and identical. Delete that folder to refetch.
