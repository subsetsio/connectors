"""Health invariants for the Lichess raw downloads.

Catches silent degradation that file existence alone misses: a truncated or
empty download of the puzzle CSV.
"""

from subsets_utils import load_raw_file


def test_puzzle_download_substantial(spec_ids):
    """The puzzle export is ~300MB compressed. A drastically smaller payload
    means a truncated/aborted download or an endpoint format switch."""
    for sid in spec_ids:
        data = load_raw_file(sid, extension="csv.zst", binary=True)
        assert len(data) > 50_000_000, (
            f"{sid}: raw csv.zst is only {len(data)} bytes; expected ~300MB"
        )
