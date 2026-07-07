from subsets_utils import load_raw_ndjson


def test_all_downloads_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no raw rows"


def test_all_rows_have_source_table_code(spec_ids):
    for spec_id in spec_ids:
        expected = spec_id.removeprefix("statistisches-landesamt-sachsen-anhalt-")
        rows = load_raw_ndjson(spec_id)
        bad = [row for row in rows[:100] if row.get("source_table_code") != expected]
        assert not bad, f"{spec_id}: rows are missing expected source_table_code"
