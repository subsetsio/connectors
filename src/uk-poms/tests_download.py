"""Health-invariant tests for UK PoMS raw downloads."""

from subsets_utils import load_raw_parquet


_EXPECTED = {
    "uk-poms-ukpoms-1kmfitcountdata-2017-2022": {
        "min_rows": 1000,
        "columns": ["sample_id", "country", "date", "year", "all_insects_total"],
    },
    "uk-poms-ukpoms-publicfitcountdata-2017-2022": {
        "min_rows": 3000,
        "columns": ["sample_id", "country", "date", "year", "all_insects_total"],
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-flowers": {
        "min_rows": 1000,
        "columns": ["sample_id", "occurrence_id", "taxon_group", "family", "year"],
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-insects": {
        "min_rows": 1000,
        "columns": ["sample_id", "occurrence_id", "taxon_group", "count", "year"],
    },
    "uk-poms-ukpoms-1kmpantrapdata-2017-2022-samples": {
        "min_rows": 1000,
        "columns": ["sample_id", "country", "date", "year", "all_invertebrates_including_bees_hoverflies"],
    },
}


def test_expected_raw_tables_present(spec_ids):
    assert set(spec_ids) == set(_EXPECTED), f"unexpected spec ids: {sorted(spec_ids)}"


def test_raw_assets_have_expected_columns_and_rows(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        expected = _EXPECTED[spec_id]
        assert table.num_rows >= expected["min_rows"], f"{spec_id}: only {table.num_rows} rows"
        for column in expected["columns"]:
            assert column in table.column_names, f"{spec_id}: missing {column!r}"


def test_years_cover_current_release_window(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        years = {value for value in table.column("year").to_pylist() if value}
        assert "2017" in years and "2022" in years, f"{spec_id}: year coverage is {sorted(years)}"
