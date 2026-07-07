from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_raw_rows_preserve_source_values(spec_ids):
    for spec_id in spec_ids:
        sample = load_raw_ndjson(spec_id)[:20]
        assert sample, f"{spec_id}: no rows to inspect"
        for row in sample:
            assert row.get("entity_id"), f"{spec_id}: missing entity_id"
            assert row.get("resource_id"), f"{spec_id}: missing resource_id"
            assert isinstance(row.get("values"), dict), f"{spec_id}: values is not an object"
            assert row["values"], f"{spec_id}: empty values object"
