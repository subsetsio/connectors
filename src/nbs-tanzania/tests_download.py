from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download node must land rows. Empty raw usually means the Next.js
    buildId lookup or the _next/data corpus fetch silently returned a stub."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_indicators_cover_both_areas(spec_ids):
    """The indicators catalog must carry Mainland and Zanzibar; a single area
    means the corpus payload came back partial."""
    sid = "nbs-tanzania-indicators"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    areas = set(table.column("area").to_pylist())
    assert {"mainland", "zanzibar"} <= areas, f"{sid}: areas={areas}"
    assert len(table) >= 380, f"{sid}: only {len(table)} indicators (expected ~434)"


def test_values_have_years_and_units(spec_ids):
    """Observations must span multiple years and carry units — a collapse to a
    single year or all-null units signals an upstream shape change."""
    sid = "nbs-tanzania-values"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) >= 3000, f"{sid}: only {len(table)} value rows"
    years = [y for y in table.column("year").to_pylist() if y is not None]
    assert len(set(years)) >= 5, f"{sid}: only {len(set(years))} distinct years"
    units = [u for u in table.column("unit").to_pylist() if u]
    assert units, f"{sid}: no non-null units"
