"""Shared helpers for the Nasdaq connector — public api.nasdaq.com.

Mechanism: undocumented REST at https://api.nasdaq.com/api/. No API key; a real
browser User-Agent + Accept: application/json are sent on every request (the
default tool UA gets the connection dropped). Responses are
{"data": ..., "status": {"rCode": 200}} envelopes; rCode != 200 (returned WITH
HTTP 200, e.g. "Symbol not exists.") is a permanent per-entity skip. Numeric
fields are human-formatted strings ($, commas, %) and are cleaned/typed in the
SQL transforms, not here.

This module holds the shared HTTP client, the envelope/scalar helpers, and the
screener-pagination enumeration reused by the screeners and the historical-price
crawl. It contains no NodeSpec definitions.
"""
from ratelimit import limits, sleep_and_retry

from subsets_utils import get, transient_retry

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


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, headers=HDRS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


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

def _screener_rows(path: str, rows_accessor) -> list[dict]:
    """Paginate a screener endpoint to completeness. The endpoint may silently
    cap the page size (the ETF screener honors at most 50/page regardless of the
    requested limit), so advance the offset by the actual rows returned, not by
    the requested limit."""
    out: list[dict] = []
    offset, limit = 0, 5000
    MAX_PAGES = 5000  # safety ceiling — raises rather than looping forever
    for _ in range(MAX_PAGES):
        payload = _get_json(f"{BASE}/screener/{path}?limit={limit}&offset={offset}")
        if not _envelope_ok(payload):
            raise RuntimeError(f"screener/{path} bad envelope at offset={offset}")
        rows, total = rows_accessor(payload["data"])
        if total is None:
            raise RuntimeError(f"screener/{path} missing totalrecords")
        if not rows:
            break
        out.extend(rows)
        offset += len(rows)
        if offset >= total:
            break
    else:
        raise RuntimeError(f"screener/{path} exceeded {MAX_PAGES} pages")
    return out


def _stock_rows() -> list[dict]:
    return _screener_rows(
        "stocks",
        lambda d: (d.get("table", {}).get("rows", []), d.get("totalrecords")),
    )


def _etf_rows() -> list[dict]:
    return _screener_rows(
        "etf",
        lambda d: (d.get("records", {}).get("data", {}).get("rows", []),
                   d.get("records", {}).get("totalrecords")),
    )
