"""Post-run health invariants for the CoinGecko raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet must hold rows — empty means the endpoint
    switched format, auth expired, or pagination broke silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_coins_catalog_large():
    """coins/list returns ~17k coins; a small count means the list endpoint
    degraded (rate-limit body, auth wall, format change)."""
    table = load_raw_parquet("coingecko-coins")
    assert len(table) >= 1000, f"coins catalog has {len(table)} rows; expected >=1000"


def test_history_has_multiple_coins():
    """The historical sweep should cover many coins and a long span; a single
    coin or a handful of rows means the top-N selection or the per-coin chart
    fetch broke."""
    table = load_raw_parquet("coingecko-coin-history")
    coins = set(table.column("coin_id").to_pylist())
    assert len(coins) >= 20, f"coin_history covers {len(coins)} coins; expected >=20"
    assert len(table) >= 10000, f"coin_history has {len(table)} rows; expected >=10000"


def test_global_single_row():
    """global is a single aggregate snapshot."""
    table = load_raw_parquet("coingecko-global")
    assert len(table) == 1, f"global has {len(table)} rows; expected exactly 1"
