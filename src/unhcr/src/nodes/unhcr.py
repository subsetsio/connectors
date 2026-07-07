"""UNHCR Refugee Data Finder connector.

Source: UNHCR population/v1 REST API (https://api.unhcr.org/population/v1/).
Open, no auth. Eight data endpoints, each its own published table:
population, asylum-applications, asylum-decisions, demographics, solutions,
idmc, unrwa, nowcasting.

Fetch shape: stateless full re-pull. The whole corpus is small (the largest,
population, is ~130k rows across 1951-present) and the API exposes no
since/cursor/ETag delta filter, so we re-fetch every endpoint in full each
refresh and overwrite. Omitting the year filter returns the complete history;
coo_all=true & coa_all=true break results down by every origin/asylum country.

Raw format: NDJSON. Measure values arrive inconsistently typed across rows
(int like 13, or string like '0', with '-' meaning missing). The fetch
normalizes '-'/'' to null and numeric strings to int so each column lands
cleanly typed; the transform SQL then TRY_CASTs defensively.
"""
import pyarrow as pa  # noqa: F401  (kept for parity; NDJSON path doesn't build a table)

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://api.unhcr.org/population/v1/"
PAGE_SIZE = 20000
MAX_PAGES = 5000  # safety ceiling; the API reports <10 pages at this size

# The entity union — copied from
# data/sources/unhcr/work/entity_union.json. Each id is also the API path.
ENTITY_IDS = [
    "asylum-applications",
    "asylum-decisions",
    "demographics",
    "idmc",
    "nowcasting",
    "population",
    "solutions",
    "unrwa",
]

# nowcasting returns only current-year national estimates and does not accept
# the per-country breakdown flags; every other endpoint takes them.
_NO_BREAKDOWN = {"nowcasting"}


def _fetch_page(endpoint: str, params: dict) -> dict:
    resp = get(BASE + endpoint + "/", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _clean(value):
    """Normalize one cell: '-'/'' -> None, numeric string -> int, else as-is."""
    if value == "-":
        return None
    if isinstance(value, str):
        s = value.strip()
        if s == "":
            return None
        if s.lstrip("-").isdigit():
            return int(s)
        return value
    return value


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    endpoint = node_id[len("unhcr-"):]

    params = {"limit": PAGE_SIZE, "page": 1, "cf_type": "ISO"}
    if endpoint not in _NO_BREAKDOWN:
        params["coo_all"] = "true"
        params["coa_all"] = "true"

    first = _fetch_page(endpoint, params)
    max_pages = int(first.get("maxPages") or 0)
    if max_pages > MAX_PAGES:
        raise RuntimeError(
            f"{endpoint}: maxPages={max_pages} exceeds safety cap {MAX_PAGES} "
            "at limit=20000 — source grew unexpectedly, review pagination"
        )

    rows = list(first.get("items") or [])
    for page in range(2, max_pages + 1):
        params["page"] = page
        doc = _fetch_page(endpoint, params)
        rows.extend(doc.get("items") or [])

    cleaned = [{k: _clean(v) for k, v in row.items()} for row in rows]
    save_raw_ndjson(cleaned, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"unhcr-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
