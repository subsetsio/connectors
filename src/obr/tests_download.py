"""Post-DAG health invariants for the OBR connector.

These catch silent degradation that a file-existence check misses: a workbook
that downloaded but parsed to nothing, a melt that lost the value columns, or a
product whose /data/ slug stopped resolving (the spec would then fail outright,
but a partial corpus is the subtler failure these guard).
"""

from subsets_utils import load_raw_parquet

# value_num is genuinely all-null for the qualitative policy-risks workbook, so
# the "has numeric values" invariant is asserted on the rest only.
_TEXT_ONLY = {"obr-policy-risks-database"}

_EXPECTED_COLS = {
    "sheet", "excel_row", "excel_col", "row_label", "col_label",
    "value_num", "value_text",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every melted workbook must hold cells. 0 rows means the download
    returned the wrong bytes (HTML error page, ZIP instead of XLSX) or the
    melt silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: melted parquet has 0 rows"


def test_schema_stable(spec_ids):
    """Every product must carry the full melt schema — a missing column means
    the parser drifted."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {sorted(missing)}"


def test_numeric_products_have_values(spec_ids):
    """Numeric workbooks must yield real numbers. If value_num is entirely null
    on, say, the public finances databank, the melt dropped the data band."""
    for sid in spec_ids:
        if sid in _TEXT_ONLY:
            continue
        table = load_raw_parquet(sid)
        nonnull = table.column("value_num").null_count
        total = len(table)
        assert total - nonnull > 0, f"{sid}: value_num is entirely null ({total} rows)"
