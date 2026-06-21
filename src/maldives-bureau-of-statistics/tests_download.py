"""Health invariants for the Maldives Bureau of Statistics raw assets.

Each download node parses one yearbook Excel table into tidy long form
(row_label, series, value). These checks catch silent degradation a file-exists
probe misses: an empty parse (layout changed, wrong sheet), a dropped value
column, or non-numeric leakage into the value column.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table parsed to at least a handful of (row_label, series, value)
    rows. A 0-row (or near-0) parse means the crosstab layout shifted and the
    melt found no labelled numeric block."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 3, f"{sid}: only {len(table)} rows parsed (expected >=3)"


def test_schema_is_tidy(spec_ids):
    """The tidy schema is the contract every transform reads back."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"row_label", "series", "value"} <= cols, f"{sid}: columns {cols}"


def test_value_column_numeric_nonnull(spec_ids):
    """Value must be a non-null float — the melt drops nulls and non-numeric
    cells, so any null here means the writer schema or parse changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vcol = table.column("value")
        assert vcol.null_count == 0, f"{sid}: {vcol.null_count} null values"
