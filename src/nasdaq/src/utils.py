"""Shared helpers for the Nasdaq connector — public api.nasdaq.com.

Mechanism: undocumented REST at https://api.nasdaq.com/api/. No API key; a real
browser User-Agent + Accept: application/json are sent on every request (the
default tool UA gets the connection dropped). Responses are
{"data": ..., "status": {"rCode": 200}} envelopes; rCode != 200 (returned WITH
HTTP 200, e.g. "Symbol not exists.") is a permanent per-entity skip. Numeric
fields are human-formatted strings ($, commas, %) and are cleaned/typed in the
SQL transforms, not here.

Robustness note: this backend is flaky from datacenter IPs. Two observed
failure modes, both handled here:
  - a 200 response with a non-JSON body (empty / HTML challenge) — `resp.json()`
    raises; treated as transient (`_BadJson`) and retried, then surfaced.
  - a screener page returning an empty rows[] for a VALID mid-stream offset —
    NOT end-of-data; the paginator retries the page instead of stopping early.

This module holds the shared HTTP client, the envelope/scalar helpers, and the
screener-pagination enumeration reused by the screeners and the historical-price
crawl. It contains no NodeSpec definitions.
"""
import json
import time

from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry, retry_if_exception, stop_after_attempt, wait_exponential,
)

from subsets_utils import get, is_transient

BASE = "https://api.nasdaq.com/api"
HDRS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
    "Accept": "application/json",
}

DIV_WINDOW_BACK = 90        # rolling calendar window (days)
DIV_WINDOW_FWD = 14


# --- HTTP -------------------------------------------------------------------


class BadJson(ValueError):
    """A 200 response whose body isn't parseable JSON. api.nasdaq.com does this
    intermittently (empty body / HTML challenge), especially from cloud IPs.
    Classified transient so the retry policy below retries it."""


def _retryable(exc: BaseException) -> bool:
    # Standard transient set (network / 429 / 5xx) PLUS non-JSON 200 bodies.
    return is_transient(exc) or isinstance(exc, (BadJson, json.JSONDecodeError))


@retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str) -> dict:
    resp = get(url, headers=HDRS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    try:
        return resp.json()
    except (json.JSONDecodeError, ValueError) as exc:
        # 200 with a non-JSON body — retry; surface as BadJson if it persists.
        raise BadJson(f"non-JSON body from {url}: {exc}") from exc


@sleep_and_retry
@limits(calls=4, period=1)  # pace the per-symbol historical crawl (~4 req/s)
def _get_json_paced(url: str) -> dict:
    return _get_json(url)


def _envelope_ok(payload: dict) -> bool:
    """api.nasdaq.com returns HTTP 200 even for errors; the real status is in
    the envelope. rCode 200 == real data; anything else (e.g. 'Symbol not
    exists.') is a permanent condition for that entity."""
    st = (payload or {}).get("status") or {}
    return st.get("rCode") == 200


def _s(v):
    """Coerce any scalar to a string (or None) so raw ndjson columns stay
    type-stable; the SQL transforms do all real typing."""
    return None if v is None else str(v)


# --- universe enumeration (shared by screeners + historical-prices) ---------
#
# The offset-paginated screener endpoint (?limit=&offset=) is unusable for a
# full pull: it caps at 50 rows/page regardless of limit, intermittently
# returns an empty page for a valid offset, AND reorders the live feed between
# requests so fixed-offset pages overlap and drop ~15% of the universe on
# dedup. The `download=true` variant returns the ENTIRE table in one request
# (stocks ~7.1k, ETFs ~4.5k), so we use that exclusively.

def _screener_download(path: str, extract, retries: int = 6) -> list[dict]:
    """Full screener snapshot via ?download=true, in one request.

    `extract` pulls the row list out of the response `data` object (the two
    screeners nest it differently). Retries a transient empty body (the backend
    is flaky from cloud IPs) before giving up loudly."""
    for attempt in range(retries):
        payload = _get_json(f"{BASE}/screener/{path}?download=true")
        if not _envelope_ok(payload):
            raise RuntimeError(f"screener/{path} download bad envelope")
        rows = extract(payload.get("data") or {})
        if rows:
            return rows
        time.sleep(1.0 * (attempt + 1))  # transient empty snapshot — retry
    raise RuntimeError(
        f"screener/{path} download returned no rows after {retries} retries"
    )


def _stock_rows() -> list[dict]:
    # stocks: data.rows
    return _screener_download("stocks", lambda d: d.get("rows") or [])


def _etf_rows() -> list[dict]:
    # etf: data.data.rows (nested one level deeper than stocks)
    return _screener_download("etf", lambda d: (d.get("data") or {}).get("rows") or [])
