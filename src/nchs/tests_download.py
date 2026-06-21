"""Health-invariant tests for the NCHS connector — run post-DAG, in-connector.

These catch silent degradation that file-existence alone misses: empty CSV
exports (auth/format switch), truncated downloads, or a raw asset that parsed
to zero columns.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every NCHS dataset export should hold rows. A 0-row table means the
    Socrata export endpoint changed format or the dataset was emptied."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_all_raw_assets_have_columns(spec_ids):
    """A parsed export with 0 columns means the CSV header was lost or the
    response body was not CSV at all."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets have 0 columns: {bad[:10]}"
