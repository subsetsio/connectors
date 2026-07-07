from subsets_utils import load_raw_parquet


def test_raw_summary_has_expected_shape(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= 6000, f"{spec_id}: expected at least 6000 country-year rows"
        assert table.num_columns == 14, f"{spec_id}: unexpected summary schema width"


def test_raw_summary_country_year_key(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        rows = table.select(["country", "year"]).to_pylist()
        keys = {(row["country"], row["year"]) for row in rows}
        assert len(keys) == len(rows), f"{spec_id}: duplicate country-year rows"
        assert len({row["country"] for row in rows}) >= 190, f"{spec_id}: too few countries"
