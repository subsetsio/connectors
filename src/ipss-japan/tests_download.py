"""Health invariants for the IPSS-Japan (JMD) raw downloads.

These run post-DAG inside the connector and load raw via subsets_utils, so a
silent degradation (endpoint switched format, truncated file, only All-Japan
fetched) trips a test rather than publishing thin tables.
"""

from subsets_utils import load_raw_parquet

# Expected row floors are deliberately conservative: ~78 years x ~111 ages x
# 48 areas (x 3 sexes for life tables) is ~1.2M; even a partial corpus should
# clear these. They mainly catch "only one area came back" / "header parse ate
# everything" regressions.
_MIN_ROWS = {
    "ipss-japan-jmd-life-tables": 500_000,
    "ipss-japan-jmd-deaths": 150_000,
    "ipss-japan-jmd-population": 150_000,
    "ipss-japan-jmd-exposures": 150_000,
    "ipss-japan-jmd-death-rates": 150_000,
    "ipss-japan-jmd-life-expectancy": 2_000,
    "ipss-japan-jmd-age-standardized-death-rates": 50_000,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_row_floors(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        table = load_raw_parquet(sid)
        assert len(table) >= floor, (
            f"{sid}: {len(table)} rows < expected floor {floor} "
            "(likely only a subset of the 48 areas was fetched)"
        )


def test_multi_area_coverage(spec_ids):
    """Every measure must span many areas (All Japan + prefectures), not just
    one. Catches a silent collapse to code 00 only."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        areas = set(table.column("area").to_pylist())
        assert len(areas) >= 40, (
            f"{sid}: only {len(areas)} distinct areas; expected ~48"
        )


def test_year_range_plausible(spec_ids):
    """Years should sit in the documented 1947-present window."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = [y for y in table.column("year").to_pylist() if y is not None]
        assert years, f"{sid}: no non-null years"
        assert min(years) <= 1960, f"{sid}: earliest year {min(years)} too late"
        assert max(years) >= 2018, f"{sid}: latest year {max(years)} too early"
        assert 1900 <= min(years) and max(years) <= 2100, (
            f"{sid}: year range {min(years)}-{max(years)} implausible"
        )
