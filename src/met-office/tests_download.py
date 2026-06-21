"""Post-DAG health invariants for the Met Office connector."""
from subsets_utils import load_raw_parquet

OBS = "met-office-observations"
STATIONS = "met-office-stations"


def test_observations_nonempty():
    """The long-format table should hold tens of thousands of monthly rows
    across all stations; a big drop means the index scrape or a station file
    silently failed."""
    t = load_raw_parquet(OBS)
    assert t.num_rows > 20000, f"{OBS}: only {t.num_rows} rows (expected >20k)"
    for col in ("station", "year", "month", "tmax_degc", "rain_mm"):
        assert col in t.column_names, f"{OBS}: missing column {col}"


def test_observations_year_span():
    """Series should span from the 19th century to the current era; a narrow
    span means header/data parsing regressed."""
    t = load_raw_parquet(OBS)
    years = t.column("year").to_pylist()
    assert min(years) <= 1900, f"earliest year {min(years)} unexpectedly late"
    assert max(years) >= 2020, f"latest year {max(years)} unexpectedly early"


def test_observations_measures_present():
    """At least one core measure must carry real (non-null) values — an
    all-null column means the marker-stripping/value parse broke."""
    t = load_raw_parquet(OBS)
    tmax = [v for v in t.column("tmax_degc").to_pylist() if v is not None]
    assert len(tmax) > 10000, f"only {len(tmax)} non-null tmax values"


def test_stations_count_and_coords():
    """~37 stations, the large majority with parsed lat/lon."""
    t = load_raw_parquet(STATIONS)
    assert t.num_rows >= 30, f"{STATIONS}: only {t.num_rows} stations (expected ~37)"
    lat = [v for v in t.column("lat").to_pylist() if v is not None]
    assert len(lat) >= 0.8 * t.num_rows, (
        f"only {len(lat)}/{t.num_rows} stations parsed lat"
    )


def test_station_slugs_unique():
    t = load_raw_parquet(STATIONS)
    slugs = t.column("station").to_pylist()
    assert len(slugs) == len(set(slugs)), "duplicate station slugs"
