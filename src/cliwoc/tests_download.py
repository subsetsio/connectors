from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "logbook_id",
    "record_date",
    "year",
    "month",
    "day",
    "latitude",
    "longitude",
    "ship_name",
    "nationality",
    "ship_type",
    "company",
    "voyage_from",
    "voyage_to",
    "logbook_language",
    "wind_direction",
    "wind_force",
    "weather",
    "precipitation",
    "archive_institution",
}


def test_raw_nonempty_and_complete(spec_ids):
    """The whole CLIWOC corpus ships in one file; a short read or a changed
    layout shows up as too few rows or missing columns."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 250000, f"{sid}: only {len(table)} rows, expected ~287k"
        missing = EXPECTED_COLUMNS - set(table.column_names)
        assert not missing, f"{sid}: missing columns {missing}"


def test_positions_present(spec_ids):
    """Position is the spine of the dataset; if the latitude column silently
    went all-null the parse misaligned."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        lat = table.column("latitude")
        non_null = len(lat) - lat.null_count
        assert non_null > len(table) // 2, (
            f"{sid}: only {non_null}/{len(table)} rows have a latitude"
        )
