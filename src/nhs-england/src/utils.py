"""NHS England statistics: workbook discovery + generic tidy extraction.

NHS England publishes each statistical work area as bespoke, human-formatted
Excel workbooks (banner blocks, multi-sheet, serial dates, merged headers)
reachable only by scraping the work-area landing page — the file URLs are
point-in-time (upload-date path + random suffix), so they are re-discovered
every refresh and NEVER hardcoded. There is no machine-readable catalog.
Research's chosen strategy is scrape_index -> bulk_files.

The workbooks are heterogeneous, but the vast majority are period-indexed time
series in one of two orientations, so we extract a UNIFORM tidy table across
every area:

    source_file (TEXT) | sheet (TEXT) | series (TEXT) | period (DATE) | value (DOUBLE)

  * vertical   — periods run DOWN a column, metrics across columns. One output
                 row per (period, metric); the series label is built from the
                 (up to 3) header rows above the first data row.
  * horizontal — periods run ACROSS a row, one data row per breakdown category.
                 One output row per (category, period).

Auto-detected per sheet (vertical first, then horizontal). Sheets with no
date-indexed table (pure banners, notes, category-only survey tables) yield no
rows and are skipped. Full re-pull each refresh (stateless): the time-series
workbooks carry the whole history and there is no incremental query parameter.
"""
import datetime as dt
import io
import math
import re
from urllib.parse import urljoin

import pandas as pd
import pyarrow as pa

from subsets_utils import get

WORK_AREA_BASE = "https://www.england.nhs.uk/statistics/statistical-work-areas/"

# Uniform raw schema for every work-area table.
SCHEMA = pa.schema([
    ("source_file", pa.string()),
    ("sheet", pa.string()),
    ("series", pa.string()),
    ("period", pa.date32()),
    ("value", pa.float64()),
])

# Safety ceilings — trip on source growth past expectation rather than
# silently truncate/hammer. Discovery raises; sub-page/file slices are bounded.
MAX_SUBPAGES = 15
MAX_FILES_PER_AREA = 6
MAX_DISCOVERED = 400

_NON_DATA_RE = re.compile(
    r"(technical[-_ ]?note|guidance|methodolog|specification|pre[-_ ]?release|"
    r"glossary|definition|read[-_ ]?me|faq|background|user[-_ ]?guide|"
    r"quality[-_ ]?statement|revisions[-_ ]?policy|annex)",
    re.I,
)
_TIME_SERIES_RE = re.compile(r"time[-_ ]?series", re.I)
_XLS_RE = re.compile(r"\.xlsx?($|\?)", re.I)
_PATH_DATE_RE = re.compile(r"/uploads/sites/\d+/(\d{4})/(\d{2})/")


# --- discovery ---------------------------------------------------------------

def _abs_links(page_url: str, html: str) -> list[str]:
    return [urljoin(page_url, h) for h in re.findall(r'href="([^"]+)"', html)]


def _path_date(url: str) -> tuple:
    m = _PATH_DATE_RE.search(url)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def discover_files(slug: str) -> list[str]:
    """Absolute .xls/.xlsx URLs for a work area. Landing-first: most areas list
    their canonical (full-history) workbook right on the landing page; only when
    the landing page carries no workbook at all do we descend one level into the
    same-section sub-pages (some areas hide their files there). PDFs are ignored."""
    landing = f"{WORK_AREA_BASE}{slug}/"
    resp = get(landing, timeout=(10, 60))
    resp.raise_for_status()
    links = _abs_links(landing, resp.text)
    files = {u for u in links if _XLS_RE.search(u)}

    if not files:
        sub_re = re.compile(rf"/statistical-work-areas/{re.escape(slug)}/[^\"?#]+/?$")
        subpages = sorted({
            u for u in links
            if sub_re.search(u) and u.rstrip("/") != landing.rstrip("/")
        })[:MAX_SUBPAGES]
        for sp in subpages:
            r = get(sp, timeout=(10, 60))
            if r.status_code != 200:
                continue
            files.update(u for u in _abs_links(sp, r.text) if _XLS_RE.search(u))

    files = sorted(files)
    if len(files) > MAX_DISCOVERED:
        raise RuntimeError(
            f"{slug}: discovered {len(files)} workbook links (> {MAX_DISCOVERED}); "
            "source shape changed — review before bulk-fetching"
        )
    return files


_SUMMARY_RE = re.compile(r"(national|overview|summary|england)", re.I)


def select_files(slug: str, files: list[str]) -> list[str]:
    """Prefer the full-history 'time series' workbooks (research: they carry the
    whole series, so a full re-fetch is natural). Within those, prefer the
    national/overview summary workbook(s) over provider/organisation-level
    monthly extracts (which repeat per period and are far larger), then most
    recent. Bounded to keep one refresh sane. Fall back to the most recent data
    files when no time-series workbook exists."""
    ts = [u for u in files if _TIME_SERIES_RE.search(u.rsplit("/", 1)[-1])]
    if ts:
        summary = [u for u in ts if _SUMMARY_RE.search(u.rsplit("/", 1)[-1])]
        pool = summary or ts
        pool.sort(key=_path_date, reverse=True)
        return pool[:MAX_FILES_PER_AREA]
    data = [u for u in files if not _NON_DATA_RE.search(u.rsplit("/", 1)[-1])]
    data.sort(key=_path_date, reverse=True)
    return data[:MAX_FILES_PER_AREA]


# --- value helpers -----------------------------------------------------------

def _is_date(v) -> bool:
    return isinstance(v, (dt.datetime, dt.date)) and not isinstance(v, bool)


def _is_num(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return True
    if isinstance(v, float):
        return not math.isnan(v)
    return False


def _to_date(v) -> dt.date:
    return v.date() if isinstance(v, dt.datetime) else v


def _clean(v) -> str:
    if v is None:
        return ""
    s = re.sub(r"\s+", " ", str(v)).strip()
    return "" if s.lower() == "nan" else s


# --- tidy extractors ---------------------------------------------------------

def _tidy_vertical(raw: pd.DataFrame) -> list[tuple]:
    """Periods down a column; metrics across columns -> (series, period, value)."""
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
    labels: dict[int, str] = {}
    if first_data > 0:
        hdr = raw.iloc[max(0, first_data - 3):first_data].ffill(axis=1)
        for c in range(ncols):
            parts = []
            for i in range(hdr.shape[0]):
                s = _clean(hdr.iat[i, c])
                if s:
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
            out.append((series, _to_date(period), float(raw.iat[r, c])))
    return out


def _tidy_horizontal(raw: pd.DataFrame) -> list[tuple]:
    """Periods across a row; one data row per category -> (series, period, value)."""
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
        parts = [_clean(raw.iat[r, c]) for c in range(first_col)]
        series = " - ".join(p for p in parts if p)
        if not series:
            continue
        for c in range(first_col, ncols):
            period = raw.iat[drow, c]
            if not _is_date(period) or not _is_num(raw.iat[r, c]):
                continue
            out.append((series, _to_date(period), float(raw.iat[r, c])))
    return out


def tidy_sheet(raw: pd.DataFrame, source_file: str, sheet: str) -> list[dict]:
    """Auto-detect orientation and return uniform tidy records for one sheet."""
    rows = _tidy_vertical(raw)
    if not rows:
        rows = _tidy_horizontal(raw)
    return [
        {"source_file": source_file, "sheet": sheet,
         "series": series, "period": period, "value": value}
        for series, period, value in rows
    ]


def iter_sheets(url: str):
    """Yield (source_file, sheet_name, raw_dataframe) for a workbook URL.
    Legacy .xls via xlrd, .xlsx via openpyxl; raw cells (header=None)."""
    resp = get(url, timeout=(10, 300))
    resp.raise_for_status()
    name = url.rsplit("/", 1)[-1].split("?")[0]
    engine = "xlrd" if name.lower().endswith(".xls") else "openpyxl"
    book = pd.ExcelFile(io.BytesIO(resp.content), engine=engine)
    for sheet_name in book.sheet_names:
        raw = book.parse(sheet_name, header=None)
        yield name, sheet_name, raw
