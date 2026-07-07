from subsets_utils import load_raw_ndjson


def test_all_raw_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_all_raw_assets_include_source_file(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [i for i, row in enumerate(rows[:100]) if not row.get("source_file")]
        assert not missing, f"{spec_id}: sampled rows missing source_file"


def test_all_raw_assets_include_row_number(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [i for i, row in enumerate(rows[:100]) if row.get("row_number") is None]
        assert not missing, f"{spec_id}: sampled rows missing row_number"
