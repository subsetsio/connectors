"""Health-invariant tests for the AAVSO connector raw assets."""

from subsets_utils import load_raw_parquet


def test_catalog_nonempty_and_large(spec_ids):
    table = load_raw_parquet("aavso-vsx-catalog")
    assert table.num_rows >= 8_000_000, (
        f"aavso-vsx-catalog: {table.num_rows:,} rows, expected >=8M"
    )


def test_catalog_schema_intact(spec_ids):
    table = load_raw_parquet("aavso-vsx-catalog")
    names = set(table.schema.names)
    required = {"recno", "OID", "Name", "RAJ2000", "DEJ2000", "Type", "max", "min", "Period"}
    missing = required - names
    assert not missing, f"aavso-vsx-catalog: missing columns {missing}"


def test_oid_unique(spec_ids):
    import pyarrow.compute as pc

    table = load_raw_parquet("aavso-vsx-catalog")
    oid = table.column("OID")
    assert oid.null_count == 0, "aavso-vsx-catalog: OID has nulls"
    distinct = pc.count_distinct(oid).as_py()
    assert distinct == table.num_rows, (
        f"aavso-vsx-catalog: {table.num_rows - distinct} duplicate OIDs"
    )


def test_references_nonempty_and_schema_intact(spec_ids):
    table = load_raw_parquet("aavso-vsx-references")
    assert table.num_rows >= 500_000, (
        f"aavso-vsx-references: {table.num_rows:,} rows, expected >=500k"
    )
    required = {"recno", "OID", "Bibcode"}
    missing = required - set(table.schema.names)
    assert not missing, f"aavso-vsx-references: missing columns {missing}"


def test_photometric_bands_nonempty_and_unique(spec_ids):
    import pyarrow.compute as pc

    table = load_raw_parquet("aavso-photometric-bands")
    assert table.num_rows >= 30, (
        f"aavso-photometric-bands: {table.num_rows:,} rows, expected >=30"
    )
    code = table.column("Code")
    assert code.null_count == 0, "aavso-photometric-bands: Code has nulls"
    distinct = pc.count_distinct(code).as_py()
    assert distinct == table.num_rows, (
        f"aavso-photometric-bands: {table.num_rows - distinct} duplicate Code values"
    )
