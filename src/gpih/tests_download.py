"""Health-invariant tests — run post-DAG, in-connector, against the raw assets.

Catch silent degradation the file-existence check misses: empty payloads (the
normalizer skipped every sheet, or the workbook 404'd to an HTML error page),
and missing the universal `__sheet__` tag every normalized record carries.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every workbook normalizes to >=1 record; 0 rows means the fetch produced
    no parseable sheet (format change, error page, or all-empty workbook)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_sheet_tag_present(spec_ids):
    """Every normalized record carries the __sheet__ provenance tag."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and "__sheet__" not in rows[0]:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets missing __sheet__: {bad[:10]}"
