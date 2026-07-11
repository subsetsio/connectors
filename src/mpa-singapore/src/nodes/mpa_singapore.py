"""Maritime and Port Authority of Singapore (MPA) — maritime statistics.

Source: data.gov.sg. MPA publishes ~22 monthly/annual maritime time-series
datasets (container/cargo throughput, bunker sales, vessel & tanker arrivals,
vessel calls, registered vessels). Each dataset is one CSV with a stable but
dataset-specific column list: a single time column (`month` = YYYY-MM, or
`year` = YYYY), zero or more string dimension columns (bunker_type, category,
vessel_type, purpose_type, cargo_type_primary/secondary), and one or two
numeric measures (throughput / tonnage / sales / vessel counts).

Fetch strategy: stateless full re-pull (shape 1). Each dataset is a small CSV
(dozens-to-thousands of rows), so we re-fetch the whole table every run and
overwrite — revisions and late corrections come for free. No watermark/cursor,
no maintain policy (a whole-corpus refetch is a handful of cents).

Access (chosen mechanism `datagov_bulk_csv`): GET
.../datasets/{id}/poll-download returns {data:{status:"DOWNLOAD_SUCCESS",
url:<presigned S3 csv>}}; the S3 URL delivers the entire table in one request.
data.gov.sg rate-limits aggressively — it returns HTTP 429 AND, on the same
endpoint, HTTP 200 carrying {code:24,name:"TOO_MANY_REQUESTS"}; both are
treated as transient and retried with backoff. The presigned URL is
short-lived, so it is resolved immediately before each download and re-resolved
if S3 returns 403.

Normalization (in the fetch fn, so the raw is clean and SQL-ready): the time
column is converted to a real `date` (date32) at the PERIOD END — last day of
the month for monthly datasets, 31 Dec for annual ones. Period-end dating keeps
freshness assertions robust: an annual value for year Y lands on Y-12-31 rather
than Y-01-01, so a `max(date) >= today - 400d` freshness check passes
year-round instead of only in January. Numeric columns are coerced to float64;
dimension columns are kept as strings. No machine-readable schema is published,
so the shape is discovered per-CSV from its header.
"""

import calendar
import csv
import datetime as dt
import io

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, get, save_raw_parquet

# --- entity union (accept-active datasets) ---------------------------------
from constants import ENTITY_IDS

_API = "https://api-open.data.gov.sg/v1/public/api/datasets/{did}"

# The two time-column names data.gov.sg uses across MPA datasets. Exactly one
# appears per CSV; it is converted to a period-end `date` column.
_MONTH_COL = "month"
_YEAR_COL = "year"


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
def _period_end_date(name: str, value: str) -> dt.date | None:
    """Convert a source time value to a period-END `date`.

    `month` "YYYY-MM" -> last day of that month; `year` "YYYY" -> 31 Dec.
    Period-end dating keeps annual values off 1 Jan so rolling freshness bounds
    hold year-round. Empty/garbage -> None (a missing period).
    """
    v = (value or "").strip()
    try:
        if name == _MONTH_COL:
            y, m = v.split("-")
            y, m = int(y), int(m)
            return dt.date(y, m, calendar.monthrange(y, m)[1])
        # _YEAR_COL
        return dt.date(int(v), 12, 31)
    except (ValueError, TypeError):
        return None


def _parse_typed(text: str) -> pa.Table:
    """Parse CSV text into a typed pyarrow table.

    The single time column (`month`/`year`) becomes a period-end `date`
    (date32). Every other column is coerced to float64 when all of its
    non-empty values parse as numbers, else kept as string. The schema is built
    explicitly from the observed columns — one full-snapshot write per asset.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise AssertionError("empty CSV (no header)")
    header = [h.strip() for h in rows[0]]
    data = [r for r in rows[1:] if any(c.strip() for c in r)]

    fields: list[pa.Field] = []
    arrays: list[pa.Array] = []
    for idx, name in enumerate(header):
        col = [r[idx] if idx < len(r) else "" for r in data]
        low = name.lower()
        if low in (_MONTH_COL, _YEAR_COL):
            dates = [_period_end_date(low, v) for v in col]
            fields.append(pa.field("date", pa.date32()))
            arrays.append(pa.array(dates, type=pa.date32()))
            continue
        numeric = True
        nums: list[float | None] = []
        for v in col:
            if v is None or v.strip() == "":
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

    if not any(f.name == "date" for f in fields):
        raise AssertionError(f"no month/year time column in header: {header}")
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
