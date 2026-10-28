"""Bulk arXiv metadata over OAI-PMH, for phrase mining and local phrase counts.

    uv run python -m bleedingedge.sources.arxiv_bulk   # harvest; resumable, ~3 hours the first time

OAI-PMH lists records by last-modified date, so harvesting from 2021 returns every paper
created since 2021 (plus older papers revised since, which are dropped by created date).
Only papers in CATEGORIES are kept: id, created date, categories, title and abstract, one
gzipped JSON line each, one file per page. A state file holds the resumption token, so a
stopped harvest picks up where it left off. arXiv metadata is CC0.
"""
import gzip
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from ..http import CACHE

BASE = "https://oaipmh.arxiv.org/oai"
CATEGORIES = {"cs.RO", "cs.LG", "cs.AI", "cs.CL"}
SINCE = date(2021, 1, 1)
DIR = CACHE / "arxiv_bulk"
STATE = DIR / "state.json"
DELAY = 3.5

NS = {"o": "http://www.openarchives.org/OAI/2.0/", "a": "http://arxiv.org/OAI/arXiv/"}


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def parse(xml: str) -> tuple[list[dict], str | None]:
    """Records kept (in CATEGORIES, created on or after SINCE) and the next resumption token."""
    root = ET.fromstring(xml)
    out = []
    for m in root.iterfind(".//o:record/o:metadata/a:arXiv", NS):
        cats = (m.findtext("a:categories", "", NS) or "").split()
        created = date.fromisoformat(m.findtext("a:created", "", NS))
        if created < SINCE or not CATEGORIES.intersection(cats):
            continue
        out.append({"id": m.findtext("a:id", "", NS), "created": created.isoformat(), "cats": cats,
                    "title": _clean(m.findtext("a:title", "", NS)),
                    "abstract": _clean(m.findtext("a:abstract", "", NS))})
    tok = root.find(".//o:resumptionToken", NS)
    return out, (tok.text.strip() if tok is not None and tok.text and tok.text.strip() else None)


def _get(url: str, retries: int = 8) -> str:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BleedingEdge-backtest (personal research)"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == retries - 1:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or min(300, 10 * 2**attempt))
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(min(300, 10 * 2**attempt))
    raise RuntimeError(url)


def harvest(log=print) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text()) if STATE.exists() else {"page": 0, "token": None, "done": False}
    while not state["done"]:
        url = (f"{BASE}?verb=ListRecords&resumptionToken={quote(state['token'], safe='')}" if state["token"]
               else f"{BASE}?verb=ListRecords&metadataPrefix=arXiv&set=cs&from={SINCE:%Y-%m-%d}")
        recs, token = parse(_get(url))
        with gzip.open(DIR / f"page{state['page']:05d}.jsonl.gz", "wt") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
        state = {"page": state["page"] + 1, "token": token, "done": token is None}
        STATE.write_text(json.dumps(state))
        if state["page"] % 20 == 0:
            log(f"page {state['page']}")
        time.sleep(DELAY)
    log(f"done: {state['page']} pages")


def first_version(pid: str, created: str, seq_max: dict[str, int]) -> date | None:
    """Date of the first version. oaipmh.arxiv.org reports <created> as a later version's date
    for revised papers (1605.05195 shows 2021-01-02), which put ~30% of records in the wrong
    month or year. A new-style id (YYMM.NNNNN) fixes the month of the first version; when
    <created> isn't in that month (or the next, for late submissions), the day is estimated from
    the id's sequence number, since ids are given out in order through the month. None for
    old-style ids (cs/0601001), which all predate SINCE."""
    m = re.fullmatch(r"(\d{2})(\d{2})\.(\d{4,5})", pid)
    if not m:
        return None
    y, mo, seq = 2000 + int(m[1]), int(m[2]), int(m[3])
    c = date.fromisoformat(created)
    if (c.year * 12 + c.month) - (y * 12 + mo) in (0, 1):
        return c
    start = date(y, mo, 1)
    days = ((start + timedelta(days=32)).replace(day=1) - start).days
    return start + timedelta(days=int((days - 1) * min(1.0, seq / seq_max[m[1] + m[2]])))


def papers() -> list[dict]:
    """Every harvested paper created since SINCE, deduplicated by id (a revised paper can appear
    twice), with "created" corrected to the first version's date (see first_version).
    Files sort page* before upd*, so the newest copy of a record wins."""
    seen: dict[str, dict] = {}
    for p in sorted(DIR.glob("*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                seen[r["id"]] = r
    seq_max: dict[str, int] = {}
    for pid in seen:
        if re.fullmatch(r"\d{4}\.\d{4,5}", pid):
            ym, n = pid.split(".")
            seq_max[ym] = max(seq_max.get(ym, 0), int(n))
    out = []
    for r in seen.values():
        d = first_version(r["id"], r["created"], seq_max)
        if d is not None and d >= SINCE:
            out.append(r | {"created": d.isoformat()})
    return out


if __name__ == "__main__":
    harvest()
