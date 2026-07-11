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
_MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}
_MONTH_RE = re.compile(
    r"\b("
    + "|".join(sorted(_MONTHS, key=len, reverse=True))
    + r")[a-z]*[\s.-]+(\d{2,4})\b",
    re.I,
)
_QUARTER_RE = re.compile(
    r"\bQ([1-4])\s*(?:-|of|for)?\s*(\d{4})(?:/(\d{2,4}))?\b|"
    r"\b(\d{4})/(\d{2,4})\s*Q([1-4])\b",
    re.I,
)
_FY_RE = re.compile(r"\b(\d{4})/(\d{2,4})\b")


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


def _two_digit_year(y: int) -> int:
    return 2000 + y if y < 80 else 1900 + y


def _parse_period(v) -> dt.date | None:
    """Parse NHS period labels such as Apr-26, March 2020 or Q4 2025/26."""
    if _is_date(v):
        return _to_date(v)
    s = _clean(v)
    if not s:
        return None
    s = re.sub(r"\([^)]*\)", "", s).strip()
    m = _MONTH_RE.search(s)
    if m:
        year = int(m.group(2))
        if year < 100:
            year = _two_digit_year(year)
        return dt.date(year, _MONTHS[m.group(1).lower()[:3]], 1)
    m = _QUARTER_RE.search(s)
    if m:
        if m.group(1):
            q = int(m.group(1))
            fy_start = int(m.group(2))
            fy_end = int(m.group(3) or fy_start + 1)
            if fy_end < 100:
                fy_end = (fy_start // 100) * 100 + fy_end
        else:
            fy_start = int(m.group(4))
            fy_end = int(m.group(5))
            if fy_end < 100:
                fy_end = (fy_start // 100) * 100 + fy_end
            q = int(m.group(6))
        year, month = {
            1: (fy_start, 6),
            2: (fy_start, 9),
            3: (fy_start, 12),
            4: (fy_end, 3),
        }[q]
        return dt.date(year, month, 1)
    return None


def _is_period(v) -> bool:
    return _parse_period(v) is not None


def _is_num(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return True
    if isinstance(v, float):
        return not math.isnan(v)
    if isinstance(v, str):
        return _to_float(v) is not None
    return False


def _to_date(v) -> dt.date:
    return v.date() if isinstance(v, dt.datetime) else v


def _to_float(v) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        if isinstance(v, float) and math.isnan(v):
            return None
        return float(v)
    s = _clean(v)
    if not s or s in {"-", "..", "*"}:
        return None
    s = s.replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


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
        if sum(_is_period(raw.iat[r, c]) for r in range(nrows)) >= 6
    ]
    if not date_cols:
        return []
    first_data = min(
        r for r in range(nrows) for c in date_cols if _is_period(raw.iat[r, c])
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
            value = _to_float(raw.iat[r, c])
            if c in date_cols or value is None:
                continue
            owners = [d for d in date_cols if d < c]
            if not owners:
                continue
            period = _parse_period(raw.iat[r, max(owners)])
            if period is None:
                continue
            series = labels.get(c) or f"col{c}"
            out.append((series, period, value))
    return out


def _tidy_horizontal(raw: pd.DataFrame) -> list[tuple]:
    """Periods across a row; one data row per category -> (series, period, value)."""
    nrows, ncols = raw.shape
    date_rows = [
        r for r in range(nrows)
        if sum(_is_period(raw.iat[r, c]) for c in range(ncols)) >= 2
    ]
    if not date_rows:
        return []
    drow = date_rows[0]
    first_col = min(c for c in range(ncols) if _is_period(raw.iat[drow, c]))
    out = []
    for r in range(drow + 1, nrows):
        parts = [_clean(raw.iat[r, c]) for c in range(first_col)]
        series = " - ".join(p for p in parts if p)
        if not series:
            continue
        for c in range(first_col, ncols):
            period = _parse_period(raw.iat[drow, c])
            value = _to_float(raw.iat[r, c])
            if period is None or value is None:
                continue
            out.append((series, period, value))
    return out


def _fiscal_quarter_period(year_label, quarter_label) -> dt.date | None:
    year_text = _clean(year_label)
    quarter_text = _clean(quarter_label)
    fy = _FY_RE.search(year_text)
    qmatch = re.search(r"[1-4]", quarter_text)
    if not fy or not qmatch:
        return None
    fy_start = int(fy.group(1))
    fy_end = int(fy.group(2))
    if fy_end < 100:
        fy_end = (fy_start // 100) * 100 + fy_end
    q = int(qmatch.group(0))
    year, month = {
        1: (fy_start, 6),
        2: (fy_start, 9),
        3: (fy_start, 12),
        4: (fy_end, 3),
    }[q]
    return dt.date(year, month, 1)


def _tidy_year_quarter(raw: pd.DataFrame) -> list[tuple]:
    """Rows with separate fiscal Year and Quarter columns."""
    nrows, ncols = raw.shape
    for hrow in range(min(nrows, 40)):
        labels = [_clean(raw.iat[hrow, c]).lower() for c in range(ncols)]
        if "year" not in labels or "quarter" not in labels:
            continue
        ycol = labels.index("year")
        qcol = labels.index("quarter")
        out = []
        for r in range(hrow + 1, nrows):
            period = _fiscal_quarter_period(raw.iat[r, ycol], raw.iat[r, qcol])
            if period is None:
                continue
            for c in range(ncols):
                if c in {ycol, qcol}:
                    continue
                value = _to_float(raw.iat[r, c])
                if value is None:
                    continue
                series = _clean(raw.iat[hrow, c]) or f"col{c}"
                out.append((series, period, value))
        if out:
            return out
    return []


def _context_period(raw: pd.DataFrame, source_file: str, sheet: str) -> dt.date | None:
    periods = []
    for text in (source_file, sheet):
        p = _parse_period(text)
        if p:
            periods.append(p)
    for r in range(min(raw.shape[0], 25)):
        for c in range(min(raw.shape[1], 8)):
            p = _parse_period(raw.iat[r, c])
            if p:
                periods.append(p)
    return max(periods) if periods else None


def _tidy_point_in_time(raw: pd.DataFrame, source_file: str, sheet: str) -> list[tuple]:
    """Tables whose observation period is in workbook/sheet metadata."""
    period = _context_period(raw, source_file, sheet)
    if period is None:
        return []
    nrows, ncols = raw.shape
    for hrow in range(min(nrows, 40)):
        headers = [_clean(raw.iat[hrow, c]) for c in range(ncols)]
        if sum(bool(h) for h in headers) < 3:
            continue
        out = []
        for r in range(hrow + 1, nrows):
            row_parts = []
            for c in range(ncols):
                value = _to_float(raw.iat[r, c])
                if value is not None:
                    header = headers[c] or f"col{c}"
                    prefix = " - ".join(row_parts)
                    series = f"{prefix} - {header}" if prefix else header
                    out.append((series, period, value))
                elif len(row_parts) < 3:
                    part = _clean(raw.iat[r, c])
                    if part and not _parse_period(part):
                        row_parts.append(part)
        if len(out) >= 3:
            return out
    return []


def tidy_sheet(raw: pd.DataFrame, source_file: str, sheet: str) -> list[dict]:
    """Auto-detect orientation and return uniform tidy records for one sheet."""
    rows = _tidy_vertical(raw)
    if not rows:
        rows = _tidy_horizontal(raw)
    if not rows:
        rows = _tidy_year_quarter(raw)
    if not rows:
        rows = _tidy_point_in_time(raw, source_file, sheet)
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
