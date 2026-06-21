"""Health invariants for the EEA Discodata connector, run post-DAG in-connector.

Memory-safe: we never fully load the multi-million-row tables (e.g.
AirQualityStatistics). Presence is checked via list_raw_files; non-emptiness by
peeking the first NDJSON line through a streaming reader on a bounded sample.

Tolerance: ~65% of tables (the bulk-blob path) are extracted from EEA's reliable
Azure datalake; the rest are SQL-API views whose backend throttles transiently
("Service currently offline"). A handful of those can legitimately fail a given
run, so the presence floor is set to catch *systemic* breakage (the blob path
itself broke) rather than tripping on a few flaky SQL views.
"""
from subsets_utils import list_raw_files, raw_reader

PRESENCE_FLOOR = 0.60  # below this, the reliable blob path itself is broken


def test_blob_path_intact(spec_ids):
    """At least the bulk-blob majority must have produced raw files. A drop
    below the floor means the Azure datalake download path broke, not just a
    few throttled SQL views."""
    present = [sid for sid in spec_ids if list_raw_files(f"{sid}.ndjson.gz")]
    frac = len(present) / max(1, len(spec_ids))
    assert frac >= PRESENCE_FLOOR, (
        f"only {len(present)}/{len(spec_ids)} ({frac:.0%}) assets present; "
        f"expected >= {PRESENCE_FLOOR:.0%} — the blob download path is broken"
    )


def test_present_sample_nonempty(spec_ids):
    """Peek the first line of a spread-out sample of *present* assets. A
    0-byte/headerless asset means the endpoint changed format or returned an
    empty payload."""
    present = sorted(sid for sid in spec_ids if list_raw_files(f"{sid}.ndjson.gz"))
    if not present:
        return  # covered by test_blob_path_intact
    step = max(1, len(present) // 25)
    empty = []
    for sid in present[::step]:
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as fh:
            if not fh.readline().strip():
                empty.append(sid)
    assert not empty, f"present-but-empty assets in sample: {empty}"
