"""Health-invariant tests for the Datos.PR connector, run post-DAG in-connector.

Each download node normalizes one CKAN package's tabular resources into a single
parquet with two provenance columns plus the package's own (all-string) columns.
These tests catch silent degradation that file-existence alone misses: empty
payloads, lost provenance columns, or a format change that drops all rows.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every package must yield at least one tabular row. Empty usually means
    the endpoint switched format, the TLS trust broke, or every resource became
    non-tabular."""
    empties = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} assets have 0 rows: {empties[:10]}"


def test_provenance_columns_present(spec_ids):
    """Both discriminator columns must exist on every asset — they are written
    by construction, so their absence means the writer path changed."""
    missing = []
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if not {"source_resource", "source_file"} <= cols:
            missing.append(sid)
    assert not missing, f"{len(missing)} assets missing provenance columns: {missing[:10]}"
