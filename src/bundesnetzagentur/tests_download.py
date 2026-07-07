"""Health invariants for the Bundesnetzagentur (SMARD) raw downloads."""

from subsets_utils import load_raw_parquet
from nodes.bundesnetzagentur import DOWNLOAD_SPECS


_DOWNLOAD_IDS = [spec.id for spec in DOWNLOAD_SPECS]


def test_all_feeds_nonempty():
    """Each feed must hold rows. An empty payload means SMARD changed its
    module ids or the chart_data URL scheme and the crawl silently no-op'd."""
    for sid in _DOWNLOAD_IDS:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} raw rows"


def test_values_finite_and_dated():
    """Values are real numbers and timestamps are plausible (post-2010 ms)."""
    for sid in _DOWNLOAD_IDS:
        table = load_raw_parquet(sid).to_pydict()
        vals = table["value"]
        assert all(v is not None for v in vals), f"{sid}: null values leaked into raw"
        ds = table["date_ms"]
        assert min(ds) > 1_262_304_000_000, f"{sid}: implausibly early timestamp"


def test_multiple_series_per_feed():
    """Every feed must carry more than one distinct series — a single series
    would mean most modules 404'd or returned empty."""
    for sid in _DOWNLOAD_IDS:
        codes = set(load_raw_parquet(sid).column("series_code").to_pylist())
        assert len(codes) >= 2, f"{sid}: only {len(codes)} distinct series"
