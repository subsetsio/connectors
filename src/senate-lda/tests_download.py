"""Post-DAG health invariants for the Senate LDA connector.

Raw is written in batches (one file per posting-month or per page-range), so
each download spec's data is a glob `<spec_id>-*` rather than a single file.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def _batch_ids(spec_id: str) -> list[str]:
    """Asset ids of the raw batches written under a download spec."""
    files = list_raw_files(f"{spec_id}-*")
    ids = []
    for f in files:
        name = f.rsplit("/", 1)[-1]
        # strip the first ndjson/json/parquet extension and everything after
        for ext in (".ndjson.zst", ".ndjson.gz", ".ndjson", ".json.gz", ".json"):
            if name.endswith(ext):
                name = name[: -len(ext)]
                break
        ids.append(name)
    return ids


def test_every_spec_has_raw_batches(spec_ids):
    """Each download spec must have written at least one raw batch. An empty
    glob means the crawl never produced data (endpoint/format/auth broke)."""
    for sid in spec_ids:
        assert _batch_ids(sid), f"{sid}: no raw batch files written"


def test_filings_rows_have_uuid(spec_ids):
    """Filings batches must carry filing_uuid + filing_year — the keys every
    downstream transform depends on. Catches a silently changed payload."""
    batches = _batch_ids("senate-lda-filings")
    assert batches, "no filings batches"
    rows = load_raw_ndjson(sorted(batches)[0])
    assert rows, "first filings batch is empty"
    sample = rows[0]
    assert sample.get("filing_uuid"), "filings row missing filing_uuid"
    assert sample.get("filing_year"), "filings row missing filing_year"


def test_activities_have_issue_codes(spec_ids):
    """Exploded activity rows must carry issue_code, the dimension that makes
    this subset distinct from filings. Empty/all-null means the explode broke."""
    batches = _batch_ids("senate-lda-lobbying-activities")
    assert batches, "no lobbying-activities batches"
    seen = set()
    for b in sorted(batches)[:3]:
        for r in load_raw_ndjson(b):
            if r.get("issue_code"):
                seen.add(r["issue_code"])
    assert len(seen) > 5, f"expected several distinct issue codes, got {seen}"
