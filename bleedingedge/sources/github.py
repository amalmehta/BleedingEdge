"""New GitHub repos whose name or description contains a phrase, by creation date.

README is not searched by default: README text is today's, so old repos that later
mentioned the phrase showed up as "early" (61 VLA repos created in 2021, before the term
existed). Deleted repos are missing either way.
"""
from datetime import date, timedelta
from urllib.parse import urlencode

from ..http import get_json

API = "https://api.github.com/search/repositories"
PER_PAGE = 100
CAP = 1000  # GitHub search returns at most 1000 results per query
# Searched fields. --with-readme adds "readme" to show how much false early lead it creates.
FIELDS = "name,description"


def query_url(phrase: str, start: date, end: date, page: int = 1) -> str:
    last = end - timedelta(days=1)  # created:A..B is inclusive
    q = f'"{phrase}" in:{FIELDS} created:{start:%Y-%m-%d}..{last:%Y-%m-%d}'
    return API + "?" + urlencode({"q": q, "per_page": PER_PAGE, "page": page})


def parse(data: dict) -> tuple[int, dict[str, date]]:
    items = {r["full_name"]: date.fromisoformat(r["created_at"][:10]) for r in data.get("items", [])}
    return data.get("total_count", 0), items


def _range(phrase: str, start: date, end: date) -> dict[str, date]:
    total, items = parse(get_json(query_url(phrase, start, end)))
    if total > CAP and (end - start).days > 1:
        mid = start + (end - start) / 2
        return _range(phrase, start, mid) | _range(phrase, mid, end)
    page = 1
    while len(items) < total and page * PER_PAGE < CAP:
        page += 1
        _, more = parse(get_json(query_url(phrase, start, end, page)))
        if not more:
            break
        items.update(more)
    return items


def dates(phrases: list[str], start: date, end: date) -> list[date]:
    items: dict[str, date] = {}
    for phrase in phrases:
        # Year by year keeps most queries under the 1000-result cap.
        y = start
        while y < end:
            nxt = min(end, date(y.year + 1, 1, 1))
            items.update(_range(phrase, y, nxt))
            y = nxt
    return list(items.values())
