"""Post-DAG health invariants for the Transparency International CPI raw assets.

These catch silent degradation (format change, truncated/empty parse) that file
existence alone misses. Thresholds are loose enough for normal year-on-year
growth, tight enough that a degraded parse (e.g. only the header survived) trips.
"""

from subsets_utils import load_raw_parquet

TIMESERIES = "transparency-international-cpi-timeseries"
DETAIL = "transparency-international-cpi-latest-detail"
REGIONAL = "transparency-international-cpi-regional-averages"


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_timeseries_shape(spec_ids):
    """CPI covers ~180 countries x many years (2012+); expect well over a
    thousand country-year rows, all with a numeric score."""
    if TIMESERIES not in spec_ids:
        return
    t = load_raw_parquet(TIMESERIES)
    assert len(t) >= 1500, f"{TIMESERIES}: only {len(t)} rows; parse likely degraded"
    for col in ("country", "iso3", "year", "cpi_score"):
        assert col in t.column_names, f"{TIMESERIES}: missing column {col}"
    scores = t.column("cpi_score").to_pylist()
    assert all(s is not None for s in scores), f"{TIMESERIES}: null cpi_score leaked through"
    assert min(scores) >= 0 and max(scores) <= 100, "CPI score out of 0..100 range"
    years = set(t.column("year").to_pylist())
    assert 2012 in years, f"{TIMESERIES}: 2012 missing; back-series truncated"


def test_detail_components(spec_ids):
    """Per-country underlying source scores; expect multiple distinct sources
    and hundreds of country-source rows."""
    if DETAIL not in spec_ids:
        return
    t = load_raw_parquet(DETAIL)
    assert len(t) >= 500, f"{DETAIL}: only {len(t)} rows; component parse degraded"
    n_sources = len(set(t.column("source_name").to_pylist()))
    assert n_sources >= 5, f"{DETAIL}: only {n_sources} distinct sources; expected >=5"


def test_regional_averages(spec_ids):
    """Six TI regions across several years."""
    if REGIONAL not in spec_ids:
        return
    t = load_raw_parquet(REGIONAL)
    assert len(t) >= 10, f"{REGIONAL}: only {len(t)} rows"
    regions = set(t.column("region").to_pylist())
    assert len(regions) >= 5, f"{REGIONAL}: only {len(regions)} regions; expected ~6"
