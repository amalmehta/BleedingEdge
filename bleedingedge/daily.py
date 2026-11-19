"""The daily email: what's new since the last one, or nothing at all.

    uv run python -m bleedingedge.daily compose --site URL     # writes site/email.json, prints a summary
    uv run python -m bleedingedge.daily sent                   # after the email went out: remember its papers
    uv run python -m bleedingedge.daily compose --date 2026-11-24 --no-fetch   # sample run, no network

A daily scheduled task runs `compose`, sends the email through Gmail only if `send` is true, then
runs `sent`. Three things can make an email, and nothing else does:
  - New arXiv papers on this week's pick and the top early topics, submitted in the last 7 days and
    never emailed before (title or abstract contains the phrase; arXiv's own search, newest first).
  - Today's step: on Tuesday to Friday, one 30-minute piece of the pick's 2-hour first step, from
    data/steps/<pick date>.json, which the Monday task writes.
  - An opportunity deadline exactly 14, 7, 3 or 1 days away (data/Opportunities.csv).
The website link rides along but never makes an email by itself. Papers count as emailed only once
`sent` runs, so a failed send shows them again tomorrow.
"""
import argparse
import csv
import html
import json
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from urllib.parse import quote

from . import brief as br
from .http import CACHE, get_text
from .notify import OPPORTUNITIES
from .site import record
from .sources.arxiv import API, NS

OUT = br.ROOT / "site" / "email.json"
SEEN = CACHE / "daily" / "seen.json"          # arXiv ids already emailed (gitignored cache)
STEPS = br.ROOT / "data" / "steps"
FRAGMENTS = br.ROOT / "data" / "Fragments.csv"  # mined phrases that aren't topics; never watched
LOOKBACK = 7                                  # days of submissions to look at
TOPICS = 4                                    # the pick plus up to 3 other early topics
PER_TOPIC = 3                                 # papers listed per topic
REMIND = (14, 7, 3, 1)                        # days before a deadline that earn a reminder


def latest_pick(day: date) -> dict | None:
    if not br.PICKS.exists():
        return None
    with br.PICKS.open(newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["date"] <= day.isoformat()]
    return rows[-1] if rows else None


def fragments() -> set[str]:
    if not FRAGMENTS.exists():
        return set()
    with FRAGMENTS.open(newline="") as f:
        return {r["phrase"] for r in csv.DictReader(f)}


def watched(day: date) -> list[str]:
    """This week's pick first, then the highest-scoring early topics of the latest brief,
    leaving out phrases listed in data/Fragments.csv."""
    pick = latest_pick(day)
    skip = fragments()
    out = [pick["topic"]] if pick else []
    briefs = sorted(p for p in br.DATA.glob("20*.json") if p.stem <= day.isoformat())
    if briefs:
        early = json.loads(briefs[-1].read_text()).get("early", [])
        for r in sorted(early, key=lambda r: -(r.get("score") or 0)):
            if r["topic"] not in out and r["topic"] not in skip and len(out) < TOPICS:
                out.append(r["topic"])
    return out


def search_url(phrase: str, day: date) -> str:
    start = day - timedelta(days=LOOKBACK)
    q = f'(ti:"{phrase}" OR abs:"{phrase}") AND submittedDate:[{start:%Y%m%d}0000 TO {day:%Y%m%d}2359]'
    return f"{API}?search_query={quote(q)}&start=0&max_results=25&sortBy=submittedDate&sortOrder=descending"


def parse(feed: str) -> list[dict]:
    out = []
    for e in ET.fromstring(feed).findall("a:entry", NS):
        pid = e.findtext("a:id", "", NS).rsplit("/", 1)[-1].split("v")[0]
        title = " ".join(e.findtext("a:title", "", NS).split())
        pub = e.findtext("a:published", "", NS)[:10]
        if pid and title:
            out.append({"id": pid, "title": title, "submitted": pub, "url": f"https://arxiv.org/abs/{pid}"})
    return out


def seen() -> set[str]:
    try:
        return set(json.loads(SEEN.read_text()))
    except (OSError, ValueError):
        return set()


def new_papers(day: date, fetch=get_text) -> dict[str, list[dict]]:
    """Per watched topic, papers not emailed before (a paper shows under its first topic only)."""
    done, out = seen(), {}
    for phrase in watched(day):
        fresh = [p for p in parse(fetch(search_url(phrase, day))) if p["id"] not in done]
        done |= {p["id"] for p in fresh}
        if fresh:
            out[phrase] = fresh
    return out


def todays_step(day: date) -> str:
    """Tuesday to Friday only: the piece the Monday task wrote for this date, if any."""
    if day.weekday() not in (1, 2, 3, 4):
        return ""
    pick = latest_pick(day)
    path = STEPS / f"{pick['date']}.json" if pick else None
    if not path or not path.exists():
        return ""
    return json.loads(path.read_text()).get("pieces", {}).get(day.isoformat(), "")


def deadlines(day: date) -> list[dict]:
    if not OPPORTUNITIES.exists():
        return []
    out = []
    with OPPORTUNITIES.open(newline="") as f:
        for r in csv.DictReader(f):
            try:
                due = date.fromisoformat(r["deadline"])
            except ValueError:
                continue                       # "rolling" and the like never earn a reminder
            if (due - day).days in REMIND:
                out.append(r | {"days": (due - day).days})
    return out


def compose(day: date, site: str = "", fetch=get_text) -> dict:
    pick = latest_pick(day)
    papers = new_papers(day, fetch)
    step = todays_step(day)
    due = deadlines(day)
    n = sum(len(v) for v in papers.values())
    send = bool(n or step or due)
    parts = ([f"{n} new paper{'s' if n != 1 else ''}"] if n else []) + (["today's step"] if step else []) \
        + ([f"{len(due)} deadline{'s' if len(due) != 1 else ''}"] if due else [])
    subject = f"BleedingEdge, {day:%-d %b}: " + ", ".join(parts) if send else ""
    text, h = [], []
    if step:
        text += ["Today's step (about 30 minutes)", f"{pick['topic']}: {step}", ""]
        h += [f"<h3>Today's step (about 30 minutes)</h3><p><b>{html.escape(pick['topic'])}</b>: {html.escape(step)}</p>"]
    if papers:
        text += ["New papers, submitted in the last 7 days"]
        h += ["<h3>New papers, submitted in the last 7 days</h3>"]
        for phrase, ps in papers.items():
            label = phrase + (" (this week's pick)" if pick and phrase == pick["topic"] else "")
            more = len(ps) - PER_TOPIC
            text += [f"{label}:"] + [f"- {p['title']} ({p['submitted']}) {p['url']}" for p in ps[:PER_TOPIC]] \
                + ([f"- and {more} more"] if more > 0 else [])
            h += [f"<p><b>{html.escape(label)}</b></p><ul>"
                  + "".join(f'<li><a href="{p["url"]}">{html.escape(p["title"])}</a> ({p["submitted"]})</li>' for p in ps[:PER_TOPIC])
                  + (f"<li>and {more} more</li>" if more > 0 else "") + "</ul>"]
        text += [""]
    if due:
        text += ["Deadlines coming up"] + [f"- {r['name']}: {r['deadline']} ({r['days']} days) {r['url']}" for r in due] + [""]
        h += ["<h3>Deadlines coming up</h3><ul>" + "".join(
            f'<li><a href="{html.escape(r["url"])}">{html.escape(r["name"])}</a>: {r["deadline"]} ({r["days"]} days)</li>'
            for r in due) + "</ul>"]
    if site:
        text += [f"Trend history and your picks: {site}"]
        h += [f'<p><a href="{html.escape(site)}">Trend history and your picks</a></p>']
    rec = record()[0]
    caveat = (f"Flags score about chance in the backtest ({rec['took_off']} of {rec['flagged']} took off), "
              "so read them as long shots.")
    text += [caveat]
    h += [f'<p style="color:#777">{caveat}</p>']
    email = {"date": day.isoformat(), "send": send, "subject": subject, "text": "\n".join(text),
             "html": "\n".join(h), "paper_ids": [p["id"] for ps in papers.values() for p in ps]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(email, indent=1, ensure_ascii=False))
    return email


def mark_sent() -> int:
    email = json.loads(OUT.read_text())
    done = seen() | set(email["paper_ids"])
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(sorted(done)))
    return len(email["paper_ids"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Compose the daily BleedingEdge email.")
    ap.add_argument("action", choices=["compose", "sent"])
    ap.add_argument("--date", type=date.fromisoformat, default=date.today())
    ap.add_argument("--site", default="", help="the website link to include")
    ap.add_argument("--no-fetch", action="store_true", help="no network: every arXiv search comes back empty")
    a = ap.parse_args()
    if a.action == "sent":
        print(f"Remembered {mark_sent()} papers as emailed.")
    else:
        empty = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        e = compose(a.date, a.site, (lambda url: empty) if a.no_fetch else get_text)
        print(f"send: {str(e['send']).lower()}" + (f" | subject: {e['subject']}" if e["send"] else " | nothing new today"))
