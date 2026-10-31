# Prompt Log

## 2026-10-25 / 26 — Interview, spec, and the backtest

1. "Read BleedingEdge.md in full and follow its meta-instructions. Use AskUserQuestion to interview me about the CONTEXT line … Write no code."
   → Four interview rounds; filled DELIVERABLES and OPEN QUESTIONS / ASSUMPTIONS; a weekly cited brief, not an app.
2. "Fill DEFINITIONS AND DEFERRED next: thresholds for heating up, outdated, leading indicator, acted on, and the scoring formula."
   → Growth ratio and score formulas, thresholds, backtest pass criteria, deferred list.
3. "Keep the 8-week lead. My reason:"
   → Asked for the missing reason; recorded "signal vs noise".
4. "also figurew out investing trends"
   → Funding rounds added as a leading signal; no buy/sell advice, ever.
5. "i caught onto RL early because it felt like the most intellectually stimulating but also most novel. robot learning at uc berkeley"
   → Added a watch-list lab signal and a 1–5 taste rating per study pick.
6. "can you give me a list and i select ..."
   → A list of late-catch candidates; you picked diffusion policies, coding agents, companies; "saw it, didn't act".
7. "Apply both: a ~2-hour first step per study pick, and companies weight 0.8."
   → Applied.
8. "alright open this bad boy up"
   → Opened the spec.
9. "sure"
   → Started the backtest: design questions (window 2021–25, API keys, funding, candidates), design doc, fetchers, scoring.
   → First run exposed method flaws (HN too sparse, burst-only missed VLAs, acronym noise, funding zeros); you chose fixes. README search found to leak hindsight and dropped. Full run: (a) passes in-sample, (b) fails at 6%. Wrote docs/BACKTEST.md with proposed fixes, not applied.
10. "Apply fixes 1 and 2: rebuild candidates from 2023 sources with a held-out half, and add the newness test to 'early'. Then re-run."
   → Added the newness test; a subagent built 97 candidates from all 2023 workshop lists by rule; hash split, held-out half sealed. Dev-half precision 0 of 3, with no reachable hits. Proposed mining new arXiv phrases.
11. "Build the phrase-mining candidate list from 2023 arXiv titles (bulk metadata), split it by hash, and re-run the dev half."
   → Harvested arXiv OAI-PMH (cs.RO/LG/AI/CL since 2021); mined 88 phrases new in 2023; dev half 52. Precision 41% vs 23% arXiv-only; caught 4 of 5 winners. Held-out half sealed.
12. "keep going"
   → Continued the harvest, mining and run.
13. "Before opening the held-out half, apply the fixes we'd want in the final method: divide by total arXiv growth and lower the 'small' bar to fit local counts. Check them on the dev half only, then stop."
   → Relative arXiv growth; small bar 30 for bulk counts (calibrated at 0.61× on 11 neutral phrases). Dev half 52% (15/29) vs 30% arXiv-only, in-sample. Held-out half not opened.
14. "Run the held-out half once with the method as it is now, and report pass or fail."
   → FAIL: 41% (12/29) vs 50%; arXiv-only 15%; 3 of 3 winners caught. Method not changed after opening.
15. "Fix the 'already crowded' error and test again on phrases new in 2024, graded on 2025–26, with a fresh held-out half and a separate cs.RO run."
   → Freshness rule (early only within 9 windows of the first flag), chosen on the spent 2023 set; grid extended to 75 windows; mined 174 phrases (all categories) and 468 (cs.RO); pre-registered, then ran dev and held-out with no changes. FAIL on both: held-out 6% (all categories, below the 13% random rate) and 45% (robotics, 7 of 9 hits from one phrase).
16. "Run the 4-week trial on cs.RO only, with the brief stating its back-test record plainly, and record this as a bar lowered after seeing results."
   → Recorded the lowered bar in the spec; built bleedingedge/brief.py, prompts/WeeklyBrief.md, docs/TrialReview.md, weekly arXiv top-up. While checking week 1, found ~30% of bulk arXiv papers misdated (OAI `created` = a later version); fixed from the arXiv id and re-ran round 2 unchanged: robotics record fell from 4 of 15 to 1 of 19 (about chance). Week 1 draft written, study pick held for your decision; scheduled task creation was denied by the permission check.
17. "Run the trial anyway as a test of the format, not the detector: write the week 1 study pick and set up the Monday task (I'll approve it)."
   → Week 1 pick: robot foundation, first step arXiv 2610.20750 (a causal analysis of VLA internals). Fixed the prompt's falsifier: 20 papers was already met at flag time, so it is now 4× today's count, the backtest's hit rule. Recorded the pick in data/Picks.csv and TrialReview; created the Monday 08:00 task.

## 2026-10-29 / 30 — Housekeeping and a project review

1. "Review the uncommitted changes, commit them in sensible commits with clear messages, and push. Don't commit secrets or build output."
   → One commit (0c24034): the shared shortcuts list and the pointer to it. Pushed to main.
2. "6,7,8"
   → Listed 6 things to cut, 7 to add and 8 to improve, ranked. Nothing built until you pick.
3. "Fix improvements 1 and 2 now: label the repo ratio correctly and read the below-random figure from the results file. Don't change the scoring."
   → Corrected the repo ratio label; the all-categories figure now comes from Run2024/Holdout/Summary.json (3%, was a stale 6%); corrected the same text in the week 1 brief; added a test. A check of mine started a real brief run by accident: stopped before scoring, it only topped up the arXiv cache.
4. "Change the all-categories wording to say the result is about random, giving the by-topic figure (1 of 14, 7%, against 6% at random), in the brief and the docs that say below random."
   → Changed the brief generator, the week 1 brief, docs/BACKTEST.md and the spec. Left the dated log of the first, misdated run as written.
