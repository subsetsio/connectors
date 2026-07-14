"""StatsWales connector — Welsh Government official statistics.

Mechanism: the StatsWales public API (https://api.stats.gov.wales/v1, no auth).
Each published dataset has a stable UUID and is served in full as a single
long-format CSV at GET /v1/{dataset_id}/download/csv. Every CSV shares the
shape: ``Data values, Data description, <one column per dimension>, Notes``.

Strategy: stateless full re-pull. One download node per dataset fetches the
whole CSV and stores it as Parquet. The corpus is ~755 small tables with no
incremental filter, so a full refresh each run is cheap and picks up revisions
for free; Parquet keeps downstream profiling and transforms from repeatedly
inferring large remote CSV files.

Integrity: the CSV endpoint answers over HTTP/2 with no Content-Length, so a
stream the server cuts short arrives as a *complete-looking* 200 with a short
body — a silent truncation no status check can catch. Run 20260712-135641 lost
>50% of two datasets that way (cc157acd: 16437 of 33810 rows). Every download
is therefore checked against an authoritative row count from the paginated view
endpoint (``page_info.total_records``) and retried on a short read, so a
truncated pull fails loudly instead of publishing a half table.
"""

import time
from io import BytesIO

import pandas as pd

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_file,
)

from constants import ENTITY_IDS

API_BASE = "https://api.stats.gov.wales/v1"

# A truncated read is transient (server-side stream cut under load), so a plain
# re-fetch is the fix; the row count is re-read each attempt so that a dataset
# legitimately republished mid-fetch settles instead of failing.
MAX_ATTEMPTS = 4
RETRY_BACKOFF_S = 2.0
_COUNT_PAGE_SIZE = 5  # the view endpoint's minimum; we only read page_info off it


def _entity_id(node_id: str) -> str:
    """Recover the dataset UUID from the spec id (strip the connector prefix)."""
    return node_id[len("statswales-"):]


def _expected_rows(dataset_id: str) -> int:
    """Authoritative row count for the dataset, straight from the API.

    Smallest page the view endpoint accepts is 5 rows; we only want the count
    that rides along in ``page_info``. Note the endpoint reports its own input
    errors as an embedded ``status`` in a 200 body, so a missing ``page_info``
    has to be raised by hand — ``raise_for_status`` never sees them.
    """
    url = f"{API_BASE}/{dataset_id}/view?page_size={_COUNT_PAGE_SIZE}&page_number=1"
    resp = get(url, timeout=(10.0, 60.0))
    resp.raise_for_status()
    body = resp.json()
    if "page_info" not in body:
        raise RuntimeError(
            f"{dataset_id}: view endpoint returned no page_info "
            f"(status={body.get('status')}, errors={body.get('errors')})"
        )
    return int(body["page_info"]["total_records"])


def _download_csv(dataset_id: str) -> bytes:
    url = f"{API_BASE}/{dataset_id}/download/csv"
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _entity_id(node_id)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        expected = _expected_rows(dataset_id)
        df = pd.read_csv(BytesIO(_download_csv(dataset_id)), dtype="string")
        if len(df) >= expected:
            break  # short reads are the failure mode; a grown table is a fresh publish
        if attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_BACKOFF_S * attempt)
    else:
        raise RuntimeError(
            f"{dataset_id}: truncated CSV download — got {len(df)} rows, "
            f"expected {expected} (view page_info.total_records) "
            f"after {MAX_ATTEMPTS} attempts"
        )

    out = BytesIO()
    df.to_parquet(out, index=False)
    save_raw_file(out.getvalue(), asset, extension="parquet")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"statswales-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
