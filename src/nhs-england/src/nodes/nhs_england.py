"""NHS England statistics connector.

NHS England has no machine-readable catalog/data API (the former CKAN at
data.england.nhs.uk is now a JS dashboard). The canonical statistical output is
bulk Excel/CSV workbooks published under ~60 "statistical work areas". This
connector covers the five flagship national waiting-times / activity / capacity
series, each delivered as a single national "time series" workbook (or, for bed
availability, three KH03 CSVs).

Fetch strategy (per research handoff): scrape the relevant static landing page
to discover the CURRENT file URL (the URLs are point-in-time — upload-date path
+ random suffix — so they are NEVER hardcoded), download the file, and parse it
into a tidy long table in Python. The published shape is uniform across all five
subsets:

    period (DATE) | sheet (TEXT) | series (TEXT) | value (DOUBLE)

The Excel workbooks are bespoke multi-sheet layouts with banner rows and merged
headers, in two orientations:
  * vertical   — periods run DOWN a column, metrics across columns (A&E, Cancer,
                 RTT). One row per (period, metric); the metric label is built
                 from the 1-3 header rows above the first data row.
  * horizontal — periods run ACROSS a row, one data row per breakdown category
                 (Diagnostics: one row per diagnostic test type). One row per
                 (category, period).
Bed availability is clean CSV (KH03 returns), parsed directly.

Full re-pull every run (stateless): each time-series workbook already carries
the entire history and there is no incremental query parameter, so we re-fetch
and overwrite. Freshness gating is the maintain step's job, not ours.
"""

import datetime as _dt
import io
import math
import re
import html as _html

import pandas as pd
import pyarrow as pa
import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

SLUG = "nhs-england"
BASE = "https://www.england.nhs.uk/statistics/statistical-work-areas/"

# Uniform published schema for every subset.
SCHEMA = pa.schema([
    ("period", pa.date32()),
    ("sheet", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])

# --- per-entity fetch configuration (constant; no I/O at module load) --------
#
# kind: "workbook" (Excel, parsed with `orient`) or "bed_csv".
# page / match: where to scrape and which link text identifies the file.
# parent / year_re: when set, first resolve the latest /…-YYYY-YY/ sub-page
#   under `parent`, then scrape THAT page for the file.
SOURCES = {
    "ae-waiting-times-and-activity": {
        "kind": "workbook",
        "orient": "vertical",
        "page": BASE + "ae-waiting-times-and-activity/",
        "match": ["monthly", "a&e", "time series"],
        "skip_sheets": ["notes", "charts", "booking"],
    },
    "cancer-waiting-times": {
        "kind": "workbook",
        "orient": "vertical",
        "page": BASE + "cancer-waiting-times/",
        "match": ["national time series", "with revisions"],
        "skip_sheets": ["cover", "quarterly", "annual"],
    },
    "rtt-waiting-times": {
        "kind": "workbook",
        "orient": "vertical",
        "parent": BASE + "rtt-waiting-times/",
        "year_re": (
            r"https://www\.england\.nhs\.uk/statistics/statistical-work-areas/"
            r"rtt-waiting-times/rtt-data-(\d{4})-\d{2}/"
        ),
        "match": ["rtt overview timeseries"],
        "skip_sheets": [],
    },
    "diagnostics-waiting-times-and-activity": {
        "kind": "workbook",
        "orient": "horizontal",
        "parent": BASE + (
            "diagnostics-waiting-times-and-activity/"
            "monthly-diagnostics-waiting-times-and-activity/"
        ),
        "year_re": (
            r"https://www\.england\.nhs\.uk/statistics/statistical-work-areas/"
            r"diagnostics-waiting-times-and-activity/"
            r"monthly-diagnostics-waiting-times-and-activity/"
            r"monthly-diagnostics-data-(\d{4})-\d{2}/"
        ),
        "match": ["time series"],
        "skip_sheets": ["guidance", "definitions"],
    },
    "bed-availability-and-occupancy": {
        "kind": "bed_csv",
        "page": BASE + "bed-availability-and-occupancy/bed-data-overnight/",
        # filename-substring -> measure label (becomes `sheet`)
        "csvs": {
            "available-overnight-only.csv": "Available Overnight",
            "occupied-overnight-only.csv": "Occupied Overnight",
        },
    },
}

ENTITY_IDS = list(SOURCES)


# --- HTTP with retry ---------------------------------------------------------

_TRANSIENT = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch(url: str) -> httpx.Response:
    resp = get(url, timeout=(15.0, 240.0))
    resp.raise_for_status()
    return resp


# --- discovery ---------------------------------------------------------------

def _latest_year_subpage(parent_url: str, year_re: str) -> str:
    """Return the /…-YYYY-YY/ sub-page with the greatest start year."""
    text = _fetch(parent_url).text
    best, best_year = None, -1
    for m in re.finditer(year_re, text):
        year = int(m.group(1))
        if year > best_year:
            best_year, best = year, m.group(0)
    if best is None:
        raise RuntimeError(f"no year sub-page found under {parent_url}")
    return best


def _resolve_file(page_url: str, match: list[str]) -> str:
    """First .xls/.xlsx whose link text contains every substring in `match`."""
    text = _fetch(page_url).text
    needles = [s.lower() for s in match]
    for m in re.finditer(
        r'<a[^>]+href="([^"]+\.xlsx?)"[^>]*>(.*?)</a>', text, re.I | re.S
    ):
        label = _html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip().lower()
        if all(n in label for n in needles):
            return m.group(1)
    raise RuntimeError(f"no file matching {match} on {page_url}")


# --- value helpers -----------------------------------------------------------

def _is_date(v) -> bool:
    return isinstance(v, (_dt.datetime, _dt.date)) and not isinstance(v, bool)


def _is_num(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return True
    if isinstance(v, float):
        return not math.isnan(v)
    return False


def _to_date(v) -> _dt.date:
    return v.date() if isinstance(v, _dt.datetime) else v


def _clean(label: str) -> str:
    return re.sub(r"\s+", " ", label).strip()


# --- tidy extractors ---------------------------------------------------------

def _tidy_vertical(raw: pd.DataFrame) -> list[tuple]:
    """Periods down a column; metrics across columns. -> (period, series, value)."""
    nrows, ncols = raw.shape
    date_cols = [
        c for c in range(ncols)
        if sum(_is_date(raw.iat[r, c]) for r in range(nrows)) >= 6
    ]
    if not date_cols:
        return []
    first_data = min(
        r for r in range(nrows) for c in date_cols if _is_date(raw.iat[r, c])
    )
    # Column labels come from the (up to) 3 header rows directly above the data,
    # ffilled left-to-right to span merged-cell headers.
    labels: dict[int, str] = {}
    if first_data > 0:
        hdr = raw.iloc[max(0, first_data - 3):first_data].ffill(axis=1)
        for c in range(ncols):
            parts = []
            for i in range(hdr.shape[0]):
                v = hdr.iat[i, c]
                s = "" if v is None else _clean(str(v))
                if s and s.lower() != "nan":
                    parts.append(s)
            labels[c] = " - ".join(dict.fromkeys(parts))
    out = []
    for r in range(first_data, nrows):
        for c in range(ncols):
            if c in date_cols or not _is_num(raw.iat[r, c]):
                continue
            owners = [d for d in date_cols if d < c]
            if not owners:
                continue
            period = raw.iat[r, max(owners)]
            if not _is_date(period):
                continue
            series = labels.get(c) or f"col{c}"
            out.append((_to_date(period), series, float(raw.iat[r, c])))
    return out


def _tidy_horizontal(raw: pd.DataFrame) -> list[tuple]:
    """Periods across a row; one data row per category. -> (period, series, value)."""
    nrows, ncols = raw.shape
    date_rows = [
        r for r in range(nrows)
        if sum(_is_date(raw.iat[r, c]) for c in range(ncols)) >= 6
    ]
    if not date_rows:
        return []
    drow = date_rows[0]
    first_col = min(c for c in range(ncols) if _is_date(raw.iat[drow, c]))
    out = []
    for r in range(drow + 1, nrows):
        parts = []
        for c in range(first_col):
            v = raw.iat[r, c]
            s = "" if v is None else _clean(str(v))
            if s and s.lower() != "nan":
                parts.append(s)
        series = " - ".join(parts)
        if not series:
            continue
        for c in range(first_col, ncols):
            period = raw.iat[drow, c]
            if not _is_date(period) or not _is_num(raw.iat[r, c]):
                continue
            out.append((_to_date(period), series, float(raw.iat[r, c])))
    return out


# --- per-kind fetchers -------------------------------------------------------

def _fetch_workbook(asset: str, cfg: dict) -> None:
    if cfg.get("parent"):
        page = _latest_year_subpage(cfg["parent"], cfg["year_re"])
    else:
        page = cfg["page"]
    url = _resolve_file(page, cfg["match"])
    engine = "xlrd" if url.lower().endswith(".xls") else "openpyxl"
    book = pd.ExcelFile(io.BytesIO(_fetch(url).content), engine=engine)
    tidy = _tidy_vertical if cfg["orient"] == "vertical" else _tidy_horizontal
    skip = [s.lower() for s in cfg.get("skip_sheets", [])]

    periods, sheets, seriess, values = [], [], [], []
    for sheet_name in book.sheet_names:
        low = sheet_name.lower()
        if any(s in low for s in skip):
            continue
        raw = book.parse(sheet_name, header=None)
        for period, series, value in tidy(raw):
            periods.append(period)
            sheets.append(sheet_name)
            seriess.append(series)
            values.append(value)

    if not periods:
        raise RuntimeError(f"{asset}: parsed 0 rows from {url}")
    table = pa.table(
        {"period": periods, "sheet": sheets, "series": seriess, "value": values},
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


def _parse_bed_dates(s: pd.Series) -> pd.Series:
    """KH03 dates mix DD/MM/YYYY and YYYY-MM-DD within a file."""
    s = s.astype("string")
    iso = pd.to_datetime(
        s.where(s.str.contains("-", na=False)), format="%Y-%m-%d", errors="coerce"
    )
    dmy = pd.to_datetime(
        s.where(s.str.contains("/", na=False)), format="%d/%m/%Y", errors="coerce"
    )
    return iso.fillna(dmy)


def _fetch_bed_csv(asset: str, cfg: dict) -> None:
    text = _fetch(cfg["page"]).text
    hrefs = re.findall(r'href="([^"]+\.csv)"', text, re.I)
    periods, sheets, seriess, values = [], [], [], []
    for needle, measure in cfg["csvs"].items():
        url = next((h for h in hrefs if h.lower().endswith(needle)), None)
        if url is None:
            raise RuntimeError(f"{asset}: KH03 csv '{needle}' not found on page")
        df = pd.read_csv(io.BytesIO(_fetch(url).content))
        df["_date"] = _parse_bed_dates(df["Effective_Snapshot_Date"])
        df = df.dropna(subset=["_date", "Number_Of_Beds"])
        for org, sector, beds, date in zip(
            df["Organisation_Code"].astype(str),
            df["Sector"].astype(str),
            pd.to_numeric(df["Number_Of_Beds"], errors="coerce"),
            df["_date"],
        ):
            if beds is None or (isinstance(beds, float) and math.isnan(beds)):
                continue
            periods.append(date.date())
            sheets.append(measure)
            seriess.append(f"{org} - {sector}")
            values.append(float(beds))

    if not periods:
        raise RuntimeError(f"{asset}: parsed 0 rows from KH03 csvs")
    table = pa.table(
        {"period": periods, "sheet": sheets, "series": seriess, "value": values},
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


def fetch_one(node_id: str) -> None:
    """Generic dispatcher. The runtime calls fn(spec.id); recover the entity."""
    asset = node_id
    entity = node_id[len(SLUG) + 1:]  # strip "nhs-england-"
    cfg = SOURCES[entity]
    if cfg["kind"] == "bed_csv":
        _fetch_bed_csv(asset, cfg)
    else:
        _fetch_workbook(asset, cfg)


# --- specs -------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
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
                CAST(period AS DATE) AS date,
                sheet,
                series,
                CAST(value AS DOUBLE) AS value
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY period, sheet, series ORDER BY value DESC
                ) AS _rn
                FROM "{s.id}"
            )
            WHERE _rn = 1
              AND period IS NOT NULL
              AND value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
