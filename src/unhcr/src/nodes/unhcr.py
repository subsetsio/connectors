"""UNHCR Refugee Data Finder connector.

Source: UNHCR population/v1 REST API (https://api.unhcr.org/population/v1/).
Open, no auth. Ten endpoints, each its own published table:

- data:      population, asylum-applications, asylum-decisions, demographics,
             solutions, nowcasting
- reference: countries, regions, years, footnotes

(The `idmc` and `unrwa` endpoints are deliberately NOT fetched: they carry
third-party data that the UNHCR Terms of Use for Datasets clause 6 excludes
from the CC BY 4.0 grant. Both entities are deferred at the accept stage.)

Fetch shape: stateless full re-pull. The whole corpus is small (the largest,
population, is ~130k rows across 1951-present) and the API exposes no
since/cursor/ETag delta filter, so we re-fetch every endpoint in full each
refresh and overwrite. Omitting the year filter returns the complete history;
coo_all=true & coa_all=true break results down by every origin/asylum country.

Raw format: NDJSON. On the data endpoints measure values arrive inconsistently
typed across rows (int like 13, or string like '0', with '-' meaning missing);
the fetch normalizes '-'/'' to null and numeric strings to int so each column
lands cleanly typed, and the transform SQL then TRY_CASTs defensively.

The reference endpoints are cleaned more conservatively -- blanks to null, but
NO numeric coercion, because `footnotes.year` is a free-text period that is
sometimes a bare year ('2015') and sometimes a range ('2015 - 2018, 2020 -
2024'). Coercing the bare years would split that column across int and string.
Reference rows also carry a junk column literally named "0" (constant 1 on
every row of countries/regions), which is dropped.
"""
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

from constants import ENTITY_IDS, REFERENCE_ENDPOINTS

BASE = "https://api.unhcr.org/population/v1/"
PAGE_SIZE = 20000
MAX_PAGES = 5000  # safety ceiling; the API reports <10 pages at this size

# nowcasting returns only current-year national estimates and does not accept
# the per-country breakdown flags; neither do the reference tables. Every other
# endpoint takes them.
_NO_BREAKDOWN = REFERENCE_ENDPOINTS | {"nowcasting"}

# Constant-1 index column the reference endpoints emit; carries no information
# and is not a legal bare identifier downstream.
_JUNK_COLUMN = "0"


def _fetch_page(endpoint: str, params: dict) -> dict:
    resp = get(BASE + endpoint + "/", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _blank_to_none(value):
    """'-' and '' mean missing on every endpoint."""
    if value == "-":
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def _clean_measure(value):
    """Data-endpoint cell: blanks -> None, numeric string -> int, else as-is."""
    value = _blank_to_none(value)
    if isinstance(value, str):
        s = value.strip()
        if s.lstrip("-").isdigit():
            return int(s)
    return value


def _clean_row(row: dict, is_reference: bool) -> dict:
    if is_reference:
        return {
            k: _blank_to_none(v) for k, v in row.items() if k != _JUNK_COLUMN
        }
    return {k: _clean_measure(v) for k, v in row.items()}


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    endpoint = node_id[len("unhcr-"):]
    is_reference = endpoint in REFERENCE_ENDPOINTS

    params = {"limit": PAGE_SIZE, "page": 1}
    if endpoint not in _NO_BREAKDOWN:
        params["coo_all"] = "true"
        params["coa_all"] = "true"
    if not is_reference:
        params["cf_type"] = "ISO"

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

    save_raw_ndjson([_clean_row(r, is_reference) for r in rows], asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"unhcr-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
