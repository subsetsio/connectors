"""Shared transport + enumeration for the Reddit (Arctic Shift) connector.

Arctic Shift (https://arctic-shift.photon-reddit.com) is the live successor to
Pushshift. Its /api/time_series endpoint serves PRECOMPUTED historical series
(date, value) for global and per-subreddit metrics; /api/subreddits/search
serves current per-subreddit metadata snapshots. We use only these two
endpoints (the chosen `arctic_shift_rest` mechanism) — never the petabyte-scale
raw dumps.

This module holds the HTTP client, retry/rate-limit policy, the time_series
fetcher, the subreddit enumeration walk, and the skip-tolerance guard shared by
two or more node files. It contains NO NodeSpec definitions.
"""

import re
import ssl

import httpx
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import get

API = "https://arctic-shift.photon-reddit.com/api"

# Coverage floor for the per-subreddit tables (subscribers). ~15.7k subreddits.
MIN_SUBSCRIBERS = 50_000
PRECISION = "month"          # monthly: stable, compact (~250 global points)
ENUM_LIMIT = 1000            # max page size for subreddits/search
ENUM_MAX_PAGES = 400         # safety ceiling — raises if exceeded (see _walk)
BATCH_SUBREDDITS = 1000      # subreddits per raw parquet batch
# Per-subreddit fetches that exhaust retries (isolated network blips over a
# ~2h crawl of ~15k communities) are skipped this run rather than aborting the
# whole node — re-pulled next run. Abort only if skips look systemic.
MAX_SKIP_FRAC = 0.05
MAX_SKIP_ABS = 100
_SUBREDDIT_KEY_RE = re.compile(r"^[A-Za-z0-9_]{1,24}$")


# --- transport ------------------------------------------------------------

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
    httpx.ProxyError,
)


# Errors a single per-subreddit fetch may raise after exhausting retries; these
# are skip-and-continue (isolated), never bugs. A bare TLS handshake timeout
# surfaces as ssl.SSLError / OSError, hence the broad-but-honest net.
_SKIPPABLE_EXC = (httpx.HTTPError, ssl.SSLError, OSError)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (ssl.SSLError, OSError)) and not isinstance(exc, httpx.HTTPError):
        # raw TLS handshake / socket timeouts during connect
        return True
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 422 here is Arctic Shift's "Timeout. Maybe slow down a bit" guard —
        # transient, worth a backed-off retry.
        return code in (422, 429) or 500 <= code < 600
    return False


@sleep_and_retry
@limits(calls=15, period=1)  # ~15 req/s — under the observed ~27/s sustained budget
@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=2, max=90),
    reraise=True,
)
def _request(path: str, params: dict) -> dict:
    # Generous connect timeout: TLS handshakes to this host occasionally stall
    # under sustained load (the failure mode that aborted run 20260618-112232).
    resp = get(f"{API}/{path}", params=params, timeout=(30.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _time_series(key: str) -> list[dict]:
    """Full historical series for one key, or [] if the key has no data."""
    payload = _request("time_series", {"key": key, "precision": PRECISION})
    data = payload.get("data") if isinstance(payload, dict) else payload
    return data or []


def _walk_subreddits() -> list[dict]:
    """Enumerate all subreddits with >= MIN_SUBSCRIBERS, descending by
    subscribers, paging via a max_subscribers cursor. Deduped by name."""
    records: list[dict] = []
    seen: set[str] = set()
    cursor = None
    for _ in range(ENUM_MAX_PAGES):
        params = {
            "sort_type": "subscribers",
            "sort": "desc",
            "limit": ENUM_LIMIT,
            "min_subscribers": MIN_SUBSCRIBERS,
        }
        if cursor is not None:
            params["max_subscribers"] = cursor
        data = _request("subreddits/search", params).get("data") or []
        if not data:
            break
        fresh = 0
        bottom = cursor
        for rec in data:
            name = rec.get("display_name")
            subs = rec.get("subscribers")
            if not name or subs is None:
                continue
            if not _SUBREDDIT_KEY_RE.fullmatch(name):
                print(f"  skip subreddit name unsupported by time_series keys: {name!r}")
                continue
            bottom = subs if bottom is None else min(bottom, subs)
            low = name.lower()
            if low in seen:
                continue
            seen.add(low)
            records.append(rec)
            fresh += 1
        if fresh == 0 or len(data) < ENUM_LIMIT:
            break
        cursor = bottom
    else:
        raise RuntimeError(
            f"subreddit enumeration exceeded {ENUM_MAX_PAGES} pages — source "
            "grew unexpectedly or pagination stalled; investigate before "
            "raising the ceiling."
        )
    return records


def _check_skips(skipped: int, total: int, node_id: str) -> None:
    """Tolerate isolated per-subreddit failures; raise if they look systemic."""
    if skipped > max(MAX_SKIP_ABS, int(MAX_SKIP_FRAC * total)):
        raise RuntimeError(
            f"{node_id}: {skipped}/{total} subreddits failed after retries — "
            "systemic source/network failure, aborting rather than publishing a "
            "silently-decimated table."
        )
    if skipped:
        print(f"  {node_id}: skipped {skipped}/{total} subreddits (isolated, retried next run)")
