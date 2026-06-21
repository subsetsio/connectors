"""Health-invariant tests for the IPEA connector raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the fetch
nodes used. They catch silent degradation (empty payloads, missing columns,
truncated catalog fetch) that file existence alone misses.
"""

from subsets_utils import load_raw_parquet


def test_series_catalog_populated():
    """The series catalog should hold ~3600 rows with the key columns."""
    table = load_raw_parquet("ipea-series")
    assert len(table) >= 3000, f"ipea-series has {len(table)} rows; expected >=3000"
    for col in ("SERCODIGO", "BASNOME", "TEMCODIGO"):
        assert col in table.column_names, f"ipea-series missing column {col}"


def test_values_nonempty_and_typed():
    """The long-format values asset must hold many observations across many
    series; an empty or tiny table means the per-series crawl broke."""
    table = load_raw_parquet("ipea-values")
    assert len(table) >= 1_000_000, f"ipea-values has {len(table)} rows; expected >=1M"
    for col in ("SERCODIGO", "VALDATA", "VALVALOR"):
        assert col in table.column_names, f"ipea-values missing column {col}"
    import pyarrow.compute as pc
    distinct_series = pc.count_distinct(table.column("SERCODIGO")).as_py()
    assert distinct_series >= 2000, f"ipea-values spans only {distinct_series} series; expected >=2000"
