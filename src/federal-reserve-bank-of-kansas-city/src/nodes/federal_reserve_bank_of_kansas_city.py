"""Federal Reserve Bank of Kansas City connector.

Two fetch surfaces, both researched:

* FRED (St. Louis Fed) keyless ``fredgraph.csv`` for the two indices KC Fed
  mirrors there cleanly — the Financial Stress Index (``KCFSI``) and the Labor
  Market Conditions Indicators (level-of-activity ``FRBKCLMCILA`` and momentum
  ``FRBKCLMCIM``). Stable CSV, no auth, no Excel parsing.

* kansascityfed.org full-history survey spreadsheets for the four Tenth District
  surveys (Manufacturing, Services, Energy, Ag Credit) — KC Fed's distinctive
  content, not carried on FRED. The numeric ``/documents/{id}/`` path mutates
  every release, so we scrape the stable product landing page each run to
  resolve the current ``.xls/.xlsx`` link, then normalise the workbook to a long
  ``(date, series, value)`` table in Python (the SQL transform stays trivial).

All raw assets share one long schema, so every transform is the same thin
parse-and-type pass. Stateless full re-pull: each spreadsheet / CSV already
carries the complete history, so we overwrite every run and pick up revisions
for free. The KC Fed site sits behind an aggressive WAF that rejects non-browser
clients; we send a desktop-browser User-Agent.
"""
from __future__ import annotations

import csv
import datetime as _dt
import io
import re
from urllib.parse import urljoin

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "federal-reserve-bank-of-kansas-city"

# A realistic desktop-browser User-Agent — the KC Fed WAF 403s/times-out plain
# library clients. ASCII-only (httpx/urllib3 reject non-ASCII header values).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "application/vnd.ms-excel,application/octet-stream,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Long raw schema shared by every asset.
SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("series", pa.string()),
        ("value", pa.float64()),
    ]
)

# ---------------------------------------------------------------------------
# FRED-backed indices
# ---------------------------------------------------------------------------

# Map our entity slug -> the FRED series ids that compose it.
_FRED_SERIES = {
    "kcfsi": ["KCFSI"],
    "lmci": ["FRBKCLMCILA", "FRBKCLMCIM"],
}

_FREDGRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv"


@transient_retry()
def _http_get(url: str, **kwargs):
    resp = get(url, timeout=(10.0, 120.0), headers=_BROWSER_HEADERS, **kwargs)
    resp.raise_for_status()
    return resp


def _parse_date(token: str):
    token = (token or "").strip()
    if not token:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return _dt.datetime.strptime(token, fmt).date()
        except ValueError:
            continue
    return None


def _to_float(token):
    if token is None:
        return None
    token = str(token).strip().replace(",", "")
    if token in ("", ".", "NA", "N/A", "n/a", "-", "--"):
        return None
    try:
        return float(token)
    except ValueError:
        return None


def fetch_fred(node_id: str) -> None:
    """Fetch one KC-Fed index from FRED's keyless fredgraph.csv as long rows."""
    configure_http(headers=_BROWSER_HEADERS)
    entity = node_id[len(SLUG) + 1 :]
    series_ids = _FRED_SERIES[entity]
    resp = _http_get(_FREDGRAPH, params={"id": ",".join(series_ids)})
    reader = csv.reader(io.StringIO(resp.text))
    header = next(reader, None)
    if not header or len(header) < 2:
        raise AssertionError(f"{node_id}: unexpected fredgraph header {header!r}")
    cols = header[1:]  # first column is the observation date
    rows = []
    for rec in reader:
        if not rec:
            continue
        d = _parse_date(rec[0])
        if d is None:
            continue
        for i, col in enumerate(cols, start=1):
            val = _to_float(rec[i]) if i < len(rec) else None
            if val is None:
                continue
            rows.append({"date": d, "series": col, "value": val})
    if not rows:
        raise AssertionError(f"{node_id}: fredgraph returned no observations")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------------------
# KC Fed survey spreadsheets
# ---------------------------------------------------------------------------

# Stable per-product landing pages (the document ids behind them mutate; the
# pages do not). We scrape each for its current .xls/.xlsx historical-data link.
_SURVEY_PAGES = {
    "manufacturing-survey": ["https://www.kansascityfed.org/surveys/manufacturing-survey/"],
    "services-survey": ["https://www.kansascityfed.org/surveys/services-survey/"],
    "energy-survey": ["https://www.kansascityfed.org/surveys/energy-survey/"],
    "ag-credit-survey": ["https://www.kansascityfed.org/agriculture/ag-credit-survey/"],
}

_XLS_HREF = re.compile(r'href=["\']([^"\']+\.xlsx?)(?:["\'#?])', re.IGNORECASE)
_ANCHOR = re.compile(r'<a\b[^>]*?href=["\']([^"\']+\.xlsx?)["\'][^>]*>(.*?)</a>',
                     re.IGNORECASE | re.DOTALL)
_PREFER = re.compile(r"histor|data|monthly|quarterly|time.?series", re.IGNORECASE)


def _resolve_data_links(page_url: str) -> list[str]:
    """Return absolute .xls/.xlsx links on a landing page, best candidates first."""
    resp = _http_get(page_url)
    html = resp.text
    preferred, others = [], []
    seen = set()
    for href, text in _ANCHOR.findall(html):
        absu = urljoin(page_url, href)
        if absu in seen:
            continue
        seen.add(absu)
        label = re.sub(r"<[^>]+>", " ", text)
        (preferred if (_PREFER.search(label) or _PREFER.search(href)) else others).append(absu)
    # Fallback: any xls/xlsx href at all (anchors without inner text).
    for href in _XLS_HREF.findall(html):
        absu = urljoin(page_url, href)
        if absu not in seen:
            seen.add(absu)
            others.append(absu)
    return preferred or others


def _melt_workbook(content: bytes, url: str, file_tag: str) -> list[dict]:
    """Normalise an Excel workbook to long (date, series, value) rows.

    Heuristic and source-agnostic: for every sheet, find the column that parses
    as dates best and treat the remaining numeric columns as series. The series
    name carries the file tag, sheet name, and column header so distinct columns
    stay distinguishable downstream.
    """
    import pandas as pd

    engine = "xlrd" if url.lower().split("?")[0].endswith(".xls") else "openpyxl"
    try:
        sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=0, engine=engine)
    except Exception:
        # Some "xls" are really xlsx (or vice versa); retry with the other engine.
        alt = "openpyxl" if engine == "xlrd" else "xlrd"
        sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=0, engine=alt)

    rows: list[dict] = []
    for sheet_name, df in sheets.items():
        if df is None or df.empty:
            continue
        df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
        if df.shape[0] < 6 or df.shape[1] < 2:
            continue
        # Pick the date column: highest fraction of parseable dates.
        best_col, best_parsed, best_frac = None, None, 0.0
        for col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce")
            frac = parsed.notna().mean()
            if frac > best_frac and parsed.notna().sum() >= 6:
                best_col, best_parsed, best_frac = col, parsed, frac
        if best_col is None or best_frac < 0.5:
            continue
        value_cols = [c for c in df.columns if c is not best_col and c != best_col]
        for col in value_cols:
            nums = pd.to_numeric(df[col], errors="coerce")
            if nums.notna().sum() == 0:
                continue
            header = str(col).strip()
            if header.lower().startswith("unnamed"):
                header = f"col{list(df.columns).index(col)}"
            series_name = f"{file_tag} | {str(sheet_name).strip()} | {header}"[:200]
            for d, v in zip(best_parsed, nums):
                if pd.isna(d) or pd.isna(v):
                    continue
                rows.append({"date": d.date(), "series": series_name, "value": float(v)})
    return rows


def _file_tag(url: str) -> str:
    stem = url.split("?")[0].rsplit("/", 1)[-1]
    stem = re.sub(r"\.xlsx?$", "", stem, flags=re.IGNORECASE)
    return stem or "data"


def fetch_survey(node_id: str) -> None:
    """Scrape a KC Fed survey landing page, download its spreadsheet(s), and
    write a long (date, series, value) table."""
    configure_http(headers=_BROWSER_HEADERS)
    entity = node_id[len(SLUG) + 1 :]
    pages = _SURVEY_PAGES[entity]

    links: list[str] = []
    for page in pages:
        links.extend(_resolve_data_links(page))
    if not links:
        raise AssertionError(f"{node_id}: no .xls/.xlsx data link found on {pages}")

    rows: list[dict] = []
    for url in links:
        resp = _http_get(url)
        rows.extend(_melt_workbook(resp.content, url, _file_tag(url)))
    if not rows:
        raise AssertionError(
            f"{node_id}: resolved {len(links)} spreadsheet(s) but parsed 0 rows"
        )
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-kcfsi", fn=fetch_fred, kind="download"),
    NodeSpec(id=f"{SLUG}-lmci", fn=fetch_fred, kind="download"),
    NodeSpec(id=f"{SLUG}-manufacturing-survey", fn=fetch_survey, kind="download"),
    NodeSpec(id=f"{SLUG}-services-survey", fn=fetch_survey, kind="download"),
    NodeSpec(id=f"{SLUG}-energy-survey", fn=fetch_survey, kind="download"),
    NodeSpec(id=f"{SLUG}-ag-credit-survey", fn=fetch_survey, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT date, series, value
            FROM (
                SELECT
                    CAST(date AS DATE)     AS date,
                    CAST(series AS VARCHAR) AS series,
                    CAST(value AS DOUBLE)  AS value
                FROM "{s.id}"
                WHERE date IS NOT NULL
                  AND series IS NOT NULL
                  AND value IS NOT NULL
            )
            QUALIFY row_number() OVER (PARTITION BY date, series ORDER BY value) = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
