"""Health invariants run post-DAG, in-connector.

Raw assets here are gzip/plain CSV (or per-year batch files), not parquet, so we
check presence via the raw-file lister rather than a typed loader. An empty or
missing raw payload is the silent-degradation case we want to catch; a truncated
download that still has bytes is caught downstream by the transform's 0-row gate.
"""

from subsets_utils import list_raw_files


def test_every_spec_has_raw_files(spec_ids):
    """Each download spec must have produced at least one raw file — either a
    single `<id>.<ext>` or a `<id>-<batch>.<ext>` set."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*") or list_raw_files(f"{sid}-*")
        assert files, f"{sid}: no raw files were written"
