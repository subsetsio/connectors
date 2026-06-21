"""Shared transport + cross-subset parsing for the Bank Negara Malaysia (BNM)
Open API connector — REST at https://api.bnm.gov.my/public.

This module is `_`-prefixed so the node loader (orchestrator.py:1123) skips it
when scanning for `*_SPECS`. It holds only the base URL / versioned Accept
header, the retrying JSON fetch, the bounded thread-pool fan-out, the start-year
discovery + month-grid helpers, and the tenor normalizer that is shared by more
than one subset module. No NodeSpecs live here.

Every request MUST carry the versioned Accept header
`application/vnd.BNM.API.v1+json` (without it the server 404s). No auth, no API
key. JSON payload sits under a top-level `data` key.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from subsets_utils import get, transient_retry

SLUG = "bank-negara-malaysia"
PREFIX = f"{SLUG}-"
BASE = "https://api.bnm.gov.my/public"
HEADERS = {"Accept": "application/vnd.BNM.API.v1+json"}

# Keep per-process concurrency modest: the orchestrator runs many download
# specs as parallel subprocesses, so peak connections to the single BNM host is
# (parallel specs x MAX_WORKERS). At 12 the server drops connections under load
# ("Server disconnected"); 4 keeps the aggregate gentle while staying fast (CI
# round-trips are ~250ms).
MAX_WORKERS = 4
MAX_YEARS_BACK = 40          # safety ceiling for start-year discovery

# ---------------------------------------------------------------- transport


@transient_retry(attempts=8, min_wait=1, max_wait=45)
def _fetch(path: str):
    """GET a BNM path; returns the parsed JSON, or None for a 404 (no records)."""
    resp = get(f"{BASE}/{path}", headers=HEADERS, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _has_rows(payload) -> bool:
    if not payload:
        return False
    data = payload.get("data")
    if isinstance(data, list):
        return len(data) > 0
    return bool(data)


def _parallel(keyed_paths):
    """keyed_paths: list of (key, path). Returns list of (key, payload)."""
    out = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(_fetch, path): key for key, path in keyed_paths}
        for fut in as_completed(futs):
            out.append((futs[fut], fut.result()))
    return out


def _now():
    n = datetime.now(timezone.utc)
    return n.year, n.month


def _discover_start_year(sample_path) -> int:
    """Probe one representative call per year backwards; return the earliest
    year that has data. `sample_path` maps a year -> path string."""
    cur_year, _ = _now()
    years = list(range(cur_year, cur_year - MAX_YEARS_BACK, -1))
    res = _parallel([(y, sample_path(y)) for y in years])
    have = [y for y, payload in res if _has_rows(payload)]
    if not have:
        raise RuntimeError(
            f"no data found probing {sample_path(cur_year)} back {MAX_YEARS_BACK}y"
        )
    return min(have)


def _month_grid(start_year):
    cur_year, cur_month = _now()
    for y in range(start_year, cur_year + 1):
        for m in range(1, 13):
            if y == cur_year and m > cur_month:
                break
            yield y, m


# ----------------------------------------------------- shared normalizer

# Used by the month-iterated tenor series (islamic-interbank-rate,
# interbank-swap) AND by the product-iterated interest feeds, so it lives here.
_TENOR_MAP = {
    "overnight": "overnight",
    "1_week": "week_1", "2_week": "week_2",
    "1_month": "month_1", "2_month": "month_2", "3_month": "month_3",
    "6_month": "month_6", "9_month": "month_9", "12_month": "month_12",
    "1_year": "year_1", "more_1_year": "more_1_year", "other": "other",
}


def _norm_tenor(rec: dict) -> dict:
    row = {"date": rec.get("date")}
    for k, v in rec.items():
        if k == "date":
            continue
        row[_TENOR_MAP.get(k, k)] = v
    return row
