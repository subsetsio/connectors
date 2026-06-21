"""Health invariants for the JMA connector raw assets.

These run post-DAG, in-connector, and load raw data through the same
subsets_utils loader the download nodes used to save it.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce rows. Empty payloads usually mean an
    endpoint changed format or a fetch silently degraded."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_amedas_station_registry_complete():
    """amedastable.json lists ~1300 stations with coordinates."""
    t = load_raw_parquet("japan-meteorological-agency-amedas-stations")
    assert len(t) >= 1000, f"only {len(t)} AMeDAS stations; expected >=1000"
    cols = set(t.column_names)
    assert {"station_id", "lat", "lon", "name_en"} <= cols, f"missing columns: {cols}"


def test_amedas_observations_long_format():
    """Latest snapshot should cover many stations across multiple elements."""
    t = load_raw_parquet("japan-meteorological-agency-amedas-observations")
    import pyarrow.compute as pc
    n_stations = pc.count_distinct(t.column("station_id")).as_py()
    n_elements = pc.count_distinct(t.column("element")).as_py()
    assert n_stations >= 500, f"only {n_stations} stations in snapshot; expected >=500"
    assert n_elements >= 3, f"only {n_elements} distinct elements; expected >=3"


def test_forecast_areas_four_levels():
    """The taxonomy must carry all four geography levels."""
    t = load_raw_parquet("japan-meteorological-agency-forecast-areas")
    levels = set(t.column("level").to_pylist())
    assert {"centers", "offices", "class10s", "class20s"} <= levels, f"levels={levels}"


def test_weather_forecasts_present():
    """Forecasts should span many offices and multiple elements."""
    t = load_raw_parquet("japan-meteorological-agency-weather-forecasts")
    import pyarrow.compute as pc
    n_offices = pc.count_distinct(t.column("office_code")).as_py()
    assert n_offices >= 30, f"only {n_offices} offices with forecasts; expected >=30"


def test_global_temperature_anomaly_history():
    """Global anomaly series goes back to 1891."""
    t = load_raw_parquet("japan-meteorological-agency-global-temperature-anomaly")
    import pyarrow.compute as pc
    min_year = pc.min(t.column("year")).as_py()
    assert min_year <= 1900, f"earliest year {min_year}; expected <=1900"


def test_enso_indices_regions():
    """ENSO product table must contain all monitored regions and both measures."""
    t = load_raw_parquet("japan-meteorological-agency-enso-sst-indices")
    regions = set(t.column("region").to_pylist())
    measures = set(t.column("measure").to_pylist())
    assert len(regions) >= 5, f"only {regions} regions; expected >=5"
    assert {"sst", "anomaly"} <= measures, f"measures={measures}"
