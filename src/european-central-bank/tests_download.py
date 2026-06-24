"""Health invariants for ECB raw downloads, run post-DAG inside the connector."""

import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath


def test_raw_has_records(spec_ids):
    """Every dataflow's raw Parquet must hold observations and carry the core
    SDMX columns. Reads only file metadata + schema (no data load) so it stays
    memory-bounded even for the multi-million-row flows (SHS, MMSR, SEC)."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            md = pq.read_metadata(path)
            cols = set(md.schema.names)
        assert md.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        missing = {"KEY", "TIME_PERIOD", "OBS_VALUE"} - cols
        assert not missing, f"{sid}: raw parquet missing SDMX columns {missing}"
