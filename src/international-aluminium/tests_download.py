"""Health-invariant tests for the international-aluminium connector.

Run post-DAG, in-connector, against the raw assets through subsets_utils
loaders. Catch silent degradation that file-existence alone misses: empty
payloads, wrong schema, all-null metrics (auth/format drift).
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "period_name",
    "period_start",
    "period_end",
    "series_group",
    "series",
    "category",
    "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every publication should flatten to at least a handful of cell rows.
    Empty means the endpoint changed shape or the token silently expired."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 5, f"{sid}: raw parquet has only {len(table)} rows"


def test_schema_stable(spec_ids):
    """The long-format schema is identical for every publication."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == EXPECTED_COLS, (
            f"{sid}: columns {sorted(table.column_names)} != {sorted(EXPECTED_COLS)}"
        )


def test_values_present_and_numeric(spec_ids):
    """`value` is the whole point — it must be a float column with no nulls
    (we drop null cells at fetch). All-null = the cell parse broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count == 0, f"{sid}: {col.null_count} null values survived"
        assert table.schema.field("value").type == "double", (
            f"{sid}: value type is {table.schema.field('value').type}, expected double"
        )


def test_keys_present(spec_ids):
    """series and category (the two dimensions) and period_end must never be
    null — they form the natural key of each row."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for key in ("series", "category", "period_end"):
            assert table.column(key).null_count == 0, f"{sid}: null in {key}"
