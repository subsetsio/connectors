"""Health invariants for the CNEMC air-quality raw assets.

These run post-DAG against the raw NDJSON the download nodes wrote, catching silent
degradation (empty payload, truncated network, schema rename) that file-existence misses.
"""

from subsets_utils import load_raw_ndjson

_STATIONS_ID = "ministry-of-ecology-and-environment-stations"
_READINGS_ID = "ministry-of-ecology-and-environment-air-quality-readings"


def test_stations_reasonable():
    rows = load_raw_ndjson(_STATIONS_ID)
    assert len(rows) >= 1000, f"{_STATIONS_ID}: only {len(rows)} stations; national network is ~1600"
    codes = {r.get("StationCode") for r in rows}
    assert len(codes) == len(rows), "duplicate StationCode rows in stations catalog"
    assert all(r.get("PositionName") for r in rows), "some station rows lack PositionName"


def test_readings_nonempty_and_typed():
    rows = load_raw_ndjson(_READINGS_ID)
    assert len(rows) >= 1000, f"{_READINGS_ID}: only {len(rows)} readings; expected >=1 hour x ~1600 stations"
    # time_ms must be parsed for every row (the .NET /Date()/ parse must not silently fail).
    bad = [r for r in rows if not isinstance(r.get("time_ms"), int)]
    assert not bad, f"{len(bad)} reading rows have no parsed time_ms (TimePoint parse broke)"
    # The pollutant field uses the underscore spelling; guard against an upstream rename.
    assert any("PM2_5" in r for r in rows), "PM2_5 field absent — upstream field rename?"


def test_readings_multi_hour():
    """The rolling-window backfill should yield more than a single hour; if only one
    TimePoint survives, the history endpoint silently stopped returning data."""
    rows = load_raw_ndjson(_READINGS_ID)
    hours = {r.get("time_ms") for r in rows if r.get("time_ms")}
    assert len(hours) >= 2, f"only {len(hours)} distinct hour(s); rolling-window backfill degraded"
