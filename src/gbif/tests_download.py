"""Post-DAG health invariants for the GBIF aggregate downloads.

Each raw asset is ndjson with at least {facet_value|year, n}. These catch silent
degradation the existence check misses: an empty facet response, a count column
that came back null/zero, or a panel that lost its outer dimension.
"""
from subsets_utils import load_raw_ndjson

PANEL_IDS = {
    "gbif-occurrences-by-year-and-country",
    "gbif-occurrences-by-year-and-kingdom",
    "gbif-occurrences-by-year-and-basis-of-record",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every facet snapshot must hold rows; 0 rows means the facet API returned
    no aggregate (format change, throttle, or empty envelope)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_counts_positive(spec_ids):
    """Counts must be positive integers — a facet bucket with count 0/None means
    the response shape drifted."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        bad = [r for r in rows if not isinstance(r.get("n"), int) or r["n"] <= 0]
        assert not bad, f"{sid}: {len(bad)} rows with non-positive/invalid count (e.g. {bad[:2]})"


def test_panels_have_year_dimension(spec_ids):
    """Year panels must carry a non-null year on every row and span multiple
    years for multiple outer values — else the per-dimension filter broke."""
    for sid in spec_ids:
        if sid not in PANEL_IDS:
            continue
        rows = load_raw_ndjson(sid)
        assert all(r.get("year") for r in rows), f"{sid}: rows missing year"
        outer = {r["facet_value"] for r in rows}
        years = {r["year"] for r in rows}
        assert len(outer) >= 2, f"{sid}: only {len(outer)} outer values; panel collapsed"
        assert len(years) >= 5, f"{sid}: only {len(years)} distinct years; year facet broke"


def test_year_series_reasonable(spec_ids):
    """The global year series should span many years and include recent ones —
    a tiny span means facetLimit silently capped the distribution."""
    sid = "gbif-occurrences-by-year"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    years = {int(r["facet_value"]) for r in rows if str(r["facet_value"]).lstrip("-").isdigit()}
    assert len(years) >= 50, f"{sid}: only {len(years)} distinct years"
    assert max(years) >= 2024, f"{sid}: latest year {max(years)} — missing recent data"
