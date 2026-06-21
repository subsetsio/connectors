"""Health-invariant tests for the Open-Meteo raw assets.

Run post-DAG inside the connector. Catch silent degradation that file existence
alone misses: empty payloads (endpoint switched format / nulled out), missing
columns (variable list changed upstream), or a collapsed location set (a request
loop broke after the first city).
"""
from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "open-meteo-archive-daily": {"name", "country", "latitude", "longitude",
                                 "date", "temperature_2m_max", "precipitation_sum"},
    "open-meteo-climate-projections": {"name", "model", "date",
                                       "temperature_2m_max"},
    "open-meteo-flood": {"name", "date", "river_discharge"},
    "open-meteo-air-quality": {"name", "time", "pm10", "pm2_5"},
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every product's raw parquet must hold rows. Empty usually means the
    endpoint changed shape or every point errored silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS.get(sid, set()) - cols
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"


def test_multiple_locations_present(spec_ids):
    """Each product samples ~24 cities; if a fetch loop broke after city #1 we'd
    see a single location. Require a healthy spread."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        names = set(table.column("name").to_pylist())
        assert len(names) >= 15, (
            f"{sid}: only {len(names)} distinct locations; fetch loop likely broke")
