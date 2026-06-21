"""National Health Mission HMIS — Item-wise HMIS reports (data.gov.in OGD API).

The HMIS source's own NIC portals (nrhm-mis.nic.in, hmis.mohfw.gov.in) are
India-geo-blocked and expose only form-driven Excel "standard reports" with no
API (see research). The Ministry of Health & Family Welfare republishes the same
HMIS data on the data.gov.in OGD platform, which we use here.

Scope — the `hmis-values` subset. data.gov.in carries ~1304 HMIS-titled resources;
they are heterogeneous. This connector publishes the one homogeneous, comparable
family: the **"Item-wise HMIS report of <GEO> for <FY>"** reports (~334 resources,
financial years 2008-09 onward). Each report is a wide table of monthly counts of
routine health-service indicators (ANC, deliveries, immunisation, family planning,
disease/NCD counts, …). Two layouts occur: an older 17-column layout (one value per
month) and a newer 69-column layout (each month split into total / public(A) /
private(B) / urban(C) / rural(D)). All-India reports carry per-STATE rows (`state`
column); per-state reports carry per-DISTRICT rows (`district` column). We normalise
both layouts into one long schema (one row per geography × indicator × type × month,
with the public/private/urban/rural breakdown kept as columns). The ~970 remaining
HMIS-titled resources are small bespoke indicator tables with idiosyncratic schemas
and are out of scope for this subset.

Fetch shape: the single `hmis-values` download node enumerates the item-wise family
at runtime and pulls each report. Reports are immutable historical snapshots, so it
uses the batched (firehose) pattern — one parquet batch per resource, a watermark of
completed resource ids in state — which makes the long backfill resumable if a run is
interrupted. There is no incremental query on the data endpoint; new financial years
appear as new resources and are picked up automatically.
"""

from __future__ import annotations

import os
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

SLUG = "national-health-mission-hmis"
STATE_VERSION = 1

_SAMPLE_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
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


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or _SAMPLE_KEY


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
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


def _list_item_wise_resources() -> list[tuple[str, str]]:
    """Enumerate the item-wise HMIS report family (resource_id, title)."""
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
            rid = r.get("index_name")
            if rid and _ITEM_WISE_RE.match(title):
                out.append((rid, title))
        total = int(doc.get("total") or 0)
        offset += _PAGE
        if not recs or offset >= total:
            break
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
        offset += _PAGE
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


def fetch_hmis_values(node_id: str) -> None:
    """Pull every Item-wise HMIS report, normalise to long, write one parquet
    batch per report. Resumable via a watermark of completed resource ids."""
    resources = _list_item_wise_resources()
    if not resources:
        raise RuntimeError("no Item-wise HMIS report resources found on data.gov.in (filter/feed changed?)")

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "done": []}
    done = set(state.get("done", []))

    for resource_id, title in resources:
        if resource_id in done:
            continue
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
    NodeSpec(id=f"{SLUG}-hmis-values", fn=fetch_hmis_values, kind="download"),
]

_MONTH_NUM = """
    CASE month
        WHEN 'january' THEN 1 WHEN 'february' THEN 2 WHEN 'march' THEN 3
        WHEN 'april' THEN 4 WHEN 'may' THEN 5 WHEN 'june' THEN 6
        WHEN 'july' THEN 7 WHEN 'august' THEN 8 WHEN 'september' THEN 9
        WHEN 'october' THEN 10 WHEN 'november' THEN 11 WHEN 'december' THEN 12
    END
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-hmis-values-transform",
        deps=[f"{SLUG}-hmis-values"],
        sql=f'''
            SELECT
                make_date(
                    fy_start_year + CASE WHEN month IN ('january','february','march') THEN 1 ELSE 0 END,
                    {_MONTH_NUM},
                    1
                )                              AS period,
                financial_year,
                level,
                state,
                district,
                s_no,
                parameter,
                type,
                total,
                public,
                private,
                urban,
                rural
            FROM "{SLUG}-hmis-values"
            WHERE fy_start_year IS NOT NULL
              AND month IS NOT NULL
              AND state IS NOT NULL
              AND parameter IS NOT NULL
              AND (total IS NOT NULL OR public IS NOT NULL OR private IS NOT NULL
                   OR urban IS NOT NULL OR rural IS NOT NULL)
            QUALIFY row_number() OVER (
                PARTITION BY level, state, district, s_no, type, period
                ORDER BY resource_id
            ) = 1
        ''',
    ),
]
