"""Shared HTTP + parsing helpers for the L2Beat connector.

Source: the free, unauthenticated JSON API that powers the l2beat.com website
(https://l2beat.com/api). No bulk export exists, so per-project time series are
fetched one slug at a time. The host sits behind Cloudflare with an aggressive,
undocumented rate limit (~10 requests/minute before a 429 / challenge), so every
request is paced (THROTTLE_S) and retried with jittered exponential backoff. The
two heavy specs (`tvs`, `activity`) run as independent subprocesses that share
that one Cloudflare bucket, hence the random jitter on backoff to avoid the two
crawlers re-colliding in lock-step.
"""

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from subsets_utils import get, is_transient

BASE = "https://l2beat.com/api"
SUMMARY_URL = f"{BASE}/scaling/summary"
THROTTLE_S = 7.0  # base pause between per-project requests. Measured cap is ~6
# requests then a ~60s cooldown (~6-10 req/min). `tvs` and `activity` run as
# concurrent subprocesses sharing this one Cloudflare bucket, so each paces
# conservatively and jittered backoff (below) absorbs the contention.

# A browser-like UA measurably reduces Cloudflare challenges on this host. ASCII only.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

_AGGREGATE_SLUG = "_ecosystem_aggregate"


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(12),
    wait=wait_random_exponential(multiplier=6, max=180),
    reraise=True,
)
def _get_json(url: str) -> dict:
    resp = get(url, headers=_HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _project_slugs() -> list[str]:
    """The per-project endpoints key on each project's `slug` field, NOT the
    dict key (which equals `id`). 11 projects differ — e.g. OP Mainnet's dict
    key is 'optimism' but its endpoint slug is 'op-mainnet'."""
    summary = _get_json(SUMMARY_URL)
    slugs = {p.get("slug") for p in summary["projects"].values() if p.get("slug")}
    return sorted(slugs)


def _chart_rows(payload: dict) -> tuple[list[str], list[list]]:
    """Pull (types, data-rows) out of an L2BEAT chart envelope, or ([], []) when
    the project has no series (some projects 200 with an empty payload)."""
    data = payload.get("data") or {}
    chart = data.get("chart") or {}
    return chart.get("types") or [], chart.get("data") or []
