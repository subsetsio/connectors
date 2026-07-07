"""Post-download invariants for UK Parliament raw assets."""

from subsets_utils import load_raw_ndjson


def test_all_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no rows saved"


def test_rows_keep_source_entity(spec_ids):
    for spec_id in spec_ids:
        expected = spec_id.removeprefix("uk-parliament-")
        rows = load_raw_ndjson(spec_id)
        bad = [row for row in rows[:100] if row.get("source_entity") != expected]
        assert not bad, f"{spec_id}: source_entity mismatch in first 100 rows"


def test_core_assets_have_reasonable_counts(spec_ids):
    floors = {
        "uk-parliament-members": 500,
        "uk-parliament-commons-votes": 1000,
        "uk-parliament-lords-votes": 1000,
        "uk-parliament-oral-questions-and-motions": 10000,
        "uk-parliament-written-questions-and-statements": 100000,
    }
    for spec_id, minimum in floors.items():
        if spec_id in spec_ids:
            rows = load_raw_ndjson(spec_id)
            assert len(rows) >= minimum, f"{spec_id}: {len(rows)} rows, expected >= {minimum}"
