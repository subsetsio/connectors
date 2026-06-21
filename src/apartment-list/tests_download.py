"""Health-invariant tests for apartment-list raw assets.

Catch silent degradation that file existence alone misses: empty/truncated
payloads, a wide history that collapsed to a single location, or a melt that
emitted columns it shouldn't.
"""

from subsets_utils import load_raw_parquet

_WIDE_LONG = [
    "apartment-list-rent-estimates",
    "apartment-list-vacancy-index",
    "apartment-list-time-on-market",
    "apartment-list-rent-growth-yoy",
    "apartment-list-rent-growth-mom",
]


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. An empty payload usually means
    the Contentful discovery returned the wrong asset or the CSV format shifted."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_wide_long_shape(spec_ids):
    """The five melted history products must be in long shape: a `month` (date)
    column and a non-null `value`, spanning many locations and many months. A
    wide file that failed to melt would have neither column."""
    for sid in _WIDE_LONG:
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"month", "value", "location_name"} <= cols, (
            f"{sid}: missing long-shape columns, got {sorted(cols)}"
        )
        months = table.column("month").to_pylist()
        locs = table.column("location_name").to_pylist()
        assert len(set(months)) >= 24, f"{sid}: only {len(set(months))} distinct months"
        assert len(set(locs)) >= 20, f"{sid}: only {len(set(locs))} distinct locations"
        assert all(v is not None for v in table.column("value").to_pylist()), (
            f"{sid}: NA cells leaked into the value column"
        )


def test_summary_snapshot_shape(spec_ids):
    """The summary product is a flat current-month snapshot with price columns."""
    sid = "apartment-list-rent-estimates-summary"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    cols = set(table.column_names)
    assert {"year", "month", "price_overall", "location_name"} <= cols, (
        f"{sid}: missing snapshot columns, got {sorted(cols)}"
    )
    assert len(table) >= 800, f"{sid}: only {len(table)} snapshot rows"
