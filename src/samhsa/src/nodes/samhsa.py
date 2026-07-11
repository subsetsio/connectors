"""SAMHSA connector.

Two openly-accessible, unauthenticated SAMHSA data surfaces (research's other
mechanisms — the NSDUH/TEDS/etc. surveys on www.samhsa.gov/data — are Akamai-WAF
blocked and ship only PDF/SAS, so they are out of scope):

1. findtreatment-facilities — the SAMHSA Behavioral Health Treatment Services
   Locator (findtreatment.gov). No bulk endpoint; the national corpus is
   enumerated by iterating the locator's state-id parameter (limitType=0,
   limitValue = numeric state id 1..~56) and paging each state. ~24.7k
   facilities. Point-in-time directory, full re-pull each run (stateless).

2. escb-scz6 — SAMHSA Synar Reports (youth tobacco sales), the one genuinely
   tabular SAMHSA dataset reachable via an open API, mirrored on CDC's Socrata
   portal (data.cdc.gov). ~1,122 rows, 1997-2018. Full re-pull each run.

Both are small enough to re-fetch in full every run, so both fetch fns are the
default stateless full-pull shape — no watermarks, no cursors.
"""

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

# --- FindTreatment locator ----------------------------------------------------

# A coordinate is required by the API but is irrelevant under a state search
# (limitType=0); results are filtered to the state, only the `miles` sort field
# depends on it. Use the geographic center of the contiguous US.
_CENTER = '"39.5,-98.35"'
# State ids are a small fixed enumeration; iterate generously and skip empties.
_STATE_ID_MAX = 60
_PAGE_SIZE = 2000
# Safety ceiling: a state with >this many pages means the API changed shape.
_MAX_PAGES_PER_STATE = 50

# Facility-level fields we keep (scalars). The nested `services` list and the
# query-relative `_irow`/`miles` fields are dropped — not part of the directory.
_FACILITY_FIELDS = (
    "name1", "name2", "street1", "street2", "city", "state", "zip",
    "phone", "intake1", "hotline1", "website", "latitude", "longitude",
    "typeFacility",
)


@transient_retry()
def _locator_page(state_id: int, page: int) -> dict:
    resp = get(
        "https://findtreatment.gov/locator/exportsAsJson/v2",
        params={
            "sAddr": _CENTER,
            "limitType": 0,        # state-based search
            "limitValue": state_id,  # numeric state id (NOT miles)
            "sType": "both",       # substance-use + mental-health
            "pageSize": _PAGE_SIZE,
            "page": page,
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_findtreatment(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    out = []
    for state_id in range(1, _STATE_ID_MAX + 1):
        first = _locator_page(state_id, 1)
        rows = first.get("rows") or []
        if not rows:
            continue  # state id maps to nothing
        total_pages = int(first.get("totalPages") or 1)
        if total_pages > _MAX_PAGES_PER_STATE:
            raise AssertionError(
                f"state {state_id}: {total_pages} pages exceeds safety cap "
                f"{_MAX_PAGES_PER_STATE} — API shape likely changed"
            )
        for r in rows:
            out.append({k: r.get(k) for k in _FACILITY_FIELDS})
        for page in range(2, total_pages + 1):
            d = _locator_page(state_id, page)
            prows = d.get("rows") or []
            if not prows:
                break
            for r in prows:
                out.append({k: r.get(k) for k in _FACILITY_FIELDS})

    if not out:
        raise AssertionError("findtreatment locator returned 0 facilities")
    save_raw_ndjson(out, asset)


# --- Synar Reports on CDC Socrata --------------------------------------------

_SYNAR_RESOURCE = "https://data.cdc.gov/resource/escb-scz6.json"
_SYNAR_PAGE = 50000  # whole dataset (~1,122 rows) fits in one request


@transient_retry()
def _synar_fetch(offset: int) -> list:
    resp = get(
        _SYNAR_RESOURCE,
        params={"$limit": _SYNAR_PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_synar(node_id: str) -> None:
    asset = node_id
    out = []
    offset = 0
    while True:
        batch = _synar_fetch(offset)
        if not batch:
            break
        out.extend(batch)
        if len(batch) < _SYNAR_PAGE:
            break
        offset += _SYNAR_PAGE

    if not out:
        raise AssertionError("Synar dataset escb-scz6 returned 0 rows")
    save_raw_ndjson(out, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="samhsa-findtreatment-facilities", fn=fetch_findtreatment, kind="download"),
    NodeSpec(id="samhsa-escb-scz6", fn=fetch_synar, kind="download"),
]
