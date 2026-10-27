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
from datetime import date
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


def papers() -> list[dict]:
    """Every harvested paper, deduplicated by id (a revised paper can appear twice)."""
    seen: dict[str, dict] = {}
    for p in sorted(DIR.glob("page*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                seen[r["id"]] = r
    return list(seen.values())


if __name__ == "__main__":
    harvest()
