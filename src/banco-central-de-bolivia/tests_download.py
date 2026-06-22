"""Health-invariant tests for the BCB Boletin Estadistico connector.

Each download node writes a long cell-grid parquet (one row per populated
spreadsheet cell). These tests catch silent degradation that file-existence
alone misses: empty/truncated payloads, a table that parsed to nothing, or a
schema that switched format.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every BCB bulletin table has many populated cells; an empty or tiny raw
    asset means the xlsx fetch/parse degraded (wrong URL, format switch)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 5, f"{sid}: raw parquet has {len(table)} cells (<5)"


def test_schema_stable(spec_ids):
    """The cell-grid schema is fixed; a missing column means the writer changed."""
    expected = {"table_code", "sheet", "row", "col", "value_num", "value_text"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"


def test_has_numeric_cells(spec_ids):
    """These are statistical tables — every one must carry at least some numeric
    values, not only text labels. All-text means the numeric grid was lost."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        non_null = pc.sum(pc.is_valid(table.column("value_num"))).as_py()
        assert non_null and non_null > 0, f"{sid}: no numeric cells parsed"
