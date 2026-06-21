"""Health-invariant tests for the US Drought Monitor raw downloads.

Catch silent degradation: truncated pulls (one state's FIPS quietly returning
empty), missing national data, or the region/measure columns vanishing.
"""

from subsets_utils import load_raw_parquet

# US national + 50 states + DC + Puerto Rico.
EXPECTED_MIN_REGIONS = 53
# Weekly since 2000-01-04 → ~1300+ weeks per region. With 53 regions, a full
# pull is ~70k rows; well under that means a chunk of FIPS pulls failed silently.
EXPECTED_MIN_ROWS = 60000


def test_severity_shape(spec_ids):
    sid = "us-drought-monitor-drought-severity"
    assert sid in spec_ids, f"{sid} did not run"
    table = load_raw_parquet(sid)
    assert len(table) >= EXPECTED_MIN_ROWS, f"{sid}: only {len(table)} rows"
    regions = set(table.column("region").to_pylist())
    assert len(regions) >= EXPECTED_MIN_REGIONS, f"{sid}: only {len(regions)} regions"
    for r in ("US", "CA", "TX"):
        assert r in regions, f"{sid}: missing region {r}"
    # Percentages must be in range; D0 (cumulative) should never exceed 100.
    for col in ("none", "d0", "d1", "d2", "d3", "d4"):
        vals = [v for v in table.column(col).to_pylist() if v is not None]
        assert vals, f"{sid}: column {col} all null"
        assert min(vals) >= 0 and max(vals) <= 100, f"{sid}: {col} out of [0,100]"


def test_dsci_shape(spec_ids):
    sid = "us-drought-monitor-dsci"
    assert sid in spec_ids, f"{sid} did not run"
    table = load_raw_parquet(sid)
    assert len(table) >= EXPECTED_MIN_ROWS, f"{sid}: only {len(table)} rows"
    regions = set(table.column("region").to_pylist())
    assert len(regions) >= EXPECTED_MIN_REGIONS, f"{sid}: only {len(regions)} regions"
    for r in ("US", "CA", "TX"):
        assert r in regions, f"{sid}: missing region {r}"
    dsci = [v for v in table.column("dsci").to_pylist() if v is not None]
    assert dsci, f"{sid}: dsci all null"
    assert min(dsci) >= 0 and max(dsci) <= 500, f"{sid}: dsci out of [0,500]"
