"""Health invariants for Baseball Savant raw assets.

The statcast pitch corpus is written as many per-window ndjson batches
(`baseball-savant-statcast-pitches-<date>`); the leaderboards are one ndjson
asset each. We assert that every leaderboard asset has rows and that the pitch
corpus produced at least one non-empty batch.
"""

import gzip

from subsets_utils import load_raw_ndjson, load_raw_file, list_raw_files

PITCHES_ID = "baseball-savant-statcast-pitches"


def test_leaderboards_nonempty(spec_ids):
    """Every leaderboard spec should have written rows. An empty payload usually
    means the endpoint changed format or the param set broke."""
    for sid in spec_ids:
        if sid == PITCHES_ID:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: leaderboard ndjson has 0 rows"


def test_statcast_pitches_have_batches():
    """The pitch firehose should have produced at least one gzipped CSV batch
    with pitch rows carrying the core tracked fields."""
    ext = ".csv.gz"
    files = list_raw_files(f"{PITCHES_ID}-*{ext}")
    assert files, f"{PITCHES_ID}: no raw CSV batch files written"
    asset_id = files[0].rsplit("/", 1)[-1][: -len(ext)]
    raw = load_raw_file(asset_id, extension="csv.gz", binary=True)
    text = gzip.decompress(raw).decode("utf-8")
    lines = text.splitlines()
    assert len(lines) >= 2, f"{asset_id}: CSV has no data rows"
    header = lines[0]
    assert "game_date" in header, f"{asset_id}: missing game_date column"
    assert "pitch_type" in header, f"{asset_id}: missing pitch_type column"
