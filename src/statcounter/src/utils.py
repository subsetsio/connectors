"""Shared helpers for the StatCounter connector.

HTTP fetch, error classification, and live region discovery used by both the
time-series statistics fetcher and the screen-resolution fetcher. Contains no
NodeSpec definitions.
"""

import re as _re
from datetime import datetime, timezone

import httpx

from subsets_utils import get

BASE_URL = "https://gs.statcounter.com/chart.php"
HOME_URL = "https://gs.statcounter.com/"

# Source minimum (stable documented fact); the upper bound is computed from the
# clock each run so we never hardcode an end year.
SOURCE_MIN_MONTH = "2009-01"
SOURCE_MIN_YEAR = 2009

# Lowercase 2-letter codes in the region dropdown are continents, not countries.
_CONTINENT_CODES = {"af", "an", "as", "eu", "na", "oc", "sa"}

_MONTH_RE = _re.compile(r"^\d{4}-\d{2}$")


def _get_text(url: str, params: dict | None = None, timeout: tuple[float, float] = (10.0, 45.0)) -> str:
    resp = get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    # Responses are served as application/octet-stream but are plain CSV/HTML.
    return resp.content.decode("utf-8-sig", errors="replace")


def _permanent_4xx(exc: BaseException) -> bool:
    return (
        isinstance(exc, httpx.HTTPStatusError)
        and 400 <= exc.response.status_code < 500
        and exc.response.status_code != 429
    )


def _classify_region(code: str) -> str:
    if code == "ww":
        return "worldwide"
    if code in _CONTINENT_CODES:
        return "continent"
    return "country"


def _discover_regions() -> list[tuple[str, str, str]]:
    """Parse the live region dropdown -> [(code, name, type), ...].

    worldwide + 7 continents + ~249 ISO alpha-2 countries. Discovered rather
    than hardcoded so a newly added country flows through automatically.
    """
    html = _get_text(HOME_URL)
    m = _re.search(r'id="region"[^>]*>(.*?)</select>', html, _re.S | _re.I)
    if not m:
        raise RuntimeError("region dropdown not found on gs.statcounter.com home page")
    opts = _re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>', m.group(1))
    regions = [(code, name.strip(), _classify_region(code)) for code, name in opts if code]
    if len(regions) < 50:
        raise RuntimeError(f"region dropdown returned only {len(regions)} options; parse likely broke")
    return regions


def _current_month() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m")
