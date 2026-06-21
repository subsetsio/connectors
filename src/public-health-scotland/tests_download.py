"""Health-invariant tests for Public Health Scotland raw assets.

Each download node writes one parquet per CKAN package, unioned across its CSV
resources. These catch silent degradation file-existence alone misses.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's raw parquet should hold rows. 0 rows usually means the
    datastore dump returned an error page or the resource list went empty."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_resource_columns_present(spec_ids):
    """We always tag each row with the resource it came from. Missing columns
    means the union/schema construction broke."""
    for sid in spec_ids:
        cols = load_raw_parquet(sid).column_names
        for c in ("resource_id", "resource_name"):
            assert c in cols, f"{sid}: missing tag column {c!r}"


def test_resource_name_populated(spec_ids):
    """resource_name is set by us for every row; a null means a row slipped
    through without being tagged (logic bug)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nulls = table.column("resource_name").null_count
        assert nulls == 0, f"{sid}: {nulls} rows have null resource_name"
