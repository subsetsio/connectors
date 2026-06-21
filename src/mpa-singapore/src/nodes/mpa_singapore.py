"""Maritime and Port Authority of Singapore (MPA) — maritime statistics.

Source: data.gov.sg. MPA publishes ~22 monthly/annual maritime time-series
datasets (container/cargo throughput, bunker sales, vessel & tanker arrivals,
vessel calls, registered vessels). Each dataset is one CSV with a stable but
dataset-specific column list.

Fetch strategy: stateless full re-pull (shape 1). Each dataset is a small CSV
(hundreds-to-thousands of rows), so we re-fetch the whole table every run and
overwrite — revisions and late corrections come for free. No watermark/cursor.

Access (chosen mechanism `datagov_bulk_csv`): GET
.../datasets/{id}/poll-download returns {data:{status:"DOWNLOAD_SUCCESS",
url:<presigned S3 csv>}}; the S3 URL delivers the entire table in one request.
data.gov.sg rate-limits aggressively, returning HTTP 200 with
{code:24,name:"TOO_MANY_REQUESTS"} rather than a 429 — that body is treated as
transient and retried with backoff. The presigned URL is short-lived, so it is
resolved immediately before each download and re-resolved if S3 returns 403.

No machine-readable schema is published; the time column is `month` (YYYY-MM)
for monthly datasets and `year` (YYYY) for annual ones. The transform casts it
to a real date / integer and leaves the (already typed) measure columns intact.
"""

import csv
import io

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

# --- entity union (rank-active datasets) -----------------------------------
from constants import ENTITY_IDS

# Datasets whose time column is annual (`year`, YYYY); everything else is
# monthly (`month`, YYYY-MM). Derived from the dataset titles on data.gov.sg.
ANNUAL_IDS = {
    "d_085682b824700b4e88d946529f503da0",  # Container Throughput, Annual
    "d_0a76d48f3754aafd08f98629324a54c6",  # Bunker Sales Breakdown, Annual
    "d_0c586210d33756a56ef6213078e749aa",  # Registered Vessels & Tonnage, Annual
    "d_1714a141d8bbf1996965eb3f71565525",  # Tanker Arrivals Breakdown, Annual
    "d_60410de1bc1e63ddcf51a619081b11b3",  # Vessel Calls (>75 GT), Annual
    "d_8392e9bea6ca351a38f67172ccdf6a6a",  # Vessel Arrivals (>75 GT) Total, Annual
    "d_8ab8d71a6bf44097889dd6a3b4258928",  # Cargo Throughput Total, Annual
    "d_a30479ad55e045bcaffacf587d05966c",  # Cargo Throughput Breakdown, Annual
    "d_b0c64c019b252698a9f1a222dcf9e0a6",  # Vessel Arrivals (>75 GT) Breakdown, Annual
    "d_ccb330e6679674ffaa330dc76136e198",  # Bunker Sales Total, Annual
    "d_eb1c7c0c9ee013f9be42cc8abf523326",  # Tanker Arrivals Total, Annual
}

_API = "https://api-open.data.gov.sg/v1/public/api/datasets/{did}"


# --- HTTP / retry ----------------------------------------------------------
class _Transient(Exception):
    """data.gov.sg rate-limit (code 24) or a stale presigned URL — retryable."""


_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (_Transient,) + _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(10),
    wait=wait_exponential(min=10, max=120),
    reraise=True,
)
def _resolve_download_url(did: str) -> str:
    """Resolve a dataset id to a presigned full-CSV download URL."""
    base = _API.format(did=did)
    resp = get(f"{base}/poll-download", timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    data = body.get("data")
    if data and data.get("status") == "DOWNLOAD_SUCCESS" and data.get("url"):
        return data["url"]
    if body.get("code") == 24 or data is None:
        raise _Transient(f"{did}: {body.get('name') or body.get('errorMsg')}")
    # Non-success status: kick the initiate step, then let retry re-poll.
    get(f"{base}/initiate-download", timeout=(10.0, 120.0)).raise_for_status()
    status = data.get("status") if data else None
    raise _Transient(f"{did}: download not ready (status={status})")


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=10, max=120),
    reraise=True,
)
def _fetch_csv_text(did: str) -> str:
    """Resolve and download the full CSV for a dataset, as text."""
    url = _resolve_download_url(did)
    try:
        resp = get(url, timeout=(10.0, 180.0))
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 403:  # presigned URL expired
            raise _Transient(f"{did}: presigned url expired, re-resolving")
        raise
    return resp.text


# --- parsing ---------------------------------------------------------------
_TIME_COLS = {"month", "year"}


def _parse_typed(text: str) -> pa.Table:
    """Parse CSV text into a typed pyarrow table.

    Time columns (`month`/`year`) are kept as strings (the transform casts
    them). Every other column is coerced to float64 when all of its non-empty
    values parse as numbers, else kept as string. The schema is built
    explicitly from the observed columns — one full-snapshot write per asset.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise AssertionError("empty CSV (no header)")
    header = rows[0]
    data = [r for r in rows[1:] if any(c.strip() for c in r)]

    fields = []
    arrays = []
    for idx, name in enumerate(header):
        col = [r[idx] if idx < len(r) else "" for r in data]
        if name.strip().lower() in _TIME_COLS:
            fields.append(pa.field(name, pa.string()))
            arrays.append(pa.array([v or None for v in col], type=pa.string()))
            continue
        numeric = True
        nums = []
        for v in col:
            if v == "" or v is None:
                nums.append(None)
                continue
            try:
                nums.append(float(v))
            except ValueError:
                numeric = False
                break
        if numeric:
            fields.append(pa.field(name, pa.float64()))
            arrays.append(pa.array(nums, type=pa.float64()))
        else:
            fields.append(pa.field(name, pa.string()))
            arrays.append(pa.array([v or None for v in col], type=pa.string()))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def _did_from_node(node_id: str) -> str:
    """Recover the data.gov.sg dataset id from a spec id.

    spec id = f"mpa-singapore-{eid.lower().replace('_','-')}"; the only
    underscore in a data.gov.sg id is the leading `d_`, so restoring the first
    hyphen of the suffix recovers the original id exactly.
    """
    suffix = node_id[len("mpa-singapore-"):]
    return suffix.replace("-", "_", 1)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    did = _did_from_node(node_id)
    table = _parse_typed(_fetch_csv_text(did))
    save_raw_parquet(table, asset)


def _spec_id(eid: str) -> str:
    return f"mpa-singapore-{eid.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


def _transform_sql(sid: str, annual: bool) -> str:
    if annual:
        return (
            f'SELECT CAST(year AS BIGINT) AS year, * EXCLUDE (year) '
            f'FROM "{sid}" WHERE year IS NOT NULL'
        )
    return (
        f"SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, "
        f'* EXCLUDE (month) FROM "{sid}" WHERE month IS NOT NULL'
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_spec_id(eid)}-transform",
        deps=[_spec_id(eid)],
        sql=_transform_sql(_spec_id(eid), eid in ANNUAL_IDS),
    )
    for eid in ENTITY_IDS
]
