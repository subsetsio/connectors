"""Shared CKAN catalog helpers for the ATO connector.

The ATO publishes through the data.gov.au CKAN portal (org
`australiantaxationoffice`). Our collect stage grouped the portal's ~1700
resources into ~489 logical tables by collapsing the per-income-year editions
of each recurring table into one entity (`<family>--<normalised-table>`), with
`income_year` lifted to a column. This module reconstructs that exact grouping
from the live catalog so a fetch fn can recover the CKAN resource ids behind a
given entity id and pull each year's flat datastore table.

The normalisation here MUST stay byte-for-byte identical to the collect stage's
(`data/sources/ato/work/code.py`) — the entity ids are derived from it and the
harness validates download-spec coverage against them.
"""

import re

from subsets_utils import get, transient_retry

BASE = "https://data.gov.au/data"
ORG = "australiantaxationoffice"

# Packages that are yearly editions of one recurring publication: the income
# year lives in the package id and the table set repeats each year. Merge them
# so a recurring table is one entity with income_year as a column.
_YEARLY_FAMILIES = [
    (re.compile(r"^taxation-statistics-(\d{4}-\d{2})$"), "taxation-statistics"),
    (re.compile(r"^international-related-party-dealings-(\d{4}-\d{2})$"),
     "international-related-party-dealings"),
]
_YEAR_TOKEN = re.compile(r"\b(19|20)\d{2}[-–]\d{2}\b|\bts\d{2}\b|\b(19|20)\d{2}\b",
                         re.IGNORECASE)


def _family_and_year(pkg_name: str):
    for pat, fam in _YEARLY_FAMILIES:
        m = pat.match(pkg_name)
        if m:
            return fam, m.group(1)
    return pkg_name, None


def _norm_table(name: str) -> str:
    s = (name or "").lower()
    s = _YEAR_TOKEN.sub(" ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unnamed"


def _entity_id(family: str, resource_name: str) -> str:
    """The collect entity id (== download spec id minus the 'ato-' prefix)."""
    key = f"{family}--{_norm_table(resource_name)}"
    return key.lower().replace("_", "-")


@transient_retry()
def _action(path: str, **params) -> dict:
    r = get(f"{BASE}/api/3/action/{path}", params=params, timeout=(10.0, 120.0))
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN action {path} returned success=false: {body!r}")
    return body["result"]


def fetch_catalog() -> list:
    """All ATO packages (with their resources inline), paginated."""
    out = []
    start = 0
    while True:
        res = _action("package_search", fq=f"organization:{ORG}", rows=50, start=start)
        batch = res.get("results", [])
        out.extend(batch)
        start += len(batch)
        if not batch or start >= res.get("count", 0):
            break
    return out


def build_groups() -> dict:
    """Reconstruct {entity_id -> [resource, ...]} from the live catalog.

    Each resource is a dict: {income_year, resource_id, format, datastore_active}.
    Mirrors the collect grouping exactly (PDF resources dropped).
    """
    groups: dict[str, list] = {}
    for pkg in fetch_catalog():
        fam, pkg_year = _family_and_year(pkg.get("name", ""))
        for res in pkg.get("resources", []):
            fmt = res.get("format") or ""
            if "pdf" in fmt.lower():
                continue
            rname = res.get("name") or res.get("id")
            eid = _entity_id(fam, rname)
            year = pkg_year
            if year is None:
                m = re.search(r"\b((?:19|20)\d{2}[-–]\d{2})\b", rname)
                if m:
                    year = m.group(1).replace("–", "-")
            groups.setdefault(eid, []).append({
                "income_year": year,
                "resource_id": res["id"],
                "format": fmt,
                "datastore_active": bool(res.get("datastore_active")),
            })
    return groups


@transient_retry()
def _datastore_page(resource_id: str, limit: int, offset: int) -> dict:
    r = get(f"{BASE}/api/3/action/datastore_search",
            params={"resource_id": resource_id, "limit": limit, "offset": offset},
            timeout=(10.0, 120.0))
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"datastore_search success=false for {resource_id}: {body!r}")
    return body["result"]


# datastore-internal columns we never want in the published table.
_DROP_COLS = {"_id", "_full_text", "rank"}

# absolute safety ceiling: trips on unexpected source growth instead of looping
# forever. ATO datastore tables are tens of thousands of rows at most.
_MAX_PAGES = 2000
_PAGE = 10000


def datastore_rows(resource_id: str, income_year):
    """Yield every row of a datastore resource as a dict, tagged with income_year.

    datastore stores all values as strings; we keep them as-is (the transform
    does light typing). Paginates by offset until `total` is reached.
    """
    offset = 0
    total = None
    pages = 0
    while True:
        result = _datastore_page(resource_id, _PAGE, offset)
        if total is None:
            total = result.get("total", 0)
        records = result.get("records", [])
        if not records:
            break
        for rec in records:
            row = {k: v for k, v in rec.items() if k not in _DROP_COLS}
            row["income_year"] = income_year
            yield row
        offset += len(records)
        pages += 1
        if offset >= total:
            break
        if pages >= _MAX_PAGES:
            raise RuntimeError(
                f"datastore resource {resource_id} exceeded {_MAX_PAGES} pages "
                f"(offset={offset}, total={total}) — unexpected source growth")
