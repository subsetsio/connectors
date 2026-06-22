"""Health-invariant tests for the AAVSO VSX catalog connector.

Run post-DAG, in-connector, against the raw assets via subsets_utils loaders.
Catch silent degradation that file-existence alone misses — a truncated paging
crawl, an empty payload, or a schema swap upstream.
"""

from subsets_utils import load_raw_parquet


def test_catalog_nonempty_and_large(spec_ids):
    """The VSX catalog held ~10.3M objects; a tiny table means paging broke
    after the first page or the TAP endpoint changed."""
    table = load_raw_parquet("aavso-vsx-catalog")
    assert table.num_rows >= 8_000_000, (
        f"aavso-vsx-catalog: {table.num_rows:,} rows, expected >=8M"
    )


def test_catalog_schema_intact(spec_ids):
    """Core columns must be present with the expected names — a VizieR table
    rename would silently shift everything."""
    table = load_raw_parquet("aavso-vsx-catalog")
    names = set(table.schema.names)
    required = {"recno", "OID", "Name", "RAJ2000", "DEJ2000", "Type", "max", "min", "Period"}
    missing = required - names
    assert not missing, f"aavso-vsx-catalog: missing columns {missing}"


def test_oid_unique(spec_ids):
    """OID is the stable per-object key; duplicates mean a paging window was
    re-pulled (overlap) and the overwrite/order contract broke."""
    import pyarrow.compute as pc

    table = load_raw_parquet("aavso-vsx-catalog")
    oid = table.column("OID")
    assert oid.null_count == 0, "aavso-vsx-catalog: OID has nulls"
    distinct = pc.count_distinct(oid).as_py()
    assert distinct == table.num_rows, (
        f"aavso-vsx-catalog: {table.num_rows - distinct} duplicate OIDs"
    )
