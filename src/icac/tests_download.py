"""Health-invariant tests for the ICAC connector's raw assets.

All four subsets are carved from one xlsx workbook. These catch silent
degradation the file-existence check misses: an empty parse (Cloudflare served
an HTML challenge instead of the workbook, or a sheet layout changed), a
truncated download, or a value column that came back entirely null.
"""

from subsets_utils import load_raw_parquet

# Minimum row counts seen in the Nov 2022 workbook, discounted for safety.
_MIN_ROWS = {
    "icac-supply-and-use-balance": 20000,
    "icac-extra-fine-cotton-supply": 1000,
    "icac-cotton-prices": 800,
    "icac-published-forecasts": 2500,
}

_EXPECTED_COLS = {
    "icac-supply-and-use-balance": {"country", "season", "year_begin", "metric", "unit", "value"},
    "icac-extra-fine-cotton-supply": {"item", "country", "year_begin", "season", "value"},
    "icac-cotton-prices": {"source_table", "table_title", "quotation", "period", "period_type", "value"},
    "icac-published-forecasts": {"variable", "forecast_season", "horizon", "publication_round", "unit", "value"},
}


def test_raw_assets_nonempty_and_shaped(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = len(table)
        floor = _MIN_ROWS.get(sid, 1)
        assert n >= floor, f"{sid}: {n} rows < expected >= {floor} (truncated/empty parse?)"
        cols = set(table.column_names)
        missing = _EXPECTED_COLS.get(sid, set()) - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_value_column_has_data(spec_ids):
    """The numeric 'value' column must hold real numbers, not be all-null."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        value = table.column("value")
        non_null = len(value) - value.null_count
        assert non_null > 0, f"{sid}: 'value' column is entirely null"
