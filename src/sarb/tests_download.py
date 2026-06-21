"""Health-invariant tests for the SARB connector raw assets.

These run post-DAG, in-connector, against the data through subsets_utils
loaders — they catch silent degradation (truncated download, format flip,
locale-parse wipeout) that file existence alone misses.
"""
from subsets_utils import load_raw_parquet


def test_values_nonempty(spec_ids):
    """The single raw asset must hold a substantial number of observations.
    On probe (2026-06-19) the 17 release groups totalled well over 100k rows;
    a big drop means a group's bulk endpoint truncated or changed format."""
    table = load_raw_parquet("sarb-values")
    assert len(table) >= 50_000, f"sarb-values: only {len(table)} rows (expected >=50k)"


def test_multiple_release_groups(spec_ids):
    """Every DataType group should be represented — if the per-group loop broke
    after the first group we'd see only one data_type."""
    table = load_raw_parquet("sarb-values")
    groups = set(table.column("data_type").to_pylist())
    assert len(groups) >= 12, f"only {len(groups)} release groups present: {sorted(groups)}"


def test_value_period_present(spec_ids):
    """Value and Period are the columns the transform types; they must be
    populated (a format change would null them out and yield an empty table)."""
    table = load_raw_parquet("sarb-values")
    sample = table.slice(0, 2000)
    vals = sample.column("value").to_pylist()
    periods = sample.column("period").to_pylist()
    assert any(v not in (None, "") for v in vals), "value column entirely empty in sample"
    assert any(p not in (None, "") for p in periods), "period column entirely empty in sample"
