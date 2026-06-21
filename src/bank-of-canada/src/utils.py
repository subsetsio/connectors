"""Shared HTTP helpers for the Bank of Canada connector — Valet REST API
(https://www.bankofcanada.ca/valet).

This module is `_`-prefixed so the node loader (orchestrator.py:1123) skips it
when scanning for `*_SPECS`. It holds only the base URL, the JSON fetch with
transient retry, and the permanent-client-error predicate — code shared by the
groups, series, and observations subset modules. No NodeSpecs live here.
"""
import httpx

from subsets_utils import get, transient_retry

BASE = "https://www.bankofcanada.ca/valet"


def _is_permanent_client_error(exc: BaseException) -> bool:
    return (
        isinstance(exc, httpx.HTTPStatusError)
        and 400 <= exc.response.status_code < 500
        and exc.response.status_code != 429
    )


@transient_retry()
def _fetch_json(url: str, **params) -> dict:
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()
