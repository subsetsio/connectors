"""Health invariants for the Central Bank (Taiwan) raw assets.

Each spec writes one melted long-format parquet (period, date, series, value).
These catch silent degradation the file-exists check misses: an endpoint that
started returning an HTML error page, a structure change that breaks the melt,
or a period-format change that nulls every date.
"""
import pyarrow.compute as pc

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"period", "date", "series", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every matrix should yield rows. An empty asset usually means the API
    returned a 404/error body that parsed to no dataSets."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols == EXPECTED_COLS, f"{sid}: columns {cols} != {EXPECTED_COLS}"


def test_each_asset_has_numeric_values(spec_ids):
    """Each matrix must carry at least one real numeric value. An all-null
    asset means the melt mapped every cell to a missing token — a sign the
    value-column parsing or cell format drifted."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        non_null = len(table) - table.column("value").null_count
        if non_null == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} assets have no numeric values: {empty[:10]}"


def test_dates_mostly_parse(spec_ids):
    """Across all assets the vast majority of rows should carry a parsed date.
    A wholesale failure means the period label format changed."""
    total = 0
    dated = 0
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        total += len(table)
        dated += len(table) - table.column("date").null_count
    assert total > 0, "no rows across any asset"
    frac = dated / total
    assert frac >= 0.95, f"only {frac:.1%} of rows have a parsed date (expected >=95%)"
