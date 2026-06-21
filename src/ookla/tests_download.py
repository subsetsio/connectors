"""Health-invariant tests for the Ookla connector.

Raw is written as one batch parquet per (type, year, quarter) partition, named
`ookla-performance-<type>-<year>-q<quarter>`. These tests assert the batch set
materialized and holds real rows — catching a silently truncated download or a
broken S3 listing that file-existence alone would miss.
"""

import pyarrow.parquet as pq

from subsets_utils import list_raw_files
from subsets_utils.io import raw_uri, get_fs


def _batch_files():
    return list_raw_files("ookla-performance-*.parquet")


def test_partition_batches_present():
    """The firehose should write dozens of partition batches (2 types x many
    quarters). A handful means the S3 listing broke after the first prefix."""
    files = _batch_files()
    assert len(files) >= 40, f"only {len(files)} partition batches written; expected >=40"


def test_both_connection_types_present():
    files = _batch_files()
    has_fixed = any("-fixed-" in f for f in files)
    has_mobile = any("-mobile-" in f for f in files)
    assert has_fixed and has_mobile, f"missing a connection type among batches: {files[:5]}"


def test_batches_nonempty():
    """Each partition batch must hold rows; an empty file means the endpoint
    switched format or returned a truncated body."""
    probe = raw_uri("__probe__", "__")
    base_uri = probe.rsplit("/", 1)[0]
    fs = get_fs(base_uri)
    for rel in _batch_files()[:5]:
        uri = f"{base_uri}/{rel}"
        with fs.open(uri, "rb") as fh:
            n = pq.ParquetFile(fh).metadata.num_rows
        assert n > 0, f"{rel}: raw parquet has 0 rows"
