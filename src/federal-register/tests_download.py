"""Health invariants for the Federal Register download nodes.

Run post-DAG, in-connector, so data is read back through the same
subsets_utils loaders the fetch fns used to write it. These catch silent
degradation that file-existence checks miss: empty payloads, truncated
crawls, a year batch that came back with the wrong shape.
"""
from subsets_utils import load_raw_parquet, list_raw_files


def test_agencies_nonempty():
    """The agency taxonomy is ~470 records; a near-empty pull means the
    endpoint changed format or returned an error envelope."""
    table = load_raw_parquet("federal-register-agencies")
    assert len(table) >= 300, f"agencies: only {len(table)} rows (expected ~470)"
    assert "id" in table.column_names, "agencies: missing id column"


def test_documents_batches_present_and_nonempty():
    """Documents are written one parquet batch per publication year
    (federal-register-documents-<year>). At least a few year batches should
    exist and each should hold rows — an empty batch means a year crawl
    silently produced nothing."""
    batches = list_raw_files("federal-register-documents-*.parquet")
    assert batches, "documents: no per-year batch files were written"
    total = 0
    for b in batches:
        # asset id is the file path without the .parquet extension
        asset_id = b.rsplit("/", 1)[-1][: -len(".parquet")]
        table = load_raw_parquet(asset_id)
        assert len(table) > 0, f"documents batch {b}: 0 rows"
        assert "document_number" in table.column_names, f"documents batch {b}: missing document_number"
        total += len(table)
    assert total >= 1000, f"documents: only {total} rows across all year batches"
