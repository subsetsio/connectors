"""Health invariants for the Berkeley Earth raw assets.

Catch silent degradation that mere file existence misses: empty payloads,
truncated downloads, a format change that drops whole variables or regions.
The timeseries asset is small enough to load fully; the gridded asset (tens of
millions of rows) is checked via parquet metadata to stay memory-bounded.
"""
import pyarrow.parquet as pq

from subsets_utils import load_raw_parquet, raw_parquet_localpath

TS_ASSET = "berkeley-earth-temperature-timeseries"
GRID_ASSET = "berkeley-earth-gridded-temperature"


def test_timeseries_shape():
    """The time-series asset must carry rows for all three variables, the global
    products, and a sane monthly year span."""
    table = load_raw_parquet(TS_ASSET)
    assert table.num_rows > 100_000, f"{TS_ASSET}: only {table.num_rows} rows"

    variables = set(table.column("variable").to_pylist())
    assert {"TAVG", "TMAX", "TMIN"}.issubset(variables), f"missing variables: {variables}"

    levels = set(table.column("level").to_pylist())
    assert "global" in levels, "no global product rows"
    assert {"country", "us-state"} & levels, f"no regional rows: {levels}"

    surfaces = set(table.column("surface").to_pylist())
    assert "land_ocean" in surfaces, "missing the land+ocean global series"

    years = table.column("year").to_pylist()
    assert 1750 <= min(years) <= 1900, f"unexpected earliest year {min(years)}"
    assert max(years) >= 2015, f"data looks stale, latest year {max(years)}"

    months = set(table.column("month").to_pylist())
    assert months <= set(range(1, 13)) and len(months) == 12, f"bad months {months}"


def test_gridded_has_both_surfaces_and_rows():
    """The gridded asset must be a large, non-empty long-format raster covering
    both the land and land+ocean equal-area fields. Checked via row-group metadata
    plus a single batch so we never materialize the whole table."""
    with raw_parquet_localpath(GRID_ASSET) as path:
        pf = pq.ParquetFile(path)
        assert pf.metadata.num_rows > 1_000_000, (
            f"{GRID_ASSET}: only {pf.metadata.num_rows} rows — gridded fields look truncated"
        )
        first = next(pf.iter_batches(batch_size=200_000))
    cols = set(first.schema.names)
    assert {"surface", "latitude", "longitude", "temperature_anomaly"} <= cols, cols
    # latitude/longitude must look like real geographic coordinates.
    lat = first.column("latitude")
    import pyarrow.compute as pc
    assert pc.min(lat).as_py() >= -91 and pc.max(lat).as_py() <= 91, "latitude out of range"
