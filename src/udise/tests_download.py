from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_report_metadata_columns_present(spec_ids):
    for spec_id in spec_ids:
        row = load_raw_ndjson(spec_id)[0]
        for col in ("_udise_report_code", "_udise_report_id", "_udise_year_id"):
            assert col in row, f"{spec_id}: missing {col}"
