"""Your feedback from the daily email: which topics you want more or less of.

    uv run python -m bleedingedge.feedback subject --id MSG --date 2026-11-24 --subject "BleedingEdge feedback: less · grasp planning" [--note "..."]
    uv run python -m bleedingedge.feedback add --id MSG --date 2026-11-24 --vote more --topic "flow policies" [--note "..."]
    uv run python -m bleedingedge.feedback show

Each topic in the email has "More like this" and "Less like this" links. They open an email to
yourself with a fixed subject; sending it is the vote. You can also reply to the email in your own
words. Before composing, the daily task reads both kinds from Gmail (only mail from you, to you)
and records them here: link votes by script (`subject`), replies by the model (`add`, with your
words kept as the note).

What a vote changes, and nothing else:
  - net = "more" votes minus "less" votes for a topic, over all time.
  - net < 0: muted. Never watched by the daily email, never on the Monday shortlist.
  - net > 0: watched by the daily email even after it leaves the early list, and on the Monday
    shortlist ranked by score + BOOST × net. This is a taste boost, kept apart from the detector:
    scores in data/Trends.csv never change, so the pick ledger still grades the detector.
Votes live in data/private/ (gitignored): the repo is public, and these are your words.
"""
import argparse
import csv
import re
from datetime import date
from urllib.parse import quote

from . import brief as br

FEEDBACK = br.ROOT / "data" / "private" / "Feedback.csv"
COLS = ["date", "id", "vote", "topic", "note"]
VOTES = ("more", "less", "note")             # "note": words with no clear vote, kept for you to read
BOOST = 0.5                                  # added to a topic's rank per net "more" vote (invented)
PREFIX = "BleedingEdge feedback:"
SUBJECT = re.compile(rf"^(?:re:\s*)?{re.escape(PREFIX)}\s*(more|less)\s*·\s*(.+?)\s*$", re.I)


def read() -> list[dict]:
    if not FEEDBACK.exists():
        return []
    with FEEDBACK.open(newline="") as f:
        return [{c: r.get(c) or "" for c in COLS} for r in csv.DictReader(f)]


def add(day: str, msg_id: str, vote: str, topic: str = "", note: str = "") -> bool:
    """Append one vote. False if this message already gave this topic a vote (re-runs are safe)."""
    vote, topic = vote.strip().lower(), " ".join(topic.lower().split())
    if vote not in VOTES or (vote != "note" and not topic):
        raise ValueError(f"vote must be one of {VOTES}, with a topic unless it's a note")
    date.fromisoformat(day)
    rows = read()
    if any(r["id"] == msg_id and r["topic"] == topic and r["vote"] == vote for r in rows):
        return False
    FEEDBACK.parent.mkdir(parents=True, exist_ok=True)
    new = not FEEDBACK.exists()
    with FEEDBACK.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow({"date": day, "id": msg_id, "vote": vote, "topic": topic, "note": " ".join(note.split())})
    return True


def parse_subject(subject: str) -> tuple[str, str] | None:
    """('less', 'grasp planning') from a link vote's subject, or None if it isn't one."""
    m = SUBJECT.match(subject.strip())
    return (m[1].lower(), " ".join(m[2].lower().split())) if m else None


def net(upto: date | None = None) -> dict[str, int]:
    """Per topic, more minus less, counting only votes dated on or before `upto` if given."""
    out: dict[str, int] = {}
    for r in read():
        if r["vote"] in ("more", "less") and (upto is None or r["date"] <= upto.isoformat()):
            out[r["topic"]] = out.get(r["topic"], 0) + (1 if r["vote"] == "more" else -1)
    return out


def muted(upto: date | None = None) -> set[str]:
    return {t for t, n in net(upto).items() if n < 0}


def wanted(upto: date | None = None) -> list[str]:
    """Topics with net 'more' votes, most wanted first."""
    return [t for t, n in sorted(net(upto).items(), key=lambda kv: -kv[1]) if n > 0]


def boost(topic: str, upto: date | None = None) -> float:
    return BOOST * max(0, net(upto).get(topic, 0))


def mailto(to: str, vote: str, topic: str) -> str:
    body = "Send this as it is to record the vote. Add a line about why if you like."
    return f"mailto:{quote(to, safe='@')}?subject={quote(f'{PREFIX} {vote} · {topic}')}&body={quote(body)}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Record feedback from the daily email.")
    ap.add_argument("action", choices=["subject", "add", "show"])
    ap.add_argument("--id", default="")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--subject", default="")
    ap.add_argument("--vote", default="")
    ap.add_argument("--topic", default="")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    if a.action == "show":
        n = net()
        print(f"{len(read())} rows | wanted: {', '.join(f'{t} (+{n[t]})' for t in wanted()) or 'none'}"
              f" | muted: {', '.join(sorted(muted())) or 'none'}")
    else:
        if not a.id:
            ap.error("--id (the Gmail message id) is required, so a message is never counted twice")
        vote, topic = (parse_subject(a.subject) or (None, None)) if a.action == "subject" else (a.vote, a.topic)
        if vote is None:
            raise SystemExit(f"not a feedback subject: {a.subject!r}")
        print("recorded" if add(a.date, a.id, vote, topic, a.note) else "already recorded")
