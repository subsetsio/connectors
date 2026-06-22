"""Health-invariant tests for the Allen-Unger commodity-prices connector.

Run post-DAG, in-connector, against the raw assets via subsets_utils loaders.
These catch silent degradation that file existence alone misses — a truncated
download, an empty payload, or an upstream format switch.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "commodity", "variety", "market", "original_measure", "standard_measure",
    "original_currency", "standard_currency", "item_year",
    "item_value_original", "item_value_standardized", "notes", "source_raw",
}


def test_commodities_nonempty_and_complete(spec_ids):
    """The Commodities table must hold ~125k rows. A small fraction means the
    37MB download was truncated; 0 rows means the endpoint changed format/auth."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 100_000, f"{sid}: only {len(table)} rows; download likely truncated"
        assert set(table.column_names) == EXPECTED_COLUMNS, (
            f"{sid}: unexpected columns {table.column_names}"
        )


def test_year_range_sane(spec_ids):
    """Years must land in the database's known historical window (965-1914).
    A year outside this band signals column misalignment in parsing."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        years = load_raw_parquet(sid).column("item_year")
        lo = pc.min(years).as_py()
        hi = pc.max(years).as_py()
        assert lo is not None and 800 <= lo <= hi <= 1920, f"{sid}: year range [{lo}, {hi}] out of band"
