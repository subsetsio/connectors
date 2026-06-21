"""Post-DAG health invariants for the FAO connector.

Reads parquet footers only (metadata, not the full table) so the check stays
memory-bounded even for the ~52M-row Detailed-trade-matrix domain.
"""

import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath


def test_all_raw_assets_nonempty(spec_ids):
    """Every FAOSTAT domain must produce a non-empty parquet. An empty payload
    means the ZIP changed layout, the Normalized member vanished, or the CSV
    parse silently dropped everything."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            md = pq.ParquetFile(path).metadata
            assert md.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present(spec_ids):
    """The transform keys off a `value` column on every domain; if a domain
    ever lacks it the published table would be meaningless."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            cols = pq.ParquetFile(path).schema.names
            assert "value" in cols, f"{sid}: no 'value' column (got {cols})"
