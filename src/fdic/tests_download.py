"""Post-DAG health invariants for the FDIC connector.

Catch silent degradation that file-existence alone misses: empty payloads,
pagination that stopped after page 1, or a curated column going entirely null
(field renamed/dropped upstream).
"""

from subsets_utils import load_raw_parquet

# Coarse floors per endpoint — well below live totals, high enough that a
# truncated crawl (stopped after one 10k page) trips the assertion.
MIN_ROWS = {
    "fdic-institutions": 25000,
    "fdic-financials": 1000000,
    "fdic-locations": 50000,
    "fdic-history": 100000,
    "fdic-failures": 3000,
    "fdic-sod": 1000000,
    "fdic-summary": 5000,
    "fdic-demographics": 100000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must have written rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_row_counts_above_floor(spec_ids):
    """Each endpoint should be near its full corpus, not truncated."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: only {n} rows (expected >= {floor})"


def test_cert_mostly_populated(spec_ids):
    """CERT is the core institution key on most endpoints; a fully-null CERT
    means the projection silently missed the field."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "CERT" not in table.column_names:
            continue
        col = table.column("CERT")
        non_null = len(col) - col.null_count
        assert non_null > 0, f"{sid}: CERT column is entirely null"
