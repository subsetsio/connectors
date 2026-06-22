"""Bulgarian National Bank (BNB) connector — exchange rates + SDMX statistics.

Two fetch surfaces, one node module:

* **exchange-rates** — the StERForeignCurrencies endpoint serves a ``<ROWSET>``
  XML of daily lev rates. The period search is capped at a 3-month window per
  request but accepts all currencies at once, so a full re-pull is ~one request
  per calendar quarter. History starts 2000-01-01: the BNB series goes back to
  1991 but the lev was redenominated 1000:1 on 1999-07-05, so pre-2000 values
  are in old lev and would put a 1000x discontinuity in ``rate_bgn``. We publish
  the continuous modern series only.

* **SDMX statistics** — five category pages (long-term interest rate, foreign
  trade exports/imports, foreign direct investment in Bulgaria, direct
  investment abroad) each expose ``download=true&TRANSFORMATION=SDMX_VERTICAL``
  links returning SpreadsheetML (Excel-XML) bundles laid out as
  ``Series Name | Series Key | <period> …`` — a wide series x period table that
  we unpivot to long form (keyfamily, freq, series_key, series_name, period,
  value). Driven by one parametric fetch function over the page table below.

Stateless full re-pull each run — the source returns full history every time.
"""

import html as _html
import re
import time
import xml.etree.ElementTree as ET
from datetime import date
from urllib.parse import quote

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, PREFIX, get_bytes, xml_root


# ---------------------------------------------------------------------------
# Exchange rates
# ---------------------------------------------------------------------------

FX_PAGE = "StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm"
# every currency/metal the BNB has ever quoted (from the period-search form)
FX_CURRENCIES = (
    "ATS,AUD,BEF,BRL,CAD,CHF,CNY,CYP,CZK,DEM,DKK,EEK,ESP,EUR,FIM,FRF,GBP,GRD,"
    "HKD,HRK,HUF,IDR,IEP,ILS,INR,IRP,ISK,ITL,JPY,KRW,KWD,LTL,LVL,MTL,MXN,MYR,"
    "NLG,NOK,NZD,PHP,PLN,PTE,ROL,RON,RUB,SEK,SGD,SIT,SKK,THB,TRL,TRY,USD,XAG,"
    "XAU,XEU,XPT,YUG,ZAR"
)
FX_START_YEAR = 2000  # post-redenomination; see module docstring


_FX_SCHEMA = pa.schema([
    ("date", pa.string()),            # ISO yyyy-mm-dd
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("ratio", pa.float64()),
    ("rate_bgn", pa.float64()),       # levs per `ratio` units of currency
    ("reverse_rate", pa.float64()),   # currency per 1 BGN
    ("gold", pa.int64()),
])


def _quarters(start_year: int):
    today = date.today()
    for year in range(start_year, today.year + 1):
        for q in range(4):
            m1 = q * 3 + 1
            m2 = m1 + 2
            if date(year, m1, 1) > today:
                return
            d2 = 31 if m2 in (1, 3, 5, 7, 8, 10, 12) else (30 if m2 != 2 else 29)
            yield (year, m1, 1, year, m2, d2)


def _text(elem, tag):
    c = elem.find(tag)
    return c.text if c is not None and c.text is not None else None


def _to_float(v):
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def _fetch_fx_window(y1, m1, d1, y2, m2, d2):
    url = (
        f"{BASE}/{FX_PAGE}?download=csv&search=true&downloadOper=true"
        f"&group1=second&periodStartDays={d1:02d}&periodStartMonths={m1:02d}"
        f"&periodStartYear={y1}&periodEndDays={d2:02d}&periodEndMonths={m2:02d}"
        f"&periodEndYear={y2}&valutes={quote(FX_CURRENCIES)}"
        f"&showChart=false&lang=EN"
    )
    content = get_bytes(url)
    try:
        root = xml_root(content)
    except ET.ParseError:
        return []  # empty windows return a non-XML stub
    rows = []
    for row in root.iter("ROW"):
        d = _text(row, "CURR_DATE")
        code = _text(row, "CODE")
        if not d or not code or d == "Date" or code == "Code":
            continue  # header row inside the ROWSET
        parts = d.split(".")
        if len(parts) != 3:
            continue
        iso = f"{parts[2]}-{parts[1]}-{parts[0]}"
        rows.append({
            "date": iso,
            "currency_code": code.strip(),
            "currency_name": (_text(row, "NAME_") or "").strip(),
            "ratio": _to_float(_text(row, "RATIO")),
            "rate_bgn": _to_float(_text(row, "RATE")),
            "reverse_rate": _to_float(_text(row, "REVERSERATE")),
            "gold": int(_to_float(_text(row, "GOLD")) or 0),
        })
    return rows


def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id
    rows = []
    for window in _quarters(FX_START_YEAR):
        rows.extend(_fetch_fx_window(*window))
        time.sleep(0.2)
    if not rows:
        raise AssertionError(f"{asset}: fetched 0 exchange-rate observations")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_FX_SCHEMA), asset)


_FX_ID = f"{PREFIX}exchange-rates"

_FX_SQL = f'''
    SELECT
        CAST(date AS DATE)                       AS date,
        currency_code,
        currency_name,
        ratio,
        rate_bgn,
        reverse_rate,
        rate_bgn / NULLIF(ratio, 0)              AS rate_bgn_per_unit,
        currency_code IN ('XAU', 'XAG', 'XPT', 'XPD') AS is_metal
    FROM (
        SELECT *, row_number() OVER (
            PARTITION BY date, currency_code ORDER BY rate_bgn
        ) AS rn
        FROM "{_FX_ID}"
    )
    WHERE rn = 1 AND rate_bgn IS NOT NULL
'''


# ---------------------------------------------------------------------------
# SDMX statistical-database dataflows
# ---------------------------------------------------------------------------

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


def _harvest_bundles(page_html: str):
    """Return list of (download_url, keyfamily, freq, page_id) for a category
    page — only links carrying an explicit series= list (others are empty
    shells that need the portal's JS form)."""
    out = []
    for raw in _DL_HREF.findall(page_html):
        href = _html.unescape(raw)
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

    page_html = get_bytes(page_url + "?lang=EN").decode("utf-8", "replace")
    bundles = _harvest_bundles(page_html)
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


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=_FX_ID, fn=fetch_exchange_rates, kind="download"),
] + [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_sdmx, kind="download")
    for eid in SDMX_PAGES
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{_FX_ID}-transform", deps=[_FX_ID], sql=_FX_SQL),
] + [
    SqlNodeSpec(
        id=f"{PREFIX}{eid}-transform",
        deps=[f"{PREFIX}{eid}"],
        sql=_sdmx_sql(f"{PREFIX}{eid}"),
    )
    for eid in SDMX_PAGES
]
