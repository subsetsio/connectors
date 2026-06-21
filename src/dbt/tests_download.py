"""Health-invariant tests for DBT raw downloads.

Each download node saves its raw payload as NDJSON (gzip) via save_raw_ndjson.
We assert every download produced a raw asset, and that the small text-heavy
tables split into multiple columns (the failure mode that once collapsed the
market-barriers table into a single blob column). Non-emptiness of every table
is already guaranteed by the transform layer — a 0-row SQL transform fails its
node — so the big tariff tables are not fully loaded here.

Loads/lists are retried briefly: in the cloud the health stage runs immediately
after the DAG and an R2 list/read can momentarily lag a just-written object.
"""

import time

from subsets_utils import list_raw_files, load_raw_ndjson

# Small, text-heavy reference tables worth fully decoding to catch a parse
# regression. The large tariff tables (millions of rows) are left to the
# per-node expectation specs to avoid loading them into the health stage.
_SMALL = {
    "dbt-market-barriers--barriers",
    "dbt-orp-regulations--uk-regulatory-documents",
    "dbt-uk-trade-quotas--quotas",
    "dbt-uk-trade-quotas--report--quotas-including-current-volumes",
}


def _download_ids(spec_ids):
    """spec_ids carries both download and transform node ids; only download
    nodes write a raw asset, so the SQL-transform leaves are filtered out."""
    return [s for s in spec_ids if not s.endswith("-transform")]


def _retry(fn, attempts=5, delay=3):
    """Call fn() until it returns a truthy value; tolerate brief R2
    read-after-write / list lag, including a transient missing-object that
    surfaces as FileNotFoundError."""
    result = None
    for _ in range(attempts):
        try:
            result = fn()
        except FileNotFoundError:
            result = None
        if result:
            return result
        time.sleep(delay)
    return result


def test_every_download_wrote_raw(spec_ids):
    """Every download spec must have produced a raw NDJSON file."""
    for sid in _download_ids(spec_ids):
        files = _retry(lambda: list_raw_files(f"{sid}.*"))
        assert files, f"{sid}: no raw file written"


def test_small_tables_have_rows_and_columns(spec_ids):
    """The small text tables must decode to multi-column records — a single
    column means a CSV failed to split into fields."""
    for sid in _download_ids(spec_ids):
        if sid not in _SMALL:
            continue
        rows = _retry(lambda: load_raw_ndjson(sid))
        assert rows, f"{sid}: NDJSON decoded to 0 rows"
        assert len(rows[0]) >= 3, (
            f"{sid}: first record has only {len(rows[0])} column(s) — "
            "raw likely failed to parse into fields"
        )
