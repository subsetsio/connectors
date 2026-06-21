"""Health-invariant tests for the Google connector raw downloads.

Run post-DAG inside the connector. They guard against silent degradation of
the mobility CSV fetch — truncated downloads, an empty payload, or a changed
column set.
"""

from subsets_utils import load_raw_parquet

ASSET = "google-community-mobility-reports"

EXPECTED_COLUMNS = {
    "country_region_code",
    "country_region",
    "sub_region_1",
    "sub_region_2",
    "metro_area",
    "iso_3166_2_code",
    "census_fips_code",
    "place_id",
    "date",
    "retail_and_recreation_percent_change_from_baseline",
    "grocery_and_pharmacy_percent_change_from_baseline",
    "parks_percent_change_from_baseline",
    "transit_stations_percent_change_from_baseline",
    "workplaces_percent_change_from_baseline",
    "residential_percent_change_from_baseline",
}


def test_mobility_columns_present():
    """The CSV header is stable; a missing/renamed column means the source
    changed format and the transform would break."""
    table = load_raw_parquet(ASSET)
    cols = set(table.column_names)
    assert EXPECTED_COLUMNS <= cols, f"{ASSET}: missing columns {EXPECTED_COLUMNS - cols}"


def test_mobility_row_count_full():
    """The full global report is ~11.7M rows (verified: the uncompressed CSV
    has 11,730,026 lines). A truncated download (the classic silent failure,
    e.g. a gzip stream cut short) lands in the thousands/low-millions — this
    floor sits well above any truncation but below the real count with margin
    for the frozen source never shrinking."""
    table = load_raw_parquet(ASSET)
    assert table.num_rows >= 10_000_000, (
        f"{ASSET}: only {table.num_rows} rows — download likely truncated"
    )


def test_mobility_has_country_and_dates():
    """Country codes and dates must be populated — an all-empty key column
    means the parse silently misaligned."""
    table = load_raw_parquet(ASSET)
    sample = table.slice(0, 1000).to_pydict()
    assert any(v for v in sample["country_region_code"]), "country_region_code all empty"
    assert all(d for d in sample["date"]), "date column has empty values in first 1000 rows"
