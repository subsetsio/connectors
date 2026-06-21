from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"location", "timeframe", "col_index", "metric", "value_raw", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator's raw parquet must hold rows. An empty payload means the
    page format changed or the llm-data block disappeared."""
    empties = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} assets have 0 rows: {empties[:10]}"


def test_schema_shape(spec_ids):
    """Long-format schema must be intact and locations/timeframes populated."""
    for sid in spec_ids[:50]:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert _EXPECTED_COLS <= cols, f"{sid}: missing columns {_EXPECTED_COLS - cols}"
        locs = table.column("location").to_pylist()
        assert all(l for l in locs), f"{sid}: blank location values"
        tfs = set(table.column("timeframe").to_pylist())
        assert tfs and all(t for t in tfs), f"{sid}: blank/empty timeframe"


def test_some_numeric_values(spec_ids):
    """Across the corpus, the parser must extract real numbers — if `value` is
    100% null everywhere the number cleaner silently broke."""
    total = 0
    non_null = 0
    for sid in spec_ids[:80]:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        total += len(vals)
        non_null += sum(1 for v in vals if v is not None)
    assert total > 0, "no rows sampled"
    assert non_null > 0.3 * total, (
        f"only {non_null}/{total} sampled values are numeric; cleaner may be broken")
