"""Growth ratios, score and flags, as defined in BleedingEdge.md (DEFINITIONS AND DEFERRED).

All thresholds are invented starting parameters; the backtest is what tests them.
Pure functions over per-window counts (4-week windows), no I/O.

Two kinds of rise, flagged separately:
  burst: this window vs the 3 before it (catches sudden jumps, e.g. DeepSeek-R1 and GRPO)
  trend: the last 12 weeks vs the same 12 weeks a year earlier (catches steady growth, e.g. VLAs)
"""
import math

YEAR = 13               # windows in a year

# Leading signals averaged into the score. Funding is not averaged: a round adds a bonus,
# and no round adds nothing, because rounds are rare.
LEADING = ["arxiv", "github", "citations", "labs"]

BURST = {"S": 1.0, "g": 1.5, "volume": {"arxiv": 5, "github": 10}}           # per 4 weeks
TREND = {"S": math.log2(3), "g": 2.0, "volume": {"arxiv": 10, "github": 30}}  # per 12 weeks
MIN_RISING = 2          # at least 2 signals must rise
FUNDING_BONUS = 0.5     # added to the score when a round lands in the window (burst) or last 12 weeks (trend)
SMALL_MAX = 50          # "early": fewer than 50 arXiv papers in the last 12 weeks...
NEW_MAX = 10            # ...and fewer than 10 in the same 12 weeks two years earlier (new, not just small)
NEW_LOOKBACK = 2 * YEAR
CONSENSUS_SHARE = 0.25  # the research crowd has arrived at 25% of the topic's peak 12-week paper count
PEAK_MIN = 20           # a topic whose peak is under 20 papers per 12 weeks never got a crowd
LEAD_WINDOWS = 2        # an 8-week lead = 2 four-week windows
SIGNAL_FLOOR = {"arxiv": 5, "github": 10, "funding": 1, "citations": 20, "labs": 2}

DOMAIN_WEIGHT = {"rl_robotics": 1.0, "ai_tooling": 0.8, "companies_labs": 0.8, "wider_tech": 0.4}


def growth(counts: list[int]) -> list[float | None]:
    """Burst: g_k = (c_k + 1) / (mean(c_{k-3..k-1}) + 1); None for the first 3 windows."""
    out: list[float | None] = [None] * min(3, len(counts))
    for k in range(3, len(counts)):
        prior = sum(counts[k - 3:k]) / 3
        out.append((counts[k] + 1) / (prior + 1))
    return out


def rolling(counts: list[int], span: int = 3) -> list[int]:
    """Sum of the last `span` windows (12 weeks for span 3), shorter at the start."""
    return [sum(counts[max(0, k - span + 1):k + 1]) for k in range(len(counts))]


def trend(counts: list[int]) -> list[float | None]:
    """Trend: (last 12 weeks + 1) / (same 12 weeks a year earlier + 1); None for the first 15 windows."""
    r = rolling(counts)
    return [None if k < YEAR + 2 else (r[k] + 1) / (r[k - YEAR] + 1) for k in range(len(counts))]


def score(gs: dict[str, list[float | None]], lam: dict[str, float], w: float, k: int) -> float | None:
    """S = w * sum(lam_s * log2 g_s) / sum(lam_s), over leading signals with data at k."""
    num = den = 0.0
    for s, series in gs.items():
        if s not in LEADING or series[k] is None or lam.get(s, 0) <= 0:
            continue
        num += lam[s] * math.log2(series[k])
        den += lam[s]
    return None if den == 0 else w * num / den


def funding_bonus(funding: list[int] | None, lam: dict[str, float], k: int, span: int) -> float:
    if not funding:
        return 0.0
    rounds = sum(funding[max(0, k - span + 1):k + 1])
    return FUNDING_BONUS * lam.get("funding", 0) if rounds else 0.0


def mode_score(gs, counts, lam, w, k, mode: str) -> float | None:
    span = 1 if mode == "burst" else 3
    s = score(gs, lam, w, k)
    return None if s is None else s + funding_bonus(counts.get("funding"), lam, k, span)


def heating_up(gs, counts, lam, w, k, mode: str = "burst") -> bool:
    """Score over threshold, >= 2 rising signals, and enough volume. `gs` holds the growth
    ratios for this mode; for trend, `counts` should already be 12-week rolling sums."""
    th = BURST if mode == "burst" else TREND
    s = mode_score(gs, counts, lam, w, k, mode)
    if s is None or s < th["S"]:
        return False
    rising = sum(1 for n, g in gs.items()
                 if n in LEADING and lam.get(n, 0) > 0 and g[k] is not None and g[k] >= th["g"])
    volume = any(counts.get(n, [0] * (k + 1))[k] >= floor for n, floor in th["volume"].items())
    return rising >= MIN_RISING and volume


def still_small(arxiv_counts: list[int], k: int) -> bool:
    """Detector-side "early": fewer than SMALL_MAX papers in the last 12 weeks."""
    return rolling(arxiv_counts)[k] < SMALL_MAX


def is_new(arxiv_counts: list[int], k: int) -> bool:
    """Fewer than NEW_MAX papers in the 12 weeks ending two years before window k.
    Small mature topics (tactile sensing, legged locomotion) fail this; False when there is
    no data two years back, so the first two years can't be called new."""
    j = k - NEW_LOOKBACK
    return j >= 2 and rolling(arxiv_counts)[j] < NEW_MAX


def early(arxiv_counts: list[int], k: int) -> bool:
    """Detector-side "early": still small and new. Uses only data up to window k."""
    return still_small(arxiv_counts, k) and is_new(arxiv_counts, k)


def consensus_window(arxiv_counts: list[int]) -> int | None:
    """Grading only (uses hindsight): first window where the 12-week paper count reaches
    25% of its peak over the whole backtest. None if the peak never reaches PEAK_MIN."""
    r = rolling(arxiv_counts)
    peak = max(r, default=0)
    if peak < PEAK_MIN:
        return None
    return next(k for k, v in enumerate(r) if v >= CONSENSUS_SHARE * peak)


def first(flags: list[bool]) -> int | None:
    return next((k for k, f in enumerate(flags) if f), None)


def signal_crossing(counts: list[int], floor: int) -> int | None:
    """First window where one signal rises on its own: a burst (g >= 1.5 with >= floor in the
    window) or a trend (g >= 2 with >= 3 x floor in 12 weeks)."""
    gb, gt, r = growth(counts), trend(counts), rolling(counts)
    return first([
        (gb[k] is not None and gb[k] >= BURST["g"] and counts[k] >= floor)
        or (gt[k] is not None and gt[k] >= TREND["g"] and r[k] >= 3 * floor)
        for k in range(len(counts))
    ])


def lead_weights(crossings: dict[str, dict[str, int | None]], consensus: dict[str, int | None]) -> dict[str, float | None]:
    """lam_s = share of test topics (with a consensus date) where s crossed >= 8 weeks earlier.

    crossings[signal][topic] and consensus[topic] are window indices or None.
    None for a signal means no test topic could be judged (no consensus date anywhere).
    """
    out = {}
    judged = [t for t, c in consensus.items() if c is not None]
    for s, by_topic in crossings.items():
        if not judged:
            out[s] = None
            continue
        led = sum(1 for t in judged if by_topic.get(t) is not None and consensus[t] - by_topic[t] >= LEAD_WINDOWS)
        out[s] = led / len(judged)
    return out
