from subsets_utils import load_raw_ndjson


def test_all_downloads_have_cells(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no parsed table cells"


def test_all_downloads_have_source_entity_ids(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [row for row in rows if not row.get("source_entity_id")]
        assert not missing, f"{spec_id}: {len(missing)} rows missing source_entity_id"
