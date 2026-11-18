"""The pick ledger: grades each study pick against the test its brief wrote down.

    uv run python -m bleedingedge.ledger                    # tops up arXiv first (a few minutes)
    uv run python -m bleedingedge.ledger 2027-01-04 --no-update

Every pick says what would prove it wrong: "its 12-week paper count (bulk) never passes N by
DATE + 1 year", where N = max(20, 4 x that week's 12-week count). That is the backtest's hit rule:
the flag was early only if the topic grows to more than 4 times its size when picked.

The weekly task appends only date, topic and first step to data/Picks.csv. This fills in the rest:
  papers_12w, bar, due   the pick's own numbers, read from that day's row in data/Trends.csv
  peak_12w, peak_on      the highest 12-week count on any day from the pick to the due date (or today)
  status                 "took off" once the peak passes the bar; "didn't take off" if the due date
                         passes first; "open" until then
Counts come from the same bulk arXiv download the brief uses (title or abstract, word match), so a
pick is graded on the numbers it was picked on. Late-announced papers are counted on their own
dates, so a past day's count can rise a little after the fact.
"""
import csv
import sys
from bisect import bisect_left
from datetime import date, timedelta

from . import brief as br
from . import mining as mn

COLS = ["date", "topic", "first_step", "papers_12w", "bar", "due", "peak_12w", "peak_on", "status", "checked_on"]
SPAN = timedelta(days=84)   # 12 weeks: three 4-week windows, as in the brief's table
MULT, FLOOR = 4, 20         # the hit rule written in every pick (prompts/WeeklyBrief.md, step 3)


def read() -> list[dict]:
    if not br.PICKS.exists():
        return []
    with br.PICKS.open(newline="") as f:
        return [{c: (r.get(c) or "") for c in COLS} for r in csv.DictReader(f)]


def write(rows: list[dict]) -> None:
    with br.PICKS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)


def papers_on(day: str, topic: str) -> int | None:
    """The 12-week bulk count the brief showed for this topic on this day, or None if it isn't there."""
    if not br.TRENDS.exists():
        return None
    with br.TRENDS.open(newline="") as f:
        for r in csv.DictReader(f):
            if r["date"] == day and r["topic"] == topic:
                return int(r["arxiv_12w"])
    return None


def a_year_after(d: date) -> date:
    try:
        return d.replace(year=d.year + 1)
    except ValueError:      # 29 Feb
        return d.replace(year=d.year + 1, day=28)


def fill(row: dict) -> dict:
    """The pick's own numbers, if they aren't recorded yet."""
    if row["bar"]:
        return row
    n = papers_on(row["date"], row["topic"])
    if n is None:
        return row          # graded as "no data" below; nothing is invented
    return row | {"papers_12w": str(n), "bar": str(max(FLOOR, MULT * n)),
                  "due": a_year_after(date.fromisoformat(row["date"])).isoformat()}


def count_12w(dates: list[date], d: date) -> int:
    """Papers in the 12 weeks before d (d itself excluded, as the brief's windows end on the run date)."""
    return bisect_left(dates, d) - bisect_left(dates, d - SPAN)


def grade(row: dict, dates: list[date], today: date) -> dict:
    row = fill(row)
    if not row["bar"]:
        return row | {"status": "no data", "checked_on": today.isoformat()}
    start, due, bar = date.fromisoformat(row["date"]), date.fromisoformat(row["due"]), int(row["bar"])
    dates = sorted(dates)
    peak, peak_on = -1, start
    d = start
    while d <= min(today, due):
        c = count_12w(dates, d)
        if c > peak:
            peak, peak_on = c, d
        d += timedelta(days=1)
    status = "took off" if peak > bar else "didn't take off" if today > due else "open"
    return row | {"peak_12w": str(max(peak, 0)), "peak_on": peak_on.isoformat(), "status": status,
                  "checked_on": today.isoformat()}


def line(r: dict) -> str:
    if r["status"] == "no data":
        return f"{r['topic']} ({r['date']}): no row in Trends.csv for that day, so no bar to grade against."
    return (f"{r['topic']} ({r['date']}): {r['status']}. Peak {r['peak_12w']} papers in 12 weeks "
            f"(on {r['peak_on']}) against a bar of {r['bar']} by {r['due']}; {r['papers_12w']} when picked.")


def main(day: date, update: bool = True, log=print) -> list[dict]:
    rows = read()
    if not rows:
        log("No picks to grade.")
        return []
    from .sources import arxiv_bulk
    if update:
        arxiv_bulk.update(log)
    dates = mn.phrase_dates(arxiv_bulk.papers(), sorted({r["topic"] for r in rows}))
    graded = [grade(r, dates[r["topic"]], day) for r in rows]
    write(graded)
    for r in graded:
        log(line(r))
    return graded


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(date.fromisoformat(args[0]) if args else date.today(), "--no-update" not in sys.argv)
