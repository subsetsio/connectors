"""Health-invariant tests for Statistics Estonia raw assets.

Each download node melts a PxWeb table into long-format NDJSON rows, each
carrying a ``value`` field plus one column per dimension. These tests catch
silent degradation that file-existence alone misses: empty payloads (endpoint
changed format / error returned 200), or rows missing the measure column.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every melted table should hold at least one cell. An empty asset means
    the json-stat2 query returned no data (format switch or silent error)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty, e.g. {empty[:5]}"


def test_rows_have_value_and_dimension(spec_ids):
    """Each melted row must carry the 'value' measure plus at least one
    dimension column. A bare {'value': ...} means the melt lost its dimensions."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        r = rows[0]
        if "value" not in r or len(r) < 2:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have malformed rows, e.g. {bad[:5]}"
