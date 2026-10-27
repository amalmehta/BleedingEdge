from datetime import date, timedelta

from bleedingedge.windows import END, N_WINDOWS, START, counts, window_index, windows


def test_windows_cover_range_without_gaps():
    w = windows()
    assert len(w) == N_WINDOWS == 75 and END == date(2026, 10, 5)
    assert w[0][0] == START == date(2021, 1, 4) and w[-1][1] == END
    assert all(a[1] == b[0] for a, b in zip(w, w[1:]))
    assert START.weekday() == 0


def test_window_index_edges():
    assert window_index(START) == 0
    assert window_index(START + timedelta(days=27)) == 0
    assert window_index(START + timedelta(days=28)) == 1
    assert window_index(START - timedelta(days=1)) is None
    assert window_index(END) is None


def test_counts_drop_out_of_range():
    c = counts([START, START, END, date(2020, 6, 1), START + timedelta(days=30)])
    assert c[0] == 2 and c[1] == 1 and sum(c) == 3
