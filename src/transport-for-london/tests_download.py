"""Health invariants run post-DAG, in-connector, through the subsets_utils loaders."""

from subsets_utils import list_raw_files, load_raw_parquet


def test_each_spec_produced_raw(spec_ids):
    """Every download spec must leave at least one raw parquet — either a single
    asset file (accident-stats) or batch files (the bucket-backed assets)."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.parquet") or list_raw_files(f"{sid}-*.parquet")
        assert files, f"{sid}: no raw parquet produced (empty download?)"


def test_accident_stats_nonempty():
    """The single-asset AccidentStats parquet should hold many years of records."""
    table = load_raw_parquet("transport-for-london-accident-stats")
    assert table.num_rows > 1000, f"accident-stats raw has only {table.num_rows} rows"
