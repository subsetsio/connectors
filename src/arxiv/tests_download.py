"""Health invariants for the arXiv download — catch silent degradation that
file existence alone misses (empty payloads, format drift, broken ids)."""
from subsets_utils import list_raw_files, load_raw_parquet

# The firehose writes month-aligned batches: arxiv-papers-<from>_<until>.
_PREFIX = "arxiv-papers-"


def _batch_assets() -> list[str]:
    """Distinct batch asset ids for the papers firehose, derived from raw files."""
    assets = set()
    for path in list_raw_files("arxiv-papers"):
        name = path.split("/")[-1]
        stem = name.split(".")[0]  # strip .parquet / .zst extensions
        if stem.startswith(_PREFIX):
            assets.add(stem)
    return sorted(assets)


def test_some_batches_written():
    """At least one month batch must exist — zero means the harvest produced
    nothing (endpoint moved, auth/format change, or watermark stuck)."""
    assert _batch_assets(), "no arxiv-papers-* batches written"


def test_batches_nonempty_and_well_formed():
    """Every batch holds rows with non-null ids and the expected schema. Empty
    payloads or missing columns usually mean the OAI response format changed."""
    expected = {
        "arxiv_id",
        "title",
        "abstract",
        "authors",
        "primary_category",
        "categories",
        "doi",
        "journal_ref",
        "comments",
        "license",
        "created",
        "updated",
        "datestamp",
    }
    for asset in _batch_assets():
        table = load_raw_parquet(asset)
        assert table.num_rows > 0, f"{asset}: 0 rows"
        assert expected.issubset(set(table.column_names)), (
            f"{asset}: columns {table.column_names} missing some of {expected}"
        )
        ids = table.column("arxiv_id").to_pylist()
        assert all(i for i in ids), f"{asset}: null/empty arxiv_id present"
