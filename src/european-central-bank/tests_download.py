"""Health invariants for ECB raw downloads, run post-DAG inside the connector."""

import json

from subsets_utils import raw_reader


def test_raw_has_records(spec_ids):
    """Every dataflow's raw NDJSON must hold at least one parseable observation.

    Streams the first line only (some flows are many millions of rows) — empty
    or unparseable raw means the endpoint switched format or returned nothing.
    """
    for sid in spec_ids:
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            first = f.readline()
        assert first and first.strip(), f"{sid}: raw NDJSON is empty"
        rec = json.loads(first)
        assert "TIME_PERIOD" in rec and "OBS_VALUE" in rec, (
            f"{sid}: first record missing expected SDMX columns; got {list(rec)[:8]}"
        )
