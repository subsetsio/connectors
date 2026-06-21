"""Health invariants for the Bundesnetzagentur (SMARD) raw downloads."""

from subsets_utils import load_raw_parquet


def test_all_feeds_nonempty(spec_ids):
    """Each feed must hold rows. An empty payload means SMARD changed its
    module ids or the chart_data URL scheme and the crawl silently no-op'd."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} raw rows"


def test_values_finite_and_dated(spec_ids):
    """Values are real numbers and timestamps are plausible (post-2010 ms)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid).to_pydict()
        vals = table["value"]
        assert all(v is not None for v in vals), f"{sid}: null values leaked into raw"
        ds = table["date_ms"]
        assert min(ds) > 1_262_304_000_000, f"{sid}: implausibly early timestamp"


def test_multiple_series_per_feed(spec_ids):
    """Every feed must carry more than one distinct series — a single series
    would mean most modules 404'd or returned empty."""
    for sid in spec_ids:
        codes = set(load_raw_parquet(sid).column("series_code").to_pylist())
        assert len(codes) >= 2, f"{sid}: only {len(codes)} distinct series"
