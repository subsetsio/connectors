from subsets_utils import load_raw_ndjson


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"
        first = rows[0]
        assert first.get("table_id"), f"{spec_id}: missing table_id"
        assert first.get("dimension_codes"), f"{spec_id}: missing dimension_codes"
        assert "value" in first, f"{spec_id}: missing value"
