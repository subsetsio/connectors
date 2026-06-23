"""Health invariants for the DSEC Macao raw assets, run post-DAG in-connector."""

from subsets_utils import load_raw_parquet


def test_indicators_nonempty_and_has_leaves(spec_ids):
    """The catalog must hold thousands of nodes, most of them leaf indicators.
    A near-empty or all-branch catalog means the tree walk degraded."""
    if "dsec-macao-indicators" not in spec_ids:
        return
    t = load_raw_parquet("dsec-macao-indicators")
    assert len(t) >= 5000, f"indicators: only {len(t)} nodes, expected ~9896"
    leaves = sum(1 for v in t.column("is_leaf").to_pylist() if v)
    assert leaves >= 4000, f"indicators: only {leaves} leaf nodes, expected ~7911"


def test_values_nonempty_and_multiperiod(spec_ids):
    """The values table must hold many observations spanning multiple period
    types; a single-period or tiny result means batches failed silently."""
    if "dsec-macao-values" not in spec_ids:
        return
    t = load_raw_parquet("dsec-macao-values")
    assert len(t) >= 100000, f"values: only {len(t)} rows, expected >100k"
    periods = set(t.column("data_period").to_pylist())
    assert "Yearly" in periods, f"values: no Yearly rows (got {periods})"
    assert len(periods) >= 2, f"values: only one period type present ({periods})"
    n_ind = len(set(t.column("indicator_id").to_pylist()))
    assert n_ind >= 3000, f"values: only {n_ind} distinct indicators, expected thousands"
