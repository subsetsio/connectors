"""Health invariants for the PubMed download — catch silent degradation
(empty payloads, format drift, broken parsing) that file existence alone misses.
"""
from subsets_utils import list_raw_files, load_raw_parquet

EXPECTED_COLS = {
    "pmid", "title", "abstract", "journal", "pub_date", "authors", "mesh_terms",
}


def _batch_asset_ids() -> list[str]:
    return [p[:-len(".parquet")] for p in list_raw_files("pubmed-citations-*.parquet")]


def test_citation_batches_present():
    """The baseline is ~1,300 files -> one parquet batch each. If only a
    handful exist the crawl broke or the listing changed format."""
    ids = _batch_asset_ids()
    assert len(ids) >= 100, (
        f"only {len(ids)} citation batches present; expected >=100 "
        "(baseline crawl likely broke or was interrupted very early)"
    )


def test_batch_schema_and_nonempty():
    """Each batch must hold rows with the expected citation columns and real
    PMIDs — an empty or reshaped batch means the XML parse silently degraded."""
    ids = _batch_asset_ids()
    assert ids, "no citation batches found"
    # Sample a few batches rather than loading the whole corpus.
    for asset_id in sorted(ids)[:3]:
        table = load_raw_parquet(asset_id)
        assert len(table) > 0, f"{asset_id}: 0 rows"
        assert EXPECTED_COLS.issubset(set(table.column_names)), (
            f"{asset_id}: missing columns; got {table.column_names}"
        )
        pmids = table.column("pmid").to_pylist()
        assert any(p for p in pmids), f"{asset_id}: all PMIDs null"
