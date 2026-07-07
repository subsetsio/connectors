from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 0, f"{spec_id}: raw parquet has no rows"


def test_current_year_present(spec_ids):
    import datetime as dt

    current_year = dt.date.today().year
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        max_year = table.column("year").combine_chunks().to_pandas().max()
        assert max_year >= current_year - 1, f"{spec_id}: max year {max_year} is stale"


def test_expected_scale(spec_ids):
    minimums = {
        "scimago-journal-country-rank-country-rankings": 5000,
        "scimago-journal-country-rank-journal-rankings": 500000,
    }
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= minimums[spec_id], (
            f"{spec_id}: got {table.num_rows} rows, expected at least {minimums[spec_id]}"
        )
