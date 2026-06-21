"""Health-invariant tests for the CSO Ireland connector.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses: empty payloads, the endpoint switching format, or the
PxStat CSV losing its core columns. Raw assets are NDJSON (one dict per CSV
row), so load with load_raw_ndjson.
"""

from subsets_utils import load_raw_ndjson

# Columns guaranteed by the PxStat CSV 1.0 format on every matrix.
CORE_COLUMNS = {"STATISTIC", "UNIT", "VALUE"}


def test_sample_raw_assets_nonempty(spec_ids):
    """A representative sample of raw assets must hold rows. Empty payloads
    usually mean the ReadDataset endpoint changed format or started erroring."""
    sample = spec_ids[:: max(1, len(spec_ids) // 50)][:50]
    for sid in sample:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_sample_has_core_columns(spec_ids):
    """Every PxStat table exposes the STATISTIC/UNIT/VALUE columns; if they
    vanish, the CSV format or our parsing broke."""
    sample = spec_ids[:: max(1, len(spec_ids) // 50)][:50]
    for sid in sample:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        keys = set(rows[0].keys())
        missing = CORE_COLUMNS - keys
        assert not missing, f"{sid}: missing core columns {missing}; got {sorted(keys)}"
