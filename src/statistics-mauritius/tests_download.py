from subsets_utils import load_raw_ndjson

_REQUIRED_INTERNAL_KEYS = {
    "__package_name",
    "__package_title",
    "__resource_id",
    "__resource_name",
    "__row_number",
}


def test_all_raw_assets_have_rows(spec_ids):
    for spec_id in _download_ids(spec_ids):
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: no rows loaded"


def test_internal_metadata_columns_present(spec_ids):
    for spec_id in _download_ids(spec_ids):
        first = load_raw_ndjson(spec_id)[0]
        missing = _REQUIRED_INTERNAL_KEYS - set(first)
        assert not missing, f"{spec_id}: missing internal metadata keys {missing}"


def test_source_columns_present(spec_ids):
    for spec_id in _download_ids(spec_ids):
        first = load_raw_ndjson(spec_id)[0]
        source_cols = [key for key in first if not key.startswith("__")]
        assert source_cols, f"{spec_id}: no source columns found"


def test_row_numbers_are_positive(spec_ids):
    for spec_id in _download_ids(spec_ids):
        for row in load_raw_ndjson(spec_id):
            row_number = row.get("__row_number")
            assert isinstance(row_number, int) and row_number >= 1, (
                f"{spec_id}: bad __row_number {row_number!r}"
            )
            break


def _download_ids(spec_ids):
    return [spec_id for spec_id in spec_ids if not spec_id.endswith("-transform")]
