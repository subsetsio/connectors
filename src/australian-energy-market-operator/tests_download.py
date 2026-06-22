from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_schema(spec_ids):
    """Each spec's raw parquet must hold rows with the expected columns.
    An empty payload or a missing column usually means the source switched
    format or the URL pattern silently broke."""
    expected = {"region", "settlement_date", "total_demand", "rrp", "period_type"}
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"
        missing = expected - set(table.column_names)
        assert not missing, f"{sid}: missing columns {missing}"


def test_regions_present(spec_ids):
    """The live NEM regions should all appear — if one is absent, that
    region's whole month range failed to fetch."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        regions = set(table.column("region").to_pylist())
        for r in ("NSW1", "QLD1", "VIC1", "SA1", "TAS1"):
            assert r in regions, f"{sid}: region {r} absent from raw data"
