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

Integrity: the CSV endpoint answers with no Content-Length (chunked over
HTTP/1.1, DATA frames over HTTP/2), so a stream cut short arrives as a
*complete-looking* 200 with a short body — a silent truncation no status check
can catch. Run 20260712-135641 lost >50% of two datasets that way (cc157acd:
16437 of 33810 rows). Every download is therefore checked against an
authoritative row count from the paginated view endpoint
(``page_info.total_records``) and retried on a short read.

Caching: the API sits behind a shared CDN (``cache-control: public, max-age=60``,
``x-cache: TCP_HIT``) that has no length to validate against either, so it will
happily store and re-serve a truncated body. That makes a short read *sticky*,
not transient: run 20260714-101546 lost 17 datasets whose 4 retries — 12s of
backoff, all inside the 60s TTL — re-read the same poisoned entry and returned
the identical short body in under a second each. A ``Cache-Control: no-cache``
request header does not help; the CDN ignores it. A unique query parameter is
the only lever that reaches the origin, so every fetch carries one (verified
payload-neutral: the origin ignores the extra param and returns byte-identical
CSV). Datasets are pulled once per run, so bypassing a 60s cache costs nothing.
"""

import time
import uuid
from io import BytesIO

import pandas as pd

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_file,
)

from constants import ENTITY_IDS

API_BASE = "https://api.stats.gov.wales/v1"

# A truncated read is a cut origin stream, which a plain re-fetch fixes only if
# it actually reaches the origin — see the CDN note above. The row count is
# re-read each attempt so a dataset legitimately republished mid-fetch settles
# instead of failing.
MAX_ATTEMPTS = 4
RETRY_BACKOFF_S = 2.0
_COUNT_PAGE_SIZE = 5  # the view endpoint's minimum; we only read page_info off it


def _entity_id(node_id: str) -> str:
    """Recover the dataset UUID from the spec id (strip the connector prefix)."""
    return node_id[len("statswales-"):]


def _uncached(url: str) -> str:
    """Append a single-use parameter so the CDN has to go to the origin.

    Both endpoints ignore unknown query params, and the cache keys on the full
    URL, so a value nothing else will reuse turns every fetch into a TCP_MISS.
    """
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}_cb={uuid.uuid4().hex}"


def _expected_rows(dataset_id: str) -> int:
    """Authoritative row count for the dataset, straight from the API.

    Smallest page the view endpoint accepts is 5 rows; we only want the count
    that rides along in ``page_info``. Note the endpoint reports its own input
    errors as an embedded ``status`` in a 200 body, so a missing ``page_info``
    has to be raised by hand — ``raise_for_status`` never sees them.
    """
    url = f"{API_BASE}/{dataset_id}/view?page_size={_COUNT_PAGE_SIZE}&page_number=1"
    resp = get(_uncached(url), timeout=(10.0, 60.0))
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
    resp = get(_uncached(url), timeout=(10.0, 180.0))
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
