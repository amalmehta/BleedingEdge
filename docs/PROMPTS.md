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
