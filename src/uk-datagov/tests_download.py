from subsets_utils import load_raw_ndjson


def test_all_downloads_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: expected non-empty raw rows"


def test_pxstat_core_columns_present(spec_ids):
    expected = {"STATISTIC", "Statistic Label", "UNIT", "VALUE"}
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = expected - set(rows[0])
        assert not missing, f"{spec_id}: missing expected columns {sorted(missing)}"


def test_values_are_populated(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        populated = [row for row in rows if str(row.get("VALUE") or "").strip()]
        assert len(populated) >= 10, f"{spec_id}: too few populated VALUE rows"
