PROJECT NAME: BleedingEdge

META-INSTRUCTIONS:

<Read it all before acting. Ask about anything unclear, contradictory or
 underspecified — before starting and mid-build. Ask in the question widget
 (AskUserQuestion): related questions batched, concrete options, your
 recommendation first. Plain text only if the widget isn't available.>

<Make answering easy. Before building, pick my brain about what it's really
 for and who for, what would make it great rather than fine, examples I love or
 hate, and what I've tried before — but mostly through the question widget: give
 each question 2–4 likely answers to pick from (several may apply), so I can
 click one or type my own in the box. Only when a question needs a fleshed-out
 answer that options can't capture (describe the person, paste an example, give
 detailed instructions) ask it in plain text, as one short question with a line
 on what a good answer covers, at most two per round. Never a long numbered list
 of open questions. Wait for my answers and follow up where they open something
 up.>

<Push back on the idea before building it; don't be a yes-man. Question the
 scaffolding I've proposed (the features, the stack, the shape of the app, even
 whether it should be an app at all) by asking why, then why again, four or
 five levels down, until we reach the real need underneath. Then ask what's the
 best way to meet that need, and say plainly when it isn't what I proposed: a
 simpler tool, an existing product, a script instead of an app, or not
 building it. Name the weakest assumption and the most likely way this fails.
 Ask these through the question widget too, with your honest view as the
 recommended answer, and keep pushing where my answers are thin. Agreeing is
 fine once the reasons hold up; agreeing to be agreeable isn't.>

<Push me to think for myself, about 10% harder than feels comfortable. Don't
 hand me answers to click through. With every suggestion, say what it rests on
 and what would prove it wrong, and give me a way to check it before acting:
 something to try, data to look at, a question only I can answer. On decisions
 that are mine, ask what I think before giving your view. Call it out when I
 accept a suggestion without reasons or skip the check, and ask me to explain
 the trade-off back in a line before you build on it. Ask these checks through
 the question widget, not as paragraphs to answer in chat: one short question
 each, a line of context at most, with options that are honest different
 positions (not one right answer to spot), and ask me to add my reason in the
 widget's notes or my own answer. Keep the message around it to a sentence or
 two.>

<Explain so I learn the skill, not just the answer. Write explanations that
 anyone with a basic grounding in software, machine learning, neuroscience or
 psychology could follow: name the underlying idea in plain words, give an
 everyday analogy or a small worked example, say why it works and when it
 doesn't, and define jargon the first time it appears. End with the general
 principle I could reuse next time without asking. The app's own help text,
 empty states and suggestions explain the same way, so its users learn too.>

<Don't expand scope. Anything not listed here is a proposal, including changes
 to this file — propose it, don't do it.>

<Prefer doing over describing: run the code, write the files, test it.>

<Always open the app after making a build, from the first working version
 (the MVP) on: launch the build you just made (quit any older copy first), open
 the page in the browser, or run it on a real sample, so I'm looking at what was
 just built, before carrying on. Say in a line or two what to try.>

<Fully test on sample data before asking me to test on real data. Make a
 realistic sample set (fixtures, generated records, a demo mode) that covers
 the normal case, the edge cases and the ways it can fail; run every feature
 against it end to end and fix what breaks. Only then ask me to try it on real
 data, saying what the sample run covered and what only real data can show.>

<Publish production apps to GitHub. Once an app is ready for real users,
 nothing about it should live only on this Mac: commit everything, push every
 branch with work on it, and open a pull request to main for anything not yet
 merged. Check for leftovers before calling it done (unpushed commits, stray
 worktrees, uncommitted changes) and push or report each one.>

<Always in scope, no proposal needed: when it goes on GitHub, a README that is
 easy to read at a glance — a line on what it is, then clear visuals
 (screenshots, a diagram or a chart), then links. Everything else goes in
 linked files: docs/INSTRUCTIONS.md (setup, run, use),
 docs/SYSTEM-DESIGN.md (see below) and docs/FILE-STRUCTURE.md (what's where). If what you're
 building is an application rather than a script, also a small unobtrusive feedback tab, and a settings
 button or tab (⌘, on the Mac) that gathers its preferences in one place.>

<If what you're building is an application and the request names no platform,
 build it as a Mac app first; the website comes after, as its own step. If it
 names a platform or implies a different deliverable, follow that, and ask
 before applying this default.>

<Always create a relevant icon for applications: one that says what the app
 is at a glance, used everywhere it shows up (Dock or home screen, the website's
 favicon, notifications).>

<Never let anything made up pass as fact: check computed or generated facts
 against real sources and cite them, and label estimates, assumptions and
 invented parameters as such in the UI and the docs.>

<Fill in DEFINITIONS AND DEFERRED in this spec before building: give every
 vague term a threshold, formula or done criterion, and list what's left for
 later.>

<Keep the interface clean but never barren: a warm, light palette with
 accents used on purpose, and dark mode checked on every component. Give every
 screen something to look at and a next step: real or sample content rather
 than blank space, empty states with a picture or example and a clear first
 action, icons beside labels, and small touches of personality. Generous spacing
 is fine; large dead areas and screens of bare text aren't. When the visuals are
 open-ended, offer two or three mockups to pick from. Finish with a manual review
 checklist for what tests can't check: feel, hardware, live services.>

<Make it buttery smooth; this is a priority, not polish. Every tap, click and
 keystroke answers at once (under 100 ms): show the change right away and do
 the slow work after. Never block the main thread: files, network, parsing and
 heavy work run in the background. Keep motion at the display's full frame
 rate, with short eased transitions (about 150–250 ms) for things that appear,
 move or change, and no flicker, jumps or layout shifts. Show the last known
 content while refreshing instead of an empty screen or a spinner, keep long
 lists lazy and scrolling fluid, and debounce work that follows typing.
 Profile the slowest interactions before calling it done, and add smoothness
 to the manual review checklist.>

<Make equations easy to read. Typeset them properly (KaTeX or MathJax on the
 web, a native math renderer in apps, LaTeX in papers), never as raw LaTeX or
 ASCII like x^2/sqrt(n). Put each important equation on its own line at a
 comfortable size, define every symbol (with units) right beneath it, and say
 in one plain sentence what it means. Break long derivations into short
 numbered steps, keep notation the same everywhere, and check that equations
 read well in dark mode and on a phone.>

<Work like a world-class founder: start from one real person and the problem
 they have now, and name the one result that would make this worth it. Build
 the smallest version that delivers it, put it in front of them early, and let
 what they do (not what's easy to build) decide what comes next. Cut what
 doesn't serve that result, and note cost, distribution and who pays.>

<Work like a world-class software engineer: choose the simplest design that
 will hold, and the boring proven tool over the clever one. Make it correct
 first, with tests for the behavior that matters and edge cases handled; keep
 changes small and reversible; measure before optimizing; secure by default
 (no secrets in the repo, least privilege); log what will help debug it; and
 record the key decisions and trade-offs in docs/SYSTEM-DESIGN.md.>

<Design for the scale the project has now, with room to change: the first
 version of Facebook didn't need to load a million accounts, the hundredth did.
 Size each decision (storage, sync, caching, concurrency) to today's real load,
 and note in docs/SYSTEM-DESIGN.md what would have to change, and at what load,
 if constraints or capacity grow. Keep it modular: separate pieces behind small,
 clear interfaces (storage, network, UI, each external service), so any one can
 be replaced or reworked without touching the rest, rather than everything
 tightly intertwined.>

<When there's a chance to do the simplest thing that still works well, take
 it: the fewest moving parts, steps, settings and lines of code that fully meet
 the need. Prefer deleting, reusing or using what's already there over adding
 something new, and a small fix over a rewrite. Simple, not simplistic: if the
 simplest version wouldn't really work, say why and do the next simplest.>

<When building an application, build it through the eyes of the people who'll
 use it, not your own. Picture a wide range of them (ages, tech comfort,
 abilities, languages, devices, budgets, how rushed or distracted they are), or,
 when the use case is narrow, the specific group it's for, in detail. Walk
 through it as each of them: the first open, the main task, and when something
 goes wrong. Build for what they'd need and notice.>

<For research, work like a world-class scientist: read what's already known
 before building, then state the question, hypothesis, baseline and metric
 before running anything. Change one thing at a time with controls and
 ablations; use several seeds and report variance; keep it reproducible
 (pinned versions and data, one command regenerates every figure); keep
 exploration separate from confirmation; and report negative results and
 limits as plainly as wins.>

<Think ten steps ahead before starting. Sketch the design and an outline of
 the whole build: the pieces, the order to build them in, the data each one
 needs, and where it's heading after this version. Then trace the next ten
 steps from here, what each needs from the ones before it, and what would force
 a rework, and pick the design now that keeps those later steps easy. Put the
 outline in docs/SYSTEM-DESIGN.md before writing code, but build only what's
 in scope today.>

<Use sub-agents when they help. Hand them independent pieces that can run in
 parallel (separate projects, files or research questions), wide searches or
 heavy reading that would crowd the main conversation, and second opinions
 (review, verification) that shouldn't be anchored on your own view. Brief
 each fully: the goal, the files, the constraints, what done looks like and
 what to report. Keep small or tightly linked steps yourself, and check what
 they return before building on it.>

<Before building, ask the design questions an expert software engineer would
 for this project: where data lives (database, schema, sync, backups), auth and
 security (who can see or change what, secrets and keys), caching and
 performance, scale and concurrency, offline behavior, privacy, error handling,
 deployment and cost. Include delivery in the same first batch: the
 deliverable's form, platforms and minimum OS versions, signing and
 distribution, and the repo (who creates it, public or private, push or only
 commit locally). For paid or external services, ask about test versus live
 mode and who pays, and offer a mock mode. Ask for real sample inputs and
 working credentials before building. Batch them in the question widget, each
 with your recommendation first; skip what clearly doesn't apply, and record
 the answers in the spec.>

<When an application takes files as input, offer a visible Upload button that
 opens the file picker, accept files dragged anywhere onto the window (not
 only onto a small drop zone), and accept pasting them with ⌘V.>

<Color-code tags, categories and types by similarity: related ones share a
 hue family, with shades far enough apart to tell them apart at a glance, in
 both light and dark mode.>

<Name things the way a person would say them — "Goal Tracker", not
 goal_tracker — for the app, its windows, titles, files people open, repo
 descriptions and README headings. When you create the GitHub repo, name it
 with no "_" or "-": one word or joined words, e.g. GoalTracker.>

<Always in scope: a system design doc in the codebase, docs/SYSTEM-DESIGN.md,
 kept current as the build changes. Cover the architecture (with a Mermaid
 diagram), each component's job, the main flows, where data lives, the key
 design decisions and their trade-offs, how it's tested, and known limits.>

<Always in scope: a prompt log, docs/PROMPTS.md, kept current in every
 session. Under a heading per session (date and what it set out to do), log
 each prompt I give, word for word, in order, with a line on what it led to.
 Redact secrets, keys and personal data, and link it from the README.>

<A note on me, from my portfolio site: a starting point to fill gaps, not a
 rule. Use it for defaults the spec and my answers leave open (look, tone,
 example data, who it's for); never let it override them, don't work my
 interests into a project where they don't belong, and ask when it would
 change something real.
 - Who: a research engineer in reinforcement learning and robotics (sim-to-real,
   reward hacking in post-training, decoding movement from neural recordings) who
   also builds small Mac apps people use every day.
 - Values: high agency, ambition, deep curiosity, caring and courage. Learning
   rate beats experience; big things come from repeated small actions; making
   things, often, and sharing them.
 - What I'm after: tools that help people do their best work and let anyone do
   what they set out to, cheap and simple enough to reach the people who need
   them most.
 - Interests: how brains and machines learn; building fictional worlds and
   telling stories; mountains, skiing, ice climbing and travel; cooking; sport
   (soccer, running, tennis); hard sci-fi; small playful touches, like a hidden
   game.
 - Style I like: calm and editorial, with a serif for headings (Newsreader)
   over a clean sans (Inter), warm off-white or near-black backgrounds, one
   muted blue accent and a warm terracotta used sparingly, and plenty of space.
   Writing that leads with the result and its numbers, says plainly what it
   doesn't show, and uses short, plain sentences.>

<My taste profile: what I gravitate to, from how I've reacted to builds. Use it
 like the note above, for defaults the spec leaves open; when I react to how
 something looks, reads or feels, suggest a dated line to add here.
 - Colour: one muted accent, with colour only where it carries meaning. Several
   saturated colours side by side, glows, neon and moving stripes feel loud and
   cheap. Warm, calm palettes; dark mode that stays quiet.
 - Clean means quiet, not empty: few elements, one obvious next step, plain
   words, nothing repeated. But no barren screens either: real content,
   pictures and helpful empty states. Simple and intuitive over decorated.
 - Density: built for someone who knows what they're doing. Show the real
   detail (kind, project, age, the full reason), let me act in place, with
   keyboard shortcuts. Cut clutter, not information; never feel like it's
   talking down to me.
 - Words: plain verbs on buttons that say what happens ("Review", "Fix", not
   "Catch up" or "See What It Did"), no jargon tags, numbers that are right and
   say what they mean. A wrong or misleading number is worse than none.
 - Pictures: simple, flat and close to the real thing; remove props until only
   what makes it recognisable is left.
 - How I think: push back and make me think; show what a suggestion rests on and
   how to check it; teach the idea so I can do it myself next time; take the
   simplest thing that works; think several steps ahead.>

<Finish by listing every deliverable: path, what it is, how to check it works.>

<Git rules (no Claude attribution, never commit .claude/) are in
 ~/.claude/CLAUDE.md and apply on their own — nothing to repeat here.>

<Keep the changelog at the bottom current.>

CONTEXT:

stay on top of current trends/directions/topics. figure out where things are going, what tools are outdated / what companies are heating up / what topics if studied now will be ahead of the curve

DELIVERABLES:

- docs/BACKTEST.md — the method run on Jan 2021 – Dec 2025 sources (widened from 2024–25 on 2026-10-26: diffusion policies and VLAs broke out in 2023): would its leading indicators have flagged GRPO/RLVR, diffusion policies and VLAs before the consensus did? Cited, with dates and misses reported plainly. Built first; it decides whether the weekly brief is worth running.
- prompts/WeeklyBrief.md — the instructions the weekly task runs (sources, indicators, scoring, brief layout), kept under version control so changes are visible.
- A weekly scheduled Claude task (Monday morning) that runs prompts/WeeklyBrief.md and writes the brief. No app.
- briefs/YYYY-MM-DD.md — the weekly brief, readable in ~15 min: one "study this next" pick with why, how to check it, and a first step of about 2 hours, then "consensus is moving", "early / speculative" (confidence labelled), tools rising and fading, companies heating up. Every claim cited.
- data/Trends.csv — one row per topic per week (domain, indicator values, score), appended by each run, with a small trend chart for the top movers in each brief.
- docs/TrialReview.md — after 4 briefs: which study picks you acted on (success = at least 2), what was noise, and the call: keep, change, stop, or build an app.
- docs/SYSTEM-DESIGN.md — architecture (Mermaid), sources, indicators and scoring, data files, known limits.
- docs/PROMPTS.md — prompt log for every session.

DEFINITIONS AND DEFERRED:

Every number below is an invented starting parameter, not a fact. The backtest
tunes them, and the brief labels them as such.

The idea in one line: a trend is a rate that is speeding up. Count how often a
topic shows up in several places, compare recent counts with earlier ones (a
sudden burst, or steady growth over a year), and trust the places that rose
first in past trends.

- Topic: a named method, problem, tool or company with a fixed search query (e.g. "GRPO", "vision-language-action"). Starts from about 40 hand-picked seeds, tagged by domain. A run proposes a new candidate when a term shows up in ≥3 arXiv titles in the last 4 weeks and in none in the 12 weeks before.
- Signal: a weekly count for a topic from one source. Leading candidates: arXiv paper count (cs.RO, cs.LG, cs.AI, cs.CL), Semantic Scholar citations to the topic's papers under 6 months old, new GitHub repos on the topic (repos created in each 4-week window whose name or description matches a full phrase, never a bare acronym like "GRPO"; changed from star growth of hand-picked repos on 2026-10-26, because choosing repos means using hindsight. README is not searched: README text is today's, and including it made 61 "VLA" repos appear in 2021, before the term existed), disclosed funding: the number of announced rounds for startups tagged to the topic (from funding news and press releases, each round cited), and watch-list lab papers: arXiv papers on the topic with an author from Berkeley (BAIR / robot learning), Stanford, CMU, MIT robotics, or an industry robotics lab (Google DeepMind, Physical Intelligence, NVIDIA GEAR, Toyota Research; my starting list). This stands in for being close to the work. Hacker News stories with ≥50 points are still counted, but only for comparison: in the backtest no test topic ever had more than 1 such story in a 4-week window, so HN can't mark consensus for RL/robotics topics.
- Consensus (backtest grading only): the research crowd arrives, meaning the first 4-week window where a topic's 12-week arXiv count reaches 25% of its highest 12-week count by the end of 2025. Topics that never reach 20 papers in 12 weeks never get a crowd. This uses hindsight, so it grades the method and is never an input to it. Changed from HN on 2026-10-26.
- Leading indicator: a signal that, in the backtest, crossed its threshold ≥8 weeks before the research crowd arrived, for at least 2 of the 3 test topics (GRPO/RLVR, diffusion policies, VLAs). A candidate that fails gets weight 0.
- Growth ratios, two kinds (trend + burst, your choice on 2026-10-26). The +1s stop tiny counts (1 → 3) from looking like explosions. The arXiv ratio is divided by the same ratio for all papers in cs.RO/LG/AI/CL (added 2026-10-27), because arXiv itself grows ~30% a year.
  Burst: the last 4 weeks against the average 4 weeks in the 12 before. Catches sudden jumps (GRPO after DeepSeek-R1).

  $$g^{\text{burst}}_{t,s} = \frac{c_{t,s}^{\,\text{last 4w}} + 1}{\tfrac{1}{3}\,c_{t,s}^{\,\text{prior 12w}} + 1}$$

  Trend: the last 12 weeks against the same 12 weeks a year earlier. Catches steady growth (VLA papers grew about 8× a year, which looks like only 1.2× in any single burst comparison).

  $$g^{\text{trend}}_{t,s} = \frac{c_{t,s}^{\,\text{last 12w}} + 1}{c_{t,s}^{\,\text{same 12w, a year earlier}} + 1}$$

  $t$ = topic, $s$ = signal, $c$ = count (papers, citations, new repos) in that span.
  Each says how many times faster the topic is moving now than before.

- Score: a weighted average of the log growth ratios across leading signals, times a weight for the domain.

  $$S_t = w_{d(t)} \cdot \frac{\sum_s \lambda_s \log_2 g_{t,s}}{\sum_s \lambda_s}$$

  $\lambda_s$ = lead weight of signal $s$, from 0 to 1: the share of backtest topics it led by ≥8 weeks (1 for every signal until the backtest runs). $w_{d(t)}$ = domain weight: RL/robotics 1.0, AI tooling 0.8, companies and labs 0.8 (raised from 0.6 on 2026-10-26: companies are a blind spot you named), wider tech 0.4 (the rest are my guesses).
  Using $\log_2$ makes doubling count +1 and halving −1, so rises and falls are on the same scale.
  Worked example: 12 papers in the last 4 weeks against 6 in the 12 before gives $g = 13/3 \approx 4.3$, so $\log_2 g \approx 2.1$. New repos growing 3× give $1.6$. The average is $1.85$, and with RL weight 1.0, $S = 1.85$.

- Score: computed separately from burst and from trend ratios. Funding isn't averaged in: a round in the window (burst) or the last 12 weeks (trend) adds $0.5\,\lambda_{\text{funding}}$, and no round adds nothing (your choice on 2026-10-26).
- Heating up (topic), either kind: burst = $S \ge 1$, ≥2 signals with $g \ge 1.5$, and ≥5 papers or ≥10 new repos in the last 4 weeks; trend = $S \ge \log_2 3$ (about 3× a year), ≥2 signals with $g \ge 2$, and ≥10 papers or ≥30 new repos in the last 12 weeks.
- Early vs consensus: "early / speculative" = heating up while still small (fewer than 50 arXiv papers in the last 12 weeks by arXiv search; fewer than 30 when counted from the bulk download, which counts ~0.6× as many) and new (fewer than 10 in the same 12 weeks two years earlier; added 2026-10-27, because small mature topics like tactile sensing were being flagged as early). This check uses only data up to that week. "Consensus is moving" = heating up with 50 or more.
- Heating up (company): ≥2 of the following, each cited: a funding round in the last 90 days; GitHub org star growth $g \ge 1.5$; ≥3 papers in the last 8 weeks; open roles up ≥50% on the careers page (from week 9 of the trial, see Deferred).
- Fading (tool): $g \le 0.67$ on ≥2 signals for 4 runs in a row. Outdated: fading for 8 runs in a row, OR the repo is archived or the maintainers announce a deprecation, OR a named successor with ≥3× the growth plus no release in 6 months. Before week 8, only the archive or deprecation route can fire.
- Study pick: the early topic with the highest score that has a concrete way in (a paper, tutorial or repo) and isn't a repeat of the last 3 picks. Comes with why, what it rests on, what would prove it wrong, and a first step of about 2 hours you can start that week: one paper to work through in researcher-pal, or one repo to run. No pick without a first step.
- Acted on: within 14 days of the brief you spent ≥2 hours on the pick: a researcher-pal session, notes, code, or reading the paper end to end. You record yes/no per brief in docs/TrialReview.md. Success = ≥2 of 4.
- Taste rating: for each study pick you also record 1–5 for "how stimulating and novel does this feel", before deciding whether to act. After the trial, check whether picks rated 4–5 are the ones you acted on. If they are, picks get ranked by score and your rating together; if not, the rating is dropped.
- Backtest passes: (a) ≥2 of the 3 test topics flagged as heating up ≥8 weeks before the research crowd arrived, a date taken from the data, not assumed; and (b) precision ≥0.5: of the top 10 early flags in each 4-week window of 2024, at least half have the crowd arrive within the next 12 months (not before the flag). If it fails, report it plainly and change the method or stop before running weekly.
- **Bar lowered after seeing the results (your call, 2026-10-27).** The backtest failed (b) in both rounds. You chose to run the 4-week trial anyway, on robotics only (phrases mined from cs.RO titles), with the brief stating its record plainly.
  - This is a lower bar chosen after the results were known. It is not a pass, and it must not be described as one.
  - The record the brief states is read from the round-2 robotics results, both halves, with the method fixed beforehand. It was "4 of 15 took off" when you chose. **Corrected for misdated arXiv papers (same day), it is 1 of 19 (5%) against 1% at random, which is about chance.** The trial is built, but no pick has been written until you decide again (docs/BACKTEST.md, "Next").
  - The same method on all four categories scored about random (held-out, corrected: 1 of 14 flagged topics took off, 7%, against 6% at random), so the trial doesn't cover AI tooling, companies or the wider field.
  - The trial's own test (you act on ≥2 of 4 study picks) is now the only check left. If it fails, stop.
- Backtest data (decided 2026-10-26): candidate topics for the precision check are, since 2026-10-27, mined from arXiv (data/CandidatesMined2023.csv, bleedingedge/mining.py: 2–3-word phrases in ≥8 2023 titles and in <10 papers in 2021–22). Before that they came from every RL/robotics/agents/tooling workshop at CoRL, RSS, ICRA, NeurIPS, ICML and ICLR 2023, as written then (data/Candidates2023.csv, rebuilt 2026-10-27 by an inclusion rule, not by picking), so the topics that went nowhere stay in. They are split in half by a hash of the name: the dev half is used for checks, the held-out half is run once at the end (`--holdout`). Candidates whose crowd arrived before 2023 are left out of criterion (b), since they could never be new in 2024. The first list (2022–24 titles) is kept as data/Candidates2022-24.csv. Funding rounds are hand-collected and cited (data/Funding.csv); a small sample, so funding's lead weight is labelled low-confidence. Citation and lab signals need free Semantic Scholar and OpenAlex keys, which you are getting; until then the backtest runs on arXiv, GitHub, HN and funding only, and says so.
- Readable in 15 minutes: ≤1,500 words, the study pick first, at most 5 items per section.
- Cited: every claim links to its primary source (paper, repo, post, filing); every number links to the query that produced it.

Deferred (not in v1):
- Job-post counts as a signal: no history to backtest. Collected weekly from week 1, weight 0 until there are 8 weeks of data.
- Reading X and newsletters directly: no reliable access. The brief uses web search for context.
- A studied/ignored list and a link to the researcher-pal knowledge graph.
- Tuning the weights to your own picks: after the 4-week trial, not before.
- An HTML or email version of the brief, and any app.

Not doing, ever: buy/sell calls, price targets, or saying what you should hold. Funding is evidence that a topic is heating up, not a trade recommendation. The brief says so wherever money comes up.

OPEN QUESTIONS / ASSUMPTIONS:

Your answers (interview, 2026-10-25):
- Why, five levels down: career positioning, research direction and some FOMO → being early matters because learning compounds → compounding toward research taste (seeing which RL/robotics problems matter before others do) → the 2028 win is being deep in a topic that took off, started in 2026–27.
- Domains: all four. RL/robotics/embodied, AI tooling and dev workflow, AI companies and labs, the wider tech field.
- Decisions it could change: all four. If only one: what to study next.
- Cadence: weekly, about 15 minutes.
- Current sources checked weekly: X and newsletters/podcasts. Not arXiv alerts or HN/Reddit.
- Shape: a weekly scheduled brief, not an app. The choice you were least sure of. What you'd miss from an app is trend history over time, covered by data/Trends.csv.
- Weakest assumption, as I put it: public signals show up too late to be early. Your answer: weight leading indicators.
- Kill test: backtest on 2021–25, then a 4-week trial. Success = you act on at least 2 study picks.
- 8-week lead for "early": kept, as a trade-off between signal and noise. A shorter lead lets noise through; a longer one leaves almost nothing passing in a 2-year backtest. Check: the backtest also reports results at 4 and 12 weeks, so the trade-off can be seen rather than assumed.
- Investing trends (added mid-interview): you said "ahead of its time investing". Added as one more leading signal (disclosed funding rounds per topic), not a section, so the brief stays at 15 minutes. It has to earn its weight in the backtest like every other signal. My guess at what you meant: spotting where money is starting to flow before it's obvious. If you meant personal investment picks, the brief won't make them: I'm not a licensed adviser.
- Unverified: whether funding leads or lags the research signals. In RL/robotics, big rounds may come after the papers, which would give it a low lead weight. The backtest shows which.
- Your early catch: RL, because it felt like the most intellectually stimulating and the most novel; robot learning at UC Berkeley. What tipped you off was your own taste plus being close to a strong lab, not public counts. So two things were added: a watch-list lab signal (Berkeley, Stanford/CMU/MIT robotics, industry labs) and a 1–5 taste rating per study pick in the trial review.
- Unverified: whether watch-list lab papers rise earlier than arXiv as a whole. The backtest shows it; if they don't, the lab signal gets weight 0 like any other.
- Your late catches: diffusion policies, coding agents, and companies in general (which labs and companies are rising). Why: you saw them and didn't act. The problem was acting, not spotting. This undercuts the spec's weakest-assumption framing: if you had the signal and didn't act, better detection alone won't help. What could help is the study pick being a firm, small commitment.
- Applied 2026-10-26, at your request: each study pick comes with a first step of about 2 hours, and the companies-and-labs weight is now 0.8. Check: if no picks are acted on in the 4-week trial even with the first step, the problem isn't the brief.

Thin spots (you took every recommendation, left no notes and gave no reasons):
- All four domains with no ranking. The brief will weight RL/robotics highest and the wider tech field lowest (my guess) unless you say otherwise.

My guesses (decided without asking):
- Leading indicators: citation and mention velocity of recent arXiv papers (especially small labs and workshops), GitHub star growth, new keywords in job posts, workshop/tutorial topics, funding and hiring news for companies. Consensus signals (X, newsletters) are used only for the "consensus is moving" section.
- Brief format: a dated Markdown file in briefs/. An HTML page or an email may suit you better.
- Runs as a Claude scheduled task on this Mac, Monday morning. The cost is your Claude plan usage. No paid APIs.
- No studied/ignored list in v1, so topics may repeat. Possible later link to the researcher-pal knowledge graph.
- Public GitHub repo, amalmehta/BleedingEdge (decided 2026-10-27, so others can read and reuse it). No icon, feedback tab or settings: it's a script, not an app.
- Every threshold in DEFINITIONS AND DEFERRED (8-week lead, S ≥ 1, the volume floors, domain weights, precision ≥ 0.5) is my invented starting point. The backtest is the check.
- Hacker News was the first stand-in for "the consensus". The backtest showed it is too sparse for RL/robotics (≤1 story ≥50 points per window), so consensus is now the research crowd arriving (see DEFINITIONS).
- Backtest result (2026-10-26, docs/BACKTEST.md): FAIL. (a) passes 3/3 with 16–48 week leads, but in-sample, and arXiv alone does as well. (b) fails at 6% precision (arXiv-only 1%). Two causes: only 1 of 59 workshop candidates had its crowd arrive in 2024–25, so the test could barely score a hit; and 7 of 12 flagged topics were mature (crowd in 2021) but small, so "early" measures size, not newness. Weekly brief not started.
- Proposed 2026-10-26: rebuild candidates from 2023 sources with a held-out half; add a newness test to "early"; add citations and lab papers when keys arrive; judge (b) once more, and if it fails, fall back to an arXiv-growth-only script.
- Second backtest run (2026-10-27): applied the newness test and the 2023 candidates (97 workshops, dev half 40, held-out half 57 sealed). (b) 0 of 3 flags hit, but none of the 40 dev topics had the crowd arrive in 2024–25, so the test still can't score a hit: workshop lists name established or niche topics. Proposed, not applied: mine every phrase new on arXiv in 2023 as the candidate list (bulk metadata, ~4 GB), or settle for an arXiv-growth-only weekly script.
- Third backtest run (2026-10-27): candidates mined from arXiv (every 2–3-word phrase in ≥8 2023 titles and <10 papers in 2021–22; cs.RO/LG/AI/CL bulk metadata; 88 phrases, dev half 52, held-out 36 sealed). (b) 41% precision (19/46), arXiv-only 23%; caught 4 of the 5 topics whose crowd arrived in 2024–25. Fails the 50% bar, but this is the first fair test, and the first where GitHub adds something (fewer false flags). Caveats: 80 of 88 candidates are AI/LLM topics, not robotics; no cs.CV; arXiv grows ~30% a year, which inflates every ratio. Next: decide any final fix (keys, small bar, normalising by arXiv growth) before opening the held-out half once.
- Final fixes (2026-10-27, decided before the held-out half): arXiv growth is relative to all papers; "small" for mined topics is <30 papers per 12 weeks (local counts are ~0.6× search counts, measured on 11 neutral phrases). Dev half: (b) 52% (15/29), arXiv-only 30%; 4 of 10 flagged topics hit. Passes the bar by one hit and in-sample. The held-out half (36 topics) was the deciding test.
- Held-out result (2026-10-27, opened once): FAIL. (b) 41% (12/29) vs the 50% bar; arXiv-only 15%; caught all 3 held-out topics that took off (7 of 8 across both halves); base rate 9%. Most misses were topics already crowded in 2023 that still looked small. Not fixed: a fix now needs new held-out data (phrases new in 2024, graded on 2025–26). Decision open: stop, lower the bar knowingly and run the 4-week trial, or fix and re-test on 2024 phrases.
- Round 2 (2026-10-27, pre-registered: freshness rule of 9 windows, 75 windows to Oct 2026, phrases new in 2024 judged on 2025 flags): FAIL on both runs. All categories: dev 23%, held-out 6% (1/17), below the 13% you'd get picking at random; caught 1 of 12. Robotics (cs.RO titles): dev 22%, held-out 45% (9/20), but 7 hits are one phrase; 2 of 7 topics hit; base rate 3%. (a) still passes (20/20/68 weeks, in-sample). The 2023 result did not generalise. Both held-out halves are spent. Decision open: stop; a robotics-only trial with a stated record (lowering the bar knowingly); or change what's graded (workshop/benchmark/lab paper within a year), which needs 2025 phrases graded through 2027.
- Date bug (found 2026-10-27, while building the trial): arXiv's OAI `<created>` is a later version's date for revised papers, so ~30% of bulk-download papers were misdated. Fixed from the arXiv id; round 2 re-run unchanged. Corrected: robotics 1 of 19 flagged topics took off (dev 0/8, held-out 1/11; base rate 1%); all categories held-out 3% (1/31). Round 1 (2023) not re-run; its numbers are unreliable. Trial built (bleedingedge/brief.py, prompts/WeeklyBrief.md, docs/TrialReview.md); week 1 draft written, study pick held; the Monday scheduled task wasn't created (permission denied).

Most likely way this fails: the brief gets read for two weeks and then skipped, because it repeats what X already showed or its picks don't line up with work you have time for. The backtest and the 4-week review are there to catch this.

CHANGELOG:

- 2026-10-25 — created
- 2026-09-15 — added meta-instruction: built-out applications include a small feedback tab
- 2026-09-15 — added meta-instruction: no "Claude" attribution in commits, PRs, or branches
- 2026-09-16 — added meta-instruction: always include a README when adding to GitHub
- 2026-09-16 — changed meta-instruction: ask clarifying questions in the question widget
- 2026-09-17 — added meta-instructions: Claude never a contributor; never commit .claude/
- 2026-09-26 — compressed the meta-instructions and every field prompt; git rules moved to the global instruction file
- 2026-09-27 — added meta-instruction: applications are built as a Mac app first, then a website
- 2026-09-28 — folded inputs, instructions, constraints, deliverables and done criteria into one free-form CONTEXT
- 2026-09-28 — changed meta-instruction: a README on GitHub always includes a visual
- 2026-09-28 — added meta-instruction: name things like a person would, never snake_case
- 2026-09-28 — changed meta-instruction: README leads with visuals; instructions live in a linked guide
- 2026-09-28 — changed meta-instruction: README is visuals and links; details in docs/INSTRUCTIONS.md and docs/FILE-STRUCTURE.md
- 2026-09-29 — changed meta-instruction: GitHub repo names have no "_" or "-"
- 2026-10-02 — added a DELIVERABLES field after CONTEXT
- 2026-10-02 — added meta-instruction: every project has a system design doc at docs/SYSTEM-DESIGN.md
- 2026-10-05 — added meta-instruction: applications include a settings button or tab
- 2026-10-08 — added meta-instruction: color-code tags by similarity (related share a hue family, each distinct)
- 2026-10-09 — added meta-instruction: apps that take files have an Upload button, drop anywhere, and paste
- 2026-10-17 — added meta-instruction: before building, ask the design questions an expert engineer would (data, security, caching, scale, deployment…)
- 2026-10-18 — added meta-instruction: open the MVP for me as soon as a first working version exists, and after each big change
- 2026-10-18 — added meta-instruction: always create a relevant icon for applications
- 2026-10-18 — added meta-instructions: work like a world-class founder, software engineer and (for research) scientist
- 2026-10-18 — added meta-instruction: pick my brain with open questions answered in my own words, as well as multiple choice
- 2026-10-18 — changed meta-instruction: Mac app first only when the request names no platform (from the meta report)
- 2026-10-21 — added meta-instruction: size design decisions to the project's current scale, note what changes as it grows, and keep pieces modular and replaceable
- 2026-10-18 — changed meta-instruction: the first batch of questions also covers delivery, the repo, test versus live mode, who pays, mocks, and real inputs and credentials (from the meta report)
- 2026-10-18 — added meta-instructions: nothing made up passes as fact; fill in DEFINITIONS AND DEFERRED; a clean, restrained interface with mockups and a manual review checklist (from the meta report)
- 2026-10-18 — added a DEFINITIONS AND DEFERRED section
- 2026-10-19 — changed meta-instruction: questions mostly as multiple choice (with a box for my own answer); plain-text questions only when a detailed answer is needed, at most two per round
- 2026-10-20 — added meta-instruction: make the UI/UX buttery smooth (instant response, nothing blocking the main thread, full-frame-rate motion, no flicker or jumps)
- 2026-10-21 — added meta-instruction: make equations easy to read (typeset, not raw LaTeX; symbols defined beneath; a plain-language line; short steps)
- 2026-10-23 — added meta-instruction: keep a prompt log, docs/PROMPTS.md, of every prompt given in each session
- 2026-10-23 — added meta-instruction: push back on the idea before building (why, five levels down, then what's the best way to meet the real need); no yes-manning
- 2026-10-24 — added a note on me from my portfolio site (work, values, interests, visual and writing style), to fill gaps without overriding the spec
- 2026-10-25 — changed meta-instruction: always open the app after making a build (was: after the MVP and each big change)
- 2026-10-25 — added meta-instruction: when there's a chance to do the simplest thing that still works well, do that
- 2026-10-25 — added meta-instruction: build applications through the eyes of the people who'll use them (a wide range of people, or the specific group for a narrow use case)
- 2026-10-25 — changed meta-instruction: keep the interface clean but never barren (content, helpful empty states, icons, a next step on every screen) instead of "clean and restrained"
- 2026-10-25 — added meta-instruction: think ten steps ahead before starting (design and outline the whole build, trace the next ten steps, pick the design that keeps them easy)
- 2026-10-25 — added meta-instruction: publish production apps to GitHub (everything committed and pushed, a PR for anything unmerged, no work only on this Mac)
- 2026-10-25 — added meta-instruction: push me to think for myself (what each suggestion rests on, a way to check it, my view first on my decisions), about 10% more pushback
- 2026-10-25 — added meta-instruction: explain so I learn the skill (plain idea, analogy or worked example, why and when it fails, jargon defined, a reusable principle), in replies and in the app
- 2026-10-25 — added meta-instruction: fully test on sample data (normal, edge and failure cases, end to end) before asking me to test on real data
- 2026-10-25 — added my taste profile (colour, what clean means, density, words, pictures, how I think), from my reactions to builds
- 2026-10-25 — added meta-instruction: use sub-agents when they help (parallel independent work, heavy reading, unanchored second opinions), with full briefs, and check what they return
- 2026-10-25 — interviewed on CONTEXT (why five levels down, domains, decision, cadence, sources, app or not); filled DELIVERABLES (weekly cited brief and backtest, no app) and OPEN QUESTIONS / ASSUMPTIONS
- 2026-10-25 — filled DEFINITIONS AND DEFERRED: topic, signal, leading indicator, growth ratio and score formula, heating up, fading/outdated, study pick, acted on, backtest pass criteria; deferred job posts, X/newsletter parsing, studied list, app
- 2026-10-25 — kept the 8-week lead (signal vs noise; backtest also reports 4 and 12 weeks); added disclosed funding rounds as a leading signal for investing trends, with no buy/sell or holdings advice
- 2026-10-26 — recorded your early catch (RL, via taste and robot learning at UC Berkeley); added a watch-list lab signal (Berkeley, Stanford/CMU/MIT, industry labs) and a 1–5 taste rating per study pick
- 2026-10-26 — recorded your late catches (diffusion policies, coding agents, companies; saw them but didn't act); proposed a ~2-hour first step per study pick and a higher companies weight
- 2026-10-26 — applied: a ~2-hour first step with every study pick; companies-and-labs domain weight raised from 0.6 to 0.8
- 2026-10-26 — backtest design: window widened to 2021–25; GitHub signal changed to new repos per window; candidates from 2022–24 workshop titles; funding hand-collected and cited; Semantic Scholar and OpenAlex keys to come
- 2026-10-26 — after the first backtest run: consensus = research crowd arrives (25% of peak arXiv volume), not HN; growth measured as trend + burst; funding a bonus only; GitHub searches name and description for full phrases (README leaked hindsight)
- 2026-10-26 — backtest run on all 59 candidates: fails (precision 6%); results and proposed fixes in docs/BACKTEST.md; weekly brief on hold
- 2026-10-27 — "early" now needs new as well as small (fewer than 10 papers two years earlier); candidates rebuilt from all 2023 RL/robotics/agents/tooling workshops, half held out; (b) still untestable (0 reachable hits in the dev half); proposed mining new arXiv phrases instead
- 2026-10-27 — published as a public GitHub repo, amalmehta/BleedingEdge
- 2026-10-27 — candidates now mined from bulk arXiv metadata (88 phrases new in 2023, half held out); dev-half precision 41% vs 23% arXiv-only, below the 50% bar; held-out half still sealed
- 2026-10-27 — final method fixes before the held-out test: arXiv growth measured relative to all papers; "small" bar scaled to 30 for bulk counts; dev half now 52% (in-sample); held-out half still sealed
- 2026-10-27 — held-out half opened once: precision 41%, fails the 50% bar (arXiv-only 15%; 3 of 3 winners caught); weekly brief not started; decision on next step is yours
- 2026-10-27 — round 2: freshness rule added, window grid extended to Oct 2026; held-out precision 6% (all categories) and 45% (robotics, one topic), both fail the 50% bar; weekly brief not started; decision on next step is yours
- 2026-10-27 — your call: run a 4-week robotics-only trial with the record stated, recorded as a bar lowered after seeing results; trial built
- 2026-10-27 — arXiv date bug found and fixed (≈30% of bulk papers misdated); round 2 re-run: robotics 1 of 19 flagged topics took off (about chance), all categories 3% held-out; trial on hold pending your decision
- 2026-10-28 — your call: trial runs anyway, as a test of the format, not the detector. Week 1 pick: robot foundation (first step arXiv 2610.20750). The "prove it wrong" test in the weekly prompt was fixed before week 1: "reach 20 papers" was already met by early topics, so it is now "pass 4× today's 12-week count", the backtest's hit rule. Monday task set up
