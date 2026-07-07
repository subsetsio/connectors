from subsets_utils import load_raw_ndjson


def test_all_raw_assets_have_chunks(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no raw chunks saved"


def test_chunk_payloads_are_jsonstat(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        for row in rows:
            payload = row.get("payload") or {}
            assert payload.get("class") == "dataset", (
                f"{spec_id}: chunk {row.get('chunk_index')} is not a JSON-stat dataset"
            )
            assert "value" in payload, (
                f"{spec_id}: chunk {row.get('chunk_index')} has no value array"
            )


def test_first_chunk_carries_metadata(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        first = min(rows, key=lambda row: row.get("chunk_index", 0))
        metadata = first.get("metadata") or {}
        assert metadata.get("id"), f"{spec_id}: first chunk missing metadata ids"
        assert metadata.get("dimension"), f"{spec_id}: first chunk missing dimensions"
