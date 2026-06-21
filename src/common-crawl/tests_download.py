"""Health invariants for the Common Crawl statistics download.

Raw is written as one parquet batch per crawl (`common-crawl-statistics-<CRAWL>`),
so we discover the batches via `list_raw_files` and load each with the same
loader the download node used.
"""
from subsets_utils import list_raw_files, load_raw_parquet

EXPECTED_COLUMNS = {"crawl_id", "crawl_date", "metric_family", "key", "count"}


def _batch_asset_ids(sid: str) -> list[str]:
    """Relative parquet files for a batched asset -> bare asset ids."""
    rels = list_raw_files(f"{sid}-*.parquet")
    return [r[: -len(".parquet")] for r in rels]


def test_statistics_batches_present(spec_ids):
    """The statistics spec must have produced at least one per-crawl batch.
    Common Crawl has well over 100 crawls, so a handful means the enumeration
    or download silently broke."""
    for sid in spec_ids:
        batches = _batch_asset_ids(sid)
        assert len(batches) >= 100, (
            f"{sid}: only {len(batches)} crawl batches found (expected 100+)"
        )


def test_statistics_batches_nonempty_and_well_formed(spec_ids):
    """Every batch holds rows, has the expected schema, carries positive counts,
    and the crawl id matches its batch name. Empty or malformed batches mean the
    stats format drifted under us."""
    for sid in spec_ids:
        for asset in _batch_asset_ids(sid):
            table = load_raw_parquet(asset)
            assert len(table) > 0, f"{asset}: raw parquet has 0 rows"
            assert EXPECTED_COLUMNS.issubset(set(table.column_names)), (
                f"{asset}: columns {table.column_names} missing {EXPECTED_COLUMNS}"
            )
            crawl_ids = set(table.column("crawl_id").to_pylist())
            expected_id = asset[len(sid) + 1:]
            assert crawl_ids == {expected_id}, (
                f"{asset}: crawl_id values {crawl_ids} != {{{expected_id}}}"
            )
            counts = table.column("count").to_pylist()
            assert all(c is not None and c >= 0 for c in counts), (
                f"{asset}: found null/negative counts"
            )
            families = set(table.column("metric_family").to_pylist())
            assert families, f"{asset}: no metric families present"
