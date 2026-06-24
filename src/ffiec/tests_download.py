"""Health invariants for the FFIEC HMDA raw assets.

Each download node writes one parquet batch per year (``ffiec-<ds>-<year>``),
globbed by the runtime as ``ffiec-<ds>-*``. These tests catch silent
degradation the structural checks miss: a node that produced no year batches,
batches with zero rows, or files missing the columns every transform depends on.
Row counts are read from parquet metadata (via a local path) so the multi-
million-row LAR files are never materialized into memory.
"""

import pyarrow.parquet as pq

from subsets_utils import list_raw_files, raw_parquet_localpath


def _asset_ids(spec_id):
    """Batch asset ids (e.g. ffiec-lar-2018) for one download spec."""
    ids = []
    for rel in sorted(list_raw_files(f"{spec_id}-*")):
        name = rel.rsplit("/", 1)[-1]
        if name.endswith(".parquet"):
            ids.append(name[: -len(".parquet")])
    return ids


def test_every_spec_has_year_batches(spec_ids):
    """Each download node must have produced at least one per-year parquet batch."""
    for sid in spec_ids:
        assets = _asset_ids(sid)
        assert assets, f"{sid}: no per-year parquet batches (ffiec-...-<year>.parquet) found"


def test_batches_nonempty_with_key_columns(spec_ids):
    """Every batch must carry rows and the key columns the transforms read."""
    for sid in spec_ids:
        total_rows = 0
        for asset in _asset_ids(sid):
            with raw_parquet_localpath(asset) as path:
                md = pq.ParquetFile(path)
                names = set(md.schema_arrow.names)
                assert "activity_year" in names, f"{asset}: missing activity_year column"
                assert "lei" in names, f"{asset}: missing lei column"
                total_rows += md.metadata.num_rows
        assert total_rows > 0, f"{sid}: all year batches are empty"
