"""The Monday desktop notification: this week's pick and last week's question, or an alert that
the weekly brief didn't finish.

    uv run python -m bleedingedge.notify                    # end of the weekly task, even after a failure
    uv run python -m bleedingedge.notify --only-if-missing  # the later check: silent if the brief finished
    uv run python -m bleedingedge.notify --dry-run          # print the message, send nothing

Reads files only. Nothing about applications is read or shown.
"""
import argparse
import csv
import re
import subprocess
from datetime import date, timedelta

from . import brief as br

OPPORTUNITIES = br.ROOT / "data" / "Opportunities.csv"
REVIEW = br.ROOT / "docs" / "TrialReview.md"
OPPS_ONLY = br.BRIEFS / "opportunities"     # the task's output once the trial's 4 briefs are done
OPPS_END = date(2026, 12, 28)               # the opportunities review date
TRIAL_BRIEFS = 4
ACT_DAYS = 14                               # a pick counts as acted on within 14 days of its brief


def expected(day: date):
    """The file the weekly task should have finished by now, or None if nothing is due."""
    done = sum(1 for p in br.BRIEFS.glob("20*.md") if br.TRIAL_START.isoformat() <= p.stem < day.isoformat())
    if done < TRIAL_BRIEFS:
        return br.BRIEFS / f"{day}.md"
    return OPPS_ONLY / f"{day}.md" if day < OPPS_END else None


def finished(path) -> bool:
    if not path.exists():
        return False
    text = path.read_text()
    return "_Not written yet." not in text and br.OPPS_DRAFT not in text


def _rows(path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def acted_cells() -> dict[str, str]:
    """Brief date -> what's in the "Acted on" column of the trial review table."""
    if not REVIEW.exists():
        return {}
    out = {}
    for line in REVIEW.read_text().splitlines():
        m = re.match(r"\|\s*\[?(\d{4}-\d{2}-\d{2})", line)
        if m:
            cells = line.split("|")
            out[m[1]] = cells[4].strip() if len(cells) > 4 else ""
    return out


def last_pick_question(day: date) -> str:
    """Ask about the oldest earlier pick not marked yet, since its window closes first."""
    acted = acted_cells()
    for r in _rows(br.PICKS):
        if r["date"] < day.isoformat() and not acted.get(r["date"]):
            by = date.fromisoformat(r["date"]) + timedelta(days=ACT_DAYS)
            return f"Did you spend 2 hours on {r['topic']}? Mark it in TrialReview (window ends {by:%-d %b})."
    return ""


def message(day: date) -> str | None:
    """What to tell the user today, or None if nothing is due."""
    path = expected(day)
    if path is None:
        return None
    if not finished(path):
        return f"No finished brief for {day:%-d %b} yet. Open the weekly brief task's latest run to see why."
    opps = sum(r["date"] == day.isoformat() for r in _rows(OPPORTUNITIES))
    listed = f"{opps} new {'opportunity' if opps == 1 else 'opportunities'}."
    if path.parent == OPPS_ONLY:
        return f"Weekly opportunities are ready: {listed}"
    pick = next((r["topic"] for r in _rows(br.PICKS) if r["date"] == day.isoformat()), None)
    parts = [f"Pick: {pick}." if pick else "No pick this week.", listed, last_pick_question(day)]
    return " ".join(p for p in parts if p)


def send(text: str) -> None:
    # The text goes in as an argument, not into the script, so nothing in a file can run as AppleScript.
    subprocess.run(["osascript", "-e", "on run argv", "-e",
                    'display notification (item 1 of argv) with title "BleedingEdge"', "-e", "end run", text],
                   check=True)


def main(day: date, only_if_missing: bool = False, dry_run: bool = False) -> None:
    path = expected(day)
    if only_if_missing and (path is None or finished(path)):
        return
    text = message(day)
    if text is None:
        return
    print(text)
    if not dry_run:
        send(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Send the weekly brief's desktop notification.")
    ap.add_argument("--only-if-missing", action="store_true", help="stay silent if the brief finished")
    ap.add_argument("--dry-run", action="store_true", help="print the message, send nothing")
    ap.add_argument("--date", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD; defaults to today")
    a = ap.parse_args()
    main(a.date, a.only_if_missing, a.dry_run)
