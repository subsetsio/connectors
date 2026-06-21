"""Health-invariant tests for DBT raw downloads.

Each download node saves its raw payload as NDJSON (gzip) via save_raw_ndjson.
We assert every download wrote a raw file with rows — empty/missing payloads
usually mean the data endpoint switched format, the `latest` redirect broke, or
the source returned an error page in place of data. Column-level shape is
covered by the per-node expectation specs under tests/.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def _download_ids(spec_ids):
    """spec_ids carries both download and transform node ids; only download
    nodes write a raw asset, so the SQL-transform leaves are filtered out."""
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_every_download_wrote_raw(spec_ids):
    """Every download spec must have produced a raw NDJSON file."""
    for sid in _download_ids(spec_ids):
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"


def test_small_tables_have_rows_and_columns(spec_ids):
    """Load the small reference tables fully and confirm they decode to
    multi-column records (catches a parse/format regression that would yield
    a single blob column or an empty file). The large tariff tables are left
    to the streaming expectation specs to avoid loading millions of rows here."""
    small = {
        "dbt-market-barriers--barriers",
        "dbt-orp-regulations--uk-regulatory-documents",
        "dbt-uk-trade-quotas--quotas",
    }
    for sid in _download_ids(spec_ids):
        if sid not in small:
            continue
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: NDJSON decoded to 0 rows"
        assert len(rows[0]) >= 3, (
            f"{sid}: first record has only {len(rows[0])} column(s) — "
            "CSV likely failed to split into fields"
        )
