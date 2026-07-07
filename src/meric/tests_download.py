"""Download health checks for MERIC raw NDJSON assets."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has 0 rows"


def test_all_rows_have_source_metadata(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        for i, row in enumerate(rows[:25]):
            assert row.get("_entity_id"), f"{spec_id} row {i}: missing _entity_id"
            assert row.get("_source_url"), f"{spec_id} row {i}: missing _source_url"
            assert row.get("_row_index") is not None, (
                f"{spec_id} row {i}: missing _row_index"
            )
