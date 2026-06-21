"""SteamDB shared transport — keyless Steam Web API + Storefront API.

Shared HTTP client, retry, base URLs, and the chart-appid universe helper used
by 2+ node files. No NodeSpec definitions live here.

Rate limits: api.steampowered.com charts are unthrottled one-shot calls;
store.steampowered.com/api is community-throttled ~200 req / 5 min per IP, so
store fetches are capped at ~16/min per process (the app-details and app-reviews
specs both hit that host and don't coordinate, so each takes ~half the budget)
with exponential backoff on 429 as the real safety net.
"""
import httpx
from ratelimit import limits, sleep_and_retry
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import get

WEB_API = "https://api.steampowered.com"
STORE_API = "https://store.steampowered.com"

# --- chart endpoints (web_api) ---
CONCURRENT_URL = f"{WEB_API}/ISteamChartsService/GetGamesByConcurrentPlayers/v1/"
MOST_PLAYED_URL = f"{WEB_API}/ISteamChartsService/GetMostPlayedGames/v1/"
TOP_RELEASES_URL = f"{WEB_API}/ISteamChartsService/GetTopReleasesPages/v1/"


# ----------------------------------------------------------------------------
# transport
# ----------------------------------------------------------------------------
class _Throttled(Exception):
    """Store API returned 200 with a null/empty body — its silent throttle."""


_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC) or isinstance(exc, _Throttled):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _web_json(url: str) -> dict:
    """Steam Web API — one-shot, unthrottled."""
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=5, max=180),
    reraise=True,
)
def _store_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body:
        raise _Throttled(f"null/empty body from {url}")
    return body


@sleep_and_retry
@limits(calls=16, period=60)  # ~80% of half the ~200/5min per-IP store budget
def _store_json_limited(url: str) -> dict:
    return _store_json(url)


def _chart_appids() -> list[int]:
    """Union of appids across the three charts — the enrichment universe."""
    ids: set[int] = set()
    for r in _web_json(CONCURRENT_URL)["response"].get("ranks", []):
        ids.add(int(r["appid"]))
    for r in _web_json(MOST_PLAYED_URL)["response"].get("ranks", []):
        ids.add(int(r["appid"]))
    for p in _web_json(TOP_RELEASES_URL)["response"].get("pages", []):
        for it in p.get("item_ids", []):
            ids.add(int(it["appid"]))
    if len(ids) < 50:
        raise AssertionError(f"chart appid union collapsed to {len(ids)} (<50); charts likely degraded")
    return sorted(ids)
