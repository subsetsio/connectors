"""Health-invariant tests for statistics-poland raw download assets.

Run post-DAG inside the connector; they read raw through subsets_utils loaders,
so they behave identically locally and in the cloud.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "group_id", "subject_id", "variable_id", "variable_name",
    "n1", "n2", "n3", "n4", "n5", "measure_unit", "measure_unit_id",
    "year", "value", "attr_id",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every group's national series must hold rows. An empty payload means the
    subgroup/variable enumeration broke or the by-unit endpoint changed shape."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empty.append(sid)
    assert not empty, f"raw parquet empty for: {empty}"


def test_schema_columns(spec_ids):
    """Raw schema must carry the full BDL national-series column set."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_variable_id_populated(spec_ids):
    """variable_id is the join key to BDL's variable catalog; it must never be
    null in any national observation."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nulls = pc.sum(pc.is_null(table.column("variable_id"))).as_py() or 0
        assert nulls == 0, f"{sid}: {nulls} rows with null variable_id"
