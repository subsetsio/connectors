from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's raw ndjson should hold rows. An empty payload means the
    datastore resource was dropped, renamed, or the endpoint changed shape."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_raw_rows_have_columns(spec_ids):
    """Each row must be a non-empty mapping. A row that decoded to {} signals the
    key-cleaning step silently dropped every column."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows and len(rows[0]) > 0, f"{sid}: first raw row has no columns"
