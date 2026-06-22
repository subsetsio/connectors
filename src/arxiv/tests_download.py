"""Health invariants for the arXiv download — catch silent degradation that
file existence alone misses (empty payloads, format drift, broken ids)."""
from subsets_utils import list_raw_files, load_raw_parquet

# The snapshot stream writes sequential batches: arxiv-papers-<NNNN>.
_PREFIX = "arxiv-papers-"


def _batch_assets() -> list[str]:
    """Distinct batch asset ids for the papers snapshot, derived from raw files."""
    assets = set()
    for path in list_raw_files("arxiv-papers"):
        name = path.split("/")[-1]
        stem = name.split(".")[0]  # strip .parquet / .zst extensions
        if stem.startswith(_PREFIX):
            assets.add(stem)
    return sorted(assets)


def test_some_batches_written():
    """At least one batch must exist — zero means the stream produced nothing
    (object moved/renamed, bucket went private, or format change)."""
    assert _batch_assets(), "no arxiv-papers-* batches written"


def test_batches_nonempty_and_well_formed():
    """Every batch holds rows with non-null ids and the expected schema. Empty
    payloads or missing columns mean the snapshot JSON format changed."""
    expected = {
        "arxiv_id",
        "title",
        "abstract",
        "authors",
        "submitter",
        "primary_category",
        "categories",
        "doi",
        "journal_ref",
        "report_no",
        "comments",
        "num_versions",
        "created_date",
    }
    for asset in _batch_assets():
        table = load_raw_parquet(asset)
        assert table.num_rows > 0, f"{asset}: 0 rows"
        assert expected.issubset(set(table.column_names)), (
            f"{asset}: columns {table.column_names} missing some of {expected}"
        )
        ids = table.column("arxiv_id").to_pylist()
        assert all(i for i in ids), f"{asset}: null/empty arxiv_id present"


def test_created_date_derivable():
    """The submission date is derived from the arXiv id; a large majority of rows
    must yield a valid YYYY-MM-01 — a low rate means the id format drifted."""
    total = 0
    dated = 0
    for asset in _batch_assets():
        col = load_raw_parquet(asset).column("created_date").to_pylist()
        total += len(col)
        dated += sum(1 for v in col if v)
    assert total > 0, "no rows to check created_date"
    assert dated >= total * 0.95, (
        f"only {dated}/{total} rows have a derived created_date (< 95%)"
    )
