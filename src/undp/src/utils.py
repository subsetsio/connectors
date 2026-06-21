"""Shared HTTP + cell-coercion helpers for the UNDP node modules."""
from subsets_utils import get, transient_retry


@transient_retry()
def fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def num(v):
    """Coerce a cell to float, or None for blanks / non-numeric markers."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s or s in ("..", "...", "n.a.", "N/A", "-", "—", "–"):
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None
