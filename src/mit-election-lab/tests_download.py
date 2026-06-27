"""Health-invariant tests for mit-election-lab raw assets.

Each download node writes one-or-more ndjson.gz batches named `<spec_id>-NNNN`.
A truncated/empty download or a silently-changed endpoint shows up as missing
batch files, which the transform's 0-row gate would otherwise surface only later.
"""

from subsets_utils import list_raw_files


def test_every_spec_wrote_batches(spec_ids):
    for sid in spec_ids:
        matches = list_raw_files(f"{sid}-*") or list_raw_files(f"{sid}.*")
        assert matches, f"{sid}: no raw ndjson batch written"


def test_batches_are_ndjson(spec_ids):
    for sid in spec_ids:
        matches = list_raw_files(f"{sid}-*")
        for rel in matches:
            assert ".ndjson" in rel.lower(), f"{sid}: unexpected raw file {rel}"
