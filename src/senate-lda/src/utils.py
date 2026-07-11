"""Shared infrastructure for the U.S. Senate LDA connector.

Single REST API at https://lda.senate.gov/api/v1/ (DRF, page size FIXED at 25;
no bulk export). HTTP (per-process rate limiting + retry) and the two crawl
drivers live here; each published subset's flattener + NodeSpecs live in its own
file under nodes/.

Set LDA_API_KEY (free, from https://lda.senate.gov/api/register/) to lift the
rate limit from 15 to 120 req/min; the connector runs anonymously without it.
"""

import os
import time
from datetime import date, datetime, timezone


from subsets_utils import (
    get,
    save_raw_ndjson,
    load_state,
    save_state,
)

API_BASE = "https://lda.senate.gov/api/v1"
STATE_VERSION = 2

# Earliest posting year per endpoint (filings from 1999, LD-203 from 2008).
MIN_YEAR = {"filings": 1999, "contributions": 2008}

# Safety ceilings — these RAISE (never silently truncate) if the source grows
# past expectations, surfacing unexpected volume instead of hiding it.
MAX_PAGES_PER_MONTH = 4000     # ~100k filings in one posting-month
MAX_PAGES_ABS = 100000         # reference-entity full crawl guard

REF_BATCH_ROWS = 5000          # rows buffered per reference-entity raw batch

# ---------------------------------------------------------------------------
# HTTP: per-process rate limiting + retry
# ---------------------------------------------------------------------------

_last_call = [0.0]
_min_interval = [60.0 / 12.0]  # default: ~80% of the 15 rpm anonymous limit


def _auth_headers() -> dict:
    """Resolve auth + rate budget for THIS process from the environment.

    Called once at the top of each fetch fn (each NodeSpec is its own process).
    """
    key = os.environ.get("LDA_API_KEY")
    rpm = 96 if key else 12  # ~80% of 120 (keyed) / 15 (anonymous)
    _min_interval[0] = 60.0 / rpm
    return {"Authorization": f"Token {key}"} if key else {}


def _throttle() -> None:
    elapsed = time.monotonic() - _last_call[0]
    if elapsed < _min_interval[0]:
        time.sleep(_min_interval[0] - elapsed)
    _last_call[0] = time.monotonic()


def _fetch(url: str, params: dict, headers: dict) -> dict:
    _throttle()
    resp = get(url, params=params, headers=headers, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Shared parse helper
# ---------------------------------------------------------------------------

def _name(person: dict) -> str | None:
    parts = [person.get("first_name"), person.get("last_name")]
    nm = " ".join(p for p in parts if p).strip()
    return nm or None


# ---------------------------------------------------------------------------
# Crawl drivers
# ---------------------------------------------------------------------------

def _next_month(y: int, m: int) -> tuple[int, int]:
    return (y + 1, 1) if m == 12 else (y, m + 1)


def _crawl_dated(asset: str, endpoint: str, flatten) -> None:
    """Crawl /filings/ or /contributions/ windowed by dt_posted month.

    One immutable raw batch per posting-month (`<asset>-YYYY-MM`). State tracks
    the next month to (re)process; the current month is re-pulled every run to
    pick up newly posted records and amendments.
    """
    headers = _auth_headers()

    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    resume = state.get("resume_month")
    if resume:
        ry, rm = int(resume[:4]), int(resume[5:7])
    else:
        ry, rm = MIN_YEAR[endpoint], 1

    today = datetime.now(timezone.utc).date()
    cur = (today.year, today.month)

    y, m = ry, rm
    while (y, m) <= cur:
        after = date(y, m, 1).isoformat()
        ny, nm = _next_month(y, m)
        before = date(ny, nm, 1).isoformat()

        rows: list[dict] = []
        page = 1
        while True:
            params = {
                "filing_dt_posted_after": after,
                "filing_dt_posted_before": before,
                "ordering": "dt_posted",
                "page": page,
            }
            data = _fetch(f"{API_BASE}/{endpoint}/", params, headers)
            for rec in (data.get("results") or []):
                rows.extend(flatten(rec))
            if not data.get("next"):
                break
            page += 1
            if page > MAX_PAGES_PER_MONTH:
                raise RuntimeError(
                    f"{asset}: {endpoint} {after}..{before} exceeded "
                    f"{MAX_PAGES_PER_MONTH} pages — source grew unexpectedly"
                )

        # Write raw FIRST, then advance state (a crash between loses only rework).
        if rows:
            save_raw_ndjson(rows, asset, fragment=f"{y:04d}-{m:02d}")

        if (y, m) != cur:
            # Past month complete and immutable — advance the resume pointer.
            save_state(asset, {
                "schema_version": STATE_VERSION,
                "resume_month": f"{ny:04d}-{nm:02d}",
            })
        y, m = ny, nm


def _crawl_paged(asset: str, endpoint: str, flatten) -> None:
    """Full crawl of a reference endpoint, ordered by id ascending.

    No working incremental filter exists, so we resume by page number — safe
    here because rows are append-mostly and id-ordered (new rows land on later
    pages without shifting earlier ones). State tracks the next page to fetch;
    raw is flushed in row-count-bounded batches (`<asset>-pNNNNN-pMMMMM`).
    """
    headers = _auth_headers()

    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    page = state.get("next_page", 1)

    buf: list[dict] = []
    batch_start = page
    while True:
        data = _fetch(f"{API_BASE}/{endpoint}/", {"ordering": "id", "page": page}, headers)
        for r in (data.get("results") or []):
            buf.append(flatten(r))
        has_next = bool(data.get("next"))

        if buf and (len(buf) >= REF_BATCH_ROWS or not has_next):
            save_raw_ndjson(buf, asset, fragment=f"p{batch_start:05d}-p{page:05d}")
            buf = []
            save_state(asset, {"schema_version": STATE_VERSION, "next_page": page + 1})
            batch_start = page + 1
        elif not has_next:
            # No rows this run (already caught up); still record progress.
            save_state(asset, {"schema_version": STATE_VERSION, "next_page": page + 1})

        if not has_next:
            break
        page += 1
        if page > MAX_PAGES_ABS:
            raise RuntimeError(
                f"{asset}: exceeded {MAX_PAGES_ABS} pages — source grew unexpectedly"
            )
