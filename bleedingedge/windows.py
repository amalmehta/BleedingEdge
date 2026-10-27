"""4-week windows for the backtest, starting on Monday 4 Jan 2021.

The growth ratio compares one window with the three before it, so 4-week windows
are the natural unit: 75 of them cover Jan 2021 to early Oct 2026 (extended from 65 on
2026-10-27 so phrases new in 2024 can be graded on 2025–26).
"""
from datetime import date, timedelta

START = date(2021, 1, 4)
WINDOW_DAYS = 28
N_WINDOWS = 75
END = START + timedelta(days=WINDOW_DAYS * N_WINDOWS)  # exclusive: 2026-10-05


def windows() -> list[tuple[date, date]]:
    """(start, end) pairs; end is exclusive."""
    return [
        (START + timedelta(days=WINDOW_DAYS * k), START + timedelta(days=WINDOW_DAYS * (k + 1)))
        for k in range(N_WINDOWS)
    ]


def window_index(d: date) -> int | None:
    """Index of the window containing d, or None if outside the range."""
    if d < START or d >= END:
        return None
    return (d - START).days // WINDOW_DAYS


def counts(dates: list[date]) -> list[int]:
    """Number of dates falling in each window; dates outside the range are dropped."""
    out = [0] * N_WINDOWS
    for d in dates:
        k = window_index(d)
        if k is not None:
            out[k] += 1
    return out
