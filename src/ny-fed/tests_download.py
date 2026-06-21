"""Health-invariant tests for the NY Fed connector raw assets.

Run post-DAG, in-connector. They load raw via the same loader the download
nodes used (NDJSON) and assert against silent degradation: empty payloads,
truncated history, a format/auth switch that quietly returns nothing.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce rows. An empty NDJSON usually means the
    endpoint changed shape or the date window stopped returning data."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_reference_rates_have_expected_types(spec_ids):
    """Secured rates must include SOFR; unsecured must include EFFR. A missing
    flagship type means the type filter or endpoint silently broke."""
    if "ny-fed-reference-rates-secured" in spec_ids:
        types = {r.get("type") for r in load_raw_ndjson("ny-fed-reference-rates-secured")}
        assert "SOFR" in types, f"secured rates missing SOFR; got {sorted(t for t in types if t)}"
    if "ny-fed-reference-rates-unsecured" in spec_ids:
        types = {r.get("type") for r in load_raw_ndjson("ny-fed-reference-rates-unsecured")}
        assert "EFFR" in types, f"unsecured rates missing EFFR; got {sorted(t for t in types if t)}"


def test_primary_dealer_many_series(spec_ids):
    """The per-keyid crawl should yield many distinct series. A collapse to a
    handful means the series listing or per-series fetch degraded."""
    if "ny-fed-primary-dealer-values" not in spec_ids:
        return
    rows = load_raw_ndjson("ny-fed-primary-dealer-values")
    series = {r.get("keyid") for r in rows}
    assert len(series) >= 100, f"primary-dealer values cover only {len(series)} series; expected >=100"


def test_soma_holdings_single_snapshot(spec_ids):
    """SOMA holdings is the latest as-of snapshot: exactly one as-of date, and
    both Treasury and Agency instrument groups present."""
    if "ny-fed-soma-holdings" not in spec_ids:
        return
    rows = load_raw_ndjson("ny-fed-soma-holdings")
    dates = {r.get("asOfDate") for r in rows}
    assert len(dates) == 1, f"expected one as-of snapshot, got {len(dates)} dates"
    groups = {r.get("instrumentGroup") for r in rows}
    assert {"Treasury", "Agency"} <= groups, f"missing instrument groups; got {groups}"
