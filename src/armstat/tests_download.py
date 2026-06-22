"""Health invariants for the armstat download nodes, run post-DAG in-connector."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw NDJSON should hold at least one cell. An empty payload
    means the PX-Web select-all/export flow silently returned nothing (selection
    not stored, session/cookie lost, or the table page changed shape)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty, e.g. {empty[:10]}"


def test_rows_have_value_column(spec_ids):
    """Every decoded cell must carry the reserved measure column `value` plus at
    least one dimension column; otherwise JSON-stat decoding produced garbage."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        cols = set(rows[0].keys())
        if "value" not in cols or len(cols) < 2:
            bad.append((sid, sorted(cols)))
    assert not bad, f"{len(bad)} assets missing value/dimension columns, e.g. {bad[:5]}"
