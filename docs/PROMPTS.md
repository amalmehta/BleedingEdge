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

## 2026-11-01 — Opportunities to apply to

1. "this should also include opportunities useful to apply to"
   → Asked about types, placement, filter and kill test. You chose all four types, a short section from tomorrow's brief, work that fits and is open now, and removal if nothing is applied to in 8 weeks. Added the section, instructions, log file and tests; tested on sample data only.
2. "0, 5, 15"
   → Listed 5 things to add and 15 to improve, ranked, and no cuts. Nothing built until you pick.
3. "Build both"
   → Added bleedingedge/notify.py, called at the end of the weekly task and again by an 11:00 Monday check; moved application records to gitignored data/private/Applications.csv.

## 2026-11-16 / 18 — Week 4 commit, a project review and the pick ledger

1. "Review the uncommitted changes, commit them in sensible commits with clear messages, and push. Don't commit secrets or build output."
   → One commit (b2edcc3): the week 4 brief, study pick, opportunities, trends and trial review row. Pushed to main.
2. "0, 5, 10"
   → Listed 5 things to add and 10 to improve, ranked, and no cuts. The trial's 4 briefs are out and the review is still blank. Nothing built until you pick.
3. "Add 1 and 2"
   → The Monday notification now says the trial review is due until it's filled in. Added bleedingedge/ledger.py, which grades every pick against its own test in data/Picks.csv; the weekly task runs it each Monday, including after the trial.
4. "open this" / "open the GitHub commits page"
   → Opened the commits page in the browser pane.
5. "is this an app? whats the deliverable?"
   → No: a weekly Markdown brief from a scheduled task, plus the notification, data files, backtest and trial review. An app was deferred to the trial's call.
6. "i want a website" / "a persistent wwesbite" / "and option to send a daily email to me"
   → Asked why, hosting and the trial first. You marked all 4 picks acted on (trial passed), chose keep plus a persistent private website and a daily email via Gmail, sent only when something's new. Recorded in the spec; nothing built yet.
7. "Trend history"
   → Showed three mockups from real data. You chose the topic explorer with a pick card on top, flagged topics and picks only, the six proposed done criteria, and "today's step" Tue–Fri only. Recorded in the spec; nothing built yet.
8. "Build the site" / "*and email"
   → Built BleedingEdge Radar on the Data page type: bleedingedge/site.py writes five data files, web/radar.html draws the explorer, pick card and pick table, and your four acted-on marks are seeded. The Monday task now rebuilds and uploads the files. The daily email comes next.
9. "Build the email"
   → Added bleedingedge/daily.py and a 7:30 daily task that sends through Gmail to you, only when there are new papers, a Tue–Fri step or a deadline 14/7/3/1 days out. A real run found "policies learn" pulling in 24 unrelated papers, so added data/Fragments.csv. Nothing sent yet.
10. "Send it now" / "open the website"
   → Ran the daily task once: sent "BleedingEdge, 19 Nov: 9 new papers". Opened the site; its check found overlapping year labels on the repos chart, fixed, now passes.
11. "email should be a bit easier to rea"
   → New layout: a one-line summary first, then today's step, deadlines, your pick's papers and other early topics, each paper a linked title with a date line; quiet footer. Previewed, not sent.
12. "*so should the website"
   → Fragments left off the site; older and not-new topics fold under "Show more"; one line explains ★ and the score; plainer picks-table headings. Uploaded; recheck runs when the page is next opened.
13. "there should be an agent specifically workign to improive this daily. set up a loop and a harness" / "we want even the everyday person to get hooked, not just folks in the field (but dont reduce qulaity at all)"
   → Asked who, what it may change, how to judge and who writes explainers. Built bleedingedge/harness.py (8 checks), docs/IMPROVE.md (rules, backlog, log), explainers on the site, and a 9:00 daily improver task that opens one PR a day and ships what you merge. Friends' visits can't be counted on this page type.

## 2026-11-24: feedback in the daily email

1. "in the email, make sure to allow user to add feedback in order to improve future suggestions"
   → Asked how, what it may change, where it's kept and a kill test. You chose More/Less links plus replies, effects on the email's topics, the Monday pick and scoring, private storage, and a 4-week kill test. Scoring was agreed as a separate taste boost so the detector's scores and the ledger stay a fair test. Built bleedingedge/feedback.py, vote links and a footer line in the email, and muting and re-ranking in the Monday shortlist, with tests. The 7:30 task's new step is written in docs/INSTRUCTIONS.md, to apply after merge.

## 2026-11-26: post-trial fixes

1. "0, 10, 20"
   → Listed 10 things to add and 20 to improve, ranked, no cuts. Top finding: the weekly brief stopped picking after the trial although the review kept it (no pick since 16 Nov, so the email's "today's step" never ran). PR #4 conflicted with main.
2. "Improve 1–5"
   → Merged main into PR #4 (no history rewritten) and kept fragments off the Monday shortlist there. On a new branch: the brief runs every Monday after the trial (`brief.KEPT`), the harness fails explainers for listed fragments (open PR #3 now fails it), and the brief says "Week 5" rather than "Week 5 of 4".
3. "merged both"
   → GitHub still showed #4 and #6 open, so nothing changed; offered to merge them.
4. "Merge them for me"
   → Merged #6, merged main into #4 (both logs kept, each side's system-design lines combined), then merged #4. Pulled main into the main checkout, updated the 7:30 task to read feedback first and compose with the vote links, and dry-ran the compose.
