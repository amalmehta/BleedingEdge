"""Hacker News stories with >= 50 points whose title contains a phrase.

Stands in for "the consensus has caught on". Exact phrase with typo tolerance off:
a plain search for GRPO matches ~5,400 stories through near-spellings; this matches 8.
"""
from datetime import date, datetime, time, timezone
from urllib.parse import urlencode

from ..http import get_json

API = "https://hn.algolia.com/api/v1/search_by_date"
MIN_POINTS = 50
PAGE = 1000  # Algolia returns at most 1000 hits per query


def _ts(d: date) -> int:
    return int(datetime.combine(d, time(), tzinfo=timezone.utc).timestamp())


def query_url(phrase: str, start: date, end: date, page: int = 0) -> str:
    return API + "?" + urlencode({
        "query": f'"{phrase}"',
        "tags": "story",
        "typoTolerance": "false",
        "restrictSearchableAttributes": "title",
        "numericFilters": f"points>={MIN_POINTS},created_at_i>={_ts(start)},created_at_i<{_ts(end)}",
        "hitsPerPage": PAGE,
        "page": page,
    })


def parse(data: dict) -> tuple[int, dict[str, date]]:
    items = {h["objectID"]: date.fromisoformat(h["created_at"][:10]) for h in data.get("hits", [])}
    return data.get("nbHits", 0), items


def _range(phrase: str, start: date, end: date) -> dict[str, date]:
    total, items = parse(get_json(query_url(phrase, start, end)))
    if total > len(items) and (end - start).days > 1:
        mid = start + (end - start) / 2
        return _range(phrase, start, mid) | _range(phrase, mid, end)
    return items


def dates(phrases: list[str], start: date, end: date) -> list[date]:
    items: dict[str, date] = {}
    for phrase in phrases:
        items.update(_range(phrase, start, end))
    return list(items.values())
