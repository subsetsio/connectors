from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty payloads usually mean
    the GitHub URL moved (master->main, file rename) or the CSV format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_key_columns_present_and_typed(spec_ids):
    """Every Big Mac asset carries date + iso_a3 (the natural key) and a
    currency_code. If a header drifted these go missing silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        names = set(table.schema.names)
        for col in ("date", "iso_a3", "currency_code", "local_price"):
            assert col in names, f"{sid}: missing column {col} (have {sorted(names)})"
