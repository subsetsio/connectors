"""Health-invariant tests run post-DAG, inside the connector, via subsets_utils
loaders. They catch silent degradation that file-existence alone misses: empty
payloads, a value column that vanished, all-null values from a format switch."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's raw parquet should hold rows. An empty payload usually
    means the JSON-stat endpoint changed shape or the dataset was retired."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present_and_typed(spec_ids):
    """Each dataset must publish a numeric `value` column — it is the one field
    every NSI dataset shares and what every downstream chart reads."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, f"{sid}: missing 'value' column"
        import pyarrow as pa

        assert pa.types.is_floating(table.schema.field("value").type), (
            f"{sid}: 'value' is {table.schema.field('value').type}, expected float"
        )


def test_value_not_all_null(spec_ids):
    """A dataset whose every value is null means the melt dropped real data or
    the source served only suppressed cells."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(table), f"{sid}: every 'value' is null"
