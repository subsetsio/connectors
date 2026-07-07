from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_rows_carry_source_metadata(spec_ids):
    required = {"_entity_id", "_rfmo", "_source_url", "_source_file"}
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = required.difference(rows[0])
        assert not missing, f"{spec_id}: first row missing metadata columns {sorted(missing)}"
