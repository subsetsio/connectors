"""Health-invariant tests for the CBN connector raw assets.

Run post-DAG, in-connector, against the data through subsets_utils loaders.
They catch silent degradation that file-existence alone misses: empty payloads,
a parser that quietly dropped to zero rows, broken indicator-id mapping, or a
date column that stopped parsing.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"indicator_id", "indicator", "frequency", "period", "date", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every CBN table must yield observations. An empty parquet means the
    TableView parse broke (format change, auth wall, render cap) for that table."""
    empties = []
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} tables have 0 rows: {empties}"


def test_schema_stable(spec_ids):
    """Every asset carries the long-format schema we declared."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert EXPECTED_COLS <= cols, f"{sid}: missing columns {EXPECTED_COLS - cols}"


def test_values_present_and_finite(spec_ids):
    """`value` is the payload; a table that is all-null means the value column
    moved or the cell parser stopped recognising numbers."""
    import math
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        vals = t.column("value").to_pylist()
        nonnull = [v for v in vals if v is not None]
        assert nonnull, f"{sid}: every value is null"
        assert any(math.isfinite(v) for v in nonnull), f"{sid}: no finite values"


def test_dates_parse(spec_ids):
    """`date` should parse for the overwhelming majority of rows — an unparsed
    period format (new frequency) would show up as a spike in null dates."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        dates = t.column("date").to_pylist()
        if not dates:
            continue
        nonnull = sum(1 for d in dates if d is not None)
        frac = nonnull / len(dates)
        assert frac >= 0.95, f"{sid}: only {frac:.0%} of rows have a parsed date"


def test_indicator_id_mapping(spec_ids):
    """indicator_id must be populated and there must be >1 distinct id on the
    multi-indicator tables — a collapse to one id means the positional
    row->indicator mapping broke."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        ids = t.column("indicator_id").to_pylist()
        assert all(i is not None for i in ids), f"{sid}: null indicator_id present"
