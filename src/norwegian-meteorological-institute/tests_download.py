"""Post-DAG health checks for MET Norway WeatherAPI downloads."""

from subsets_utils import load_raw_ndjson


def test_raw_assets_nonempty(spec_ids):
    for spec_id in spec_ids:
        rows = load_raw_ndjson(spec_id)
        assert rows, f"{spec_id}: raw NDJSON has no rows"


def test_tidalwater_has_many_harbors(spec_ids):
    spec_id = "norwegian-meteorological-institute-tidalwater"
    if spec_id not in spec_ids:
        return
    rows = load_raw_ndjson(spec_id)
    harbors = {row.get("harbor") for row in rows if row.get("harbor")}
    assert len(harbors) >= 25, f"tidalwater: only {len(harbors)} harbors"
    assert all(row.get("observed_at") for row in rows), "tidalwater: missing observed_at"


def test_textforecast_covers_available_forecasts(spec_ids):
    spec_id = "norwegian-meteorological-institute-textforecast"
    if spec_id not in spec_ids:
        return
    rows = load_raw_ndjson(spec_id)
    forecasts = {row.get("forecast") for row in rows if row.get("forecast")}
    assert len(forecasts) >= 7, f"textforecast: only {len(forecasts)} forecast types"
