"""Announced funding rounds, hand-collected and cited in data/Funding.csv."""
import csv
from datetime import date
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "data" / "Funding.csv"


def rows(path: Path = PATH) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def dates(topic_key: str, start: date, end: date, path: Path = PATH) -> list[date]:
    out = []
    for r in rows(path):
        if r["topic"].strip() != topic_key:
            continue
        d = date.fromisoformat(r["announced"].strip())
        if start <= d < end:
            out.append(d)
    return out
