from subsets_utils import load_raw_ndjson


def test_raw_assets_have_source_and_cell_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON is empty"
        record_types = {row.get("record_type") for row in rows}
        assert "source" in record_types, f"{spec_id}: missing source coverage rows"
        assert "cell" in record_types, f"{spec_id}: missing parsed tabular cell rows"


def test_glacier_lengths_expected_source_count(spec_ids):
    if "pangaea-glacierlengthsaustria" not in spec_ids:
        return
    rows = load_raw_ndjson("pangaea-glacierlengthsaustria")
    source_dois = {
        row.get("source_doi")
        for row in rows
        if row.get("record_type") == "source" and row.get("source_doi")
    }
    assert len(source_dois) == 69, (
        "pangaea-glacierlengthsaustria: expected 69 source DOIs from OAI set "
        f"GlacierLengthsAustria, got {len(source_dois)}"
    )


def test_cell_rows_have_core_fields(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        cell_rows = [row for row in rows if row.get("record_type") == "cell"]
        missing = [
            row
            for row in cell_rows[:1000]
            if not row.get("dataset_doi")
            or not row.get("file_name")
            or not row.get("column_name")
            or row.get("source_row_number") is None
        ]
        assert not missing, f"{spec_id}: sampled cell rows are missing core fields"
