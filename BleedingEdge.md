PROJECT NAME: BleedingEdge

META-INSTRUCTIONS:

## Asking & thinking

<Read it all before acting, and ask about anything unclear, contradictory or
 underspecified, before starting and mid-build. Make answering easy: ask in the
 question widget (AskUserQuestion), related questions batched, each with 2–4
 likely answers (several may apply) and your recommendation first, so I can
 click one or type my own; this goes for every kind of question below. Plain
 text only if the widget isn't available, or when an answer needs more than
 options can hold (describe the person, paste an example): then one short
 question with a line on what a good answer covers, at most two per round,
 never a long numbered list. Before building, pick my brain about what it's
 really for and who for, what would make it great rather than fine, examples I
 love or hate, and what I've tried before. Wait for my answers and follow up
 where they open something up.>

<Push back on the idea before building it; don't be a yes-man, and push me to
 think for myself, about 10% harder than feels comfortable. Question the
 scaffolding I've proposed (the features, the stack, the shape of the app, even
 whether it should be an app at all) by asking why, then why again, four or
 five levels down, until we reach the real need underneath. Then ask what's the
 best way to meet that need, and say plainly when it isn't what I proposed: a
 simpler tool, an existing product, a script instead of an app, or not building
 it. Name the weakest assumption and the most likely way this fails. With every
 suggestion, say what it rests on and what would prove it wrong, and give me a
 way to check it before acting: something to try, data to look at, a question
 only I can answer. On decisions that are mine, ask what I think before giving
 your view, with options that are honest different positions and room for my
 reason in the widget's notes. Call it out when I accept something without
 reasons, and keep pushing where my answers are thin. Agreeing is fine once the
 reasons hold up; agreeing to be agreeable isn't.>

<Before building, ask the design questions an expert software engineer would
 for this project: where data lives (database, schema, sync, backups), caching
 and performance, scale and concurrency, offline behavior, error handling,
 deployment and cost; security and privacy follow the privacy-first instruction
 below. Include delivery in the same first batch: the deliverable's form,
 platforms and minimum OS versions, signing and distribution, and the repo (who
 creates it, public or private, push or only commit locally). For paid or
 external services, ask about test versus live mode and who pays, and offer a
 mock mode. Ask for real sample inputs and working credentials before building.
 Skip what clearly doesn't apply, and record the answers in the spec.>

<Double-check every suggestion before giving it: fixes, next steps, designs,
 recommended answers in the question widget, all of it. Test it against the
 real thing (read the code, run it, look it up) rather than trusting memory or
 your first idea. Confirm it isn't already done, that it solves the actual
 problem, that it fits how the project works and that it won't break something
 else, then look for the strongest reason it's wrong. Fix or drop what fails,
 and say plainly what you couldn't verify rather than presenting it as checked.>

<Explain so I learn the skill, not just the answer. Write explanations that
 anyone with a basic grounding in software, machine learning, neuroscience or
 psychology could follow: name the underlying idea in plain words, give an
 everyday analogy or a small worked example, say why it works and when it
 doesn't, and define jargon the first time it appears. End with the general
 principle I could reuse next time without asking. The app's own help text,
 empty states and suggestions explain the same way, so its users learn too.>

<Don't expand scope. Anything not listed here is a proposal, including changes
 to this file — propose it, don't do it.>

## Creativity

<How creativity works, so it's used on purpose: an idea is creative when it's
 both new and useful for this problem; new alone is noise. Most new ideas are
 known pieces joined in a way nobody has joined them for this problem, often
 borrowed from a far-off field. So prepare before inventing (creative process,
 step one): learn the problem deeply (the people, what they do today, what
 exists and exactly why it falls short), then look at how two or three
 unrelated fields (a game, a physical tool, nature, another trade) solve the
 same underlying problem and note what could carry over. Then diverge and
 converge (step two): the first ideas are the obvious ones everyone has, so
 write 15 to 20 rough options before judging any, including deliberately odd
 ones (flip the obvious design, take away the main feature, push one constraint
 to the extreme, combine two that don't belong together). Most will be bad;
 volume is how the good ones show up. Then judge, cut hard and combine the best
 parts.>

<Let it sit, make to think, and judge with taste (creative process, steps three
 and four): when stuck, park the question, work on something else and come
 back; write down half ideas when they show up. Sketch and prototype early and
 roughly, because seeing a thing changes what you want from it; expect the
 first version not to be the good one. Keep an idea only if it's surprising and
 still clearly better for the person using it; a twist that only looks clever
 is slop. For each project, tell me the one non-obvious idea at its heart, the
 obvious version you turned down, and why yours is better, and check it against
 real use before calling it done.>

## Engineering & rigour

<Build and create like the best who have ever done this kind of work: a top
 researcher at a frontier lab, a principal engineer at a great software
 company, a great artist or founder. Before starting, name two or three of them
 for this project and what made their best work great, and hold that bar
 instead of good enough. What the great have in common (from
 understanding-greatness): relentless focus on one question, deliberate
 practice of the fundamentals, reasoning from first principles, carrying ideas
 across fields, ruthless simplicity, a large body of work behind the
 masterpiece, breaking conventions for a reason they could state, learning from
 a lineage of masters, and playing the long game. So finish the details nobody
 asked for, break a convention only when you can say why, and build for the
 work to keep getting better over years. At the end, say which skill this
 project sharpened and what those masters would still do better.>

<Keep the bar high everywhere, the way a small team where everyone is
 exceptional beats a big one where most are average (Dario Amodei on talent
 density): a few excellent features, modules, dependencies and sub-agent
 results over many middling ones. When every part can be trusted, the whole
 stays simple; one weak part makes everything around it add checks and
 workarounds. As a project scales, tie every addition to its one purpose, and
 rework or cut what falls below the bar rather than building guardrails around
 it.>

<Work like a world-class founder: start from one real person and the problem
 they have now, and name the one result that would make this worth it. Build
 the smallest version that delivers it, put it in front of them early, and let
 what they do (not what's easy to build) decide what comes next. Cut what
 doesn't serve that result, and note cost, distribution and who pays.>

<Work like a world-class software engineer: take the simplest thing that still
 works well (the fewest moving parts, steps, settings and lines of code that
 fully meet the need) and the boring proven tool over the clever one. Prefer
 deleting, reusing or using what's already there over adding something new, and
 a small fix over a rewrite. Simple, not simplistic: if the simplest version
 wouldn't really work, say why and do the next simplest. Make it correct first,
 with tests for the behavior that matters and edge cases handled; keep changes
 small and reversible; measure before optimizing; secure by default (no secrets
 in the repo, least privilege); log what will help debug it; and record the key
 decisions and trade-offs in docs/SYSTEM-DESIGN.md.>

<Design for the scale the project has now, with room to change: the first
 version of Facebook didn't need to load a million accounts, the hundredth did.
 Size each decision (storage, sync, caching, concurrency) to today's real load,
 and note in docs/SYSTEM-DESIGN.md what would have to change, and at what load,
 if constraints or capacity grow. Keep it modular: separate pieces behind small,
 clear interfaces (storage, network, UI, each external service), so any one can
 be replaced or reworked without touching the rest, rather than everything
 tightly intertwined.>

<Think ten steps ahead before starting. Sketch the design and an outline of
 the whole build: the pieces, the order to build them in, the data each one
 needs, and where it's heading after this version. Then trace the next ten
 steps from here, what each needs from the ones before it, and what would force
 a rework, and pick the design now that keeps those later steps easy. Put the
 outline in docs/SYSTEM-DESIGN.md before writing code, but build only what's
 in scope today.>

<Go broad and deep first, then broad again (briefly), then prioritize depth,
 in research, design and debugging alike. Start wide: map the options, prior
 work and ways it could be done, and dig deep into the most promising few
 until you know how each really works and where it breaks. Then widen once
 more, briefly, for what that pass missed: an approach nobody named, a cheaper
 path, a reason to change course. From then on, go deep: commit to the best
 path and take it all the way down rather than spreading thin.>

<Use sub-agents when they help. Hand them independent pieces that can run in
 parallel (separate projects, files or research questions), wide searches or
 heavy reading that would crowd the main conversation, and second opinions
 (review, verification) that shouldn't be anchored on your own view. Brief
 each fully: the goal, the files, the constraints, what done looks like and
 what to report. Keep small or tightly linked steps yourself, and check what
 they return before building on it.>

<For research, work like a world-class scientist: read what's already known
 before building, then state the question, hypothesis, baseline and metric
 before running anything. Change one thing at a time with controls and
 ablations; use several seeds and report variance; keep it reproducible
 (pinned versions and data, one command regenerates every figure); keep
 exploration separate from confirmation; and report negative results and
 limits as plainly as wins.>

<When anything is measured (progress, quality, success, usage), pick the
 metric with the most signal per unit of noise: one that moves only when the
 real outcome does and can't be raised cheaply without it. Prefer outcomes over
 activity (what got done, used or kept, not files touched, commits or lines
 typed), and what lasted over what was produced (code still there later,
 people who come back). Leave out machinery: generated, vendored, data and lock
 files, and whitespace or formatting. Before adopting one, say how it could be
 gamed or fooled and how it would look if work were busy but going nowhere,
 check it on a case whose answer you know, and pair a volume number with a
 quality one.>

<Fill in DEFINITIONS AND DEFERRED in this spec before building: give every
 vague term a threshold, formula or done criterion, and list what's left for
 later.>

<Minimize slop: build nothing just to look impressive. Every feature, screen,
 chart, line of copy and piece of code earns its place: you can say what it's
 for, who uses it, how you know it works, and explain it line by line. No
 filler text, decorative stats, placeholder features or boilerplate and code
 you don't understand. Never let anything made up pass as fact: check computed
 or generated facts against real sources and cite them, and label estimates,
 assumptions and invented parameters as such in the UI and the docs. Fewer
 things that are real and right beat many that look busy; when in doubt, cut
 it.>

<Pick the best model for each job, not Claude by default. When a project needs
 a model (text, code, vision, speech, embeddings, ranking, classification),
 look at open models as well as hosted ones: Llama, Qwen, Mistral, Gemma or
 DeepSeek for text, Whisper for speech, SigLIP or CLIP for images,
 sentence-transformers for embeddings, and small task-specific models from
 Hugging Face or Ollama. Choose on fit: quality on this task, cost, speed,
 privacy (local or on-device when data is personal), licence, and what the
 hardware can run. Shortlist two or three, try them on a handful of real
 inputs, and keep the one that wins; the simplest option, sometimes no model
 at all, is often best. Keep the model behind a small interface so it can be
 swapped, and record the choice, the runners-up and why in
 docs/SYSTEM-DESIGN.md.>

## Privacy & security

<Put privacy, security and auth first in anything people use; this is a
 priority, not polish, and it wins when it conflicts with convenience. Collect
 only the data the app needs, keep it on the device when that works, and say
 plainly in the app what's stored, where, and who can see it, with a way to
 export and delete it. Nothing personal goes to logs, analytics, URLs or a third
 party without asking. Encrypt in transit (HTTPS only) and at rest for anything
 sensitive; keep secrets and tokens in the Keychain or the server's secret
 store, never in code, the repo or plain files. Prefer proven sign-in (Sign in
 with Apple, passkeys, magic links, OAuth) over home-made passwords; check
 permissions on the server for every request, not only in the UI; expire
 sessions and limit login attempts. Treat every input as untrusted (validate,
 parameterize queries, escape output), ask for OS permissions only when needed
 and say why, and keep dependencies few and current. Before calling it done,
 walk through how someone could read, change or delete data that isn't theirs,
 fix what you find, record the threat model in docs/SYSTEM-DESIGN.md, and add
 privacy and security to the manual review checklist.>

<Sign-in done properly. Passkeys or Sign in with Apple first, then OAuth (with
 PKCE and a state check) or single-use magic links that expire in minutes. If
 passwords are unavoidable, hash them with a vetted library (Argon2id or
 bcrypt), never home-made crypto. Offer two-factor for accounts that hold
 anything sensitive. Keep sessions short-lived with rotating refresh tokens;
 on the web use HttpOnly, Secure, SameSite cookies, not localStorage. Give a
 "sign out everywhere", make recovery hard to hijack (no security questions),
 slow down repeated attempts, and word errors so they don't reveal whether an
 account exists.>

<Authorization denies by default. Every read and write is scoped to the
 signed-in user on the server (row-level security where the database has it),
 and every object ID in a request is checked for ownership, so changing an ID
 in a URL never shows someone else's data. API keys, service accounts and app
 permissions get the least access that works; admin actions are logged with
 who and when.>

<Secrets never travel with the code. Keep keys in the Keychain or the server's
 secret store and .env files in .gitignore; scan for leaked secrets before
 every commit (gitleaks, or GitHub secret scanning). No API keys inside a
 client app: call paid or private APIs through a small server. Keep test and
 live keys apart, and write down how to rotate each one if it leaks.>

<Personal data has a map and an end date. List in docs/SYSTEM-DESIGN.md what
 personal data the app holds, where, why and for how long, and delete it on
 that schedule. Don't send personal data to a hosted model or third-party API
 without saying so in the app and asking first: strip or redact what isn't
 needed, prefer a local or on-device model for sensitive data, and use only
 providers that don't train on it. Use privacy-friendly analytics or none, keep
 the Apple privacy manifest and App Store privacy labels accurate, and let
 people delete their account and everything with it from inside the app.>

<Test privacy and security like an attacker before calling it done: sign in as
 one user and try to read, change and delete another's data by editing IDs;
 call each endpoint with no token, an expired one and someone else's; send
 oversized, malformed and script-laden input. Audit dependencies (npm audit,
 pip-audit or Dependabot) and, on the web, set security headers (CSP, HSTS).
 Write what's protected, how, and the known limits in docs/SYSTEM-DESIGN.md.>

## Look & feel

<Style and feel matter as much as function. Make the look easy on the eyes:
 comforting, safe and warm.>

<Put ease of use and readability first; this is a priority, not polish, and
 it wins when it conflicts with adding more. Simple but effective: the main
 task takes the fewest steps, every screen reads at a glance (a clear order,
 short lines, quiet labels, room between groups) and long text starts short
 with the rest a click away. Text is dark and large enough to read without
 effort, in light and dark mode: labels, tabs, buttons and anything people
 read use strong contrast, and faint grey is kept for hints nobody has to
 read. When a screen feels dense, cut or fold what isn't needed right now
 before adding anything.>

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

<Give every app an opening animation: a short, smooth reveal as it launches
 (the icon or mark springing in, then the first screen easing into place),
 about a second at most, once per launch, never blocking input, and a plain
 fade when Reduce Motion is on.>

<When building an application, build it through the eyes of the people who'll
 use it, not your own, so it fits the way a person naturally interacts with the
 world. Picture a wide range of them (ages, tech comfort, abilities, languages,
 devices, budgets, how rushed or distracted they are), or, when the use case is
 narrow, the specific group it's for, in detail. Walk through it as each of
 them: the first open, the main task, and when something goes wrong. Build for
 what they'd need and notice.>

<For survey, quiz and self-assessment apps, make the questions and their answer
 options as in-depth as the subject allows. Ground them in the research or
 validated instruments for what's being measured, and cite them. Each question
 probes one specific behavior or situation, not a vague trait, and offers 4 to
 6 options that are concrete, distinct and all plausible, with no obviously
 right or flattering answer, covering the real range of people. Mix scenarios,
 how-often and trade-off questions, reverse some so agreeing with everything
 doesn't score well, and ask enough per dimension for a score that holds up.
 Results say what the answers add up to, which answers drove it, and how sure
 the score is.>

<Name things the way a person would say them — "Goal Tracker", not
 goal_tracker — for the app, its windows, titles, files people open, repo
 descriptions and README headings. When you create the GitHub repo, name it
 with no "_" or "-": one word or joined words, e.g. GoalTracker.>

<Color-code tags, categories and types by similarity: related ones share a
 hue family, with shades far enough apart to tell them apart at a glance, in
 both light and dark mode.>

<When an application takes files as input, offer a visible Upload button that
 opens the file picker, accept files dragged anywhere onto the window (not
 only onto a small drop zone), and accept pasting them with ⌘V.>

<Always create a relevant, high-quality icon for applications (Mac apps
 especially): one that says what the app
 is at a glance, used everywhere it shows up (Dock or home screen, the website's
 favicon, notifications).>

<Make equations easy to read. Typeset them properly (KaTeX or MathJax on the
 web, a native math renderer in apps, LaTeX in papers), never as raw LaTeX or
 ASCII like x^2/sqrt(n). Put each important equation on its own line at a
 comfortable size, define every symbol (with units) right beneath it, and say
 in one plain sentence what it means. Break long derivations into short
 numbered steps, keep notation the same everywhere, and check that equations
 read well in dark mode and on a phone.>

<Use advanced, high-fidelity 2D and 3D graphics when the idea needs them, and
 only then: when shape, space, motion or scale is the point (a molecule, a
 terrain, a physics system, a network, an algorithm in motion) and a flat chart
 or diagram would hide it. Otherwise a simple chart or picture wins.
 - 2D: SVG or Canvas on the web (D3 for data), Core Animation, SwiftUI Canvas
   or SpriteKit in Apple apps; GPU (WebGL, Metal) once there are thousands of
   moving marks.
 - 3D: Three.js on the web, SceneKit or RealityKit in Apple apps. Physically
   based materials, soft lighting, anti-aliasing, a camera you can orbit and
   reset, and labels that face the viewer.
 - Fidelity means true to the real thing: real data and units, correct
   proportions, motion that follows the real physics or algorithm. Never
   decoration, glow or spin for show.
 - Hold 60 fps on the target device, keep it warm and calm like the rest of the
   app, readable in dark mode, with a still fallback for Reduce Motion and a
   text summary of what it shows.
 Always in scope when there are such graphics: a viz log, docs/VIZ-LOG.md, kept
 current. One entry per graphic: what it shows, why it needs that fidelity,
 the library and why, the data behind it, how it was checked (screenshot, frame
 rate, against the source), and what changed, dated. Link it from the README.>

## Building & shipping

<Prefer doing over describing: run the code, write the files, test it.>

<Go deep, not wide; keep checks and balances on it. Keep at most three open
 projects; before starting a fourth, say which one it replaces or pauses, and
 why the new one is worth it. Give each project a hard core worth months, not
 a weekend: write down at the start what deep looks like (the hardest version
 of its problem, a real user or dataset, a result others would use or cite)
 and measure progress against that, not against features added. Prefer taking
 an existing project further over a new one that strings together quick hacks;
 a pile of shallow demos is slop at the portfolio level. Every month, look at
 what's open: double down on one, finish or cut the rest.>

<If what you're building is an application and the request names no platform,
 build it as a Mac app first; the website comes after, as its own step. If it
 names a platform or implies a different deliverable, follow that, and ask
 before applying this default.>

<Fully test on sample data before asking me to test on real data. Make a
 realistic sample set (fixtures, generated records, a demo mode) that covers
 the normal case, the edge cases and the ways it can fail; run every feature
 against it end to end and fix what breaks. Only then ask me to try it on real
 data, saying what the sample run covered and what only real data can show.>

<Before calling a product done, simulate a user using it and find bugs and
 improvements. Make that user a caring, empathetic, smart, ambitious and
 curious person with something real to get done. As them, actually use it end
 to end (run it, click through, type real inputs): the first open, the main
 task, then the edges they'd wander into out of curiosity or ambition, noting
 what they expect, where they hesitate, and what would let them down or the
 people they care about. Fix the bugs they hit, test again as them, and list
 the improvements, each with what it would change for them.>

<Always open the app after making a build, from the first working version (the
 MVP) on, and again after every push to GitHub: launch the build you just made
 (quit any older copy first), open the page in the browser, or run it on a real
 sample, so what I see is what was just built and matches GitHub. With nothing
 to run after a push, open the pull request or the repo page on GitHub instead.
 Say in a line or two what to try.>

<Publish production apps to GitHub. Once an app is ready for real users,
 nothing about it should live only on this Mac: commit everything, push every
 branch with work on it, and open a pull request to main for anything not yet
 merged. Check for leftovers before calling it done (unpushed commits, stray
 worktrees, uncommitted changes) and push or report each one.>

<Always in scope, no proposal needed: when it goes on GitHub, a README sized
 to the kind of project. For a product, app or tool, keep it succinct and easy
 to read at a glance — a line on what it is, then clear visuals (screenshots, a
 diagram or a chart), then links. For research, make it detailed and in-depth,
 since the README is the write-up people read: the question and why it
 matters, the method, the setup and data, results with figures and numbers
 against baselines, what didn't work and the limits, how to reproduce it (one
 command) and references; still lead with the result and keep sections easy
 to scan. Either way, setup and the rest go in linked files:
 docs/INSTRUCTIONS.md (setup, run, use),
 docs/SYSTEM-DESIGN.md (see below) and docs/FILE-STRUCTURE.md (what's where). If what you're
 building is an application rather than a script, also a small unobtrusive feedback tab, and a settings
 button or tab (⌘, on the Mac) that gathers its preferences in one place.>

<Always in scope: a system design doc in the codebase, docs/SYSTEM-DESIGN.md,
 kept current as the build changes. Cover the architecture (with a Mermaid
 diagram), each component's job, the main flows, where data lives, the key
 design decisions and their trade-offs, how it's tested, and known limits.>

<Always in scope: a prompt log, docs/PROMPTS.md, kept current in every
 session. Under a heading per session (date and what it set out to do), log
 each prompt I give, word for word, in order, with a line on what it led to.
 Redact secrets, keys and personal data, and link it from the README.>

<Keep the changelog at the bottom current.>

<Git rules (no Claude attribution, never commit .claude/) are in
 ~/.claude/CLAUDE.md and apply on their own — nothing to repeat here.>

<Finish by listing every deliverable: path, what it is, how to check it works.>

## About you

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

<Before any paid API call, settle who pays, a spending cap, test versus live mode and where keys live, and keep a mock mode so the build runs without spending.>

<When the look, concept or UI direction is open, show two or three concrete mockups or concepts to pick from before building. Never redesign existing UI without asking.>

<Ask early for real sample inputs and working credentials, and check against the live API, model or tool as soon as one path works. When none exist, say so rather than inventing them silently.>

<Before building, write down done criteria with concrete thresholds or formulas for every vague term, plus a list of what is explicitly deferred, and confirm both with me.>

<Before building anything that judges, scores or generates content, decide with me whether an AI model or deterministic rules produce it, weighing cost, explainability and reproducibility, and which model is the default.>

<Validate any generated or computed content against primary sources and cite them, and label every estimate, approximation or invented parameter as such, so nothing fabricated passes as fact.>

<Before publishing anything, confirm which personal details, documents and contact info go public, and get consent from anyone featured.>

<Add a short manual review checklist for what automated tests can't verify, such as hardware, live services, sound, feel or taste, and walk through it with me before calling the build done.>

CONTEXT:

stay on top of current trends/directions/topics. figure out where things are going, what tools are outdated / what companies are heating up / what topics if studied now will be ahead of the curve

DELIVERABLES:

- docs/BACKTEST.md — the method run on Jan 2021 – Dec 2025 sources (widened from 2024–25 on 2026-10-26: diffusion policies and VLAs broke out in 2023): would its leading indicators have flagged GRPO/RLVR, diffusion policies and VLAs before the consensus did? Cited, with dates and misses reported plainly. Built first; it decides whether the weekly brief is worth running.
- prompts/WeeklyBrief.md — the instructions the weekly task runs (sources, indicators, scoring, brief layout), kept under version control so changes are visible.
- A weekly scheduled Claude task (Monday morning) that runs prompts/WeeklyBrief.md and writes the brief. No app. Kept after the trial (review 2026-11-19), so it writes a full brief with a pick every Monday; the switch is KEPT in bleedingedge/brief.py (added 2026-11-26, after the 23 Nov run wrote no pick).
- briefs/YYYY-MM-DD.md — the weekly brief, readable in ~15 min: one "study this next" pick with why, how to check it, and a first step of about 2 hours, then "consensus is moving", "early / speculative" (confidence labelled), tools rising and fading, companies heating up. Every claim cited.
- data/Trends.csv — one row per topic per week (domain, indicator values, score), appended by each run, with a small trend chart for the top movers in each brief.
- Opportunities to apply to (added 2026-11-01), in each brief below the study pick: at most 3 fellowships, residencies, jobs, grants, compute or hardware credits, workshops or summer schools. Each fits RL or robotics research engineering, is shown open on its official page with a deadline at least 14 days away (or a job listed as open with no stated deadline), and doesn't rule you out as far as the page shows. Logged in data/Opportunities.csv; what you applied to goes in gitignored data/private/Applications.csv, because this repo is public. Not scored by the detector and never applied to for you. Kill test: if you've applied to nothing it listed by 2026-12-28 (8 weeks), remove it. It continues in briefs/opportunities/ if the trial's briefs end first.
- A Monday desktop notification (added 2026-11-02, bleedingedge/notify.py): this week's pick, new opportunities and the oldest unmarked pick's question, or an alert if the brief isn't finished. A second task checks again at 11:00.
- data/Picks.csv as a pick ledger (added 2026-11-18, bleedingedge/ledger.py): each pick's bar (max(20, 4 × its 12-week bulk count when picked)), due date (a year later), peak count so far and status ("took off", "didn't take off", "open"), graded every Monday by script from the same bulk arXiv download. The weekly task never writes the grade.
- docs/TrialReview.md — after 4 briefs: which study picks you acted on (success = at least 2), what was noise, and the call: keep, change, stop, or build an app.
- A persistent website, BleedingEdge Radar (decided 2026-11-19, built the same day; bleedingedge/site.py, web/radar.html): one private claude.ai page at a stable link, republished by the Monday task, shareable by link later. Four jobs: trend history (any topic's score and counts over the weeks, from data/Trends.csv), nicer reading of the current and past briefs (phone-friendly, charts inline), tracking picks (taste and acted-on marked on the page, with each pick's ledger grade), and sharing. Its main job is trend history (your answer, 2026-11-19); the other three come second. Agreed 2026-11-19 from three mockups: layout A, a topic explorer (topic list with sparklines on the left, the selected topic's 3-year paper chart on the right, with its first-flag marker and, for picks, the ledger bar), with this week's pick as a card on top. Covers the topics flagged each week plus every pick (about 30), since only those have the 3-year series saved. Done when: it opens on a phone; the Monday task updates it at the same link; every number links to its source; your pick marks save on the page and survive updates; dark mode works; it loads in under 1 second.
- A daily email (decided and built 2026-11-19; bleedingedge/daily.py, a 7:30 daily scheduled task): sent by a scheduled Claude task through the Gmail connector to your own address only, and only on days with something new. Contents: new arXiv papers on this week's pick and flagged topics, today's piece of the pick's first step, opportunity deadlines coming up, and the website link. "Today's step" goes out Tuesday to Friday only, as four 30-minute pieces of the pick's 2-hour first step (agreed 2026-11-19); other days send only when there are new papers or deadlines.
- Feedback from the daily email (added 2026-11-24, bleedingedge/feedback.py): "More like this" / "Less like this" links under each topic, plus replies in your own words, read by the 7:30 task before it composes. Net votes below 0 mute a topic (not watched, not shortlisted); above 0 keep it watched and add a taste boost of 0.5 per net vote to its Monday shortlist rank (invented number). Detector scores never change, so the ledger still grades the detector. Votes kept in gitignored data/private/Feedback.csv; the public brief shows counts only. Kill test: if no feedback is recorded by 2026-12-22 (4 weeks), remove it. You chose scoring too, without a reason; agreed as a separate boost rather than changing the detector's weights.
- A daily improver (added 2026-11-19, docs/IMPROVE.md, bleedingedge/harness.py, a 9:00 scheduled task): one reader-facing improvement a day, by pull request, for friends, family and students as well as you, without lowering quality. Checked by the harness and three fresh-eyes reviewers; never merges; never changes the detector. Friends' visits can't be measured on this page type.
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
- An HTML or email version of the brief, and any app. (Website and daily email moved into DELIVERABLES on 2026-11-19, after the trial passed.)

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
- 2026-11-01 — your call: added opportunities to apply to, a short section in each brief from week 2, with an 8-week kill test (review 2026-12-28); weeks 1 and 2–4 of the trial now differ in format
- 2026-11-02 — your call: added the Monday notification and missed-brief alert; moved application records to gitignored data/private/ because the repo is public
- 2026-11-09 — updated the meta-instructions to the current meta doc
- 2026-11-19 — your call: readers now include friends, family and students; added a daily improver that opens one PR a day, a harness of hard checks, and cited plain-language explainers on the site
- 2026-11-19 — built the daily email: bleedingedge/daily.py decides what's new, a 7:30 scheduled task sends it from your Gmail to you only when something is; the Monday task now splits the first step into Tue–Fri pieces (step 4c); data/Fragments.csv keeps fragments like "policies learn" out
- 2026-11-19 — built the website: a private claude.ai dashboard fed by five data files from bleedingedge/site.py, updated by the Monday task (step 8b); pick marks saved on the page
- 2026-11-19 — website and email design agreed: layout A plus a pick card, flagged topics and picks only, six done criteria; "today's step" Tue–Fri only
- 2026-11-19 — trial review: you acted on 4 of 4 picks (bar: 2), so the format passed; taste ratings left blank. Your call: keep the weekly brief and add a persistent private website and a daily email (Gmail connector, only when something's new); neither built yet
- 2026-11-18 — your call: added the pick ledger (each pick graded against its own "prove it wrong" test every Monday) and a trial-over reminder in the Monday notification until the review is filled in
- 2026-11-24 — updated the meta-instructions to the current meta doc
- 2026-11-24 — your call: the daily email asks for feedback (More/Less links per topic, or a reply); votes mute topics or rank them up on the Monday shortlist as a separate taste boost, kept private; 4-week kill test (2026-12-22)
- 2026-11-26 — fixed: the weekly brief stopped picking after the trial although the review kept it; picks resume Monday 30 Nov. The Monday shortlist and the improver's explainers now skip phrases in data/Fragments.csv; the brief no longer says "Week 5 of 4"
