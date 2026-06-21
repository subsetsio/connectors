"""PPAC (Petroleum Planning & Analysis Cell, India) connector.

Two fetch mechanisms, one published Delta table per rank-accepted entity:

* 8 REST entities (consumption, production, prices, imports, gas) are served by
  PPAC's AjaxController as uniform JSON: ``{"result": {idx: {title, april..march,
  total, colspan, ...}}}``. One generic ``fetch_rest`` melts every page into a
  tidy long table ``(financial_year, section, item, period, unit, value)``. The
  ``colspan`` rows are section headers; a two-slot (major/minor) tracker rebuilds
  the category path so nested blocks (e.g. gross vs net gas production) stay
  distinct. The API only serves the recent financial years listed in each page's
  dropdown, which we discover live (never hard-coded).

* 5 XLSX entities publish a downloadable Excel export (point-in-time URL, so the
  link is re-discovered from the page each run). Each has a dedicated parser:
  two state/value snapshots, the refinery-capacity register, the deep state-wise
  consumption history, and LNG import totals.

Full re-pull every refresh (a few hundred KB total); freshness is the maintain
step's concern, so no short-circuits here.
"""

import io
import re
import json

import pyarrow as pa

from subsets_utils import (
    NodeSpec, SqlNodeSpec, get, post, save_raw_parquet, transient_retry,
)
from constants import REST_CONFIG, XLSX_SNAPSHOT, ENTITY_IDS

import openpyxl

BASE = "https://ppac.gov.in"
PREFIX = "ppac-"
MONTHS = [
    "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "january", "february", "march",
]
_FY_MONTH_OFFSET = {m: i for i, m in enumerate(MONTHS)}  # 0=April

REST_SCHEMA = pa.schema([
    ("financial_year", pa.string()),
    ("section", pa.string()),
    ("item", pa.string()),
    ("month", pa.string()),
    ("period", pa.string()),
    ("unit", pa.string()),
    ("value", pa.float64()),
])
SNAPSHOT_SCHEMA = pa.schema([
    ("state", pa.string()),
    ("as_of", pa.string()),
    ("unit", pa.string()),
    ("value", pa.float64()),
])
REFCAP_SCHEMA = pa.schema([
    ("company", pa.string()),
    ("refinery", pa.string()),
    ("state", pa.string()),
    ("capacity", pa.float64()),
    ("as_of", pa.string()),
    ("unit", pa.string()),
])
STATEWISE_SCHEMA = pa.schema([
    ("product", pa.string()),
    ("region", pa.string()),
    ("state", pa.string()),
    ("fiscal_year", pa.string()),
    ("unit", pa.string()),
    ("value", pa.float64()),
])
LNG_SCHEMA = pa.schema([
    ("metric", pa.string()),
    ("fiscal_year", pa.string()),
    ("unit", pa.string()),
    ("value", pa.float64()),
])


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _entity_of(node_id: str) -> str:
    return node_id[len(PREFIX):]


def _strip_html(s) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s))).strip()


def _num(v):
    """Coerce a cell to float, or None for empty/non-numeric/HTML cells."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "")
    if not s or "<" in s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _as_date_str(v):
    """Best-effort YYYY-MM-DD from a header cell (datetime or ISO-ish string)."""
    if v is None:
        return None
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m-%d")
    s = str(v)
    m = re.search(r"\d{4}-\d{2}-\d{2}", s)
    if m:
        return m.group(0)
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", s)   # D.MM.YYYY (refinery as-of)
    if m:
        d, mo, y = m.groups()
        return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"
    return None


def _fy_month_date(financial_year: str, month: str) -> str:
    start = int(financial_year.split("-")[0])
    offset = _FY_MONTH_OFFSET[month]          # April=0 .. March=11
    # April..December -> start year; January..March -> start+1
    year = start if offset <= 8 else start + 1
    calendar_month = (4 + offset - 1) % 12 + 1
    return f"{year:04d}-{calendar_month:02d}-01"


def _find_row(rows, pred):
    for i, r in enumerate(rows):
        if pred(r):
            return i
    return None


@transient_retry()
def _get_text(url: str) -> str:
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.text


@transient_retry()
def _get_bytes(url: str) -> bytes:
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.content


@transient_retry()
def _post_ajax(method: str, fy: str, report_by: str, page_id: str):
    r = post(
        f"{BASE}/AjaxController/{method}",
        data={"financialYear": fy, "reportBy": report_by, "pageId": page_id},
        headers={"X-Requested-With": "XMLHttpRequest"},
        timeout=(10.0, 120.0),
    )
    r.raise_for_status()
    # Content-Type is text/html but the body is JSON (verified during research).
    return json.loads(r.text).get("result")


def _discover_financial_years(page_path: str):
    html = _get_text(f"{BASE}/{page_path}")
    fys = sorted(set(re.findall(r'<option value="(\d{4}-\d{4})"', html)))
    if not fys:
        raise RuntimeError(f"no financial years found in dropdown on /{page_path}")
    return fys


def _discover_xlsx_url(page_path: str) -> str:
    html = _get_text(f"{BASE}/{page_path}")
    urls = re.findall(
        r'(https://ppac\.gov\.in/uploads/[^"\']+\.xlsx'
        r'|https://ppac\.gov\.in/download\.php\?file=[^"\']+\.xlsx)',
        html,
    )
    urls = list(dict.fromkeys(urls))
    if not urls:
        raise RuntimeError(f"no xlsx download link found on /{page_path}")
    return urls[0]


def _load_xlsx(url: str):
    return openpyxl.load_workbook(io.BytesIO(_get_bytes(url)), data_only=True, read_only=True)


def _rows_of(ws):
    return [list(r) for r in ws.iter_rows(values_only=True)]


# --------------------------------------------------------------------------- #
# REST fetch (8 entities)
# --------------------------------------------------------------------------- #
def _parse_uniform(result, financial_year: str, unit: str, item_override=None):
    """Melt one AjaxController FY response into long observations."""
    rows_in = list(result.values()) if isinstance(result, dict) else (result or [])
    major = None
    minor = None
    out = []
    for row in rows_in:
        if not isinstance(row, dict):
            continue
        title = _strip_html(row.get("title", ""))
        colspan = str(row.get("colspan") or "").strip()
        if colspan:                       # section header or footnote row
            if not title:
                continue
            if re.match(r"^[A-Za-z]\)", title):   # sub-header like "A) Onshore:"
                minor = title
            else:
                major, minor = title, None
            continue
        if not title:
            continue
        section = " - ".join(x for x in (major, minor) if x)
        for m in MONTHS:
            v = _num(row.get(m))
            if v is None:
                continue
            out.append({
                "financial_year": financial_year,
                "section": section,
                "item": item_override or title,
                "month": m,
                "period": _fy_month_date(financial_year, m),
                "unit": unit,
                "value": v,
            })
    return out


def fetch_rest(node_id: str) -> None:
    entity = _entity_of(node_id)
    cfg = REST_CONFIG[entity]
    rows = []
    for fy in _discover_financial_years(cfg["page_path"]):
        result = _post_ajax(cfg["method"], fy, cfg["report_by"], cfg["page_id"])
        rows.extend(_parse_uniform(result, fy, cfg["unit"], cfg.get("item_override")))
    if not rows:
        raise RuntimeError(f"{node_id}: AjaxController returned no observations")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=REST_SCHEMA), node_id)


# --------------------------------------------------------------------------- #
# XLSX fetches (5 entities)
# --------------------------------------------------------------------------- #
def fetch_snapshot(node_id: str) -> None:
    """State -> single current value (active LPG customers / PMUY connections)."""
    entity = _entity_of(node_id)
    cfg = XLSX_SNAPSHOT[entity]
    ws = _load_xlsx(_discover_xlsx_url(cfg["page_path"])).worksheets[0]
    rs = _rows_of(ws)
    hdr = _find_row(rs, lambda r: bool(r) and str(r[0] or "").strip().upper().startswith("STATE/UT"))
    if hdr is None:
        raise RuntimeError(f"{node_id}: no STATE/UT header row in workbook")
    as_of = _as_date_str(rs[hdr][1]) if len(rs[hdr]) > 1 else None
    out = []
    for r in rs[hdr + 1:]:
        state = r[0] if r else None
        value = _num(r[1]) if len(r) > 1 else None
        if state and value is not None:
            out.append({"state": str(state).strip(), "as_of": as_of,
                        "unit": cfg["unit"], "value": value})
    if not out:
        raise RuntimeError(f"{node_id}: parsed 0 state rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=SNAPSHOT_SCHEMA), node_id)


def fetch_refinery_capacity(node_id: str) -> None:
    ws = _load_xlsx(_discover_xlsx_url("infrastructure/installed-refinery-capacity")).worksheets[0]
    rs = _rows_of(ws)
    hdr = _find_row(rs, lambda r: any(str(c or "").strip().upper() == "REFINERIES" for c in (r or [])))
    if hdr is None:
        raise RuntimeError(f"{node_id}: no REFINERIES header row")
    header = rs[hdr]
    idx = {}
    for j, c in enumerate(header):
        name = str(c or "").strip().upper()
        if name == "COMPANY":
            idx["company"] = j
        elif name == "REFINERIES":
            idx["refinery"] = j
        elif name == "STATE":
            idx["state"] = j
    cap_idx = len(header) - 1
    as_of = _as_date_str(header[cap_idx])
    company = None
    out = []
    for r in rs[hdr + 1:]:
        comp = r[idx["company"]] if "company" in idx and idx["company"] < len(r) else None
        if comp and str(comp).strip():
            company = str(comp).strip()
        refi = r[idx["refinery"]] if "refinery" in idx and idx["refinery"] < len(r) else None
        state = r[idx["state"]] if "state" in idx and idx["state"] < len(r) else None
        cap = _num(r[cap_idx]) if cap_idx < len(r) else None
        if not refi or cap is None:
            continue
        refi = str(refi).strip()
        if "TOTAL" in refi.upper():        # skip company / all-India subtotals
            continue
        out.append({"company": company, "refinery": refi,
                    "state": (str(state).strip() if state else None),
                    "capacity": cap, "as_of": as_of, "unit": "'000 MT"})
    if not out:
        raise RuntimeError(f"{node_id}: parsed 0 refinery rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=REFCAP_SCHEMA), node_id)


def _sheet_to_product(title: str) -> str:
    rest = re.sub(r"(?i)^PT[_ ]?Cons[_ ]?Statewise", "", title).strip()
    return rest if rest else "All Products"


def fetch_statewise_consumption(node_id: str) -> None:
    wb = _load_xlsx(_discover_xlsx_url("consumption/state-wise"))
    out = []
    for ws in wb.worksheets:
        product = _sheet_to_product(ws.title)
        rs = _rows_of(ws)
        hdr = _find_row(rs, lambda r: bool(r) and str(r[0] or "").strip().upper().startswith("STATE/UT"))
        if hdr is None:
            continue
        years = [(j, str(y).strip()) for j, y in enumerate(rs[hdr])
                 if j >= 1 and y and re.match(r"^\d{4}-\d{2,4}$", str(y).strip())]
        region = None
        for r in rs[hdr + 1:]:
            lbl = r[0] if r else None
            if not lbl:
                continue
            lbl = str(lbl).strip()
            vals = [(yr, _num(r[j]) if j < len(r) else None) for j, yr in years]
            if all(v is None for _, v in vals):
                if lbl.upper().startswith("REGION"):
                    region = lbl
                continue
            for yr, v in vals:
                if v is not None:
                    out.append({"product": product, "region": region, "state": lbl,
                                "fiscal_year": yr, "unit": "'000 Metric Tonnes", "value": v})
    if not out:
        raise RuntimeError(f"{node_id}: parsed 0 state-wise rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=STATEWISE_SCHEMA), node_id)


def _lng_unit(metric: str) -> str:
    m = metric.upper()
    if "MMT" in m:
        return "MMT"
    if "CRORE" in m or "RS" in m:
        return "Rs Crore"
    return ""


def fetch_lng_import(node_id: str) -> None:
    ws = _load_xlsx(_discover_xlsx_url("natural-gas/import")).worksheets[0]
    rs = _rows_of(ws)
    hdr = _find_row(rs, lambda r: bool(r) and str(r[0] or "").strip().lower() == "year")
    if hdr is None:
        raise RuntimeError(f"{node_id}: no 'Year' header row in LNG workbook")
    years = [(j, str(y).strip()) for j, y in enumerate(rs[hdr])
             if j >= 1 and y and re.match(r"^\d{4}-\d{2}$", str(y).strip())]
    out = []
    for r in rs[hdr + 1:]:
        lbl = r[0] if r else None
        if not lbl:
            continue
        lbl = str(lbl).strip()
        for j, yr in years:
            v = _num(r[j]) if j < len(r) else None
            if v is not None:
                out.append({"metric": lbl, "fiscal_year": yr, "unit": _lng_unit(lbl), "value": v})
    if not out:
        raise RuntimeError(f"{node_id}: parsed 0 LNG rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=LNG_SCHEMA), node_id)


# --------------------------------------------------------------------------- #
# DOWNLOAD_SPECS — one per entity-union member
# --------------------------------------------------------------------------- #
def _spec_id(entity_id: str) -> str:
    return f"{PREFIX}{entity_id.lower().replace('_', '-')}"


_XLSX_BESPOKE = {
    "infrastructure-installed-refinery-capacity": fetch_refinery_capacity,
    "consumption-state-wise": fetch_statewise_consumption,
    "natural-gas-import": fetch_lng_import,
}

DOWNLOAD_SPECS = (
    [NodeSpec(id=_spec_id(e), fn=fetch_rest, kind="download") for e in REST_CONFIG]
    + [NodeSpec(id=_spec_id(e), fn=fetch_snapshot, kind="download") for e in XLSX_SNAPSHOT]
    + [NodeSpec(id=_spec_id(e), fn=fn, kind="download") for e, fn in _XLSX_BESPOKE.items()]
)


# --------------------------------------------------------------------------- #
# TRANSFORM_SPECS — one published Delta table per download
# --------------------------------------------------------------------------- #
def _transform_sql(entity_id: str, dep_id: str) -> str:
    if entity_id in REST_CONFIG:
        return f'''
            SELECT CAST(period AS DATE) AS date,
                   financial_year,
                   section,
                   item,
                   unit,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep_id}"
            WHERE value IS NOT NULL
        '''
    if entity_id in XLSX_SNAPSHOT:
        return f'''
            SELECT state,
                   TRY_CAST(as_of AS DATE) AS as_of,
                   unit,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep_id}"
            WHERE state IS NOT NULL AND value IS NOT NULL
        '''
    if entity_id == "infrastructure-installed-refinery-capacity":
        return f'''
            SELECT company,
                   refinery,
                   state,
                   CAST(capacity AS DOUBLE) AS capacity_kt,
                   TRY_CAST(as_of AS DATE) AS as_of,
                   unit
            FROM "{dep_id}"
            WHERE refinery IS NOT NULL AND capacity IS NOT NULL
        '''
    if entity_id == "consumption-state-wise":
        return f'''
            SELECT product,
                   region,
                   state,
                   fiscal_year,
                   unit,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep_id}"
            WHERE value IS NOT NULL
        '''
    if entity_id == "natural-gas-import":
        return f'''
            SELECT metric,
                   fiscal_year,
                   unit,
                   CAST(value AS DOUBLE) AS value
            FROM "{dep_id}"
            WHERE value IS NOT NULL
        '''
    raise RuntimeError(f"no transform SQL for entity {entity_id}")


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_transform_sql(_entity_of(s.id), s.id))
    for s in DOWNLOAD_SPECS
]
