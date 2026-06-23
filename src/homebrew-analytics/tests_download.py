"""Health invariants for Homebrew analytics raw assets.

Each download asset is a parquet of the three rolling windows for one analytics
category. Catch silent degradation a file-exists check misses: an empty payload,
a single window that quietly failed (so windows < 3), or percent/count columns
that stopped parsing to numeric.
"""

from subsets_utils import load_raw_parquet

EXPECTED_WINDOWS = {"30d", "90d", "365d"}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_all_three_windows_present(spec_ids):
    """Every category publishes 30d/90d/365d. Missing a window means one of the
    per-window fetches silently returned nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        windows = set(table.column("window").to_pylist())
        assert windows == EXPECTED_WINDOWS, f"{sid}: windows={sorted(windows)}, expected 30d/90d/365d"


def test_percent_in_range(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        pcts = table.column("percent").to_pylist()
        bad = [p for p in pcts if p is None or p < 0 or p > 100]
        assert not bad, f"{sid}: {len(bad)} percent values outside 0..100 (e.g. {bad[:3]})"


def test_rank_starts_at_one(spec_ids):
    """Each window is a 1-based ranking; rank 1 must exist per window."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        rows = table.to_pylist()
        for w in EXPECTED_WINDOWS:
            ranks = [r["rank"] for r in rows if r["window"] == w]
            assert ranks and min(ranks) == 1, f"{sid}/{w}: min rank is {min(ranks) if ranks else None}, expected 1"
