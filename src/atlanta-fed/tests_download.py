"""Health-invariant tests for the atlanta-fed GDPNow connector.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses: a truncated/empty workbook, a renamed sheet, or a parse that
quietly drops the history down to the current quarter.
"""
from subsets_utils import load_raw_parquet


def test_track_record_full_history(spec_ids):
    """The track record has one row per forecast quarter since 2011:Q3
    (~57+ and growing). A small count means a renamed sheet or a parse that
    only caught summary rows."""
    sid = "atlanta-fed-gdpnow-track-record"
    assert sid in spec_ids, f"{sid} not among ran specs: {spec_ids}"
    t = load_raw_parquet(sid)
    assert t.num_rows >= 50, f"{sid}: only {t.num_rows} quarters; expected >=50"
    quarters = t.column("quarter_end_date").to_pylist()
    assert min(quarters) <= "2012-01-01", f"earliest quarter too late: {min(quarters)}"
    assert max(quarters) >= "2024-01-01", f"latest quarter too old: {max(quarters)}"
    # forecast / actual must be populated for every track-record row
    for col in ("gdpnow_forecast", "bea_advance_estimate"):
        nn = sum(1 for v in t.column(col).to_pylist() if v is None)
        assert nn == 0, f"{sid}: {nn} null values in {col}"


def test_forecast_evolution_long_history(spec_ids):
    """Forecast evolution is the full long-format archive (2011-present),
    hundreds of forecast updates per year. If it collapses to a few dozen
    rows, the archive sheets were lost and only the current quarter survived."""
    sid = "atlanta-fed-gdpnow-forecast-evolution"
    assert sid in spec_ids, f"{sid} not among ran specs: {spec_ids}"
    t = load_raw_parquet(sid)
    assert t.num_rows >= 1500, f"{sid}: only {t.num_rows} updates; expected >=1500"
    fdates = t.column("forecast_date").to_pylist()
    assert min(fdates) <= "2012-01-01", f"earliest forecast date too late: {min(fdates)}"
    # the headline nowcast must always be present
    nn = sum(1 for v in t.column("gdp_nowcast").to_pylist() if v is None)
    assert nn == 0, f"{sid}: {nn} null gdp_nowcast values"
