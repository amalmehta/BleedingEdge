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
