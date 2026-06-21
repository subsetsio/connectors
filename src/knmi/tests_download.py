from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce rows. Empty payloads usually mean the
    open-data listing returned nothing (auth expired) or the file-name filter
    stopped matching after an upstream rename."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_matrix_assets_have_value(spec_ids):
    """Climate-normals matrices must yield at least some non-null values; an
    all-null column means the metric/period unpivot misread the layout."""
    for sid in spec_ids:
        if "climate-normals" not in sid:
            continue
        rows = load_raw_ndjson(sid)
        assert any(r.get("value") is not None for r in rows), \
            f"{sid}: every parsed value is null — matrix parse likely misaligned"
