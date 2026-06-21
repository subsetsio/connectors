from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. An empty payload
    usually means the blob endpoint changed format or returned an error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_cover_all_indices(spec_ids):
    """The long-format values asset must carry all 16 OBMMI indices; fewer
    means a series was dropped during flattening or the source shape changed."""
    table = load_raw_parquet("optimal-blue-values")
    names = set(table.column("index_name").to_pylist())
    assert len(names) == 16, f"expected 16 distinct indices, got {len(names)}: {sorted(names)}"
