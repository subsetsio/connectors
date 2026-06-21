"""Shared HTTP client and popular-package enumeration for the npm connector.

The npm search API (/-/v1/search) is the only way to rank packages by
popularity; it requires a text term, caps useful pagination below ~6000 offset
(deeper offsets wrap back to the head — `_MAX_FROM` guards this), and 429s under
sustained load (handled by the tenacity retry). We therefore enumerate over a
fixed list of broad generic terms, dedup by name, and keep the top TARGET by
monthly downloads — a stable, reproducible proxy for "the most-popular packages".

Download nodes are independent (the harness gives them no deps), so the three
per-package feeds each re-enumerate the popular set themselves via
`_popular_records` / `_popular_names`.
"""
import time

from tenacity import (
    retry, retry_if_exception, stop_after_attempt, wait_exponential,
)

from subsets_utils import get, post, is_transient

# ---------------------------------------------------------------------------
# Endpoints / tuning
# ---------------------------------------------------------------------------
SEARCH_URL = "https://registry.npmjs.org/-/v1/search"
REGISTRY_URL = "https://registry.npmjs.org"

# How many popular packages to track across all per-package feeds.
TARGET = 2000
# Broad generic terms; popularity-weighted search returns the most-downloaded
# packages whose metadata matches each term. Blended + deduped they approximate
# the global popular head. Fixed list => reproducible enumeration.
SEARCH_TERMS = [
    "the", "js", "react", "node", "data", "api", "type", "test", "util", "web",
    "app", "file", "string", "json", "http", "vue", "css", "build", "cli", "core",
    "server", "client", "config", "parse", "async",
]
PAGE_SIZE = 250
PAGES_PER_TERM = 8          # blend across terms instead of draining one
_MAX_FROM = 5000            # search wraps to the head beyond ~6000 — stay clear

_retry = retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(7),
    wait=wait_exponential(multiplier=2, min=5, max=120),
    reraise=True,
)


@_retry
def _get_json(url, **kwargs):
    resp = get(url, timeout=(10.0, 180.0), **kwargs)
    resp.raise_for_status()
    return resp.json()


@_retry
def _get_resp(url, **kwargs):
    """GET returning the response; None on a permanent 404 (deleted package)."""
    resp = get(url, timeout=(10.0, 180.0), **kwargs)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp


@_retry
def _post_json(url, payload):
    resp = post(url, json=payload, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Shared popular-package enumeration
# ---------------------------------------------------------------------------
def _popular_records() -> list[dict]:
    """Return the top TARGET packages as flat metadata dicts, ranked by
    monthly downloads (desc). Deterministic given SEARCH_TERMS / TARGET."""
    by_name: dict[str, dict] = {}
    for term in SEARCH_TERMS:
        for page in range(PAGES_PER_TERM):
            frm = page * PAGE_SIZE
            if frm >= _MAX_FROM:
                # Safety: never page into the wrap-around zone.
                raise RuntimeError(f"search offset {frm} >= guard {_MAX_FROM}")
            data = _get_json(SEARCH_URL, params={
                "text": term, "size": PAGE_SIZE, "from": frm,
                "popularity": 1.0, "quality": 0.0, "maintenance": 0.0,
            })
            objs = data.get("objects", [])
            if not objs:
                break
            for obj in objs:
                pkg = obj.get("package") or {}
                name = pkg.get("name")
                if not name:
                    continue
                downloads = obj.get("downloads") or {}
                monthly = downloads.get("monthly")
                rec = {
                    "name": name,
                    "version": pkg.get("version"),
                    "description": pkg.get("description"),
                    "license": pkg.get("license"),
                    "date": pkg.get("date"),
                    "publisher_username": (pkg.get("publisher") or {}).get("username"),
                    "maintainers_count": len(pkg.get("maintainers") or []),
                    "keywords": pkg.get("keywords") or [],
                    "repository_url": (pkg.get("links") or {}).get("repository"),
                    "homepage_url": (pkg.get("links") or {}).get("homepage"),
                    "npm_url": (pkg.get("links") or {}).get("npm"),
                    "monthly_downloads": int(monthly) if monthly is not None else None,
                    "weekly_downloads": (
                        int(downloads["weekly"]) if downloads.get("weekly") is not None else None
                    ),
                    "dependents_count": (
                        int(obj["dependents"]) if obj.get("dependents") is not None else None
                    ),
                    "search_score": (
                        float(obj["searchScore"]) if obj.get("searchScore") is not None else None
                    ),
                }
                prev = by_name.get(name)
                # Keep the record carrying the larger monthly-downloads signal.
                if prev is None or (rec["monthly_downloads"] or 0) > (prev["monthly_downloads"] or 0):
                    by_name[name] = rec
        time.sleep(0.2)

    records = sorted(
        by_name.values(),
        key=lambda r: (r["monthly_downloads"] or 0),
        reverse=True,
    )
    if len(records) < TARGET:
        # Enumeration degraded (terms returned far less than expected).
        raise RuntimeError(f"only {len(records)} popular packages found; expected >= {TARGET}")
    return records[:TARGET]


def _popular_names() -> list[str]:
    return [r["name"] for r in _popular_records()]
