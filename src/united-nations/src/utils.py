"""Shared HTTP + parse helpers for the United Nations SDG connector.

Holds the base URL, the JSON GET helper used by every subset, and the
order-preserving dedupe used by the indicator/series flatteners. No NodeSpec
definitions live here.
"""
from subsets_utils import get, transient_retry

BASE = "https://unstats.un.org/sdgapi/v1/sdg/"


@transient_retry()
def get_json(path: str, **params):
    resp = get(BASE + path, params=params or None, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def dedupe(seq) -> list:
    """Order-preserving dedupe — a series can list the same goal/target twice."""
    seen, out = set(), []
    for x in seq or []:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
