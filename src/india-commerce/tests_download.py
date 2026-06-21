"""Health invariants for the india-commerce raw assets.

These run post-DAG, in-connector, against the data as written by the download
nodes. They catch silent degradation (empty payloads, a country/commodity
dimension that collapsed to a handful of rows, a flow that vanished).
"""
from subsets_utils import load_raw_parquet


def test_country_trade_shape(spec_ids):
    t = load_raw_parquet("india-commerce-country-trade")
    assert len(t) > 0, "country_trade: empty"
    n_countries = len(set(t.column("country_code").to_pylist()))
    assert n_countries >= 150, f"country_trade: only {n_countries} countries (expected >=150)"
    n_years = len(set(t.column("year").to_pylist()))
    assert n_years >= 5, f"country_trade: only {n_years} distinct years"


def test_commodity_trade_shape(spec_ids):
    t = load_raw_parquet("india-commerce-commodity-trade")
    assert len(t) > 0, "commodity_trade: empty"
    flows = set(t.column("flow").to_pylist())
    assert {"Export", "Import"} <= flows, f"commodity_trade: missing flows, saw {flows}"
    n_chapters = len(set(t.column("hs2_code").to_pylist()))
    assert n_chapters >= 90, f"commodity_trade: only {n_chapters} HS2 chapters (expected ~98)"


def test_state_trade_shape(spec_ids):
    t = load_raw_parquet("india-commerce-state-trade")
    assert len(t) > 0, "state_trade: empty"
    n_states = len(set(t.column("state").to_pylist()))
    assert n_states >= 20, f"state_trade: only {n_states} states (expected ~30+)"
