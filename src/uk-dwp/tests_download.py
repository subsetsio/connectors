"""Post-DAG health invariants for the uk-dwp connector.

These run in-connector after the download nodes, loading raw through the same
subsets_utils loader the fetch fn used to save it.
"""
from subsets_utils import load_raw_parquet

PROV = {"resource_name", "resource_id", "resource_last_modified", "source_url", "row_index"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's unioned parquet must hold rows. Zero rows means the CSV
    parsing silently produced nothing (encoding/delimiter/header regression)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_provenance_columns_present(spec_ids):
    """Every asset must carry the provenance columns we attach per row; their
    absence means the schema-construction path changed."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = PROV - cols
        assert not missing, f"{sid}: missing provenance columns {missing}"


def test_has_data_columns_beyond_provenance(spec_ids):
    """Each package must contribute at least one real (non-provenance) column;
    otherwise we only captured bookkeeping and dropped the actual CSV content."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        data_cols = cols - PROV
        assert data_cols, f"{sid}: no data columns beyond provenance"


def test_source_url_populated(spec_ids):
    """source_url is set on every row; a null here means a row was emitted
    outside the per-resource loop."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nulls = table.column("source_url").null_count
        assert nulls == 0, f"{sid}: {nulls} rows have null source_url"
