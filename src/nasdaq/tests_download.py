"""Post-DAG health invariants for the Nasdaq connector.

Run in-connector after the download nodes, so loaders resolve the same raw the
fetch fns wrote (ndjson). Catch silent degradation: empty payloads, a screener
that quietly truncated, a per-symbol crawl that wrote no batches.
"""
from subsets_utils import load_raw_ndjson, list_raw_files

HIST = "nasdaq-historical-prices"


def test_simple_assets_nonempty(spec_ids):
    """Every non-batched download asset must hold rows. Empty usually means the
    endpoint changed shape or started dropping us."""
    for sid in spec_ids:
        if sid == HIST:
            continue
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson is empty"


def test_screener_universe_large(spec_ids):
    """Screeners list thousands of instruments; a small count means pagination
    broke or we were throttled mid-pull."""
    if "nasdaq-stocks" in spec_ids:
        assert len(load_raw_ndjson("nasdaq-stocks")) >= 3000, "stocks screener too small"
    if "nasdaq-etfs" in spec_ids:
        assert len(load_raw_ndjson("nasdaq-etfs")) >= 1000, "etf screener too small"


def test_historical_batches_present(spec_ids):
    """The per-symbol firehose writes batch files nasdaq-historical-prices-*;
    there must be many of them and they must carry OHLCV rows."""
    if HIST not in spec_ids:
        return
    files = list_raw_files(f"{HIST}-*")
    assert len(files) >= 10, f"only {len(files)} historical batch files; crawl likely incomplete"
    # spot-check the first batch holds typed-able rows
    sample = load_raw_ndjson(f"{HIST}-000000")
    assert sample, "first historical batch is empty"
    r0 = sample[0]
    for col in ("symbol", "date", "close"):
        assert col in r0, f"historical row missing column {col}"
