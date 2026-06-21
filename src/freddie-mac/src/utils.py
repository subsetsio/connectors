"""Shared helpers for the Freddie Mac connector.

Both bulk CSV files (FMHPI, PMMS) are tiny, stateless full re-pulls over the same
HTTP path, and share the same blank/'.'-means-missing float convention.
"""

from subsets_utils import get, transient_retry


@transient_retry()
def fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def to_float(value):
    """Parse a CSV cell to float; blank, whitespace and '.' mean missing."""
    s = (value or "").strip()
    if s in ("", "."):
        return None
    try:
        return float(s)
    except ValueError:
        return None
