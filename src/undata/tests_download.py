"""Health invariants for the UNdata raw downloads.

Raw assets can be very large (the SDG flow is hundreds of MB), so these tests
read only the first line of each gzipped NDJSON rather than loading the whole
file — enough to catch silent degradation (empty payload, format switch,
truncated header) without materializing the corpus in memory.
"""

import json

from subsets_utils import list_raw_files, raw_reader


def test_all_raw_assets_present_and_nonempty(spec_ids):
    """Every download spec must produce a non-empty ndjson.gz raw asset.
    An empty payload usually means the SDMX endpoint changed format or the
    dataflow id stopped resolving."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.ndjson.gz")
        assert files, f"{sid}: no raw ndjson.gz file written"
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first = f.readline()
        assert first.strip(), f"{sid}: raw ndjson.gz has no rows"


def test_raw_rows_have_obs_value_and_time(spec_ids):
    """Each observation row must carry the SDMX OBS_VALUE and TIME_PERIOD keys
    (parsed straight from the SDMX-CSV header). Missing keys means the CSV
    column layout shifted and the transform's cast would silently drop data."""
    for sid in spec_ids:
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first = f.readline()
        rec = json.loads(first)
        assert "OBS_VALUE" in rec, f"{sid}: row missing OBS_VALUE key: {sorted(rec)[:8]}"
        assert "TIME_PERIOD" in rec, f"{sid}: row missing TIME_PERIOD key: {sorted(rec)[:8]}"
