"""Health-invariant tests for the Philadelphia Fed connector.

Run post-DAG, in-connector, against the raw parquet each download node wrote.
They catch silent degradation that file-existence alone misses: an endpoint that
switched to an HTML soft-404, a workbook whose layout drifted so parsing yields a
near-empty frame, or a melt that collapsed to a single column/value.
"""
from subsets_utils import load_raw_parquet


def test_all_assets_nonempty(spec_ids):
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert len(t) > 0, f"{sid}: raw parquet has 0 rows"


def test_ads_daily_history():
    """ADS is daily since 1960 -> tens of thousands of rows spanning >60 years."""
    t = load_raw_parquet("philadelphia-fed-ads-business-conditions")
    assert len(t) > 15000, f"ADS only {len(t)} rows; expected daily series since 1960"
    dates = t.column("date").to_pylist()
    assert min(dates) < "1965-01-01", f"ADS earliest {min(dates)}; expected 1960s"
    assert max(dates) > "2024-01-01", f"ADS latest {max(dates)}; expected recent"


def test_spf_consensus_shape():
    """SPF must carry many variables and all four statistic x measure combos."""
    t = load_raw_parquet("philadelphia-fed-spf-consensus")
    assert len(t) > 5000, f"SPF only {len(t)} rows"
    variables = set(t.column("variable").to_pylist())
    assert len(variables) >= 10, f"SPF only {len(variables)} variables"
    combos = set(zip(t.column("statistic").to_pylist(), t.column("measure").to_pylist()))
    assert combos == {("mean", "level"), ("mean", "growth"),
                      ("median", "level"), ("median", "growth")}, f"SPF combos: {combos}"


def test_state_coincident_panel():
    """Coincident indexes cover the 50 states (+ US) as a long panel."""
    t = load_raw_parquet("philadelphia-fed-state-coincident-indexes")
    states = set(t.column("state").to_pylist())
    assert len(states) >= 50, f"coincident only {len(states)} states/areas"


def test_rtdsm_many_variables():
    """RTDSM unions ~59 macro variables; a broken discovery would collapse this."""
    t = load_raw_parquet("philadelphia-fed-real-time-data-set-macroeconomists")
    variables = set(t.column("variable").to_pylist())
    assert len(variables) >= 40, f"RTDSM only {len(variables)} variables"


def test_atsix_term_structure():
    """ATSIX is a term structure -> many distinct horizons per date."""
    t = load_raw_parquet("philadelphia-fed-atsix")
    horizons = set(t.column("horizon_months").to_pylist())
    assert len(horizons) >= 50, f"ATSIX only {len(horizons)} horizons"
