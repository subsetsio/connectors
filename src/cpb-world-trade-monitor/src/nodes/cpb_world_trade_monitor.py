"""CPB World Trade Monitor connector.

The WTM is a single statistical product published monthly by CPB (NL) on behalf
of the European Commission as ONE Excel workbook (.xlsx) with two sheets:

  * ``trade_out`` — Merchandise world trade (volume index 2021=100 and unit-value
    price index), imports/exports by region.
  * ``inpro_out`` — Industrial production volume excluding construction
    (index 2021=100), import- and production-weighted.

Each sheet is WIDE: one row per series (col B = human label, col C = series code
like ``mgz_us_qnmi_sn``, col D = 2021 weight/value), with monthly columns from
``2000m01`` onward. Every release is a FULL historical snapshot, so we fetch only
the single latest workbook each run and overwrite (stateless full re-pull — the
file is ~350 kB).

The download URL is point-in-time (month name embedded) with no stable "latest"
alias and releases lag ~2 months, so we discover the current file by walking
month URLs backwards until one returns 200.

We parse the workbook with the stdlib (zipfile + xml.etree) rather than openpyxl,
which chokes on a stale ``xl/drawings`` reference in these files.

Two published subsets:
  * ``series`` — reference catalog, one row per series (code + decoded metadata).
  * ``values`` — long-format monthly observations (the flagship table).
"""

import datetime
import io
import re
import zipfile
import xml.etree.ElementTree as ET

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# ----------------------------- fetch / discovery -----------------------------

_FILE_TMPL = "https://www.cpb.nl/system/files/cpbmedia/cpb-world-trade-monitor-{month}-{year}.xlsx"
_MONTHS = ["january", "february", "march", "april", "may", "june",
           "july", "august", "september", "october", "november", "december"]


@transient_retry()
def _get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _fetch_latest_workbook() -> bytes:
    """Download the most recent WTM .xlsx by probing month URLs backwards.

    A 404 means that month's release isn't out yet — walk to the previous month.
    Transient errors are retried inside ``_get``; genuine failures propagate.
    """
    today = datetime.date.today()
    y, m = today.year, today.month
    for _ in range(12):
        url = _FILE_TMPL.format(month=_MONTHS[m - 1], year=y)
        try:
            resp = _get(url)
            if resp.content[:2] == b"PK":  # valid zip / xlsx magic
                return resp.content
            raise RuntimeError(f"{url} did not return an xlsx (got {resp.content[:16]!r})")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                m -= 1
                if m == 0:
                    m, y = 12, y - 1
                continue
            raise
    raise RuntimeError("could not locate a recent CPB World Trade Monitor .xlsx")


# ------------------------------- xlsx parsing --------------------------------

_M_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_CODE_RE = re.compile(r"^[a-z]{3}_[a-z0-9]{2}_[a-z]{4}_[a-z]{2}$")
_PERIOD_RE = re.compile(r"^\d{4}m\d{2}$")

# Decode tokens of the <variable>_<region>_<measure>_<weighting> series code.
_REGION = {
    "w1": "World", "i1": "Advanced economies", "e6": "Euro Area",
    "us": "United States", "gb": "United Kingdom", "jp": "Japan",
    "a3": "Advanced Asia excl Japan", "r2": "Other advanced economies",
    "d1": "Emerging economies", "cn": "China",
    "a5": "Emerging Asia excl China", "t1": "Eastern Europe / CIS",
    "l1": "Latin America", "f3": "Africa and Middle East",
}
_VARIABLE = {
    "tgz": "total merchandise trade", "mgz": "merchandise imports",
    "xgz": "merchandise exports", "ipz": "industrial production",
    "hfl": "fuels price (HWWI)",
    "hpr": "primary commodities price excl fuels (HWWI)",
}
_MEASURE = {"qnmi": "volume index (2021=100)", "pdmi": "unit value / price index"}
_WEIGHTING = {
    "sn": "seasonally adjusted",
    "sm": "import-weighted, seasonally adjusted",
    "sp": "production-weighted, seasonally adjusted",
    "nn": "not adjusted",
}


def _shared_strings(zf: zipfile.ZipFile) -> list:
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(t.text or "" for t in si.iter(f"{{{_M_NS}}}t"))
            for si in root.findall(f"{{{_M_NS}}}si")]


def _sheet_rows(zf: zipfile.ZipFile, path: str, shared: list) -> list:
    """Return a list of {column_letter: value} dicts, one per row."""
    root = ET.fromstring(zf.read(path))
    out = []
    for row in root.iterfind(f".//{{{_M_NS}}}sheetData/{{{_M_NS}}}row"):
        cells = {}
        for c in row.findall(f"{{{_M_NS}}}c"):
            col = "".join(ch for ch in c.get("r", "") if ch.isalpha())
            t = c.get("t")
            v = c.find(f"{{{_M_NS}}}v")
            if v is None or v.text is None:
                continue
            if t == "s":
                val = shared[int(v.text)]
            elif t == "str":
                val = v.text
            else:
                try:
                    val = float(v.text)
                except ValueError:
                    val = v.text
            cells[col] = val
        out.append(cells)
    return out


def _sheet_paths(zf: zipfile.ZipFile) -> dict:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {r.get("Id"): r.get("Target") for r in rels}
    paths = {}
    for sh in wb.iterfind(f".//{{{_M_NS}}}sheets/{{{_M_NS}}}sheet"):
        target = rid_to_target[sh.get(f"{{{_R_NS}}}id")]
        target = target.lstrip("/") if target.startswith("/") else "xl/" + target.lstrip("/")
        paths[sh.get("name")] = target
    return paths


def _parse_workbook(data: bytes):
    """Return (series_rows, value_rows).

    series_rows: list of dicts (series_code, label, sheet, variable, region,
                 measure, weighting, weight_2021).
    value_rows:  long-format dicts (series_code, period, value) enriched with the
                 decoded series metadata (variable/region/measure/weighting/label)
                 so the values subset is self-describing and its transform needs
                 no cross-dependency on the series asset.
    """
    zf = zipfile.ZipFile(io.BytesIO(data))
    shared = _shared_strings(zf)
    series_rows, value_rows = [], []

    for sheet_name, path in _sheet_paths(zf).items():
        rows = _sheet_rows(zf, path, shared)
        # The period header is the row carrying the most '<yyyy>m<mm>' tokens.
        period_cols = {}
        for row in rows:
            cand = {c: v for c, v in row.items()
                    if isinstance(v, str) and _PERIOD_RE.match(v)}
            if len(cand) > len(period_cols):
                period_cols = cand
        if not period_cols:
            raise RuntimeError(f"no period header row found on sheet {sheet_name!r}")

        for row in rows:
            code = row.get("C")
            label = row.get("B")
            if not isinstance(code, str) or not _CODE_RE.match(code):
                continue
            var, region, measure, weighting = code.split("_")
            variable = _VARIABLE.get(var, var)
            region_name = _REGION.get(region, region)
            measure_name = _MEASURE.get(measure, measure)
            weighting_name = _WEIGHTING.get(weighting, weighting)
            clean_label = (label or code).strip()
            weight = row.get("D")
            series_rows.append({
                "series_code": code,
                "label": clean_label,
                "sheet": sheet_name,
                "variable": variable,
                "region": region_name,
                "measure": measure_name,
                "weighting": weighting_name,
                "weight_2021": float(weight) if isinstance(weight, (int, float)) else None,
            })
            for col, period in period_cols.items():
                v = row.get(col)
                if isinstance(v, (int, float)):
                    # '2000m01' -> '2000-01-01'
                    yr, mo = period.split("m")
                    value_rows.append({
                        "series_code": code,
                        "period": f"{yr}-{mo}-01",
                        "variable": variable,
                        "region": region_name,
                        "measure": measure_name,
                        "weighting": weighting_name,
                        "label": clean_label,
                        "value": float(v),
                    })
    return series_rows, value_rows


# ------------------------------- download fns --------------------------------

_SERIES_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("label", pa.string()),
    ("sheet", pa.string()),
    ("variable", pa.string()),
    ("region", pa.string()),
    ("measure", pa.string()),
    ("weighting", pa.string()),
    ("weight_2021", pa.float64()),
])

_VALUES_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("period", pa.string()),
    ("variable", pa.string()),
    ("region", pa.string()),
    ("measure", pa.string()),
    ("weighting", pa.string()),
    ("label", pa.string()),
    ("value", pa.float64()),
])


def fetch_series(node_id: str) -> None:
    """Reference catalog: one row per WTM series with decoded metadata."""
    series_rows, _ = _parse_workbook(_fetch_latest_workbook())
    table = pa.Table.from_pylist(series_rows, schema=_SERIES_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_values(node_id: str) -> None:
    """Long-format monthly observations across all WTM series."""
    _, value_rows = _parse_workbook(_fetch_latest_workbook())
    table = pa.Table.from_pylist(value_rows, schema=_VALUES_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="cpb-world-trade-monitor-series", fn=fetch_series, kind="download"),
    NodeSpec(id="cpb-world-trade-monitor-values", fn=fetch_values, kind="download"),
]
