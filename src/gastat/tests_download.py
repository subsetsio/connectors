from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every GASTAT table should return rows. An empty NDJSON asset means the
    CData endpoint returned an error envelope, switched format, or the table
    was retired upstream — all silent-degradation modes file existence misses."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if len(rows) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_assets_have_columns(spec_ids):
    """A parsed CSV row must carry at least one column. Zero-key rows indicate
    the CSV header failed to parse (e.g. an HTML/JSON error body slipped through)."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not any(r for r in rows[:1] if r):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have keyless rows: {bad[:10]}"
