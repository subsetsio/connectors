"""European Environment Agency — Discodata data warehouse.

Each accepted entity is one table in the `latest` schema of EEA's Discodata SQL
warehouse (https://discodata.eea.europa.eu). Two fetch paths, picked per table:

1. **Bulk blob (primary, ~463 tables).** Discodata materializes most tables to
   its Azure datalake as a single per-table ZIP holding one semicolon-delimited
   CSV. One HTTP request returns the whole table — the optimal whole-table
   pattern, and it sidesteps the SQL backend entirely. The version-pinned blob
   URL is captured in `constants.py` from `/md`; if a version bump makes it 404,
   we fall back to SQL automatically.
2. **SQL API (fallback, ~251 unmaterialized views).** Tables that are computed
   views have no bulk file, so we page `SELECT *` through the SQL endpoint. That
   backend returns a 200-body `{"errors":[{"error":"Service currently offline"}]}`
   under heavy load; we treat it as transient and back off. Pages are kept small
   so each query stays light.

Raw is written as gzip NDJSON, one asset per table. The 714 tables are wildly
heterogeneous (1..460 columns), so a per-table declared parquet schema is
impractical — NDJSON lets the SQL transform re-type on read. Full re-pull every
run (stateless); EEA publishes full snapshots and the corpus re-fetches cheaply.
"""
from __future__ import annotations

import io
import csv
import json
import os
import time
import fcntl
import zipfile

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import NodeSpec, get, is_transient, raw_writer
from constants import ENTITIES

SLUG = "european-environment-agency"
SQL_URL = "https://discodata.eea.europa.eu/sql"

PAGE = 5000          # rows per SQL page — small enough to stay a light query
MAX_PAGES = 100_000  # safety ceiling; raises rather than silently truncating
SQL_MIN_INTERVAL = 1.5
SQL_LOCK_PATH = "/tmp/european_environment_agency_discodata_sql.lock"
SQL_LAST_REQUEST_PATH = "/tmp/european_environment_agency_discodata_sql.last"


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-" + entity_id.lower().replace("_", "-")


# spec id -> (database, table, blob_url). Pure computation over an imported
# literal (same shape the DOWNLOAD_SPECS comprehension relies on), not I/O.
_META = {_spec_id(eid): (db, tbl, url) for eid, db, tbl, url in ENTITIES}


class _Offline(Exception):
    """Discodata SQL backend reported itself offline (a transient throttle)."""


def _retryable(exc: BaseException) -> bool:
    return isinstance(exc, _Offline) or is_transient(exc)


def _throttled_sql_get(query: str, page: int) -> httpx.Response:
    """Serialize Discodata SQL calls across DAG worker processes.

    The SQL endpoint returns a 200-body "Service currently offline" when hit
    with bursts. Bulk ZIP downloads stay concurrent; only SQL page requests use
    this process-wide lock.
    """
    os.makedirs(os.path.dirname(SQL_LOCK_PATH), exist_ok=True)
    with open(SQL_LOCK_PATH, "a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            last = 0.0
            try:
                with open(SQL_LAST_REQUEST_PATH, "r", encoding="utf-8") as state:
                    last = float(state.read().strip() or "0")
            except (FileNotFoundError, ValueError):
                pass
            delay = SQL_MIN_INTERVAL - (time.monotonic() - last)
            if delay > 0:
                time.sleep(delay)
            response = get(
                SQL_URL,
                params={"query": query, "nrOfHits": PAGE, "p": page},
                timeout=(10.0, 300.0),
            )
            with open(SQL_LAST_REQUEST_PATH, "w", encoding="utf-8") as state:
                state.write(str(time.monotonic()))
            return response
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


# ---- blob path -------------------------------------------------------------

@retry(retry=retry_if_exception(is_transient),
       wait=wait_exponential(multiplier=4, min=4, max=120),
       stop=stop_after_attempt(6), reraise=True)
def _http_get(url: str) -> httpx.Response:
    r = get(url, timeout=(10.0, 300.0))
    r.raise_for_status()
    return r


def _csv_delimiter(header: str) -> str:
    # EEA datalake CSVs are semicolon-delimited; fall back to comma defensively.
    return ";" if header.count(";") >= header.count(",") else ","


def _fetch_blob(node_id: str, blob_url: str) -> None:
    """Download the per-table ZIP, stream its CSV into gzip NDJSON."""
    resp = _http_get(blob_url)
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    members = [n for n in zf.namelist() if n.lower().endswith(".csv")] or zf.namelist()
    member = members[0]
    with zf.open(member) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        first = text.readline()
        if not first:
            # Empty file — write nothing; the transform will fail loudly (0 rows),
            # which is the correct signal that this table has no data.
            with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip"):
                pass
            return
        delim = _csv_delimiter(first)
        fieldnames = next(csv.reader([first], delimiter=delim))
        reader = csv.DictReader(text, fieldnames=fieldnames, delimiter=delim)
        with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
            for row in reader:
                # csv.DictReader stuffs overflow cells under a None key; drop it.
                row.pop(None, None)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---- SQL fallback path -----------------------------------------------------

@retry(retry=retry_if_exception(_retryable),
       wait=wait_exponential(multiplier=8, min=8, max=120),
       stop=stop_after_attempt(8), reraise=True)
def _sql_page(query: str, page: int) -> list[dict]:
    r = _throttled_sql_get(query, page)
    r.raise_for_status()
    payload = r.json()
    errors = payload.get("errors") if isinstance(payload, dict) else None
    if errors:
        msg = (errors[0] or {}).get("error", "")
        if "offline" in msg.lower():
            raise _Offline(msg)
        raise RuntimeError(f"discodata query error for {query!r}: {errors}")
    return payload.get("results", [])


def _fetch_sql(node_id: str, database: str, table: str) -> None:
    query = f"SELECT * FROM [{database}].[latest].[{table}]"
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for page in range(MAX_PAGES):
            rows = _sql_page(query, page)
            for row in rows:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
            if len(rows) < PAGE:
                return
        raise RuntimeError(f"{database}.{table}: exceeded MAX_PAGES={MAX_PAGES}")


def fetch_one(node_id: str) -> None:
    database, table, blob_url = _META[node_id]
    if blob_url:
        try:
            _fetch_blob(node_id, blob_url)
            return
        except httpx.HTTPStatusError as exc:
            # Stale/missing bulk file (version bump) — fall through to SQL.
            if exc.response is None or exc.response.status_code != 404:
                raise
            print(f"[eea] blob 404 for {node_id}; falling back to SQL")
    _fetch_sql(node_id, database, table)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid, _db, _tbl, _url in ENTITIES
]
