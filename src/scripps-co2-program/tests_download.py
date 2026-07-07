from subsets_utils import load_raw_ndjson


def test_all_downloads_have_rows(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no parsed source rows"


def test_all_downloads_have_multiple_source_files(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        files = {row.get("source_file") for row in rows if row.get("source_file")}
        assert files, f"{spec_id}: no source files recorded"


def test_required_provenance_fields_present(spec_ids):
    required = {
        "entity_id",
        "source_url",
        "source_file",
        "raw_row_number",
        "raw_fields_json",
        "columns_json",
    }
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        missing = required - set(rows[0])
        assert not missing, f"{spec_id}: first row missing provenance fields {sorted(missing)}"
