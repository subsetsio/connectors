"""Post-DAG health invariants for Teranet-National Bank raw assets."""

import pyarrow.compute as pc

from subsets_utils import load_raw_parquet


def test_observations_nonempty_long_history():
    table = load_raw_parquet("teranet-national-bank-hpi-observations")
    assert len(table) >= 10_000, f"observations: only {len(table)} rows"
    cols = set(table.column_names)
    expected = {"index_id", "period", "index_value", "sales_pair_count"}
    missing = expected - cols
    assert not missing, f"observations: missing columns {sorted(missing)}"

    index_ids = set(table.column("index_id").to_pylist())
    assert "c11" in index_ids, "observations: missing Composite 11 series"
    assert "bc_vancouver" in index_ids, "observations: missing Vancouver series"


def test_observations_values_present():
    table = load_raw_parquet("teranet-national-bank-hpi-observations")
    nonnull = pc.sum(pc.is_valid(table.column("index_value"))).as_py()
    assert nonnull >= 8_000, f"observations: only {nonnull} non-null index values"


def test_series_metadata_complete():
    table = load_raw_parquet("teranet-national-bank-hpi-series")
    assert len(table) >= 30, f"series: only {len(table)} rows"
    assert table.column("index_id").null_count == 0, "series: null index_id present"
    assert table.column("name").null_count == 0, "series: null name present"

    index_ids = set(table.column("index_id").to_pylist())
    assert "c11" in index_ids, "series: missing Composite 11 profile"
    assert "mc" in index_ids, "series: missing All Metropolitan Areas profile"
