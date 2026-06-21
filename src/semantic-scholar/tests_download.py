"""Health invariants for the Semantic Scholar raw downloads.

The accepted datasets are large (authors ~75M rows), so we never load a whole
asset into memory — we stream the first record of each ndjson.gz shard set and
assert shape, which catches the silent-degradation modes (empty payload,
truncated download, format switch, missing key fields) that file existence
alone misses.
"""

import json

from subsets_utils import raw_reader

# Scalar keys we depend on downstream (the transform SELECTs these).
_REQUIRED_KEYS = {
    "semantic-scholar-authors": {"authorid", "name"},
    "semantic-scholar-publication-venues": {"id", "name"},
}


def _first_record(sid: str) -> dict:
    with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
        for line in f:
            line = line.strip()
            if line:
                return json.loads(line)
    raise AssertionError(f"{sid}: raw ndjson.gz held no records")


def test_raw_assets_nonempty_and_well_shaped(spec_ids):
    for sid in spec_ids:
        rec = _first_record(sid)
        assert isinstance(rec, dict) and rec, f"{sid}: first record is not a non-empty object"
        required = _REQUIRED_KEYS.get(sid, set())
        missing = required - set(rec)
        assert not missing, f"{sid}: first record missing expected keys {sorted(missing)}"
