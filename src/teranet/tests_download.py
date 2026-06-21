"""Health invariants for the Teranet HPI raw asset."""
import datetime as dt

from subsets_utils import load_raw_parquet


def test_values_nonempty():
    table = load_raw_parquet("teranet-values")
    assert len(table) > 0, "teranet-values: raw parquet has 0 rows"


def test_values_has_composite_and_metros():
    """C11 composite plus the 11 metros must all be present."""
    table = load_raw_parquet("teranet-values")
    markets = set(table.column("market").to_pylist())
    assert "c11" in markets, "C11 composite missing"
    assert len(markets) >= 12, f"expected >=12 markets, got {len(markets)}: {sorted(markets)}"


def test_values_long_history_and_fresh():
    """History should reach back to the 1990s and run to within ~6 months of today —
    catches a truncated download or a stalled feed."""
    table = load_raw_parquet("teranet-values")
    dates = table.column("date").to_pylist()
    dmin, dmax = min(dates), max(dates)
    assert dmin.year <= 1991, f"history starts too late: {dmin}"
    cutoff = dt.date.today() - dt.timedelta(days=200)
    assert dmax >= cutoff, f"latest month {dmax} is stale (cutoff {cutoff})"


def test_values_index_in_plausible_range():
    """Index values are positive and not absurd (base 100 = June 2005)."""
    table = load_raw_parquet("teranet-values")
    idx = [v for v in table.column("index").to_pylist() if v is not None]
    assert idx, "no non-null index values"
    assert min(idx) > 0, f"non-positive index value: {min(idx)}"
    assert max(idx) < 2000, f"implausibly large index value: {max(idx)}"
