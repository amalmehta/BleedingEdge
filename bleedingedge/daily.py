"""The daily email: what's new since the last one, or nothing at all.

    uv run python -m bleedingedge.daily compose --site URL --to ADDRESS   # writes site/email.json, prints a summary
    uv run python -m bleedingedge.daily sent                   # after the email went out: remember its papers
    uv run python -m bleedingedge.daily compose --date 2026-11-24 --no-fetch   # sample run, no network

A daily scheduled task runs `compose`, sends the email through Gmail only if `send` is true, then
runs `sent`. Three things can make an email, and nothing else does:
  - New arXiv papers on this week's pick and the top early topics, submitted in the last 7 days and
    never emailed before (title or abstract contains the phrase; arXiv's own search, newest first).
  - Today's step: on Tuesday to Friday, one 30-minute piece of the pick's 2-hour first step, from
    data/steps/<pick date>.json, which the Monday task writes.
  - An opportunity deadline exactly 14, 7, 3 or 1 days away (data/Opportunities.csv).
The website link rides along but never makes an email by itself. With --to, each topic gets
"More like this" / "Less like this" links that open a ready-to-send email to you; the task records
those and your replies with bleedingedge.feedback before composing, so muted topics aren't watched. Papers count as emailed only once
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
from . import feedback as fb
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
    """This week's pick first, then topics you asked for more of, then the highest-scoring early
    topics of the latest brief. Leaves out phrases in data/Fragments.csv and topics you muted."""
    pick = latest_pick(day)
    skip = fragments() | fb.muted()
    cands = ([pick["topic"]] if pick else []) + fb.wanted()
    briefs = sorted(p for p in br.DATA.glob("20*.json") if p.stem <= day.isoformat())
    if briefs:
        early = json.loads(briefs[-1].read_text()).get("early", [])
        cands += [r["topic"] for r in sorted(early, key=lambda r: -(r.get("score") or 0))]
    out = []
    for t in cands:
        if t not in out and t not in skip and len(out) < TOPICS:
            out.append(t)
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


# Email layout: one narrow column, a one-line summary first, then the step, deadlines and papers,
# each paper a linked title with a quiet date line under it. Inline styles only: Gmail drops <style>.
INK, MUTED, LINE, ACCENT = "#1f1f1d", "#6b6a66", "#e4e2dc", "#2f5d8a"
BOX = f"max-width:600px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;color:{INK}"
H = f"font-size:13px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:{MUTED};margin:28px 0 8px"


def _short(d: str) -> str:
    return f"{date.fromisoformat(d):%-d %b}"


FEEDBACK_LINE = ("Want more or less of a topic? Use the links under it, or reply in your own words. "
                 "Your votes change which topics tomorrow's email watches and which topic Monday's brief picks, "
                 "not the detector's scores. They're kept on your Mac only.")
FEEDBACK_TEXT = ("Want more or less of a topic? Reply in your own words. Your votes change which topics "
                 "tomorrow's email watches and which topic Monday's brief picks, not the detector's scores. "
                 "They're kept on your Mac only.")


def votes(to: str, phrase: str) -> str:
    """'More like this · Less like this' under a topic: each opens a ready-to-send email to you."""
    if not to:
        return ""
    e = html.escape
    a = lambda v, label: f'<a href="{e(fb.mailto(to, v, phrase))}" style="color:{MUTED}">{label}</a>'
    return f'<p style="margin:0 0 12px;font-size:13px;color:{MUTED}">{a("more", "More like this")} · {a("less", "Less like this")}</p>'


def render(day, pick, papers, step, due, site, caveat, parts, to="") -> tuple[str, str]:
    e = html.escape
    T = [f"BleedingEdge, {day:%A %-d %B}", " · ".join(parts), ""]
    Hh = [f'<div style="{BOX}">',
          f'<p style="margin:0;font-size:13px;color:{MUTED}">BleedingEdge · {day:%A %-d %B}</p>',
          f'<p style="margin:4px 0 0;font-size:18px">{e(" · ".join(parts).capitalize())}</p>']
    if step:
        T += ["TODAY'S STEP, ABOUT 30 MINUTES", f"{pick['topic'].capitalize()}: {step}", ""]
        Hh += [f'<p style="{H}">Today\'s step · about 30 minutes</p>',
               f'<div style="border-left:3px solid {ACCENT};padding:4px 0 4px 14px">'
               f'<p style="margin:0;color:{MUTED};font-size:13px">{e(pick["topic"].capitalize())}</p>'
               f'<p style="margin:2px 0 0">{e(step)}</p></div>']
    if due:
        T += ["DEADLINES"] + [f"{r['name']}: closes {_short(r['deadline'])}, in {r['days']} day{'s' if r['days'] != 1 else ''}\n  {r['url']}" for r in due] + [""]
        Hh += [f'<p style="{H}">Deadlines</p>'] + [
            f'<p style="margin:0 0 10px"><a href="{e(r["url"])}" style="color:{ACCENT};text-decoration:none">{e(r["name"])}</a>'
            f'<br><span style="color:{MUTED};font-size:13px">Closes {_short(r["deadline"])}, in {r["days"]} day{"s" if r["days"] != 1 else ""}</span></p>'
            for r in due]
    groups = []
    if pick and pick["topic"] in papers:
        groups.append((f"Your pick: {pick['topic']}", {pick["topic"]: papers[pick["topic"]]}))
    rest = {k: v for k, v in papers.items() if not (pick and k == pick["topic"])}
    if rest:
        groups.append(("Other early topics", rest))
    for title, topics in groups:
        T += [title.upper()]
        Hh += [f'<p style="{H}">{e(title)}</p>']
        for phrase, ps in topics.items():
            more = len(ps) - PER_TOPIC
            if title == "Other early topics":
                T += [f"{phrase.capitalize()}"]
                Hh += [f'<p style="margin:14px 0 6px;font-weight:600">{e(phrase.capitalize())}</p>']
            for p in ps[:PER_TOPIC]:
                T += [f"- {p['title']}\n  {_short(p['submitted'])} · {p['url']}"]
                Hh += [f'<p style="margin:0 0 10px"><a href="{p["url"]}" style="color:{ACCENT};text-decoration:none">{e(p["title"])}</a>'
                       f'<br><span style="color:{MUTED};font-size:13px">{_short(p["submitted"])} · arXiv {p["id"]}</span></p>']
            if more > 0:
                T += [f"  and {more} more"]
                Hh += [f'<p style="margin:0 0 10px;color:{MUTED};font-size:13px">and {more} more</p>']
            Hh += [votes(to, phrase)]
        T += [""]
    T += ["", "Papers: submitted in the last 7 days, title or abstract matches, never emailed before."]
    if site:
        T += [f"Trend history and your picks: {site}"]
    T += [caveat, "", FEEDBACK_TEXT]
    Hh += [f'<div style="margin-top:32px;padding-top:12px;border-top:1px solid {LINE};font-size:13px;color:{MUTED}">',
           "<p style=\"margin:0 0 6px\">Papers: submitted in the last 7 days, title or abstract matches, never emailed before.</p>"]
    if site:
        Hh += [f'<p style="margin:0 0 6px"><a href="{e(site)}" style="color:{ACCENT}">Trend history and your picks</a></p>']
    Hh += [f'<p style="margin:0 0 6px">{e(caveat)}</p>',
           f'<p style="margin:0">{e(FEEDBACK_LINE if to else FEEDBACK_TEXT)}</p></div></div>']
    return "\n".join(T), "\n".join(Hh)


def compose(day: date, site: str = "", fetch=get_text, to: str = "") -> dict:
    pick = latest_pick(day)
    papers = new_papers(day, fetch)
    step = todays_step(day)
    due = deadlines(day)
    n = sum(len(v) for v in papers.values())
    send = bool(n or step or due)
    plural = lambda k, w: f"{k} {w}{'s' if k != 1 else ''}"
    parts = ([plural(n, "new paper")] if n else []) + (["today's step"] if step else []) \
        + ([plural(len(due), "deadline")] if due else [])
    subject = f"BleedingEdge, {day:%-d %b}: " + ", ".join(parts) if send else ""
    rec = record()[0]
    caveat = (f"Flags score about chance in the backtest ({rec['took_off']} of {rec['flagged']} took off), "
              "so read them as long shots.")
    text, html_out = render(day, pick, papers, step, due, site, caveat, parts, to)
    email = {"date": day.isoformat(), "send": send, "subject": subject, "text": text,
             "html": html_out, "paper_ids": [p["id"] for ps in papers.values() for p in ps]}
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
    ap.add_argument("--to", default="", help="your address, for the More/Less links (kept out of the repo)")
    ap.add_argument("--no-fetch", action="store_true", help="no network: every arXiv search comes back empty")
    a = ap.parse_args()
    if a.action == "sent":
        print(f"Remembered {mark_sent()} papers as emailed.")
    else:
        empty = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        e = compose(a.date, a.site, (lambda url: empty) if a.no_fetch else get_text, a.to)
        print(f"send: {str(e['send']).lower()}" + (f" | subject: {e['subject']}" if e["send"] else " | nothing new today"))
