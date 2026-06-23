"""Post-DAG health invariants for OHSS raw assets.

Each download node parses one workbook sheet into NDJSON records. The dominant
silent-failure modes are: the Akamai TLS block returns (403 -> empty), the
point-in-time workbook URL rotated and the sheet vanished, or the sheet layout
changed and header detection produced nothing. All surface as empty/degenerate
raw, which these catch.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw NDJSON must hold rows. 0 rows means the fetch
    or the sheet parse silently degraded."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty: {empty[:10]}"


def test_rows_have_columns(spec_ids):
    """Each record should be a non-empty dict (parsed columns), not a scalar or
    an empty object — a sign the parser fell back to nothing useful."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not (isinstance(rows[0], dict) and len(rows[0]) >= 1):
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have rows without columns: {bad[:10]}"


def test_some_numeric_value_present(spec_ids):
    """These are statistical tables: across an asset's first rows there should
    be at least one numeric (float/int) cell. An all-text asset means value
    columns were misclassified or the wrong sheet was read."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[:50]
        has_num = any(
            isinstance(v, (int, float)) and not isinstance(v, bool)
            for r in sample if isinstance(r, dict)
            for v in r.values()
        )
        if sample and not has_num:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets carry no numeric values: {bad[:10]}"
