from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has 0 rows"


def test_rows_keep_source_identity(spec_ids):
    for spec_id in spec_ids:
        sample = load_raw_ndjson(spec_id)[:5]
        assert sample, f"{spec_id}: no sample rows"
        for row in sample:
            assert row.get("_source_type_name"), f"{spec_id}: missing _source_type_name"
            assert row.get("_feature_id"), f"{spec_id}: missing _feature_id"
