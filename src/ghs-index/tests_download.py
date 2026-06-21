from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. An empty payload means the
    CSV endpoint moved/changed format or the melt silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_scores_in_range(spec_ids):
    """GHS Index scores are normalised 0-100. Values outside that band mean the
    wrong column was read or a header/value misalignment in the melt."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("score")
        import pyarrow.compute as pc
        non_null = pc.drop_null(col)
        if len(non_null) == 0:
            continue
        lo = pc.min(non_null).as_py()
        hi = pc.max(non_null).as_py()
        assert lo >= 0 and hi <= 100, f"{sid}: score out of [0,100]: min={lo} max={hi}"


def test_both_years_present(spec_ids):
    """The 2021 release carries both the 2019 and 2021 assessments; missing one
    means the source file changed or rows were dropped."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("year").to_pylist())
        assert {2019, 2021}.issubset(years), f"{sid}: expected years 2019 & 2021, got {sorted(years)}"
