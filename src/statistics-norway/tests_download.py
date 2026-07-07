from subsets_utils import load_raw_json


def test_raw_jsonstat_payloads_nonempty(spec_ids):
    for spec_id in spec_ids:
        payload = load_raw_json(spec_id)
        assert payload.get("table_id"), f"{spec_id}: missing table_id"
        assert payload.get("metadata", {}).get("id"), f"{spec_id}: missing dimensions"
        assert payload.get("data", {}).get("value"), f"{spec_id}: missing values"
