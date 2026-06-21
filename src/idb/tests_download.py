"""Health-invariant tests run post-DAG inside the connector.

Catch silent degradation that file-existence alone misses: empty payloads,
a dropped provenance column, or a fetch that returned a header with no rows.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's raw parquet should hold at least one row. An empty
    payload usually means the datastore dump / file download silently returned
    nothing (auth flip, endpoint change, or a package that lost its data)."""
    empties = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} raw assets have 0 rows: {empties[:10]}"


def test_provenance_column_present(spec_ids):
    """Every published table carries the `source_resource` provenance column.
    Its absence means the schema assembly in fetch_one broke."""
    missing = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "source_resource" not in table.column_names:
            missing.append(sid)
    assert not missing, f"{len(missing)} raw assets missing source_resource: {missing[:10]}"
