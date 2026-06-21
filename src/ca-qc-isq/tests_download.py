"""Health-invariant tests for ca-qc-isq raw assets.

Every spec publishes the same uniform long schema (row_idx, row_label,
col_label, value_raw, value_num). These tests catch silent degradation that
file-existence alone misses: empty payloads, a dropped column, or a parser that
emitted nothing but didn't raise.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"row_idx", "row_label", "col_label", "value_raw", "value_num"}


def test_all_raw_assets_nonempty(spec_ids):
    """Each table must melt to at least one cell row. 0 rows means the page
    layout changed or the data backend returned nothing."""
    empty = []
    for sid in spec_ids:
        if load_raw_parquet(sid).num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} assets have 0 rows, e.g. {empty[:5]}"


def test_schema_is_uniform(spec_ids):
    """Every asset carries the full long schema; a missing column means the
    melt/save path silently changed shape."""
    bad = []
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if not EXPECTED_COLS.issubset(cols):
            bad.append((sid, sorted(cols)))
    assert not bad, f"{len(bad)} assets missing expected columns, e.g. {bad[:3]}"


def test_value_num_not_entirely_null(spec_ids):
    """ISQ tables are statistical, so across the whole corpus the numeric column
    must be populated for the large majority of tables. A wholesale collapse to
    null means number parsing broke (e.g. separator handling)."""
    import pyarrow.compute as pc
    all_null = 0
    checked = 0
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            continue
        checked += 1
        nn = pc.sum(pc.is_valid(t.column("value_num"))).as_py() or 0
        if nn == 0:
            all_null += 1
    assert checked == 0 or all_null <= 0.2 * checked, (
        f"{all_null}/{checked} assets have an all-null value_num column; "
        "number parsing likely regressed"
    )
