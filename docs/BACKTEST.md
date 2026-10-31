# Backtest: would the method have spotted past trends early?

**Verdict: FAIL.** Every precision test failed the 50% bar. After a data bug was fixed (below), the robotics record is **1 of 19 flagged topics took off**. That is close to what picking at random would find.

> **Correction, 2026-10-27.** arXiv's OAI server reports `<created>` as a *later* version's date for revised papers. About 30% of harvested papers sat in the wrong month or year; for example, a May 2016 paper was dated Jan 2021. Every count made from the bulk download was affected: candidate mining, newness, the totals and phrase counts. The 3 test topics were not affected, because they use arXiv search.
>
> The fix takes the first-version month from the arXiv id (`arxiv_bulk.first_version`). Round 2 was re-run on corrected data with the method unchanged; see [Round 2 results](#round-2-results). Round 1 (2023 phrases) was **not** re-run. Its numbers below were computed on misdated data, so treat them as unreliable.

| Round 2, corrected | All categories, held-out | Robotics, dev + held-out |
|---|---|---|
| Flagged topics that took off | 1 of 14 (7%) | **1 of 19 (5%)** |
| Share of all candidates that took off (picking at random) | 6 of 93 (6%) | 6 of 491 (1%) |
| Precision by window, full method | 3% (1/31) | 7% (2/30) |
| Winners caught | 1 of 6 | 1 of 6 |

Criterion (a) passes, but it's in-sample, so it's weak evidence.

Round 1 ran on 2026-10-26 over Jan 2021 – Dec 2025 (65 four-week windows). Round 2 ran on 2026-10-27 over Jan 2021 – Oct 2026 (75 windows; outputs in `data/backtest/Run2024*/`). Round 1 used, 3 test topics, 59 candidate topics. The signals were arXiv, new GitHub repos and funding rounds. Citations and lab papers were left out because they wait on API keys. Every count, query URL and chart is in [BacktestResults.md](BacktestResults.md), which is generated. Raw counts are in `data/backtest/Counts.csv`.

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

## Third run: candidates mined from arXiv

**What changed (2026-10-27):**

1. **Nobody picks the candidates.** I downloaded metadata for every arXiv paper since 2021 in cs.RO, cs.LG, cs.AI and cs.CL: about 420,000 papers, CC0 licensed.
   - A **candidate** is a 2–3-word phrase that was in at least 8 titles in 2023, but in fewer than 10 papers (titles or abstracts) in 2021–22. Both cutoffs are invented.
   - Only data up to the end of 2023 chooses the candidates.
   - The code is [`bleedingedge/mining.py`](../bleedingedge/mining.py), and the list is [`data/CandidatesMined2023.csv`](../data/CandidatesMined2023.csv): 88 phrases.
2. **Counts come from the downloaded metadata.** For these candidates, arXiv counts come from the bulk download instead of the search API. GitHub and Hacker News are still searched online.
3. **Same hash split as before.** The dev half has 52 topics. The held-out half has 36 and is still sealed.

**Dev-half result:**

| Method | Flags in 2024 | Crowd arrived within 12 months | Precision | Topics flagged | Topics that hit |
|---|---|---|---|---|---|
| Full method (tuned) | 46 | 19 | **41%** | 12 | 4 |
| arXiv only | 117 | 27 | 23% | 20 | 4 |

"Flags" counts each topic once per 4-week window it was flagged in, so one topic can count several times.

**What it got right:**

- **The test can finally score hits.** 5 of the 52 dev topics had their crowd arrive in 2024–25.
- **It caught 4 of those 5:** flow matching, low-rank adaptation (LoRA), large vision-language models, and chain-of-thought reasoning. It missed "reasoning in language".
- **GitHub earns its place on this list.** Both methods caught the same 4 winners. The full method flagged about a third as many topic-windows (46 vs 117) and wasn't fooled by "AI act" or "latent diffusion". That's the first evidence that a second signal adds anything. On the 3 test topics, it added nothing.

**What it got wrong:**

- **Precision is 41%, below the 50% bar.** Most misses are one topic flagged many times. "Large multimodal models" was flagged in 10 windows, but its crowd had already arrived in Nov 2023.
  - The cause: "early" means fewer than 50 papers in 12 weeks. On these 4-category counts, 50 is generous. A topic can be crowded at 30 papers.
  - I haven't changed it. Tuning on the dev half after seeing it would spend its credibility.
- **Counted by distinct topic, precision is 33%.** 4 of the 12 flagged topics took off.

**Before trusting this, know that:**

- **This list is mostly LLM and generative-AI topics.** 80 of 88 candidates are tagged AI tooling and only 8 robotics. Robotics phrases rarely reach 8 titles a year. So this run tests the method on AI topics, not on your main domain.
- **cs.CV isn't in the download.** Diffusion and vision work mostly lives there, so some phrases ("latent diffusion") look newer than they are.
- **arXiv itself is growing.** It had about 30% more papers each year in these categories (39k in 2021, 91k in 2025). Every topic's growth ratio is inflated by that much. A fix would divide by total volume, but it isn't applied.
- **I adjusted the mining rules twice before this run.** That included keeping hyphenated words whole and dropping title boilerplate like "leveraging large language". I did it after reading the 2023 candidate list, but before looking at any 2024–25 outcome.

## Held-out result

I ran this once, with the method frozen as it was after the final fixes:

```bash
uv run python -m bleedingedge.backtest --holdout
```

- The output is in `data/backtest/Holdout/`.
- The 36 held-out topics had never been searched on GitHub or Hacker News or scored before this run.
- This is the only clean number in this document. **(b): 41%, fail.**

| Method | Flags in 2024 | Crowd arrived within 12 months | Precision | Topics that hit / flagged |
|---|---|---|---|---|
| Full method (tuned weights) | 29 | 12 | **41%** | 3 / 7 |
| Full method (untuned, all weights 1) | 27 | 12 | 44% | 3 / 7 |
| arXiv only | 91 | 14 | 15% | 3 / 19 |

**What it got right:**

- **It caught all 3 held-out topics whose crowd arrived in 2024–25:** hallucination detection, prompt optimisation, and large vision-language models. Across both halves it caught 7 of 8.
- **Its flags beat chance by a wide margin.** Only 8 of the 88 mined candidates (9%) took off in 2024–25. Picking at random, about 1 in 11 flags would hit. The detector's flags hit about 4 in 10.
- **The extra signals pay off on clean data.** Adding GitHub cut false flags from 91 to 29, compared with arXiv alone, and kept every hit.
- **Lead weights from the test topics didn't help.** Tuned (41%) is no better than untuned (44%).

**What it got wrong:**

- **4 of the 7 flagged topics had already been crowded since 2023:** "foundational models", Segment Anything, "GPT models" and "chain of thought".
- **The cause is that "early" asks whether a topic is small and new, but not whether its crowd already came and went.** A topic that peaked early and then settled can still look small.
- **This is the obvious next fix, and I haven't made it.** Changing the method after opening the held-out half would make this test worthless. A fix needs fresh held-out data, for example phrases new in 2024, graded on 2025–26.

**Before relying on these numbers:**

- 29 flags from 7 topics is a small sample.
- 33 of the 36 held-out topics are AI/LLM, not robotics.
- Citation and lab-paper signals were never added.

## Final fixes: relative growth and a calibrated "small" bar

These were decided 2026-10-27, before the held-out half was opened.

1. **Relative growth.** A topic's arXiv growth ratio is now divided by the same ratio for all harvested papers.
   - Without this, arXiv's own growth (about 30% a year in these categories) counted as every topic heating up.
   - Example: a topic that only keeps pace with arXiv now scores 1, not 1.3.
   - This applies to arXiv only. GitHub repos and funding are left as they were.
   - For the 3 test topics, arXiv counts come from search across all categories, but they're divided by the 4-category total. That's an approximation.
2. **"Small" bar calibrated to the downloaded counts.** The downloaded counts cover 4 categories and match whole words only, so they come out lower than arXiv search counts for the same phrase.
   - I checked 11 neutral phrases that are neither test topics nor candidates, such as "imitation learning" and "federated learning". The download counted a median of 0.61 of what search counts.
   - So "small" for mined topics is now fewer than 30 papers in 12 weeks (50 × 0.6). The test topics keep 50.
   - Calibration data: [`data/backtest/calibration/SmallBar.txt`](../data/backtest/calibration/SmallBar.txt).

**Each fix's effect on the dev half** (full method, tuned):

| Version | Precision | Flags | Topics that hit / flagged | arXiv-only precision |
|---|---|---|---|---|
| Third run (neither fix) | 41% | 46 | 4 / 12 | 23% |
| Relative growth only | 44% | 41 | 4 / 10 | 26% |
| Small bar only | 48% | 33 | 4 / 12 | 27% |
| **Both (final)** | **52%** | 29 | 4 / 10 | 30% |

Criterion (a) is unchanged at 16 / 16 / 48 weeks.

**What the fixes do:**

- **Both fixes only remove flags.** They catch no new winners: it's the same 4 of 5 either way.
- **Most of the removed flags were repeats.** "Large multimodal models" dropped from 10 flags to 5.
- **The remaining misses are topics whose crowd arrived in 2023:** large multimodal models, Segment Anything and AI-generated text. They were still under 30 papers per 12 weeks when flagged in 2024.

**How much to trust 52%:**

- **It's in-sample.** I picked these fixes after seeing the dev half.
- **The 29 flags aren't independent.** One topic is flagged in several windows.
- **The margin is one hit.** A rough 95% interval on 15 of 29 is 34–69%.

**The held-out half is the real test.** Open it once, with nothing changed in between:

```bash
uv run python -m bleedingedge.backtest --holdout
```

## Other findings

- **README search leaks hindsight.** When GitHub search included README text, 61 "VLA" repos showed up as created in 2021, before the term existed, because README text is what the repo says today. That gave VLAs a fake 96-week lead. GitHub now searches only names and descriptions. Run `--with-readme` to reproduce the comparison; results go to `data/backtest/WithReadme/`.
- **Hacker News can't mark consensus for RL/robotics.** No test topic ever had more than 1 story with ≥ 50 points in a 4-week window. Diffusion policies never got one at all. HN is still counted, but only for comparison.
- **Funding.** Funding scored a lead weight of 0.67 on 3 topics with 15 hand-collected rounds. Diffusion policies had none, so the weight is low-confidence.

## Limits

- The citation and lab-paper signals aren't in yet. They might add lead, and they're the most likely to do so for VLAs, since big labs drove that topic.
- arXiv phrase search matches loosely and only searches titles and abstracts. Counts may be off in either direction, though the error should be consistent across years.
- Deleted GitHub repos are missing. This biases older windows downward.
- 3 test topics is a very small sample. One topic changing its result moves (a) a lot.

## Round 2: phrases new in 2024, graded on 2025–26

**Written 2026-10-27, before any 2024 result was seen.** Everything below is fixed before the run.

**Changes to the method.** All were chosen on the spent 2023 set (dev and held-out combined, 88 topics).

1. **Freshness.** A topic counts as "early" only within 9 four-week windows (36 weeks) of its first heating-up flag. After that, the detector has already told you.
   - Most 2023 misses had been flagged in 2023 already, plateaued, and then got flagged again in 2024.
   - On the 2023 set, the full method went from 47% to 70% and kept all 7 winners. arXiv-only went from 22% to 41%.
   - Shorter settings scored higher but lost winners: 24 weeks gave 74%, but with 6 of 7 winners.
   - An age-since-first-papers test was also tried. It changed nothing for the full method, so it was dropped.
2. **Longer window grid.** The grid now runs to 5 Oct 2026: 75 windows instead of 65, so 2025 flags can be graded on 2025–26.
   - This moves every topic's peak, so the 2023 numbers above would shift slightly if re-run. The 3 test topics are re-fetched to the new end date.
3. **Everything else is unchanged:** relative arXiv growth, the "small" bar of 30 for downloaded counts, lead weights from the test topics, and the 50% bar.

**Two runs.** Each is split by the same hash into dev and held-out halves:

| Run | Candidates | Title bar | File |
|---|---|---|---|
| **All four categories** | 2–3-word phrases in ≥ 8 titles in 2024 and in < 10 papers in 2022–23 | 8 | `data/CandidatesMined2024.csv` |
| **Robotics** | The same, but titles from cs.RO papers only | 8 × cs.RO's share of 2024 papers, at least 3 | `data/CandidatesMined2024RO.csv` |

- Phrases are counted in all four categories in both runs.
- Flags are judged in 2025. A hit means the crowd arrived within the next 12 months, which is data up to Oct 2026.
- Flags from late 2025 get less than 12 months to be proven right. That makes this test stricter, not easier.

**Order.** For each run, the dev half goes first, then the held-out half straight after. Nothing is changed in between, because the method was fixed on 2023 data.

**Pass.** A run passes if the held-out half reaches ≥ 50% precision with tuned weights. The dev half is reported too.

## Round 2 results

**Run 2026-10-27, as pre-registered above, then re-run the same day on corrected dates.** The method was not changed between or after runs. The corrected run replaces the first one. Both fail.

| Corrected data | All, dev | All, held-out | Robotics, dev | Robotics, held-out |
|---|---|---|---|---|
| Candidates in the half | 91 | 93 | 253 | 238 |
| Took off in 2025–26 (base rate) | 8 (9%) | 6 (6%) | 2 (1%) | 4 (2%) |
| Precision by window, full method (tuned) | 22% (7/32) | **3% (1/31)** | 0% (0/8) | **9% (2/22)** |
| Precision by window, arXiv only | 9% | 16% | 0% | 8% |
| Flagged topics that took off | 3 of 14 | 1 of 14 | 0 of 8 | 1 of 11 |
| Winners caught | 3 of 8 | 1 of 6 | 0 of 2 | 1 of 4 |

**The first run, on misdated data** (kept in `data/backtest/Misdated/`): robotics held-out scored 45% (9/20), with 4 of 15 topics across both halves; all categories held-out scored 6%. **Most of the robotics result came from the date bug.**

**What this says, plainly:**
1. **Robotics: indistinguishable from chance.**
   - One flagged topic took off out of 19 ("physically grounded", again flagged in 8 windows running).
   - At a 1% base rate, picking 19 at random would land at least one winner about 1 time in 5 (an estimate: 1 − 0.99¹⁹ ≈ 17–21%). One hit is not evidence that the method works.
2. **All categories: about random.** On held-out phrases, 1 of 14 flagged topics took off (7%), against 6% at random. By window, the method scored 3%, worse than arXiv alone (16%). The dev half's 22% didn't carry over.
3. **Criterion (a) still passes** on the 3 test topics, at 20 / 20 / 68 weeks. It is in-sample and unaffected by the bug.

**Known biases** (direction estimated, not measured):
- Late-2025 flags had less than 12 months to be proven right, which pushes precision down a little.
- Some phrases are fragments ("platform for autonomous", "system for robotic"). They count, because an automatic miner produces them.
- Dates estimated from arXiv ids are accurate to within the month. That is finer than the 4-week windows can resolve.

## Next: your call

On 2026-10-27 you chose a robotics-only 4-week trial, with the brief stating its record and the bar recorded as lowered after seeing the results. That choice rested on the record "4 of 15 topics took off".

Corrected, the record is 1 of 19, which is about chance. The trial is built (`bleedingedge/brief.py`, `prompts/WeeklyBrief.md`) and the week 1 draft exists. No study pick has been written yet, because the premise changed.

1. **Stop.** The backtest has now failed three times on clean data.
2. **Run the trial anyway, as a test of the format, not the detector.** The brief already states "1 of 19" plainly.
   - What the trial can still tell you: whether a weekly, small, firm study pick gets you to act. You said acting, not spotting, was the problem with diffusion policies and coding agents.
   - Picks would then be roughly as good as a well-read guess.

## Reproduce

```bash
uv run python -m bleedingedge.sources.arxiv_bulk  # bulk arXiv metadata, ~2.5 h the first time, resumable
uv run python -m bleedingedge.mining              # mine candidates from it
uv run python -m bleedingedge.backtest            # dev half
uv run python -m bleedingedge.backtest --holdout  # held-out half: run once, at the end
uv run python -m bleedingedge.mining 2024 --ro    # round 2: phrases new in 2024 (drop --ro for all categories)
uv run python -m bleedingedge.backtest --year 2024 --ro [--holdout]
```

The cached API responses in `data/cache/` make re-runs free and identical. Delete that folder to refetch.
