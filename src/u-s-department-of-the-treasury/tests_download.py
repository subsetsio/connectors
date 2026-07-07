from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has 0 rows"


def test_all_raw_assets_have_record_date(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert "record_date" in rows[0], f"{spec_id}: first row has no record_date"
