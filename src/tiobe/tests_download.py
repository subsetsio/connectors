"""Health-invariant tests for the TIOBE connector raw assets.

Catches silent degradation the per-node YAML expectations can't: an empty
payload, a layout change that strips one of the five tables, or the chart-series
regex matching nothing.
"""

from subsets_utils import load_raw_parquet

# minimum row counts that should always hold if parsing succeeded
_MIN_ROWS = {
    "tiobe-historical-ratings": 2000,
    "tiobe-current-rankings": 20,
    "tiobe-next-50-languages": 25,
    "tiobe-hall-of-fame": 15,
    "tiobe-very-long-term-history": 20,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold a sane number of rows. Empty or
    tiny payloads mean the page layout changed or a parser silently matched
    nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows, expected >= {floor}"


def test_historical_ratings_span(spec_ids):
    """The history series must span from 2001 to a recent year — a collapsed
    span means the series regex captured only a fragment."""
    sid = "tiobe-historical-ratings"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    years = {d.year for d in table.column("date").to_pylist()}
    assert min(years) <= 2002, f"history should start ~2001, got {min(years)}"
    assert max(years) >= 2024, f"history should reach recent years, got {max(years)}"
