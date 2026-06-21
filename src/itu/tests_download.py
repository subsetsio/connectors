"""Health-invariant tests for the ITU connector raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. Empty payloads
    usually mean the endpoint changed format or the throughput cap swallowed
    every request."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_countries_count_reasonable():
    """country/all returns ~236 economies; far fewer means a truncated response."""
    table = load_raw_parquet("itu-countries")
    assert len(table) >= 200, f"itu-countries: only {len(table)} economies"


def test_values_breadth():
    """The observations table should span many indicators/series and many rows;
    a thin table means most indicator downloads silently failed."""
    table = load_raw_parquet("itu-values")
    assert len(table) >= 10000, f"itu-values: only {len(table)} rows"
    n_series = len(set(table.column("series_id").to_pylist()))
    assert n_series >= 50, f"itu-values: only {n_series} distinct series"
    n_iso = len(set(table.column("entity_iso").to_pylist()))
    assert n_iso >= 100, f"itu-values: only {n_iso} distinct economies"
