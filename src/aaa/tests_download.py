"""Health invariants for the AAA fuel-price connector.

Raw is written as date-keyed batches (`<spec-id>-<YYYY-MM-DD>.parquet`), so we
enumerate batches with list_raw_files and load each by its asset id. Catches the
silent-degradation modes file existence alone misses: a Cloudflare challenge page
parsed into 0 rows, or the price column quietly going all-null after a markup
change.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def _batches(spec_id: str):
    files = list_raw_files(f"{spec_id}-*.parquet")
    return [f[:-len(".parquet")] for f in files]


def test_every_spec_has_a_nonempty_batch(spec_ids):
    for sid in spec_ids:
        batches = _batches(sid)
        assert batches, f"{sid}: no raw batch files written"
        total = sum(len(load_raw_parquet(b)) for b in batches)
        assert total > 0, f"{sid}: all raw batches are empty"


def test_prices_present_and_positive(spec_ids):
    """Every batch must carry real positive prices; an all-null/zero price column
    means the table markup changed and we parsed labels but no numbers."""
    for sid in spec_ids:
        for b in _batches(sid):
            t = load_raw_parquet(b)
            if len(t) == 0:
                continue
            prices = [p for p in t.column("price_usd").to_pylist() if p is not None]
            assert prices, f"{b}: price_usd is entirely null"
            assert min(prices) > 0, f"{b}: non-positive price {min(prices)}"
