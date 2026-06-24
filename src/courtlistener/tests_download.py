"""Post-DAG health invariants for the CourtListener bulk connector.

Each download node streams one bulk CSV table into an all-string Parquet raw
asset. These checks catch silent degradation file-existence alone misses: an
empty/truncated download, or a payload that lost its header (so the `id` primary
key column vanished).

Reads are **metadata-only**: the biggest bulk tables (dockets ~7.6 GB,
opinion-clusters ~4 GB compressed) decompress to tens of GB as a materialized
Arrow table, so loading them just to count rows OOM-kills the runner. Instead we
open each parquet's footer over a range-capable filesystem and read the row
count and schema from the metadata — constant memory regardless of file size.
"""

import pyarrow.parquet as pq

from subsets_utils import get_fs
from subsets_utils.config import raw_uri


def _raw_meta(asset_id):
    """(num_rows, column_names) for a raw asset, read from the parquet footer
    only — no row data is materialized."""
    uri = raw_uri(asset_id, "parquet")
    if uri.startswith("s3://"):
        fs = get_fs(uri)
        with fs.open(uri, "rb") as fh:
            md = pq.ParquetFile(fh)
            return md.metadata.num_rows, list(md.schema_arrow.names)
    md = pq.ParquetFile(uri)
    return md.metadata.num_rows, list(md.schema_arrow.names)


def test_all_raw_assets_nonempty(spec_ids):
    """Every bulk table should hold rows. 0 rows means the S3 object was empty,
    the range/stream truncated, or the bz2 decode produced nothing."""
    for sid in spec_ids:
        num_rows, _ = _raw_meta(sid)
        assert num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_have_id(spec_ids):
    """Every CourtListener bulk table is keyed by an `id` column. Its absence
    means the CSV header was dropped or the columns shifted."""
    for sid in spec_ids:
        _, columns = _raw_meta(sid)
        assert "id" in columns, f"{sid}: missing 'id' column ({columns[:6]}...)"
