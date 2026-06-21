"""Health invariants for the SNB connector raw downloads.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
node used to save. Catches silent degradation that file-existence alone misses:
schema drift, mass-empty payloads, all-null value columns.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "cube_id", "series_key", "series_label",
    "frequency", "unit", "scale", "period", "value",
}


def test_raw_assets_schema_and_nonempty(spec_ids):
    """Every cube's raw parquet must carry the expected long-format columns,
    and effectively all of them must hold rows. A widespread empty/missing set
    means the JSON endpoint changed shape or the warehouse '@'->'.' rewrite
    broke; we tolerate at most a tiny handful of genuinely retired cubes."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == _EXPECTED_COLS, (
            f"{sid}: columns {sorted(table.column_names)} != expected"
        )
        if table.num_rows == 0:
            empty.append(sid)
    tolerance = max(2, len(spec_ids) // 50)  # ~2% slack for retired cubes
    assert len(empty) <= tolerance, (
        f"{len(empty)} of {len(spec_ids)} raw assets are empty "
        f"(tolerance {tolerance}); first few: {empty[:10]}"
    )


def test_value_column_has_real_numbers(spec_ids):
    """Across the corpus there must be a substantial body of non-null numeric
    observations — guards against an all-null degenerate pull where every cube
    technically has rows but no actual values."""
    import pyarrow.compute as pc

    total_nonnull = 0
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            continue
        total_nonnull += table.num_rows - pc.sum(
            pc.is_null(table.column("value"))
        ).as_py()
    assert total_nonnull >= 10_000, (
        f"only {total_nonnull} non-null observations across all cubes; "
        "expected tens of thousands"
    )
