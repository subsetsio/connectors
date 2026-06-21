"""Shared transport + catalogue helpers for the ITU DataHub connector.

Source: ITU DataHub REST API (https://api.datahub.itu.int/v2), the public API
backing datahub.itu.int — the successor to the discontinued World
Telecommunication/ICT Indicators (WTID) database.

This module holds only the HTTP client and the genuinely cross-subset parse
helpers (catalogue codeIDs, int coercion). NodeSpec definitions live in the
per-subset modules under nodes/.
"""

from subsets_utils import get, transient_retry

BASE = "https://api.datahub.itu.int/v2"


@transient_retry(attempts=7)
def _get_json(path: str, params: dict | None = None):
    resp = get(f"{BASE}/{path}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _catalogue_code_ids() -> tuple[list[int], dict[int, dict]]:
    """Return the catalogue codeIDs plus a codeID -> taxonomy info map."""
    cats = _get_json("dictionaries/getcategories")
    code_ids: list[int] = []
    info: dict[int, dict] = {}
    for cat in cats:
        cname = cat.get("category")
        for sc in cat.get("subCategory", []):
            scname = sc.get("subCategory")
            for it in sc.get("items", []):
                cid = it["codeID"]
                code_ids.append(cid)
                info[cid] = {
                    "category": cname,
                    "sub_category": scname,
                    "is_collection": bool(it.get("isCollection")),
                }
    return code_ids, info


def _as_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None
