"""Post-DAG health invariants for the NBMP connector.

Catch silent degradation that file-existence misses: an xlsx whose sheet layout
changed so parsing emitted nothing useful, a collapsed year span, or the trend
summary losing its short/long-term split.
"""

from subsets_utils import load_raw_parquet


def test_trend_indices_full(spec_ids):
    sid = "nbmp-trend-indices"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    # sheet '1_Trend_indices_and_CIs' is ~2000 rows; a layout change drops to near 0.
    assert t.num_rows >= 1500, f"{sid}: only {t.num_rows} rows; sheet parse degraded"
    cols = set(t.column_names)
    assert {"geographical_scale", "species", "year", "smoothed_index"} <= cols, cols
    years = [int(y) for y in t.column("year").to_pylist() if y and y.isdigit()]
    assert min(years) <= 2000 and max(years) >= 2023, f"year span looks wrong: {min(years)}-{max(years)}"
    assert len(set(t.column("species").to_pylist())) >= 8, "too few distinct species"


def test_population_trends_full(spec_ids):
    sid = "nbmp-population-trends"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    # two stacked tables (short + long term), ~70 rows total.
    assert t.num_rows >= 40, f"{sid}: only {t.num_rows} rows; sheet parse degraded"
    terms = set(t.column("term").to_pylist())
    assert {"short_term", "long_term"} <= terms, f"missing a trend term, got {terms}"
    countries = set(t.column("country").to_pylist())
    assert {"GB", "England", "Wales", "Scotland"} <= countries, f"missing geographies: {countries}"
