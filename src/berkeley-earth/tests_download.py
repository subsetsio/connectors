"""Health invariants for the Berkeley Earth raw asset.

Catch silent degradation that mere file existence misses: empty payloads,
truncated downloads, a format change that drops whole variables or regions.
The single time-series asset is small enough to load fully.
"""
from subsets_utils import load_raw_parquet

TS_ASSET = "berkeley-earth-temperature-timeseries"


def test_timeseries_shape():
    """The time-series asset must carry rows for all three variables, the global
    land+ocean and land products, regional series, and a sane monthly span."""
    table = load_raw_parquet(TS_ASSET)
    assert table.num_rows > 100_000, f"{TS_ASSET}: only {table.num_rows} rows"

    variables = set(table.column("variable").to_pylist())
    assert {"TAVG", "TMAX", "TMIN"}.issubset(variables), f"missing variables: {variables}"

    levels = set(table.column("level").to_pylist())
    assert "global" in levels, "no global product rows"
    assert {"country", "us-state"} & levels, f"no regional rows: {levels}"

    domains = set(table.column("domain").to_pylist())
    assert "land_and_ocean" in domains, "missing the land+ocean global series"
    assert "land" in domains, "missing land-only series"

    years = table.column("year").to_pylist()
    assert 1750 <= min(years) <= 1900, f"unexpected earliest year {min(years)}"
    assert max(years) >= 2015, f"data looks stale, latest year {max(years)}"

    months = set(table.column("month").to_pylist())
    assert months <= set(range(1, 13)) and len(months) == 12, f"bad months {months}"
