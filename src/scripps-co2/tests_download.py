"""Health invariants for the Scripps CO2 raw assets (run post-DAG, in-connector)."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every subset must parse at least some data rows. An empty asset usually
    means the CSV format changed or every line was misclassified as a header."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_flagship_keeling_curve_has_value(spec_ids):
    """The monthly Mauna Loa in-situ record (the Keeling Curve) must carry real
    CO2 values across a long span — the single most important series here."""
    sid = "scripps-co2-monthly-in-situ-co2"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    valued = [r for r in rows if r.get("value_filled") is not None]
    assert len(valued) > 600, f"{sid}: only {len(valued)} filled monthly values (<600)"
    # 1958 onward: plausible CO2 ppm range.
    vals = [r["value_filled"] for r in valued]
    assert 300 < min(vals) < 360, f"{sid}: min CO2 {min(vals)} out of range"
    assert 380 < max(vals) < 500, f"{sid}: max CO2 {max(vals)} out of range"


def test_flask_co2_multi_station(spec_ids):
    """Daily flask CO2 folds many sampling stations into one table; a single
    station means the station-folding regressed to one file."""
    sid = "scripps-co2-daily-flask-co2"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    stations = {r.get("station") for r in rows}
    assert len(stations) >= 5, f"{sid}: only {len(stations)} stations: {stations}"
