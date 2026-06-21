"""Shared helpers for the World Justice Project connector.

WJP has no programmatic catalog API; each data product is a single bulk file at
a stable, year-versioned HTTPS URL. The download + cell-coercion helpers below
are shared by every product's node file.
"""

from subsets_utils import get, transient_retry


@transient_retry()
def download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def to_float(v):
    """Coerce a cell to float, returning None for blanks / non-numeric sentinels."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "")
    if not s or s.upper() in ("NA", "N/A", "-", "."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_str(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None
