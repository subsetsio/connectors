"""Health-invariant tests for the SEC connector's raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used to write. They catch silent degradation (empty payloads, blocked UA
returning an error body, Frames format change) that file-existence misses.
"""
from subsets_utils import list_raw_files, load_raw_parquet

EXPECTED_COMPANY_COLS = {"cik", "name", "ticker", "exchange"}


def test_companies_reasonable():
    """company_tickers_exchange.json carried ~10,400 filers when probed; far
    fewer means a truncated download or the UA was rejected (403 body)."""
    t = load_raw_parquet("sec-companies")
    assert t.num_rows >= 5000, f"sec-companies has only {t.num_rows} rows"
    assert EXPECTED_COMPANY_COLS <= set(t.column_names), t.column_names


def test_concepts_present_and_labelled():
    """One row per curated concept, and most should carry an upstream label —
    if labels are all null the Frames metadata probe silently failed."""
    t = load_raw_parquet("sec-concepts")
    assert t.num_rows >= 20, f"sec-concepts has only {t.num_rows} rows"
    labels = [x for x in t.column("label").to_pylist() if x]
    assert len(labels) >= 15, f"only {len(labels)} concepts resolved a label"


def test_facts_batches_nonempty():
    """Facts are written as one parquet batch per concept (sec-facts-*). Expect
    many batches and a substantial total row count across all filers/periods."""
    files = list_raw_files("sec-facts-*.parquet")
    assert len(files) >= 10, f"only {len(files)} facts batches written"
    total = 0
    for rel in files:
        asset = rel[: -len(".parquet")]
        t = load_raw_parquet(asset)
        assert t.num_rows > 0, f"{asset}: 0 rows"
        total += t.num_rows
    assert total >= 100_000, f"facts total rows {total:,} unexpectedly low"
