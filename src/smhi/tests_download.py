from subsets_utils import load_raw_ndjson


def test_all_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no rows written"


def test_observation_assets_have_required_keys(spec_ids):
    required = {"family_id", "parameter_key", "station_key", "period_key", "date", "value"}
    for spec_id in spec_ids:
        if not spec_id.endswith("-observations"):
            continue
        sample = load_raw_ndjson(spec_id)[:100]
        missing = [row for row in sample if not required.issubset(row)]
        assert not missing, f"{spec_id}: observation sample missing required keys"
