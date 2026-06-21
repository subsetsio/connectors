"""Health-invariant tests for the CBS connector — catch silent degradation
(empty payloads, broken pagination, format switches) that file-existence misses."""

from subsets_utils import list_raw_files, load_raw_parquet

SLUG = "central-bureau-of-statistics"

# Batched (multi-file) download assets — written as one parquet per subject/chapter.
_BATCHED = {f"{SLUG}-series-values", f"{SLUG}-price-index-values"}


def test_single_assets_nonempty(spec_ids):
    """Single-file download assets must hold rows. Empty usually means the
    endpoint switched format, auth/UA broke, or the crawl stopped at page 1."""
    for sid in spec_ids:
        if sid in _BATCHED:
            continue
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def _batch_total(prefix, min_files):
    files = list_raw_files(f"{prefix}-*.parquet")
    assert len(files) >= min_files, f"only {len(files)} {prefix} batch files; crawl likely broke"
    total = 0
    for rel in files:
        # rel is "<asset_id>.parquet"; strip the extension to get the asset id.
        total += len(load_raw_parquet(rel[:-len(".parquet")]))
    return total


def test_series_values_batches_nonempty():
    """series-values writes one parquet per subject; expect many batches with rows."""
    assert _batch_total(f"{SLUG}-series-values", 10) > 0, "series-values batches have 0 rows"


def test_price_values_batches_nonempty():
    """price-index-values writes one parquet per chapter; expect several with rows."""
    assert _batch_total(f"{SLUG}-price-index-values", 5) > 0, "price-index-values batches have 0 rows"
