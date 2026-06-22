"""Health-invariant tests — run post-DAG, in-connector, via subsets_utils loaders."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every OGD dataset is a populated statistical cube; an empty raw asset
    means the CSV endpoint 404'd to HTML, switched format, or truncated."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_rows_have_columns(spec_ids):
    """A parsed row must carry at least one field; a row of all-None means the
    semicolon parse or column mapping silently collapsed."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not any(v is not None for v in rows[0].values()):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have all-null first rows: {bad[:10]}"
