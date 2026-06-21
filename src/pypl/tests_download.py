from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every index's raw parquet should hold many rows (months x countries x
    entities). An empty or tiny payload means the .js format changed or a
    country file 404'd silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: raw parquet has only {len(table)} rows"


def test_all_six_countries_present(spec_ids):
    """Each index must carry all six country slices; a missing one means a
    fetch dropped silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        countries = set(table.column("country").to_pylist())
        assert countries == {"All", "US", "GB", "DE", "FR", "IN"}, (
            f"{sid}: countries={sorted(countries)}"
        )


def test_shares_in_unit_range(spec_ids):
    """Shares are fractional search interest in [0, 1]."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        shares = table.column("share")
        assert pc.min(shares).as_py() >= 0.0, f"{sid}: negative share"
        assert pc.max(shares).as_py() <= 1.0, f"{sid}: share > 1"
