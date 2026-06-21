"""Health invariants for the NBB raw download layer.

Run post-DAG, in-connector, through subsets_utils loaders. These catch silent
degradation that file-existence alone misses: a missing cube, or an endpoint
that quietly stopped emitting SDMX-CSV (records without the expected keys).
"""

import json

from subsets_utils import list_raw_files, raw_reader

RAW_EXT = "ndjson.gz"


def test_each_spec_has_raw(spec_ids):
    """Every download spec must have produced a raw NDJSON file."""
    missing = [sid for sid in spec_ids if not list_raw_files(f"{sid}.{RAW_EXT}")]
    assert not missing, f"{len(missing)} spec(s) wrote no raw file: {missing[:10]}"


def test_sdmx_record_shape(spec_ids):
    """The first record of each cube must carry the canonical SDMX keys —
    DATAFLOW, TIME_PERIOD and OBS_VALUE are present in every NBB.Stat dataflow.
    A missing key means the endpoint changed format or returned an error page.

    Reads only the first line (gzip streams), so this is cheap even for the
    largest cubes."""
    bad = []
    for sid in spec_ids:
        with raw_reader(sid, RAW_EXT, mode="rt", compression="gzip") as f:
            first = f.readline()
        if not first.strip():
            bad.append((sid, "<empty>"))
            continue
        rec = json.loads(first)
        if not {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}.issubset(rec.keys()):
            bad.append((sid, sorted(rec.keys())[:8]))
    assert not bad, f"{len(bad)} spec(s) have non-SDMX records: {bad[:5]}"
