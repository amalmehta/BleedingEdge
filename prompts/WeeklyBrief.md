# Weekly brief: what the Monday task does

This file is the instruction set for the weekly scheduled task. It's under version control so any change to how briefs get made shows up in the diff.

**Trial scope (2026-10-27):** robotics only. The backtest failed its 50% bar. The user chose to run this trial anyway, on a bar lowered after seeing the results (BleedingEdge.md, "Bar lowered after seeing the results"). The brief must say so plainly every week. The generated track-record paragraph already does this, so never remove or soften it.

## Steps

1. **Check the trial isn't over.** Count the brief files in `briefs/` (named `YYYY-MM-DD.md`) dated 2026-10-27 or later.
   - If there are already 4, write no brief.
   - Instead, say the trial is done and that `docs/TrialReview.md` needs filling in, then stop.
2. **Generate the data and the draft.** Run this from the project root:
   ```bash
   uv run python -m bleedingedge.brief
   ```
   - It tops up arXiv, scores this year's candidate list, and writes `briefs/YYYY-MM-DD.md`, `briefs/img/YYYY-MM-DD.png`, `data/briefs/YYYY-MM-DD.json` and rows in `data/Trends.csv`.
   - It takes about 10–30 minutes, mostly GitHub searches.
   - If it fails, report the error and write nothing by hand.
3. **Write the study pick.** Replace the text between `<!-- pick:start -->` and `<!-- pick:end -->`, and keep the markers.
   - **Choose:** the highest-scoring shortlist topic that has a concrete way in, meaning a paper you can read end to end, or a repo with code you can run.
     - The shortlist and its recent papers are in `data/briefs/YYYY-MM-DD.json`. Read the abstracts of the listed papers (arxiv.org/abs links) before choosing.
     - If the phrase turns out to be a fragment rather than a topic (for example "platform for autonomous"), skip it and say so in one line.
     - If no shortlist topic has a way in, write "No pick this week" and say why. Never force a pick.
   - **Write**, in this order and under 250 words:
     - **What it is**, in two plain sentences.
     - **Why now:** the numbers from the table, which are its score, its growth, and how many papers and repos it has.
     - **What it rests on:** the 2–3 papers, linked.
     - **What would prove it wrong:** "Its 12-week paper count (bulk) never passes N by DATE + 1 year", where N is the larger of 20 and 4 × the "Papers, 12 wk" figure in the table. This is the backtest's hit test: the crowd arrives when the 12-week count reaches 25% of its peak (with the peak at 20 or more), so the flag was early only if the peak ends up more than 4 times today's count.
     - **First step, about 2 hours:** one paper to work through with researcher-pal, or one repo to clone and run, linked, with what you should have at the end.
     - Every claim gets a link. Web search is allowed for context, such as a lab page or a code release. Cite what you use, and never invent a paper, repo or number.
4. **Record the pick.** Append `date,topic,first_step_url` to `data/Picks.csv`, creating it with that header if it's missing. This stops the pick from repeating in the next 3 briefs.
5. **Add a row to `docs/TrialReview.md`** under "Briefs": the date, the pick, and empty cells for taste (1–5) and acted on (y/n). The user fills those in.
6. **Check the brief:**
   - It's under 1,500 words.
   - The track-record paragraph is intact.
   - No section has more than 5 items.
   - Nothing gives buy, sell or hold advice.
7. **Report** in 3 lines: the pick, how many topics were early, and anything odd. That includes zero candidates, an error, or a number that looks wrong.

## Don't

- Don't change any threshold, weight or scoring code. The method stays fixed for the 4 weeks, or the trial measures nothing.
- Don't commit or push. The user does that.
- Don't add sections the trial left out: tools, companies, the wider field.
