"""National Health Mission HMIS — Item-wise HMIS reports (data.gov.in OGD API).

The HMIS source's own NIC portals (nrhm-mis.nic.in, hmis.mohfw.gov.in) are
India-geo-blocked and expose only form-driven Excel "standard reports" with no
API (see research). The Ministry of Health & Family Welfare republishes the same
HMIS data on the data.gov.in OGD platform, which we use here.

Two published subsets, one per accepted collect entity:

- ``hmis-reports`` — the catalog of Item-wise HMIS reports (one row per report:
  resource id, geography, financial year, publisher, column count). Reference
  data, joinable to ``hmis-values`` on ``resource_id``.
- ``hmis-values`` — the long-format observations. data.gov.in carries ~1304
  HMIS-titled resources; they are heterogeneous. We publish the one homogeneous,
  comparable family: the **"Item-wise HMIS report of <GEO> for <FY>"** reports
  (financial years 2008-09 onward). Each report is a wide table of monthly counts
  of routine health-service indicators (ANC, deliveries, immunisation, family
  planning, disease/NCD counts, ...). Two layouts occur: an older 17-column layout
  (one value per month) and a newer 69-column layout (each month split into
  total / public(A) / private(B) / urban(C) / rural(D)). All-India reports carry
  per-STATE rows (``state`` column); per-state reports carry per-DISTRICT rows
  (``district`` column). We normalise both layouts into one long schema (one row
  per geography x indicator x type x month, keeping the public/private/urban/rural
  breakdown as columns). The remaining HMIS-titled resources are small bespoke
  indicator tables with idiosyncratic schemas and are out of scope for this subset.

Auth: the data.gov.in OGD API requires an ``api-key`` query parameter. The public
sample key is NOT usable in production — it hard-caps ``limit`` at 10 rows/request
(silently truncating multi-thousand-row reports) and its globally-shared quota
429-throttles CI egress IPs within a few hundred requests. A registered (free)
key MUST be supplied via the ``DATA_GOV_IN_API_KEY`` environment variable.

Fetch shape: ``hmis-values`` enumerates the item-wise family at runtime and pulls
each report. Reports are immutable historical snapshots, so it uses the batched
(firehose) pattern — one parquet batch per resource, a watermark of completed
resource ids in state — which makes the long backfill resumable if a run is
interrupted. There is no incremental query on the data endpoint; new financial
years appear as new resources and are picked up automatically. Pagination advances
by the number of rows actually returned (never a fixed step), so a server-side
``limit`` cap can never silently skip rows.
"""

from __future__ import annotations

import os
import re

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

SLUG = "national-health-mission-hmis"
STATE_VERSION = 1

_LISTS = "https://api.data.gov.in/lists"
_RESOURCE = "https://api.data.gov.in/resource/{}"
_PAGE = 1000
_PAGINATION_CEILING = 5_000_000  # safety: rows per resource; raises, never silently truncates

# Fiscal-year month order (April..March).
_MONTHS = [
    "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "january", "february", "march",
]

# Item-wise family selector: "Item-wise HMIS report of <GEO> for <FY>".
_ITEM_WISE_RE = re.compile(r"^\s*item-wise hmis report of .+ for \d{4}[-/]\d{2,4}\s*$", re.I)
_FY_RE = re.compile(r"for\s+(\d{4})[-/](\d{2,4})", re.I)
_GEO_RE = re.compile(r"\bof\s+(.+?)\s+for\s+\d{4}[-/]\d{2,4}", re.I)

SCHEMA = pa.schema([
    ("resource_id", pa.string()),
    ("financial_year", pa.string()),
    ("fy_start_year", pa.int64()),
    ("level", pa.string()),
    ("state", pa.string()),
    ("district", pa.string()),
    ("s_no", pa.string()),
    ("parameter", pa.string()),
    ("type", pa.string()),
    ("month", pa.string()),
    ("total", pa.float64()),
    ("public", pa.float64()),
    ("private", pa.float64()),
    ("urban", pa.float64()),
    ("rural", pa.float64()),
])

CATALOG_SCHEMA = pa.schema([
    ("resource_id", pa.string()),
    ("title", pa.string()),
    ("geography", pa.string()),
    ("financial_year", pa.string()),
    ("fy_start_year", pa.int64()),
    ("org_type", pa.string()),
    ("org", pa.string()),
    ("sector", pa.string()),
    ("catalog_uuid", pa.string()),
    ("num_columns", pa.int64()),
    ("created_epoch", pa.int64()),
    ("updated_epoch", pa.int64()),
])


def _api_key() -> str:
    key = os.environ.get("DATA_GOV_IN_API_KEY")
    if not key:
        raise RuntimeError(
            "DATA_GOV_IN_API_KEY is not set — a registered data.gov.in OGD API key is "
            "required to fetch National Health Mission HMIS. The public sample key hard-caps "
            "limit at 10 rows/request and 429-throttles CI IPs; it silently corrupts the "
            "backfill and must not be used."
        )
    return key


# The registered key has generous limits, but pace politely on a large fan-out.
# ratelimit is per-process; each spec runs in its own process, so this bounds the
# node that owns it. Use ~80% headroom below any documented ceiling.
@sleep_and_retry
@limits(calls=8, period=1)
def _http_get(url: str, params: dict):
    return get(url, params=params, timeout=(10.0, 120.0))


# Long, 429-tolerant retry so a throttle window is ridden out rather than failing
# the backfill (the response carries X-Ratelimit-Reset; transient_retry backs off).
@transient_retry(attempts=12, min_wait=10, max_wait=300)
def _get_json(url: str, params: dict) -> dict:
    resp = _http_get(url, params)
    resp.raise_for_status()
    return resp.json()


def _parse_fy(title: str):
    m = _FY_RE.search(title or "")
    if not m:
        return None, None
    y1, y2 = m.group(1), m.group(2)
    if len(y2) == 2:
        y2 = y1[:2] + y2
    return f"{y1}-{y2}", int(y1)


def _parse_geo(title: str):
    m = _GEO_RE.search(title or "")
    return m.group(1).strip() if m else None


def _clean(v):
    if v is None:
        return None
    s = str(v).strip().strip("'").strip()
    return s or None


def _join_list(v):
    if isinstance(v, list):
        s = ", ".join(str(x) for x in v if x)
        return s or None
    return _clean(v)


def _to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _to_float(v):
    if v is None:
        return None
    s = str(v).strip().replace(",", "")
    if s in ("", "NA", "N/A", "-", "--", "nan", "NaN", "null", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _classify_col(field_id: str):
    """Map a raw column id to (month, breakdown), or None if it isn't a monthly
    measure. Handles both the 17-col layout (`april`) and the 69-col layout
    (`april___public_a_`), plus the leading/extra-underscore variants used by
    per-state reports. Annual `total...` columns are intentionally skipped."""
    f = (field_id or "").lower().strip("_")
    for m in _MONTHS:
        if f == m or f.startswith(m):
            rest = f[len(m):]
            if "public" in rest:
                bd = "public"
            elif "private" in rest:
                bd = "private"
            elif "urban" in rest:
                bd = "urban"
            elif "rural" in rest:
                bd = "rural"
            else:
                bd = "total"
            return m, bd
    return None


def _list_item_wise_records() -> list[dict]:
    """Enumerate the item-wise HMIS report family — full /lists records."""
    out, offset = [], 0
    while True:
        doc = _get_json(_LISTS, {
            "api-key": _api_key(),
            "format": "json",
            "filters[active]": "1",
            "notfilters[source]": "visualize.data.gov.in",
            "filters[title]": "HMIS",
            "limit": str(_PAGE),
            "offset": str(offset),
        })
        recs = doc.get("records", []) or []
        for r in recs:
            title = r.get("title", "") or ""
            if r.get("index_name") and _ITEM_WISE_RE.match(title):
                out.append(r)
        total = int(doc.get("total") or 0)
        # advance by rows actually returned — never a fixed step — so a server-side
        # limit cap can never make us skip a window of the catalog.
        offset += len(recs)
        if not recs or offset >= total:
            break
        if offset > _PAGINATION_CEILING:
            raise RuntimeError("runaway pagination enumerating HMIS /lists")
    return out


def _fetch_report_rows(resource_id: str) -> list[dict]:
    rows, offset = [], 0
    while True:
        doc = _get_json(_RESOURCE.format(resource_id), {
            "api-key": _api_key(),
            "format": "json",
            "offset": str(offset),
            "limit": str(_PAGE),
        })
        recs = doc.get("records", []) or []
        rows.extend(recs)
        total = int(doc.get("total") or 0)
        # advance by rows actually returned — guards against a limit cap silently
        # skipping rows (a fixed `offset += _PAGE` step would).
        offset += len(recs)
        if not recs or offset >= total:
            break
        if offset > _PAGINATION_CEILING:
            raise RuntimeError(f"runaway pagination for resource {resource_id} (>{_PAGINATION_CEILING} rows)")
    return rows


def _melt(rows: list[dict], resource_id: str, financial_year, fy_start_year, geo) -> list[dict]:
    out = []
    for r in rows:
        if "district" in r:
            level, state, district = "district", geo, _clean(r.get("district"))
        elif "state" in r:
            level, state, district = "state", _clean(r.get("state")), None
        else:
            continue
        s_no = _clean(r.get("s_no_") or r.get("_s_no_"))
        parameter = _clean(r.get("parameters"))
        typ = _clean(r.get("type"))
        by_month: dict[str, dict] = {}
        for k, v in r.items():
            cls = _classify_col(k)
            if not cls:
                continue
            month, bd = cls
            by_month.setdefault(month, {})[bd] = _to_float(v)
        for month, bds in by_month.items():
            vals = {b: bds.get(b) for b in ("total", "public", "private", "urban", "rural")}
            if all(x is None for x in vals.values()):
                continue
            out.append({
                "resource_id": resource_id,
                "financial_year": financial_year,
                "fy_start_year": fy_start_year,
                "level": level,
                "state": state,
                "district": district,
                "s_no": s_no,
                "parameter": parameter,
                "type": typ,
                "month": month,
                **vals,
            })
    return out


def fetch_hmis_reports(node_id: str) -> None:
    """The catalog of Item-wise HMIS reports (reference data, one row per report)."""
    records = _list_item_wise_records()
    if not records:
        raise RuntimeError("no Item-wise HMIS report resources found on data.gov.in (filter/feed changed?)")
    rows = []
    for r in records:
        title = r.get("title", "") or ""
        fy, fy_start = _parse_fy(title)
        rows.append({
            "resource_id": r.get("index_name"),
            "title": title,
            "geography": _parse_geo(title),
            "financial_year": fy,
            "fy_start_year": fy_start,
            "org_type": _clean(r.get("org_type")),
            "org": _join_list(r.get("org")),
            "sector": _join_list(r.get("sector")),
            "catalog_uuid": _clean(r.get("catalog_uuid")),
            "num_columns": len(r.get("field") or []),
            "created_epoch": _to_int(r.get("created")),
            "updated_epoch": _to_int(r.get("updated")),
        })
    table = pa.Table.from_pylist(rows, schema=CATALOG_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_hmis_values(node_id: str) -> None:
    """Pull every Item-wise HMIS report, normalise to long, write one parquet
    batch per report. Resumable via a watermark of completed resource ids."""
    records = _list_item_wise_records()
    if not records:
        raise RuntimeError("no Item-wise HMIS report resources found on data.gov.in (filter/feed changed?)")

    # Raw is run-scoped (<connector>/runs/<run_id>/raw/...) but state is
    # connector-scoped, so the done-set is only a valid resume signal *within*
    # one run id (a supervisor self-retrigger chain shares it). A fresh run id
    # means fresh run-scoped raw, so reset the watermark and re-fetch in full.
    run_id = os.environ.get("RUN_ID")
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION or state.get("run_id") != run_id:
        state = {"schema_version": STATE_VERSION, "run_id": run_id, "done": []}
    done = set(state.get("done", []))

    for r in records:
        resource_id = r.get("index_name")
        if resource_id in done:
            continue
        title = r.get("title", "") or ""
        financial_year, fy_start_year = _parse_fy(title)
        geo = _parse_geo(title)
        rows = _fetch_report_rows(resource_id)
        long_rows = _melt(rows, resource_id, financial_year, fy_start_year, geo)
        if long_rows:
            table = pa.Table.from_pylist(long_rows, schema=SCHEMA)
            save_raw_parquet(table, f"{node_id}-{resource_id}")  # raw FIRST
        done.add(resource_id)
        state["done"] = sorted(done)
        save_state(node_id, state)                               # then watermark


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-hmis-reports", fn=fetch_hmis_reports, kind="download"),
    NodeSpec(id=f"{SLUG}-hmis-values", fn=fetch_hmis_values, kind="download"),
]
