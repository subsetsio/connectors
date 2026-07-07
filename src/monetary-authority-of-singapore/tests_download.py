"""Post-download invariants for MAS data.gov.sg raw assets."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_rows_have_source_resource_id(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [row for row in rows[:50] if not row.get("source_resource_id")]
        assert not missing, f"{spec_id}: missing source_resource_id in sample"


def test_rows_have_datastore_ids(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = [row for row in rows[:50] if row.get("_id") is None]
        assert not missing, f"{spec_id}: missing datastore _id in sample"
