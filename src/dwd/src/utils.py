"""Shared transport for the DWD (Deutscher Wetterdienst) CDC connector.

The public, anonymous nginx file server at
https://opendata.dwd.de/climate_environment/CDC/ exposes Apache-style directory
indexes; node modules walk those indexes then fetch leaf files off their stable
URLs. Retry transient errors (429/5xx/timeouts), surface everything else.
"""

import re

import httpx

from subsets_utils import get, transient_retry

CDC = "https://opendata.dwd.de/climate_environment/CDC"
OBS = f"{CDC}/observations_germany/climate"
REG = f"{CDC}/regional_averages_DE"


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_text(url: str, encoding: str | None = None) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    if encoding:
        resp.encoding = encoding
    return resp.text


def _list_hrefs(url: str) -> list[str]:
    """Apache autoindex hrefs (excluding sort/parent links). [] on 404."""
    try:
        html = _get_text(url)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return []
        raise
    return [h for h in re.findall(r'href="([^"?][^"]*)"', html) if not h.startswith("..")]
