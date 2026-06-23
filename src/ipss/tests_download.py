"""Health invariants for IPSS raw assets — catch silent degradation that file
existence alone misses (empty parse, all-null values, wrong shape)."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every Excel table has numeric data, so its parsed extraction must hold
    rows. Zero rows means the parse found no numeric cells — the source layout
    changed or the download was truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: parsed raw parquet has 0 rows"


def test_value_column_present_and_populated(spec_ids):
    """The 'value' column is the payload; it must exist and carry real numbers.
    An all-null value column means cell parsing silently failed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, f"{sid}: missing 'value' column"
        non_null = table.column("value").null_count
        assert non_null < table.num_rows, f"{sid}: 'value' column is entirely null"
