from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty payloads mean the NCEI
    file moved, changed format, or the fixed-width parse silently dropped everything."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_regions_is_27(spec_ids):
    """The database is fixed at 27 regional composite series — no more, no less."""
    sid = "grape-harvest-dates-regions"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) == 27, f"{sid}: expected 27 regions, got {len(table)}"
    codes = table.column("region_code").to_pylist()
    assert len(set(codes)) == 27, f"{sid}: region codes not unique: {codes}"


def test_harvest_dates_shape(spec_ids):
    """Burgundy (Bur) is the longest series and reaches back to 1354 — the most
    ancient harvest date in the dataset. If the oldest year drifts forward or
    the row count collapses, the column-alignment parse broke."""
    sid = "grape-harvest-dates-harvest-dates"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) > 4000, f"{sid}: only {len(table)} observations; parse likely degraded"
    years = table.column("year").to_pylist()
    assert min(years) == 1354, f"{sid}: oldest year {min(years)}, expected 1354 (Burgundy)"
    codes = set(table.column("region_code").to_pylist())
    assert codes == set(load_raw_parquet("grape-harvest-dates-regions").column("region_code").to_pylist()), \
        f"{sid}: harvest-date region codes do not match the regions table"
