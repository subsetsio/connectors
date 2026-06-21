"""Health-invariant tests run post-DAG, in-connector, through subsets_utils.

Each cube writes either a single parquet named exactly after its spec id (small
cubes) or a set of `<spec_id>-<batch>.parquet` files (large cubes partitioned to
dodge the server's 413 cap). These tests catch silent degradation that file
existence alone misses — an empty payload, a partition loop that wrote nothing.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def _raw_files(sid):
    return list_raw_files(f"{sid}.parquet") or list_raw_files(f"{sid}-*.parquet")


def test_every_spec_has_raw(spec_ids):
    for sid in spec_ids:
        assert _raw_files(sid), f"{sid}: no raw parquet written (single or batched)"


def test_raw_batches_nonempty(spec_ids):
    """The first raw batch of every cube must hold rows. An empty payload
    usually means the data endpoint changed shape or a partition silently
    returned only a header."""
    for sid in spec_ids:
        files = _raw_files(sid)
        assert files, f"{sid}: no raw parquet"
        asset = files[0][: -len(".parquet")]
        table = load_raw_parquet(asset)
        assert table.num_rows > 0, f"{sid}: raw batch {files[0]} has 0 rows"
