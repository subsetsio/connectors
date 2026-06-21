"""Health invariants for the ifo Institute raw assets.

These run post-DAG against the saved raw parquet. They catch silent degradation
the DAG's own 0-row check misses: a bot-challenge HTML body slipping through as a
"file", a sheet-layout change collapsing series, or a truncated download.
"""

from subsets_utils import load_raw_parquet

# Minimum rows we expect per standard product (well below normal, above degraded).
_STD_MIN_ROWS = {
    "ifo-institute-ifo-business-climate-germany": 5000,
    "ifo-institute-ifo-export-expectations": 200,
    "ifo-institute-ifo-employment-barometer": 800,
    "ifo-institute-ifo-business-climate-eastern-germany": 400,
    "ifo-institute-ifo-business-climate-saxony": 400,
    "ifo-institute-ifo-export-climate": 400,
    "ifo-institute-ifo-import-climate": 200,
}
_VINTAGE_ID = "ifo-institute-ifo-business-climate-vintage"


def test_standard_assets_nonempty_and_typed(spec_ids):
    """Each standard product has plenty of rows, a usable date span, and at
    least one named series — a collapsed/empty parse trips this."""
    for sid, min_rows in _STD_MIN_ROWS.items():
        if sid not in spec_ids:
            continue
        t = load_raw_parquet(sid)
        assert len(t) >= min_rows, f"{sid}: {len(t)} rows < expected {min_rows}"
        cols = set(t.column_names)
        assert {"date", "series", "value"} <= cols, f"{sid}: cols={cols}"
        series = set(t.column("series").to_pylist())
        assert series and all(s for s in series), f"{sid}: empty/blank series labels"
        dates = t.column("date").to_pylist()
        assert min(dates).year <= 2006, f"{sid}: history starts too late ({min(dates)})"


def test_vintage_asset_shape(spec_ids):
    """The vintage union covers all 8 sectors, 3 indicators, many vintages."""
    if _VINTAGE_ID not in spec_ids:
        return
    t = load_raw_parquet(_VINTAGE_ID)
    assert len(t) >= 100_000, f"{_VINTAGE_ID}: only {len(t)} rows"
    sectors = set(t.column("sector").to_pylist())
    indicators = set(t.column("indicator").to_pylist())
    vintages = set(t.column("vintage").to_pylist())
    assert len(sectors) >= 8, f"expected >=8 sectors, got {sorted(sectors)}"
    assert {"Climate", "Situation", "Expectations"} <= indicators, f"indicators={indicators}"
    assert len(vintages) >= 50, f"expected many vintages, got {len(vintages)}"


def test_values_finite(spec_ids):
    """No NaN/inf leaked through float parsing."""
    import math

    for sid in spec_ids:
        t = load_raw_parquet(sid)
        for v in t.column("value").to_pylist():
            assert v is not None and math.isfinite(v), f"{sid}: bad value {v!r}"
