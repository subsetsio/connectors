"""Health-invariant tests for the bom connector raw assets."""

from subsets_utils import load_raw_parquet


def test_observations_nonempty_and_rich():
    """The Daily Weather Observations corpus should hold a large number of
    daily rows across many stations; a tiny count means the bulk archive
    download or CSV parse silently degraded."""
    t = load_raw_parquet("bom-daily-weather-observations")
    assert len(t) > 100_000, f"observations: only {len(t)} rows"
    stations = set(t.column("station_slug").to_pylist())
    assert len(stations) >= 300, f"observations: only {len(stations)} distinct stations"
    # At least one core measured variable must carry real (non-null) values.
    import pyarrow.compute as pc

    nn = pc.sum(pc.is_valid(t.column("max_temp_c"))).as_py()
    assert nn > 0, "observations: max_temp_c is entirely null"


def test_stations_catalogue():
    """The station catalogue should hold ~500 stations with valid coordinates."""
    t = load_raw_parquet("bom-stations")
    assert len(t) >= 300, f"stations: only {len(t)} rows"
    ids = t.column("bom_station_id").to_pylist()
    assert all(i for i in ids), "stations: empty station id present"
    assert len(set(ids)) == len(ids), "stations: duplicate station ids"
    lats = [v for v in t.column("latitude").to_pylist() if v is not None]
    assert lats and all(-45 < v < -9 for v in lats), "stations: latitudes outside Australia"
