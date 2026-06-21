"""ifo Institute — standard monthly business-cycle time series.

Standard time series (Business Climate Germany, Export Expectations,
Employment Barometer, Eastern Germany, Saxony, Export/Import Climate): one or
more sheets, each with a few title/note rows, optional merged column-group
header rows (region / measure), a date-header row whose column-A label contains
"Month"/"Monat", then monthly rows of float values. We forward-fill the merged
group rows, compose a descriptive ``series`` label per data column, and melt to
``(date, series, value)``.

The monthly files carry a ``-YYYYMM`` stamp in their filename, so we probe
recent months newest-first and take the first that exists.
"""

import datetime as dt
import io
import re
import time

import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, save_raw_parquet
from utils import (
    FILES,
    HTTP_HEADERS,
    THROTTLE_S,
    get_xlsx,
    parse_month,
    sheet_rows,
    to_float,
)

_MONTHS_BACK = 8  # how many recent months to probe for a monthly file

# Monthly products: node entity id -> a filename pattern under
# /sites/default/files/secure/timeseries/, with {ym} = YYYYMM. We probe recent
# months newest-first and take the first that exists (HTTP 200 + xlsx body).
_PATTERNS = {
    "ifo-business-climate-germany": "secure/timeseries/gsk-e-{ym}.xlsx",
    "ifo-export-expectations": "secure/timeseries/export-e-{ym}.xlsx",
    "ifo-employment-barometer": "secure/timeseries/empl-e-{ym}.xlsx",
    "ifo-business-climate-eastern-germany": "secure/timeseries/ostd-e-{ym}.xlsx",
    "ifo-business-climate-saxony": "secure/timeseries/ku-sachsen-{ym}-LR-en.xlsx",
    "ifo-export-climate": "secure/timeseries/exklima-e-{ym}.xlsx",
    "ifo-import-climate": "secure/timeseries/imklima-e-{ym}.xlsx",
}


def _recent_months(n: int) -> list[str]:
    """YYYYMM strings for the current month and the previous n-1 months."""
    today = dt.date.today()
    y, mo = today.year, today.month
    out = []
    for _ in range(n):
        out.append(f"{y}{mo:02d}")
        mo -= 1
        if mo == 0:
            mo = 12
            y -= 1
    return out


def _fetch_monthly(entity: str) -> bytes:
    """Probe recent months newest-first; return the first published xlsx."""
    pattern = _PATTERNS[entity]
    tried = []
    for ym in _recent_months(_MONTHS_BACK):
        url = FILES + pattern.format(ym=ym)
        tried.append(ym)
        status, content = get_xlsx(url)
        if status == 200:
            return content
        time.sleep(THROTTLE_S)
    raise RuntimeError(
        f"{entity}: no monthly file found for any of {tried} (pattern {pattern})"
    )


def _ffill(row: list, ncols: int) -> list:
    """Forward-fill a (merged-cell) header row to the right across ``ncols``."""
    out = [None] * ncols
    last = None
    for c in range(ncols):
        v = row[c] if c < len(row) else None
        if v is not None and str(v).strip():
            last = str(v).strip()
        out[c] = last
    return out


def _parse_standard(content: bytes) -> list[tuple]:
    """Parse a standard ifo time-series workbook → list of (date, series, value)."""
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    out: list[tuple] = []
    try:
        for sn in wb.sheetnames:
            rows = sheet_rows(wb[sn])
            if not rows:
                continue

            # The date-header row: column-A label mentions Month/Monat.
            hidx = None
            for i, r in enumerate(rows):
                c0 = str(r[0]).strip().lower() if r and r[0] is not None else ""
                if "month" in c0 or "monat" in c0:
                    hidx = i
                    break
            if hidx is None:
                continue
            header = rows[hidx]
            ncols = max((len(r) for r in rows), default=len(header))

            # Merged column-group rows form the CONTIGUOUS block directly above
            # the date-header (col A empty, data to the right). Stop at the first
            # row that breaks the run so stray notes / wrapped source citations
            # higher up the sheet are not mistaken for column groups.
            groupings = []
            for i in range(hidx - 1, -1, -1):
                r = rows[i]
                c0_empty = r[0] is None or not str(r[0]).strip()
                has_other = any(c is not None and str(c).strip() for c in r[1:])
                if c0_empty and has_other:
                    groupings.insert(0, _ffill(r, ncols))
                else:
                    break

            # Legend lines like "R1: ifo Export Climate ...".
            legend = {}
            first_title = None
            for r in rows[:hidx]:
                if not (r and r[0] is not None and str(r[0]).strip()):
                    continue
                txt = str(r[0]).strip()
                if first_title is None:
                    first_title = txt
                m = re.match(r"^(R\d+)\s*[:\-]\s*(.+)$", txt)
                if m:
                    legend[m.group(1)] = m.group(2).strip()

            # Compose a descriptive label per data column.
            labels = {}
            for c in range(1, ncols):
                parts = []
                for g in groupings:
                    v = g[c] if c < len(g) else None
                    if v:
                        parts.append(str(v).strip())
                leaf = header[c] if c < len(header) else None
                leaf = str(leaf).strip() if leaf is not None else ""
                leaf = legend.get(leaf, leaf)
                if leaf:
                    parts.append(leaf)
                seen = []
                for p in parts:
                    if p and p not in seen:
                        seen.append(p)
                labels[c] = " | ".join(seen) if seen else (first_title or sn)

            for r in rows[hidx + 1 :]:
                d = parse_month(r[0] if r else None)
                if d is None:
                    continue
                for c in range(1, ncols):
                    val = to_float(r[c] if c < len(r) else None)
                    if val is None:
                        continue
                    out.append((d, labels[c], val))
    finally:
        wb.close()
    return out


_STD_SCHEMA = pa.schema(
    [("date", pa.date32()), ("series", pa.string()), ("value", pa.float64())]
)


def fetch_timeseries(node_id: str) -> None:
    """Fetch + parse one standard monthly time-series product."""
    asset = node_id
    entity = node_id[len("ifo-institute-") :]

    configure_http(headers=HTTP_HEADERS)
    content = _fetch_monthly(entity)

    records = _parse_standard(content)
    if not records:
        raise RuntimeError(f"{asset}: parsed 0 rows from monthly file")

    table = pa.table(
        {
            "date": [r[0] for r in records],
            "series": [r[1] for r in records],
            "value": [r[2] for r in records],
        },
        schema=_STD_SCHEMA,
    )
    save_raw_parquet(table, asset)


def _std_sql(dep: str) -> str:
    return f'''
        SELECT
            CAST(date AS DATE)    AS date,
            series,
            CAST(value AS DOUBLE) AS value
        FROM "{dep}"
        WHERE value IS NOT NULL
        ORDER BY series, date
    '''


DOWNLOAD_SPECS = [
    NodeSpec(id=f"ifo-institute-{eid}", fn=fetch_timeseries, kind="download")
    for eid in _PATTERNS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"ifo-institute-{eid}-transform", deps=[f"ifo-institute-{eid}"], sql=_std_sql(f"ifo-institute-{eid}"))
    for eid in _PATTERNS
]
