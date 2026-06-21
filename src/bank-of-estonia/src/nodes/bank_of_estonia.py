"""Bank of Estonia (Eesti Pank) statistical database connector.

Mechanism `ep_statistics`: the official statistical database at
statistika.eestipank.ee exposes ~390 reports ('andmestik'); ~290 are public
and carry data (collect filtered on the onAvalik/onAndmetega flags). Each public
report is downloaded as a semicolon-delimited CSV time-series matrix from a single
stable URL — `Reports?id=<andmestikId>&format=csv&lng=en` — and reshaped from the
wide (periods-as-columns) cross-tab into long (date, series, value) rows.

Fetch shape: stateless full re-pull. Each report's CSV is small and the whole
public corpus re-fetches in minutes, so there is no watermark/cursor. The plain
CSV download returns the source's default display window (the most recent ~12
periods per getDefaultAjad); full deep history would require the coupled
getVeerud(fullDataMode)+getRead protocol, which is intentionally not used here to
keep one robust request per report against a Cloudflare-fronted, 429-prone host.
"""
import re
import xml.etree.ElementTree as ET
from datetime import date

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://statistika.eestipank.ee"
PREFIX = "bank-of-estonia-"

SCHEMA = pa.schema([
    ("period", pa.string()),   # original column header label, e.g. "06/2025"
    ("date", pa.string()),     # normalized ISO date (first day of period), or null
    ("series", pa.string()),   # hierarchical row path + column dimension path
    ("value", pa.float64()),
])


@transient_retry(attempts=8)
def _fetch_default_ajad(report_id: str) -> str:
    resp = get(
        f"{BASE}/spring/getDefaultAjad",
        params={"andmestikId": report_id},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    return resp.text


def _date_range(xml_text: str):
    """Full available date range for a report, as (date1, date2) in the
    YYYY-M-D format the Reports servlet expects. The plain (no-date) CSV only
    returns the servlet's recent default window — which is empty for reports
    whose data lives in older periods (periodic surveys, discontinued series) —
    so we always span the report's full advertised year range."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None, None

    def _yr(s):
        s = (s or "").strip()
        return int(s) if s.isdigit() else None

    ymin = _yr(root.findtext("aastaValikVaikseim"))
    ymax = _yr(root.findtext("aastaValikSuurim"))
    if not (ymin and ymax):  # fall back to the default-window endpoints (dd.mm.yyyy)
        def _yr_dot(tag):
            parts = (root.findtext(tag) or "").strip().split(".")
            return int(parts[-1]) if len(parts) == 3 and parts[-1].isdigit() else None
        ymin = ymin or _yr_dot("AegAlgus")
        ymax = ymax or _yr_dot("AegLopp")
    if ymin and ymax and ymin <= ymax:
        return f"{ymin}-1-1", f"{ymax}-12-31"
    return None, None


@transient_retry(attempts=8)
def _fetch_csv(report_id: str, date1=None, date2=None) -> str:
    params = {"id": report_id, "format": "csv", "lng": "en"}
    if date1 and date2:
        params["date1"] = date1
        params["date2"] = date2
    resp = get(f"{BASE}/Reports", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


_NULLS = {"", "-", "..", ":", "x", "n/a", "..."}


def _num(s):
    s = (s or "").strip()
    if s.lower() in _NULLS:
        return None
    s = s.replace("%", "").strip()
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    s = s.replace("\xa0", "").replace(" ", "").replace(",", "")  # en-format thousands sep
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def _parse_date(label):
    s = (label or "").strip()
    if not s:
        return None
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)            # dd/mm/yyyy
    if m:
        d, mo, y = map(int, m.groups())
        try:
            return date(y, mo, d).isoformat()
        except ValueError:
            return None
    m = re.match(r"^(\d{1,2})/(\d{4})$", s)                      # mm/yyyy
    if m:
        mo, y = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return date(y, mo, 1).isoformat()
    m = re.match(r"^(\d{4})$", s)                                # yyyy
    if m:
        return date(int(m.group(1)), 1, 1).isoformat()
    mq = re.search(r"Q([1-4]).*?(\d{4})|(\d{4}).*?Q([1-4])", s)  # quarter
    if mq:
        q = mq.group(1) or mq.group(4)
        y = mq.group(2) or mq.group(3)
        return date(int(y), (int(q) - 1) * 3 + 1, 1).isoformat()
    return None


def _parse_report_csv(text: str) -> list[dict]:
    """Reshape a wide EP report matrix (CSV) into long (period, date, series, value)
    records. Handles single-row date headers and multi-row column cross-tabs, plus
    indentation-based row hierarchy."""
    rows = [ln.split(";") for ln in text.splitlines()]
    # The leading metadata block (title — sometimes wrapped over two lines, the
    # 2nd being a bare ";" — plus "Bank of Estonia" and "Last updated") all have
    # a non-empty FIRST cell, except a wrap line which has NO non-empty cell at
    # all. The table's header block begins at the first row whose first cell is
    # empty but which carries content further right (the period/label header).
    start = None
    for i, r in enumerate(rows):
        if (r[0].strip() if r else "") == "" and any((c or "").strip() for c in r[1:]):
            start = i
            break
    if start is None:
        return []
    # Header rows are the consecutive rows from there whose first column is blank.
    h = start
    while h < len(rows) and (rows[h][0].strip() if rows[h] else "") == "":
        h += 1
    headers, data = rows[start:h], rows[h:]
    ncol = max((len(r) for r in headers + data), default=0)
    if ncol < 2:
        return []

    def ffill(r):
        out, last = [], ""
        for j in range(ncol):
            v = r[j].strip() if j < len(r) else ""
            if v:
                last = v
            out.append(last)
        return out

    H = [ffill(r) for r in headers]
    dates = H[0]
    dimrows = H[1:]

    # Orientation detection. Default (TIMELINEHORZ) has periods in the top header
    # row and series labels down column 0. Some reports (TIMELINEVERT, e.g. the
    # effective exchange-rate indices) are transposed: periods run down column 0
    # and series names are the column headers. Detect by where the dates live.
    def _date_frac(labels):
        cand = [x for x in labels if (x or "").strip()]
        if not cand:
            return 0.0
        return sum(1 for x in cand if _parse_date(x)) / len(cand)

    hdr_frac = _date_frac(dates[1:])
    row_frac = _date_frac([(r[0].strip() if r else "") for r in data])

    recs = []
    if row_frac >= 0.5 and row_frac > hdr_frac:
        # Transposed: column j is one series (joined from all header rows), each
        # data row is one period (its first cell is the date).
        col_series = []
        for j in range(ncol):
            parts = []
            for hr in H:
                v = hr[j]
                if v and (not parts or parts[-1] != v):
                    parts.append(v)
            col_series.append(" | ".join(parts))
        for r in data:
            if all((c or "").strip() == "" for c in r):
                continue
            period = r[0].strip() if r else ""
            dt = _parse_date(period)
            for j in range(1, ncol):
                val = _num(r[j] if j < len(r) else "")
                if val is None:
                    continue
                recs.append({"period": period, "date": dt, "series": col_series[j], "value": val})
        return recs

    # Row-key columns. Many reports carry the row key across SEVERAL leading
    # columns (e.g. "Housing loans;EUR;Real estate;<values…>" — loan type /
    # currency / collateral), not just column 0. The data cells then start after
    # that block. Those columns are exactly the ones left blank in the period
    # header row, so count its leading blanks to find how many key columns there
    # are. Using only column 0 (the previous behaviour) silently collapsed every
    # distinct (currency, collateral, maturity, …) breakdown into one series,
    # producing many rows sharing one (period, series) key with different values.
    nlabel = 0
    period_row = headers[0] if headers else []
    for j in range(ncol):
        if (period_row[j].strip() if j < len(period_row) else "") == "":
            nlabel += 1
        else:
            break
    nlabel = max(nlabel, 1)

    # Column 0 keeps its indentation-hierarchy treatment; the extra key columns
    # (1 … nlabel-1) are forward-filled with reset (a flat multi-column key in the
    # common case, a merged-cell hierarchy in the sectioned ones).
    stack = []
    carry = [""] * nlabel
    for r in data:
        c0 = r[0] if r else ""
        if all((c or "").strip() == "" for c in r):
            continue
        indent = len(c0) - len(c0.lstrip())
        label = c0.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = [s[1] for s in stack] + [label]
        col0_series = " > ".join(p for p in path if p)
        stack.append((indent, label))
        for c in range(1, nlabel):
            v = (r[c].strip() if c < len(r) else "")
            if v:
                carry[c] = v
                for cc in range(c + 1, nlabel):
                    carry[cc] = ""
        key_parts = [col0_series] + [carry[c] for c in range(1, nlabel)]
        row_series = " > ".join(p for p in key_parts if p)
        for j in range(nlabel, ncol):
            val = _num(r[j] if j < len(r) else "")
            if val is None:
                continue
            dims = []
            for dr in dimrows:
                dv = dr[j]
                if dv and (not dims or dims[-1] != dv):
                    dims.append(dv)
            series = row_series + (" | " + " | ".join(dims) if dims else "")
            recs.append({
                "period": dates[j],
                "date": _parse_date(dates[j]),
                "series": series,
                "value": val,
            })
    return recs


def fetch_one(node_id: str) -> None:
    asset = node_id                       # the spec id IS the asset name
    report_id = node_id[len(PREFIX):] if node_id.startswith(PREFIX) else node_id
    date1, date2 = _date_range(_fetch_default_ajad(report_id))
    text = _fetch_csv(report_id, date1, date2)
    recs = _parse_report_csv(text)
    table = pa.Table.from_pylist(recs, schema=SCHEMA)
    save_raw_parquet(table, asset)


# Entity union — the rank-accepted report ids (numeric andmestikId).
from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE) AS date,
                series,
                CAST(value AS DOUBLE) AS value,
                period
            FROM "{s.id}"
            WHERE date IS NOT NULL AND value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
