"""Post-DAG health invariants for the FSA connector.

Each download node writes a long/cell-level parquet (one row per non-empty
spreadsheet cell). These tests catch silent degradation — empty payloads, a
resource whose format flipped to something unparseable, a dropped `value`
column — that mere file existence would miss.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "resource_id", "resource_name", "sheet",
    "row_idx", "col_idx", "value", "num_value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every package should yield at least one extracted cell. An empty raw
    asset means all of the package's spreadsheet resources failed to fetch or
    parse — usually a moved url or a format switch."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """Every asset carries the uniform long/cell schema."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert EXPECTED_COLS <= cols, f"{sid}: missing columns {EXPECTED_COLS - cols}"


def test_value_nonnull(spec_ids):
    """`value` is non-null by construction (only non-empty cells are emitted);
    a null here means the writer/schema drifted."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.column("value").null_count == 0, \
            f"{sid}: value column has nulls"
