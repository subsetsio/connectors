"""Shared transport for the NASA connector node files.

Canonical retry on transient failures only, plus the two no-auth request
helpers (JSON and text) used by the JPL, GISTEMP and EONET node modules. The
Exoplanet TAP node streams straight to disk and only needs the retry decorator.
"""

from __future__ import annotations

from subsets_utils import get, transient_retry

# Canonical retry on transient failures only.
retry = transient_retry()


@retry
def get_json(url: str, params: dict | None = None):
    resp = get(url, params=params or {}, timeout=(15.0, 300.0))
    resp.raise_for_status()
    return resp.json()


@retry
def get_text(url: str, params: dict | None = None) -> str:
    resp = get(url, params=params or {}, timeout=(15.0, 180.0))
    resp.raise_for_status()
    return resp.text
