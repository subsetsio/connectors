"""Shared PyPI transport + spine helpers.

Both published subsets share a single retried JSON transport and the same
"top PyPI projects" universe (hugovk/top-pypi-packages, regenerated monthly
from PyPI's official BigQuery download stats). This module holds that shared
machinery; the per-subset fetch/parse/schema live in ``nodes/``.
"""

import httpx

from subsets_utils import get, transient_retry

TOP_PACKAGES_URL = (
    "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
)


@transient_retry()
def get_json(url, **kwargs):
    """GET returning parsed JSON, retried on transient (429/5xx/timeout)."""
    resp = get(url, timeout=(10.0, 120.0), **kwargs)
    resp.raise_for_status()
    if not resp.content:
        # pypistats occasionally returns an empty 200 under load — treat as
        # transient so the retry backoff finds a working moment.
        raise httpx.ReadTimeout("empty response body", request=resp.request)
    return resp.json()


def load_universe():
    """Top PyPI projects (descending by 30-day downloads) from the bulk file."""
    data = get_json(TOP_PACKAGES_URL)
    rows = data["rows"]
    rows = sorted(rows, key=lambda r: r.get("download_count") or 0, reverse=True)
    return rows


def s(v):
    """Render a scalar as a nullable string cell for the raw parquet."""
    return None if v is None else str(v)
