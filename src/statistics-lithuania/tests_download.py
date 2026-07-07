from subsets_utils import load_raw_ndjson


def test_raw_assets_have_observations(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no observations saved"
        assert all(row.get("flow_id") for row in rows[:100]), f"{spec_id}: missing flow_id"
        assert any(row.get("period") for row in rows[:100]), f"{spec_id}: missing period values"
