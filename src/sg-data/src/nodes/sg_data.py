"""Data.gov.sg (sg-data) connector — catalog of CSV statistical tables.

data.gov.sg is a heterogeneous government data portal: every dataset has its
own column schema, so each rank-accepted dataset becomes its own published
Delta table (one download + one passthrough transform per dataset).

Fetch mechanism (research's chosen `bulk_download`):
  GET https://api-open.data.gov.sg/v1/public/api/datasets/{id}/poll-download
  -> when data.status == "DOWNLOAD_SUCCESS", data.url is a short-lived signed
     AWS S3 URL to the COMPLETE dataset CSV (no pagination). Cold datasets need
     an initiate-download first to materialize the CSV server-side, then polling
     until ready. The signed S3 fetch does not count against the API quota.

Rate limit: the api-open download API hard-caps ~5 requests/minute per IP
(429 on exceed); there is no API key provisioned, so every call rides
`transient_retry` (retries 429/5xx with backoff) and we poll-first so an
already-materialized dataset costs a single request.

Shape: stateless full re-pull — the source exposes no delta endpoint, so each
refresh fetches the full per-dataset CSV snapshot and overwrites. The raw CSV
is saved as-is (`save_raw_file(..., extension="csv")`); the transform is a thin
`SELECT *` passthrough because the column set differs per dataset and DuckDB's
read_csv_auto types it on read.
"""

import time

from subsets_utils import NodeSpec, get, save_raw_file, transient_retry
from constants import ENTITY_IDS

_API = "https://api-open.data.gov.sg/v1/public/api/datasets"
_POLL_ATTEMPTS = 60          # ~ up to a few minutes of server-side materialization
_POLL_INTERVAL = 4.0         # seconds between polls (spaces requests under the cap)


# Reverse map: spec id -> original datasetId. The spec id mangles the id's
# underscores to dashes (d_abc -> sg-data-d-abc), which is not invertible by
# string surgery, so we recover the exact datasetId from the entity union.
_ID_BY_NODE = {
    f"sg-data-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


def _dataset_id(node_id: str) -> str:
    """Recover the data.gov.sg datasetId (d_...) from the spec id."""
    return _ID_BY_NODE[node_id]


@transient_retry(attempts=12, min_wait=8, max_wait=240)
def _poll(dataset_id: str) -> dict:
    resp = get(f"{_API}/{dataset_id}/poll-download", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return (resp.json() or {}).get("data") or {}


@transient_retry(attempts=12, min_wait=8, max_wait=240)
def _initiate(dataset_id: str) -> None:
    resp = get(f"{_API}/{dataset_id}/initiate-download", timeout=(10.0, 120.0))
    resp.raise_for_status()


@transient_retry(attempts=8, min_wait=4, max_wait=120)
def _download_csv(url: str) -> bytes:
    # Signed S3 URL — full CSV body, unsigned-quota (not rate-limited).
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _signed_url(dataset_id: str) -> str:
    """Resolve the signed CSV URL, materializing the download if needed."""
    # Fast path: an already-materialized dataset returns the URL on first poll.
    data = _poll(dataset_id)
    if data.get("status") == "DOWNLOAD_SUCCESS" and data.get("url"):
        return data["url"]

    # Cold path: kick off materialization, then poll until ready.
    _initiate(dataset_id)
    for _ in range(_POLL_ATTEMPTS):
        data = _poll(dataset_id)
        status = data.get("status")
        if status == "DOWNLOAD_SUCCESS" and data.get("url"):
            return data["url"]
        if status and status not in ("DOWNLOAD_IN_PROGRESS", "INITIATED", "PROCESSING"):
            raise RuntimeError(f"{dataset_id}: unexpected download status {status!r}")
        time.sleep(_POLL_INTERVAL)
    raise TimeoutError(f"{dataset_id}: CSV not ready after {_POLL_ATTEMPTS} polls")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _dataset_id(node_id)
    url = _signed_url(dataset_id)
    csv_bytes = _download_csv(url)
    save_raw_file(csv_bytes, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"sg-data-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
