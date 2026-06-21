"""Health invariants for the Cboe Global Indices download.

Catch silent degradation the file-existence check misses: an empty payload, a
collapsed catalog (the CDN switching format would yield few/no symbols), or a
column-mapping regression that nulls out every close price.
"""
from subsets_utils import load_raw_parquet


def test_values_nonempty(spec_ids):
    """The unified daily-price asset should hold a large multi-symbol panel."""
    table = load_raw_parquet("cboe-global-markets-values")
    assert len(table) > 100_000, f"values: only {len(table)} rows — expected the full panel"


def test_values_many_symbols():
    """~2000 indices are published; a collapse to a handful means the catalog
    enumeration or per-symbol fetch silently broke."""
    table = load_raw_parquet("cboe-global-markets-values")
    n_symbols = len(set(table.column("symbol").to_pylist()))
    assert n_symbols > 500, f"values: only {n_symbols} distinct symbols"


def test_values_close_present():
    """Close is the one column every series carries; an all-null close means the
    header-to-column mapping regressed."""
    table = load_raw_parquet("cboe-global-markets-values")
    closes = table.column("close").to_pylist()
    non_null = sum(1 for c in closes if c is not None)
    assert non_null > 0.9 * len(closes), f"values: only {non_null}/{len(closes)} non-null close"


def test_benchmark_symbols_present():
    """VIX and SPX are flagship benchmarks; their absence means a headline series
    dropped out of the crawl."""
    table = load_raw_parquet("cboe-global-markets-values")
    symbols = set(table.column("symbol").to_pylist())
    for sym in ("VIX", "SPX"):
        assert sym in symbols, f"benchmark {sym} missing from values"
