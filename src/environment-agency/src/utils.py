"""Shared HTTP + linked-data flatten helpers for the Environment Agency
(England) Hydrology API connector.

Source: https://environment.data.gov.uk/hydrology (Epimorphics linked-data
platform, Open Government Licence v3, no auth).
"""

from subsets_utils import get, transient_retry

_BASE = "https://environment.data.gov.uk/hydrology"


# --------------------------------------------------------------------------- #
# HTTP with retry/backoff
# --------------------------------------------------------------------------- #


@transient_retry()
def _get_json(path: str, **params):
    resp = get(f"{_BASE}/{path}", params=params, timeout=(10.0, 300.0),
               headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_csv_text(path: str, **params) -> str:
    resp = get(f"{_BASE}/{path}", params=params, timeout=(10.0, 300.0),
               headers={"Accept": "text/csv"})
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# Flatten helpers — collapse the nested linked-data records to flat scalars
# --------------------------------------------------------------------------- #

def _last_seg(uri):
    if isinstance(uri, str):
        return uri.rsplit("/", 1)[-1]
    return None


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _id_of(v):
    """Last URI segment of a {@id: ...} struct or a bare string."""
    if isinstance(v, dict):
        return _last_seg(v.get("@id"))
    return _last_seg(v)


def _label_of(v):
    """label of a {@id, label} struct, else last URI segment, else str."""
    if isinstance(v, dict):
        return v.get("label") or _last_seg(v.get("@id"))
    return v if isinstance(v, str) else None


def _str(v):
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, list):
        return ", ".join(s for s in (_str(x) for x in v) if s) or None
    if isinstance(v, dict):
        return _label_of(v)
    return str(v)


def _to_int(v):
    try:
        return int(v) if v is not None and v != "" else None
    except (ValueError, TypeError):
        return None


def _to_float(v):
    try:
        return float(v) if v is not None and v != "" else None
    except (ValueError, TypeError):
        return None
