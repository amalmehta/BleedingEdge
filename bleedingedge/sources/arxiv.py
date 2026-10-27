"""arXiv papers whose title or abstract contains a phrase, by first-submission date."""
import xml.etree.ElementTree as ET
from datetime import date
from urllib.parse import quote

from ..http import get_text

API = "https://export.arxiv.org/api/query"
PAGE = 1000
NS = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/"}


def _search(phrase: str, start: date, end: date) -> str:
    p = f'"{phrase}"'
    return (
        f"(ti:{p} OR abs:{p}) AND submittedDate:"
        f"[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]"
    )


def query_url(phrase: str, start: date, end: date, offset: int = 0, size: int = PAGE) -> str:
    return (
        f"{API}?search_query={quote(_search(phrase, start, end))}"
        f"&start={offset}&max_results={size}&sortBy=submittedDate&sortOrder=ascending"
    )


def parse(feed: str) -> tuple[int, dict[str, date]]:
    """(total results, {arxiv id: published date}) for one page."""
    root = ET.fromstring(feed)
    total = int(root.findtext("os:totalResults", "0", NS))
    items = {}
    for e in root.findall("a:entry", NS):
        pid = e.findtext("a:id", "", NS).rsplit("/", 1)[-1].split("v")[0]
        pub = e.findtext("a:published", "", NS)
        if pid and pub:
            items[pid] = date.fromisoformat(pub[:10])
    return total, items


def dates(phrases: list[str], start: date, end: date) -> list[date]:
    items: dict[str, date] = {}
    for phrase in phrases:
        offset, total = 0, None
        while total is None or offset < total:
            total, page = parse(get_text(query_url(phrase, start, end, offset)))
            if not page:
                break
            items.update(page)
            offset += PAGE
    return list(items.values())
