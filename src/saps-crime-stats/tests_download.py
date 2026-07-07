from subsets_utils import load_raw_parquet


def test_crime_statistics_raw_nonempty(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows >= 250_000, f"{spec_id}: expected substantial raw rows, got {table.num_rows}"


def test_crime_statistics_release_coverage(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        workbooks = table.column("source_workbook").unique()
        assert len(workbooks) >= 20, f"{spec_id}: expected at least 20 source workbooks, got {len(workbooks)}"


def test_crime_statistics_core_columns_populated(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        for col in ("station", "province", "crime_category", "crime_code"):
            nulls = table.column(col).null_count
            assert nulls == 0, f"{spec_id}: {col} has {nulls} nulls"
