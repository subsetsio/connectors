"""Health-invariant tests for the Guangdong yearbook connector.

Each download node melts one yearbook table's .xls files into a long-format
parquet. These checks catch silent degradation (empty payloads, format change,
the server returning an HTML error page instead of an .xls) that file existence
alone misses.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "table_id", "part", "row_pos", "col_pos",
    "row_label_cn", "row_label_en", "column_header",
    "value_num", "value_str",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table should melt to at least one data cell. Empty usually means
    the .xls 404'd (HTML error page) or the workbook was truncated."""
    empty = []
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if len(t) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_schema_stable(spec_ids):
    """Every raw asset must carry the full melt schema; a missing column means
    the parser silently changed shape."""
    bad = []
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if not EXPECTED_COLS.issubset(cols):
            bad.append((sid, sorted(EXPECTED_COLS - cols)))
    assert not bad, f"raw assets missing columns: {bad[:5]}"


def test_some_numeric_values(spec_ids):
    """Across the corpus, the vast majority of tables must contain numeric
    values. If almost none do, numeric parsing broke."""
    import pyarrow.compute as pc
    with_num = 0
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value_num")
        if pc.sum(pc.is_valid(col)).as_py() > 0:
            with_num += 1
    frac = with_num / max(len(spec_ids), 1)
    assert frac >= 0.9, f"only {with_num}/{len(spec_ids)} tables have numeric values"
