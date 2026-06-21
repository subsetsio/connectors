"""BNB SDMX statistical-database dataflows.

Five category pages (long-term interest rate, foreign trade exports/imports,
foreign direct investment in Bulgaria, direct investment abroad) each expose
``download=true&TRANSFORMATION=SDMX_VERTICAL`` links; each link returns a
SpreadsheetML (Excel-XML) bundle laid out as ``Series Name | Series Key |
<period> …`` — a wide series x period table that we unpivot to long form
(series_key, series_name, freq, period, value). Driven by one parametric fetch
function over the page table below.

Stateless full re-pull each run — the source returns full history every time.
"""

import re
import time

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, PREFIX, get_bytes, xml_root

# entity id -> statistics category page that exposes its SDMX download links
SDMX_PAGES = {
    "long-term-interest-rate": "StMonetaryInterestRate/StIRLTIR",
    "foreign-trade-exports": "StExternalSector/StForeignTrade/StFTExports",
    "foreign-trade-imports": "StExternalSector/StForeignTrade/StFTImports",
    "foreign-direct-investment-in-bulgaria": "StExternalSector/StDirectInvestments/StDIBulgaria",
    "direct-investment-abroad": "StExternalSector/StDirectInvestments/StDIAbroad",
}

SS = "urn:schemas-microsoft-com:office:spreadsheet"  # SpreadsheetML namespace

_DL_HREF = re.compile(r'href="(\?[^"]*download=true[^"]*)"')


def _harvest_bundles(html: str):
    """Return list of (download_url, keyfamily, freq, page_id) for a category
    page — only links carrying an explicit series= list (others are empty
    shells that need the portal's JS form)."""
    import html as _h
    out = []
    for raw in _DL_HREF.findall(html):
        href = _h.unescape(raw)
        if "series=" not in href:
            continue
        kf = re.search(r"KEYFAMILY=([A-Za-z0-9_]+)", href)
        freq = re.search(r"FREQ=([A-Z,]+)", href)
        pid = re.search(r"pageId=(\d+)", href)
        if not kf:
            continue
        out.append((
            href.replace("'", "%27"),
            kf.group(1),
            freq.group(1) if freq else None,
            pid.group(1) if pid else None,
        ))
    return out


def _spreadsheet_rows(content: bytes):
    """Yield each Row of a SpreadsheetML doc as a dense list of cell strings,
    honouring sparse ss:Index gaps."""
    root = xml_root(content)
    idx_attr = "{%s}Index" % SS
    for row in root.iter("{%s}Row" % SS):
        cells = []
        col = 0
        for cell in row.findall("{%s}Cell" % SS):
            idx = cell.get(idx_attr)
            if idx:
                col = int(idx) - 1
            data = cell.find("{%s}Data" % SS)
            while len(cells) < col:
                cells.append(None)
            cells.append(data.text if data is not None else None)
            col = len(cells)
        yield cells


_PERIOD_RE = re.compile(r"^\d{4}([-/].+)?$")


def _emit(rows, keyfamily, freq, page_id, series_key, series_name, period, raw):
    if raw is None or str(raw).strip() in ("", ":", "-"):
        return
    try:
        val = float(str(raw).replace(",", "").strip())
    except ValueError:
        return
    rows.append({
        "keyfamily": keyfamily,
        "freq": freq,
        "page_id": page_id,
        "series_key": series_key,
        "series_name": series_name,
        "period": str(period).strip(),
        "value": val,
    })


def _parse_sdmx_bundle(content: bytes, keyfamily, freq, page_id):
    """Unpivot one SpreadsheetML bundle to long rows.

    Two layouts occur. Multi-series bundles have a header row
    ``Series Name | Series Key | <period> | <period> …`` followed by one row
    per series. Single-series bundles list the dimensions as ``key | value``
    metadata rows (including ``Series Key`` and ``Series Name``) and then a
    plain ``<period> | <value>`` table.
    """
    rows = []
    all_rows = [[(c or "").strip() for c in cells] for cells in _spreadsheet_rows(content)]

    wide_idx = next(
        (i for i, h in enumerate(all_rows)
         if len(h) >= 2 and h[0] == "Series Name" and h[1] == "Series Key"),
        None,
    )

    if wide_idx is not None:
        periods = all_rows[wide_idx][2:]
        for cells in all_rows[wide_idx + 1:]:
            if len(cells) < 2 or not cells[1]:
                continue
            series_name, series_key = cells[0], cells[1]
            for i, per in enumerate(periods):
                if not per:
                    continue
                raw = cells[2 + i] if 2 + i < len(cells) else None
                _emit(rows, keyfamily, freq, page_id, series_key, series_name, per, raw)
        return rows

    # single-series layout
    series_key = series_name = None
    for cells in all_rows:
        c0 = cells[0] if len(cells) > 0 else ""
        c1 = cells[1] if len(cells) > 1 else ""
        if c0 == "Series Key":
            series_key = c1
            continue
        if c0 == "Series Name":
            series_name = c1
            continue
        if series_key and _PERIOD_RE.match(c0) and c1:
            _emit(rows, keyfamily, freq, page_id, series_key, series_name, c0, c1)
    return rows


_SDMX_SCHEMA = pa.schema([
    ("keyfamily", pa.string()),
    ("freq", pa.string()),
    ("page_id", pa.string()),
    ("series_key", pa.string()),
    ("series_name", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])


def fetch_sdmx(node_id: str) -> None:
    asset = node_id
    entity = node_id[len(PREFIX):]
    page = SDMX_PAGES[entity]
    page_url = f"{BASE}/{page}/index.htm"

    html = get_bytes(page_url + "?lang=EN").decode("utf-8", "replace")
    bundles = _harvest_bundles(html)
    if not bundles:
        raise AssertionError(f"{asset}: no SDMX download bundles on {page}")

    rows = []
    for href, kf, freq, pid in bundles:
        content = get_bytes(page_url + href + "&lang=EN")
        rows.extend(_parse_sdmx_bundle(content, kf, freq, pid))
        time.sleep(0.2)

    if not rows:
        raise AssertionError(f"{asset}: parsed 0 observations from {len(bundles)} bundles")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_SDMX_SCHEMA), asset)


def _sdmx_sql(dep_id: str) -> str:
    return f'''
        SELECT
            keyfamily,
            freq,
            series_key,
            series_name,
            period,
            value
        FROM (
            SELECT *, row_number() OVER (
                PARTITION BY series_key, freq, period ORDER BY value
            ) AS rn
            FROM "{dep_id}"
        )
        WHERE rn = 1 AND value IS NOT NULL
    '''


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_sdmx, kind="download")
    for eid in SDMX_PAGES
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{PREFIX}{eid}-transform",
        deps=[f"{PREFIX}{eid}"],
        sql=_sdmx_sql(f"{PREFIX}{eid}"),
    )
    for eid in SDMX_PAGES
]
