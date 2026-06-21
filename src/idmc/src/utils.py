"""Shared HTTP + parse helpers for the IDMC connector.

All endpoints live under `https://helix-tools-api.idmcdb.org/external-api/` and
require the public `client_id` query param (IDMCWSHSOLO009 — the one IDMC's own
data portal uses; omitting it returns 403 "Client is not registered."). No
header/token auth.
"""

from subsets_utils import get, transient_retry

BASE = "https://helix-tools-api.idmcdb.org/external-api"
CLIENT_ID = "IDMCWSHSOLO009"  # public client_id used by IDMC's own data portal
PAGE_SIZE = 100000            # GIDD returns the full corpus in one page at this size
MAX_PAGES_ABS = 50           # safety ceiling: raise if the corpus grows ~50x (don't silently stop)


# ---------------------------------------------------------------------------
# HTTP with honest retry semantics
# ---------------------------------------------------------------------------


@transient_retry()
def get_json(url: str, params: dict | None):
    resp = get(url, params=params, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.json()


def join_field(v):
    """Collapse a nested array (or scalar) field to a scalar string; None if empty."""
    if v is None or v == "" or v == []:
        return None
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    return str(v)


# ---------------------------------------------------------------------------
# GIDD JSON endpoints (paginated envelope)
# ---------------------------------------------------------------------------
def fetch_gidd(path: str) -> list[dict]:
    url = f"{BASE}/gidd/{path}/"
    params = {"client_id": CLIENT_ID, "limit": PAGE_SIZE}
    rows: list[dict] = []
    pages = 0
    while url:
        j = get_json(url, params)
        rows.extend(j.get("results", []))
        url = j.get("next")     # absolute next-page URL (carries client_id+limit)
        params = None           # only the first request needs params
        pages += 1
        if pages > MAX_PAGES_ABS:
            raise AssertionError(
                f"gidd/{path}: exceeded {MAX_PAGES_ABS} pages — corpus grew far past "
                f"expectations or pagination is not terminating"
            )
    return rows
