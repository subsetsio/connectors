from subsets_utils import load_raw_parquet

# Per-catalog floor counts — well below the live corpus sizes (~1.9M models,
# ~450k datasets, ~650k spaces as of mid-2026) but high enough that a crawl
# that broke after the first page (cursor lost, auth flipped, format changed)
# trips the test instead of silently publishing a stub.
_MIN_ROWS = {
    "huggingface-models": 200_000,
    "huggingface-datasets": 50_000,
    "huggingface-spaces": 50_000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every catalog's raw parquet should hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_catalog_sizes_plausible(spec_ids):
    """Each catalog must clear its floor — guards against pagination breaking
    after page 1 (which would yield ~1000 rows, not hundreds of thousands)."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: got {n} rows; expected >= {floor}"


def test_ids_unique_and_present(spec_ids):
    """Repo id is the natural key — it must be present and (post-crawl) the
    dominant column. Heavy duplication means the cursor looped."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        ids = table.column("id").to_pylist()
        assert all(i for i in ids[:1000]), f"{sid}: null/empty ids in first 1000"
        distinct = len(set(ids))
        assert distinct >= 0.9 * len(ids), (
            f"{sid}: only {distinct} distinct ids of {len(ids)} — cursor likely looped"
        )
