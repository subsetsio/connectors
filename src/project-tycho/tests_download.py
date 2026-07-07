"""Post-download health checks for Project Tycho raw parquet assets."""

from subsets_utils import load_raw_parquet


EXPECTED_COLUMNS = {
    "project-tycho-level-1-data": {
        "epi_week",
        "state",
        "loc",
        "loc_type",
        "disease",
        "cases",
        "incidence_per_100000",
    },
    "project-tycho-level-2-data": {
        "epi_week",
        "country",
        "state",
        "loc",
        "loc_type",
        "disease",
        "event",
        "number",
        "from_date",
        "to_date",
        "url",
    },
}


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has no rows"


def test_expected_columns(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        expected = EXPECTED_COLUMNS[spec_id]
        assert set(table.column_names) == expected, (
            f"{spec_id}: expected columns {sorted(expected)}, got {table.column_names}"
        )


def test_historical_row_counts(spec_ids):
    minimums = {
        "project-tycho-level-1-data": 700000,
        "project-tycho-level-2-data": 3000000,
    }
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= minimums[spec_id], (
            f"{spec_id}: got {table.num_rows} rows, expected at least {minimums[spec_id]}"
        )
