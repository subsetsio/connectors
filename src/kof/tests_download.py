"""Health-invariant tests for the KOF connector raw assets."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every collection's raw parquet should hold observations. An empty
    payload means the /collections endpoint switched format or returned an
    error envelope silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_some_values(spec_ids):
    """Raw must carry the long-format columns, and across the corpus a healthy
    fraction of observations must be non-null — an all-null pull means the
    value field stopped parsing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"series_key", "obs_index", "date", "value"} <= cols, f"{sid}: cols={cols}"
        # series_key and date are never null
        assert table.column("series_key").null_count == 0, f"{sid}: null series_key"
        assert table.column("date").null_count == 0, f"{sid}: null date"
        # at least one non-null value somewhere in the asset
        vals = table.column("value")
        assert len(vals) - vals.null_count > 0, f"{sid}: all values null"
