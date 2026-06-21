"""Health-invariant tests for the Apple charts connector.

Run post-DAG, in-connector, against the raw assets the download nodes wrote.
They catch silent degradation that file-existence alone misses: empty/truncated
charts, a feed that switched format, or storefront-sweep collapse.
"""
from subsets_utils import load_raw_ndjson

# Charts cap at 100 entries; a healthy media sweeps many storefronts, so each
# asset should hold well more than a single chart's worth of rows.
_MIN_ROWS = 100

_REQUIRED_KEYS = {
    "snapshot_date", "storefront", "media", "feed_type", "rank", "entity_id",
}


def _download_ids(spec_ids):
    """spec_ids carries every DAG node (downloads AND transforms). Only the
    download nodes write raw NDJSON, so the transform leaves (id ends in
    '-transform') would raise FileNotFoundError if loaded — filter them out."""
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. An empty payload usually means the
    feed switched format or every storefront request failed silently."""
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        assert len(rows) >= _MIN_ROWS, f"{sid}: only {len(rows)} rows (< {_MIN_ROWS})"


def test_required_columns_present(spec_ids):
    """Each row must carry the long-format key dimensions; a missing key means
    the parse drifted from the feed shape."""
    for sid in _download_ids(spec_ids):
        row = load_raw_ndjson(sid)[0]
        missing = _REQUIRED_KEYS - set(row)
        assert not missing, f"{sid}: row missing keys {missing}"


def test_multiple_storefronts(spec_ids):
    """A working sweep collects more than one storefront. Collapse to a single
    storefront signals the cross-country sweep broke (throttling / skips)."""
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        storefronts = {r.get("storefront") for r in rows}
        assert len(storefronts) > 1, f"{sid}: only storefronts {storefronts}"


def test_rank_is_positive_int(spec_ids):
    """Rank is the chart position — a positive integer on every row."""
    for sid in _download_ids(spec_ids):
        for r in load_raw_ndjson(sid):
            rank = r.get("rank")
            assert isinstance(rank, int) and rank >= 1, f"{sid}: bad rank {rank!r}"
            break
