"""Shared HTTP helpers for the USAspending connector.

USAspending.gov is a public, no-auth REST/JSON API (base
https://api.usaspending.gov/api/v2). Both endpoint families share the same
client + transient retry wrapper, so the GET/POST helpers live here.
"""
from subsets_utils import get, post, transient_retry

API_BASE = "https://api.usaspending.gov/api/v2"


@transient_retry()
def _get(path: str) -> dict:
    resp = get(f"{API_BASE}{path}", timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post(path: str, payload: dict) -> dict:
    resp = post(f"{API_BASE}{path}", json=payload, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()
