"""Health-invariant tests run post-DAG, in-connector, after the download nodes.

Catch silent degradation that file existence alone misses: empty payloads,
truncated pulls, or the Socrata endpoint quietly switching format/auth.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every CDLE table holds rows. An empty parquet usually means the SODA
    endpoint changed format or started rejecting the request."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_tables_have_columns(spec_ids):
    """Each table carries several columns — guards against a degraded response
    that collapses to a single error/envelope field."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 3, (
            f"{sid}: only {table.num_columns} columns"
        )
