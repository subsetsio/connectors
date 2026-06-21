from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "table_id", "series_cod", "series_name", "unit_id", "scale_id",
    "period_id", "data_type_id", "year", "date", "value", "secret",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw parquet should hold rows. Empty payloads usually mean
    DATOS_TABLA changed shape or returned an error envelope silently."""
    empty = []
    for sid in spec_ids:
        if len(load_raw_parquet(sid)) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets empty, e.g. {empty[:10]}"


def test_schema_stable(spec_ids):
    """Raw parquet must carry the long-format INE schema. A missing column
    means the flattening logic or upstream payload changed."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"
