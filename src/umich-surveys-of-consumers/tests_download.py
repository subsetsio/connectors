"""Health invariants for the UMich Surveys of Consumers raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw parquet should hold rows. Empty payloads usually mean
    the POST form changed or the CSV format shifted."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_long_schema(spec_ids):
    """Raw is the uniform long shape (year, month, series, value)."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"year", "month", "series", "value"} <= cols, f"{sid}: cols={cols}"


def test_index_table_present(spec_ids):
    """Table 1 (Index of Consumer Sentiment) is the headline series and must
    carry a long monthly history with non-null values."""
    sid = "umich-surveys-of-consumers-table-1"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) >= 400, f"{sid}: only {len(table)} rows; expected monthly since 1978"
    series_vals = set(table.column("series").to_pylist())
    assert "Index" in series_vals, f"{sid}: series={series_vals}"
    values = table.column("value").to_pylist()
    assert any(v is not None for v in values), f"{sid}: all values null"
