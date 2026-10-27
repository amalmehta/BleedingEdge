import math

from bleedingedge import scoring as sc


def test_growth_matches_spec_worked_example():
    # 12 papers in the last window vs 6 across the 3 before: g = 13 / 3
    g = sc.growth([2, 2, 2, 12])
    assert g[:3] == [None, None, None]
    assert math.isclose(g[3], 13 / 3)
    assert math.isclose(math.log2(g[3]), 2.115, abs_tol=1e-3)


def test_growth_flat_and_zero_counts():
    assert sc.growth([5, 5, 5, 5])[3] == 1.0
    assert sc.growth([0, 0, 0, 0])[3] == 1.0  # the +1 keeps empty windows at "no change"
    assert sc.growth([0, 0, 0, 2])[3] == 3.0  # tiny counts still move, but the volume floor stops them


def test_growth_short_series():
    assert sc.growth([]) == []
    assert sc.growth([1, 2]) == [None, None]


def test_score_spec_example():
    gs = {"arxiv": [13 / 3], "github": [3.0]}
    s = sc.score(gs, {"arxiv": 1, "github": 1}, 1.0, 0)
    assert math.isclose(s, (math.log2(13 / 3) + math.log2(3)) / 2)
    assert math.isclose(s, 1.85, abs_tol=0.01)


def test_score_ignores_consensus_zero_weight_and_missing():
    gs = {"arxiv": [4.0], "github": [None], "hn": [100.0], "funding": [1.0]}
    assert sc.score(gs, {"arxiv": 1, "github": 1, "funding": 0}, 1.0, 0) == 2.0
    assert sc.score({"hn": [8.0]}, {"hn": 1}, 1.0, 0) is None


def test_score_domain_weight():
    assert sc.score({"arxiv": [4.0]}, {"arxiv": 1}, 0.4, 0) == 0.8


def _topic(arxiv, github):
    counts = {"arxiv": arxiv, "github": github}
    return counts, {k: sc.growth(v) for k, v in counts.items()}


def test_heating_up_burst_needs_score_two_signals_and_volume():
    lam = {"arxiv": 1, "github": 1}
    counts, gs = _topic([2, 2, 2, 12], [3, 3, 3, 15])
    assert sc.heating_up(gs, counts, lam, 1.0, 3)
    # only one signal rising
    counts, gs = _topic([2, 2, 2, 30], [3, 3, 3, 3])
    assert not sc.heating_up(gs, counts, lam, 1.0, 3)
    # both rising but below both volume floors
    counts, gs = _topic([0, 0, 0, 4], [0, 0, 0, 9])
    assert not sc.heating_up(gs, counts, lam, 1.0, 3)


def test_rolling_and_trend():
    c = [1] * 13 + [0, 0, 2] + [10] * 13 + [20, 20, 20]
    assert sc.rolling([1, 2, 3, 4]) == [1, 3, 6, 9]
    t = sc.trend(c)
    assert all(v is None for v in t[:15])
    # window 31: last 12 weeks 60 papers vs the same 12 weeks a year earlier 30
    assert math.isclose(t[31], 61 / 31)


def test_trend_catches_steady_growth_burst_misses():
    # ~8x a year, smooth: burst ratio stays near 1.2, trend is large
    c = [round(2 * 1.174 ** k) for k in range(40)]
    assert max(g for g in sc.growth(c)[3:]) < 1.5
    assert sc.trend(c)[39] > 3


def test_heating_up_trend_mode():
    c = {"arxiv": [round(2 * 1.174 ** k) for k in range(40)],
         "github": [round(5 * 1.174 ** k) for k in range(40)]}
    lam = {"arxiv": 1, "github": 1}
    gt = {s: sc.trend(v) for s, v in c.items()}
    rolled = {s: sc.rolling(v) for s, v in c.items()}
    assert sc.heating_up(gt, rolled, lam, 1.0, 39, "trend")
    gb = {s: sc.growth(v) for s, v in c.items()}
    assert not sc.heating_up(gb, c, lam, 1.0, 39, "burst")


def test_funding_is_a_bonus_never_a_drag():
    lam = {"arxiv": 1, "github": 1, "funding": 1}
    gs = {"arxiv": [2.0], "github": [2.0]}
    assert sc.mode_score(gs, {"funding": [0]}, lam, 1.0, 0, "burst") == 1.0
    assert sc.mode_score(gs, {"funding": [1]}, lam, 1.0, 0, "burst") == 1.5
    assert sc.mode_score(gs, {}, lam, 1.0, 0, "burst") == 1.0


def test_consensus_window_and_still_small():
    c = [0, 0, 0, 4, 4, 4, 10, 30, 40]
    # rolling = [0,0,0,4,8,12,18,44,80]; peak 80, 25% = 20 -> window 7
    assert sc.consensus_window(c) == 7
    assert sc.consensus_window([1, 2, 3, 1]) is None  # peak 6 < PEAK_MIN
    assert sc.still_small(c, 6) and not sc.still_small(c, 8)


def test_signal_crossing_and_never():
    assert sc.signal_crossing([1, 1, 1, 1, 8, 9], 5) == 4
    assert sc.signal_crossing([5] * 20, 5) is None


def test_lead_weights():
    crossings = {"arxiv": {"a": 2, "b": 10, "c": 1}, "github": {"a": None, "b": 3, "c": None}}
    consensus = {"a": 6, "b": 11, "c": None}  # c never reached consensus: not judged
    lam = sc.lead_weights(crossings, consensus)
    assert lam["arxiv"] == 0.5   # led a by 4 windows; b by only 1
    assert lam["github"] == 0.5  # led b by 8 windows
    assert sc.lead_weights(crossings, {"a": None, "b": None, "c": None}) == {"arxiv": None, "github": None}


def test_early_needs_new_not_just_small():
    k = 40
    mature_small = [8] * 41          # ~24 papers per 12 weeks for years: small but not new
    new_small = [0] * 30 + [3] * 11  # nothing two years ago, ~9 per 12 weeks now
    assert sc.still_small(mature_small, k) and not sc.is_new(mature_small, k)
    assert not sc.early(mature_small, k)
    assert sc.early(new_small, k)
    assert not sc.early([0] * 41 + [40] * 3, 43)  # new but no longer small (120 in 12 weeks)
    assert not sc.is_new([0] * 20, 19)            # no data two years back: can't call it new
