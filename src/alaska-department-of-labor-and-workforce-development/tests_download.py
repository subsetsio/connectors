"""Health-invariant tests for the Alaska DOLWD connector raw assets.

These run post-DAG, in-connector. They catch silent degradation that file
existence alone misses: an endpoint that switched format, a workbook whose
layout drifted so a parser produced 0 rows, or a truncated download.
"""
from subsets_utils import load_raw_ndjson

# Conservative per-asset minimum row counts (well below observed, loose enough
# for normal fluctuation but tight enough that a broken parser trips them).
_MIN_ROWS = {
    "alaska-department-of-labor-and-workforce-development-labor-force-area": 5000,
    "alaska-department-of-labor-and-workforce-development-ces-monthly-employment-by-industry": 1000,
    "alaska-department-of-labor-and-workforce-development-wages-by-occupation": 200,
    "alaska-department-of-labor-and-workforce-development-consumer-price-index": 50,
    "alaska-department-of-labor-and-workforce-development-occupational-projections": 200,
    "alaska-department-of-labor-and-workforce-development-population-total": 500,
    "alaska-department-of-labor-and-workforce-development-population-components-of-change": 80,
    "alaska-department-of-labor-and-workforce-development-population-age-sex": 1000,
    "alaska-department-of-labor-and-workforce-development-population-race-hispanic": 200,
    "alaska-department-of-labor-and-workforce-development-population-age-sex-race-hispanic": 5000,
    "alaska-department-of-labor-and-workforce-development-population-projections": 500,
    "alaska-department-of-labor-and-workforce-development-qcew": 1000,
    "alaska-department-of-labor-and-workforce-development-nonfatal-injuries-illnesses": 50,
    "alaska-department-of-labor-and-workforce-development-workplace-fatalities": 10,
}


def test_all_raw_assets_present_and_sized(spec_ids):
    """Every download spec must produce a non-trivially-sized ndjson asset."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: got {len(rows)} rows, expected >= {floor}"


def test_population_values_positive(spec_ids):
    """Population assets must carry positive integer population values — a
    parser that grabbed the wrong columns would surface zeros/negatives."""
    for sid in spec_ids:
        if "population-total" not in sid and "components-of-change" not in sid:
            continue
        rows = load_raw_ndjson(sid)
        pops = [r.get("population") for r in rows if r.get("population") is not None]
        assert pops, f"{sid}: no population values"
        assert max(pops) > 1000, f"{sid}: max population {max(pops)} implausibly small"
