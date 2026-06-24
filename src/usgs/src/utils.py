"""Shared transport for the USGS node module (water OGC + FDSN earthquakes).

Both surfaces are cursor-paged crawls over HTTP services that throttle with
HTTP 429 (and intermittent 5xx) under sustained load. A full-corpus crawl runs
for over an hour and accumulates throttle pressure, so a blind exponential
backoff is not enough — an earlier run rode 10 retries of up to 180s and still
saw a persistent 429 on the `continuous` collection's first page, aborting the
whole DAG.

This transport fixes that two ways:

  1. **Pacing** — a global minimum interval between requests keeps the steady
     crawl under the service's rate ceiling instead of relying on post-hoc
     backoff. Nodes run sequentially (DAG_PARALLELISM=1), so the module-level
     pacer spans the whole run within each node process.
  2. **Retry-After awareness** — on a 429 we honor the server's `Retry-After`
     cooldown (which can far exceed any fixed backoff cap) rather than hammering
     through it, which only extends the block. 5xx and transient network errors
     fall back to exponential backoff. The budget is deliberately patient: a
     throttled crawl should wait the source out, not fail the connector.
"""
from __future__ import annotations

import time

import httpx

from subsets_utils import get

# Pure infinite-loop guard — bounded collections terminate well below this and
# windowed/time-bounded crawls are time-bounded. A hit means the cursor never
# advanced.
MAX_PAGES = 200_000

# --- pacing ------------------------------------------------------------------
# Minimum spacing between consecutive requests (~2 req/s). Cheap insurance: the
# extra wall-clock over a multi-hundred-page crawl is a few minutes, far less
# than one 429 cooldown.
_MIN_INTERVAL_S = 0.5
_last_request_ts = 0.0

# --- retry budget ------------------------------------------------------------
_MAX_ATTEMPTS = 12
_BACKOFF_BASE = 4.0      # exponential backoff for 5xx / network errors
_BACKOFF_CAP = 300.0
_RETRY_AFTER_CAP = 600.0  # clamp a pathological server Retry-After

# Network-layer failures that are safe to retry.
_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _pace() -> None:
    """Block until at least _MIN_INTERVAL_S has elapsed since the last request."""
    global _last_request_ts
    wait = _MIN_INTERVAL_S - (time.monotonic() - _last_request_ts)
    if wait > 0:
        time.sleep(wait)
    _last_request_ts = time.monotonic()


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    """Parse a numeric `Retry-After` header (seconds). HTTP-date form → None
    (caller falls back to exponential backoff)."""
    ra = resp.headers.get("Retry-After")
    if not ra:
        return None
    try:
        return max(0.0, float(ra))
    except ValueError:
        return None


def _backoff(attempt: int) -> float:
    return min(_BACKOFF_CAP, _BACKOFF_BASE * (2 ** (attempt - 1)))


def _request(url: str, params: dict | None) -> httpx.Response:
    """GET with pacing + patient, Retry-After-aware retries on 429/5xx/network."""
    last_exc: BaseException | None = None
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        _pace()
        try:
            resp = get(url, params=params, timeout=(10.0, 300.0))
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            if code != 429 and not (500 <= code < 600):
                raise  # non-transient (4xx other than 429): fail honestly
            last_exc = exc
            if attempt == _MAX_ATTEMPTS:
                raise
            sleep_s = _retry_after_seconds(exc.response) if code == 429 else None
            sleep_s = min(_RETRY_AFTER_CAP, sleep_s) if sleep_s is not None else _backoff(attempt)
            print(
                f"  retry {attempt}/{_MAX_ATTEMPTS} on HTTP {code} for {url} "
                f"— sleeping {sleep_s:.0f}s"
            )
            time.sleep(sleep_s)
        except _TRANSIENT_EXC as exc:
            last_exc = exc
            if attempt == _MAX_ATTEMPTS:
                raise
            sleep_s = _backoff(attempt)
            print(
                f"  retry {attempt}/{_MAX_ATTEMPTS} on {type(exc).__name__} for {url} "
                f"— sleeping {sleep_s:.0f}s"
            )
            time.sleep(sleep_s)
    assert last_exc is not None
    raise last_exc


def get_json(url: str, params: dict | None) -> dict:
    return _request(url, params).json()


def get_text(url: str, params: dict | None) -> str:
    return _request(url, params).text
