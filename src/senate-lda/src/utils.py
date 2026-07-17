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
    list_raw_fragments,
    save_raw_ndjson,
    load_state,
    save_state,
)

API_BASE = "https://lda.senate.gov/api/v1"
STATE_VERSION = 3

# Earliest posting year per endpoint (filings from 1999, LD-203 from 2008).
MIN_YEAR = {"filings": 1999, "contributions": 2008}

# Safety ceilings — these RAISE (never silently truncate) if the source grows
# past expectations, surfacing unexpected volume instead of hiding it.
MAX_PAGES_PER_MONTH = 4000     # ~100k filings in one posting-month
MAX_PAGES_ABS = 100000         # reference-entity full crawl guard

REF_BATCH_PAGES = 200          # 5k rows per reference-entity raw batch

# Leave enough room for the DAG parent to commit raw manifests and retrigger
# before GitHub's runner deadline. Override only for local probing.
LEG_SECONDS = int(os.environ.get("LDA_LEG_SECONDS", str(4 * 60 * 60)))

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


def _month_range(start_year: int) -> list[tuple[int, int]]:
    today = datetime.now(timezone.utc).date()
    out = []
    y, m = start_year, 1
    while (y, m) <= (today.year, today.month):
        out.append((y, m))
        y, m = _next_month(y, m)
    return out


def dated_complete(asset: str, endpoint: str, *, max_age_days: int = 7) -> bool:
    """True when every historical month exists and the live month is fresh."""
    fragments = list_raw_fragments(asset, "ndjson.zst")
    expected = {f"{y:04d}-{m:02d}" for y, m in _month_range(MIN_YEAR[endpoint])}
    if not expected.issubset(fragments):
        return False
    current = fragments.get(max(expected))
    fetched_at = (current or {}).get("fetched_at")
    if not fetched_at:
        return False
    try:
        then = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (datetime.now(timezone.utc) - then).days <= max_age_days


def reference_complete(asset: str, *, max_age_days: int = 30) -> bool:
    """True when a reference crawl has reached its final page recently enough."""
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION or not state.get("complete"):
        return False
    fragments = list_raw_fragments(asset, "ndjson.zst")
    if not fragments:
        return False
    latest = max(
        (meta.get("fetched_at") for meta in fragments.values() if meta.get("fetched_at")),
        default=None,
    )
    if not latest:
        return False
    try:
        then = datetime.fromisoformat(latest.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (datetime.now(timezone.utc) - then).days <= max_age_days


def _crawl_dated(asset: str, endpoint: str, flatten) -> bool | None:
    """Crawl /filings/ or /contributions/ windowed by dt_posted month.

    One raw fragment per posting-month (`<asset>-YYYY-MM`). Historical months
    are skipped once committed in the raw manifest; the current month is always
    re-pulled to pick up newly posted records. Continuation resume is manifest
    based, so an interrupted child cannot advance state past uncommitted raw.
    """
    headers = _auth_headers()
    run_id = os.environ.get("RUN_ID", "unknown")
    deadline = time.monotonic() + LEG_SECONDS

    months = _month_range(MIN_YEAR[endpoint])
    cur = months[-1]
    committed = list_raw_fragments(asset, "ndjson.zst")
    done = {
        frag for frag, meta in committed.items()
        if meta.get("run_id") == run_id or frag != f"{cur[0]:04d}-{cur[1]:02d}"
    }

    for i, (y, m) in enumerate(months, 1):
        frag = f"{y:04d}-{m:02d}"
        if frag in done:
            continue
        if time.monotonic() >= deadline:
            print(f"{asset}: leg budget spent at {i - 1}/{len(months)} months")
            return True

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

        if rows:
            save_raw_ndjson(rows, asset, fragment=frag)
        print(f"{asset}: {frag} {len(rows):,} rows ({i}/{len(months)})")

    return None


def _crawl_paged(asset: str, endpoint: str, flatten) -> bool | None:
    """Full crawl of a reference endpoint, ordered by id ascending.

    No working incremental filter exists, so we crawl id-ordered pages and store
    fixed page-range fragments. Existing committed fragments are skipped; a
    completion marker is written only after the endpoint reports no next page.
    """
    headers = _auth_headers()
    deadline = time.monotonic() + LEG_SECONDS

    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        state = {}

    done = set(list_raw_fragments(asset, "ndjson.zst"))
    done_ranges = []
    for frag in done:
        if not frag.startswith("p"):
            continue
        try:
            start, end = frag.split("-p", 1)
            done_ranges.append((int(start[1:]), int(end)))
        except ValueError:
            continue

    page = 1

    buf: list[dict] = []
    batch_start = page
    while True:
        covered = next(((lo, hi) for lo, hi in done_ranges if lo <= page <= hi), None)
        if covered:
            page = covered[1] + 1
            batch_start = page
            continue

        if time.monotonic() >= deadline:
            print(f"{asset}: leg budget spent before page {page}")
            return True

        data = _fetch(f"{API_BASE}/{endpoint}/", {"ordering": "id", "page": page}, headers)
        for r in (data.get("results") or []):
            buf.append(flatten(r))
        has_next = bool(data.get("next"))

        if buf and ((page - batch_start + 1) >= REF_BATCH_PAGES or not has_next):
            frag = f"p{batch_start:05d}-p{page:05d}"
            save_raw_ndjson(buf, asset, fragment=frag)
            print(f"{asset}: wrote {frag} ({len(buf):,} rows)")
            buf = []
            batch_start = page + 1
        elif not has_next:
            save_state(asset, {
                "schema_version": STATE_VERSION,
                "complete": True,
                "last_page": page,
            })

        if not has_next:
            break
        page += 1
        if page > MAX_PAGES_ABS:
            raise RuntimeError(
                f"{asset}: exceeded {MAX_PAGES_ABS} pages — source grew unexpectedly"
            )

    return None
