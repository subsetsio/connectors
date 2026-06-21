"""Health invariants for the EEA Discodata connector, run post-DAG in-connector.

Memory-safe: we never fully load the multi-million-row tables (e.g.
AirQualityStatistics). Presence is checked for every asset via list_raw_files;
non-emptiness is checked by peeking the first NDJSON line through a streaming
reader on a bounded sample.
"""
from subsets_utils import list_raw_files, raw_reader


def test_every_asset_has_raw_file(spec_ids):
    """Each download spec must have written a raw NDJSON file. A missing file
    means the fetch raised through (blob 404 + SQL offline, or a bug)."""
    missing = [sid for sid in spec_ids if not list_raw_files(f"{sid}.ndjson.gz")]
    assert not missing, f"{len(missing)} specs wrote no raw file, e.g. {missing[:10]}"


def test_sample_assets_nonempty(spec_ids):
    """Peek the first line of a spread-out sample. A 0-byte/headerless asset
    usually means the endpoint changed format or returned an empty payload."""
    ordered = sorted(spec_ids)
    # 25 evenly spread across the catalog — cheap, and covers blob + SQL paths.
    step = max(1, len(ordered) // 25)
    sample = ordered[::step]
    empty = []
    for sid in sample:
        if not list_raw_files(f"{sid}.ndjson.gz"):
            empty.append(f"{sid}:missing")
            continue
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as fh:
            if not fh.readline().strip():
                empty.append(f"{sid}:empty")
    assert not empty, f"empty/broken assets in sample: {empty}"
