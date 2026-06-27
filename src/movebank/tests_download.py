"""Health invariants for the Movebank connector, run post-DAG in-connector.

Memory-safe: we never load a whole study CSV (some are millions of rows). We
check that every download spec produced a raw ndjson file and that a sample of
them parse to non-empty, core-schema records.
"""
import json

from subsets_utils import list_raw_files, raw_reader

CORE_FIELDS = {
    "event_id", "timestamp", "longitude", "latitude",
    "sensor_type", "taxon", "individual_id", "tag_id", "study_name",
}


def test_every_spec_has_raw(spec_ids):
    """Every download spec must have written its raw ndjson asset. A missing
    file means the fetch silently produced nothing (bad handle, empty bundle)."""
    files = set(list_raw_files("*.ndjson.gz"))
    missing = [sid for sid in spec_ids if f"{sid}.ndjson.gz" not in files]
    assert not missing, f"{len(missing)} specs have no raw ndjson: {missing[:5]}"


def test_sample_raw_nonempty_and_core_schema(spec_ids):
    """Spot-check a spread of specs: the first record must parse and carry the
    core schema keys. Catches truncated downloads and column-mapping drift
    without materializing any full file."""
    sample = spec_ids[:: max(1, len(spec_ids) // 12)][:12]
    for sid in sample:
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first = f.readline()
        assert first.strip(), f"{sid}: raw ndjson is empty"
        rec = json.loads(first)
        assert CORE_FIELDS.issubset(rec.keys()), (
            f"{sid}: first record missing core fields; got {sorted(rec.keys())}"
        )
