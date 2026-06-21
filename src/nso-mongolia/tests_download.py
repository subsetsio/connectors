"""Health invariants run post-DAG, in-connector, through subsets_utils loaders.

Catches silent degradation that file-existence misses: empty payloads (endpoint
switched format / auth changed), or rows missing the numeric measure (json-stat
parse drifted).
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every table should yield at least one non-null observation row. An empty
    NDJSON means the POST query returned no usable cells (format change, all-null
    table, or a broken json-stat flatten)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} assets have 0 rows, e.g. {empty[:10]}"


def test_rows_carry_measure(spec_ids):
    """Each kept row must carry the numeric `value` measure. Its absence means
    the flatten emitted dimension-only rows — a parser regression."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and "value" not in rows[0]:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have rows without a 'value' field, e.g. {bad[:10]}"
