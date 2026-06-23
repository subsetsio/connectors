from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "id", "obs_type", "latitude", "longitude", "elevation_m",
    "local_date", "local_time", "ut_date", "ut_time", "limiting_mag",
    "sqm_reading", "sqm_serial", "cloud_cover", "constellation",
    "sky_comment", "location_comment", "country", "file_year",
}


def test_raw_nonempty(spec_ids):
    """The observations raw asset should hold many rows. An empty/tiny payload
    means the maps-data scrape found no CSV links or the CSVs changed format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 150000, f"{sid}: only {len(table)} rows (expected >150k)"


def test_raw_schema(spec_ids):
    """Column set must match what the transform reads back; a drift here means
    a source header change slipped through silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == EXPECTED_COLUMNS, (
            f"{sid}: columns {set(table.column_names)} != {EXPECTED_COLUMNS}"
        )


def test_multiple_years(spec_ids):
    """Corpus must span many years; collapse to one year means the year-discovery
    scrape regressed to a single link."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("file_year").to_pylist())
        assert len(years) >= 18, f"{sid}: only {len(years)} distinct years: {sorted(years)}"
