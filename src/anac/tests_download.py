"""Health invariants for the ANAC raw downloads, run post-DAG in-connector.

Each subset's raw is a single line-delimited JSON file (`<spec_id>.ndjson.gz`).
The streaming read of the first line catches the common silent failures —
empty payload, truncated/format-switched download — without loading
potentially multi-GB assets (airfares, VRA) fully into memory.
"""
from subsets_utils import list_raw_files, raw_reader


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first_line = f.readline()
        assert first_line.strip(), f"{sid}: raw ndjson is empty"
