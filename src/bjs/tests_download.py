"""Health invariants for BJS raw downloads.

Raw is streamed NDJSON (gzip), some assets running to millions of rows, so we
check liveness through the manifest-backed reader without loading whole files
into memory: every spec must resolve to raw, and its first line must be a
non-empty JSON object. This catches the silent-degradation failures file
existence alone misses: empty payloads, a format switch, or a truncated-to-zero
download.
"""

import json

from subsets_utils import raw_reader


def test_raw_assets_present_and_nonempty(spec_ids):
    for sid in spec_ids:
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first = f.readline()

        assert first.strip(), f"{sid}: raw NDJSON is empty"
        row = json.loads(first)
        assert isinstance(row, dict) and row, (
            f"{sid}: first record is not a non-empty JSON object"
        )
