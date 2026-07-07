from subsets_utils import load_raw_ndjson


def test_all_raw_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_lmi_assets_have_sheet_coordinates(spec_ids):
    lmi_ids = [sid for sid in spec_ids if "-lmi-" in sid]
    assert lmi_ids, "expected at least one Texas LMI report asset"
    for spec_id in lmi_ids:
        rows = load_raw_ndjson(spec_id)
        sample = rows[0]
        for key in ("source_file", "sheet_name", "row_number"):
            assert key in sample, f"{spec_id}: missing {key} in parsed workbook rows"


def test_socrata_assets_preserve_fields(spec_ids):
    socrata_ids = [sid for sid in spec_ids if "-socrata-" in sid]
    assert socrata_ids, "expected at least one Socrata asset"
    for spec_id in socrata_ids:
        rows = load_raw_ndjson(spec_id)
        assert any(row for row in rows if len(row) >= 2), f"{spec_id}: Socrata rows look empty"
