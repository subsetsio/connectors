"""Health invariants for the Ember raw downloads.

Run post-DAG, in-connector, against the data through subsets_utils loaders.
Catches silent degradation (empty payload, truncated download, wrong format)
that mere file existence misses.
"""

from subsets_utils import load_raw_parquet

# Columns every Ember long-format raw asset must carry, regardless of scope.
_COMMON = {"Category", "Subcategory", "Variable", "Unit", "Value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Each download spec's raw parquet should hold rows. An empty payload
    usually means the static CSV moved or the endpoint changed format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_long_format_columns_present(spec_ids):
    """The long-format metric columns must survive the CSV parse — a header
    drift would silently strip them and produce a useless table."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _COMMON - cols
        assert not missing, f"{sid}: missing long-format columns {missing}"


def test_value_column_has_observations(spec_ids):
    """Value is the payload — if every Value is null the download is junk."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        non_null = len(table) - pc.sum(pc.is_null(table["Value"])).as_py()
        assert non_null > 0, f"{sid}: Value column is entirely null"
