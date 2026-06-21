"""Post-DAG health invariants for the NBP connector."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet must hold rows. Empty usually means the
    endpoint changed format or every window 404'd."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_mid_has_both_tables(spec_ids):
    """The mid asset must carry both table A and table B rows — if one
    endpoint silently broke we'd see only one."""
    sid = "narodowy-bank-polski-exchange-rates-mid"
    if sid not in spec_ids:
        return
    tables = set(load_raw_parquet(sid).column("table").to_pylist())
    assert {"A", "B"} <= tables, f"expected tables A and B, got {tables}"


def test_mid_long_history(spec_ids):
    """Mid rates run back to 2002; a truncated crawl would start much later."""
    sid = "narodowy-bank-polski-exchange-rates-mid"
    if sid not in spec_ids:
        return
    dates = load_raw_parquet(sid).column("date").to_pylist()
    assert min(dates) <= "2003-01-01", f"earliest mid date too late: {min(dates)}"


def test_bid_ask_present(spec_ids):
    """Table C bid/ask must be non-null floats for a sane share of rows."""
    sid = "narodowy-bank-polski-exchange-rates-bid-ask"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    bids = [b for b in t.column("bid").to_pylist() if b is not None]
    assert len(bids) > 0.9 * len(t), f"too many null bids in {sid}"
