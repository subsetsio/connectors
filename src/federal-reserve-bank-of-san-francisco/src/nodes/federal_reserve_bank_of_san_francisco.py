"""Federal Reserve Bank of San Francisco — Economic Research "Data and Indicators".

FRBSF publishes a curated set of statistical indicators, each on its own page at
https://www.frbsf.org/research-and-insights/data-and-indicators/<slug>/ and each
backed by one (occasionally a few) downloadable Excel workbook(s) hosted at stable
wp-content/uploads/<file>.xlsx URLs. Workbook layouts vary widely (1-11 sheets;
metadata sheets to skip; date axes formatted as ISO dates, 'YYYY:Qn' quarters, or
bare years; a couple of true panels keyed by a dimension such as US state).

Strategy (stateless full re-pull — every file is tiny, the whole source is a few
MB): for each indicator we re-discover its xlsx link(s) from the (stable-slug)
indicator page each run, download them, and run a single universal *wide-to-long
melt* that produces one tidy schema for every indicator:

    sheet (str) | period (str, raw label) | date (date) | dimension (str|null) | series (str) | value (double)

Each indicator publishes its own Delta table, so the 22 tables differ by content
(series/dimension values), not by column list. There is no incremental query
support and no machine-readable schema; we re-melt the full workbook each refresh.
"""
import io
import re

import numpy as np
import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

SLUG = "federal-reserve-bank-of-san-francisco"
PREFIX = f"{SLUG}-"
HUB = "https://www.frbsf.org/research-and-insights/data-and-indicators/"

# Raw long-format schema, shared by every indicator (explicit = the contract).
SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("period", pa.string()),
    ("date", pa.date32()),
    ("dimension", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])

_XLSX_LINK = re.compile(
    r'href="([^"]*wp-content/uploads/[^"]+?\.xlsx)(?:\?[^"]*)?"', re.I
)
_META_SHEET = re.compile(
    r"(readme|methodolog|description|contents?|notes|about|^info|cover|citation|legend|sources?|disclaimer)",
    re.I,
)
_DATE_HDR = re.compile(r"(date|period|month|week|quarter|release|observation)", re.I)


# ---------------------------------------------------------------------------
# Universal workbook parser (wide-to-long melt)
# ---------------------------------------------------------------------------
def _parse_period_strings(str_series: pd.Series):
    """Parse a string Series into dates. Operates only on the string form so plain
    integers are never misread as nanosecond epochs. Handles ISO datetimes,
    'YYYY:Qn'/'YYYYQn', 'YYYYmMM', and bare 'YYYY'. Returns (date Series, ok_frac)."""
    s = str_series
    out = pd.to_datetime(s, errors="coerce", format="mixed")
    miss = out.isna() & s.notna() & (s.str.strip() != "")
    for idx in np.where(miss.to_numpy())[0]:
        v = str(s.iloc[idx]).strip()
        m = re.match(r"^(\d{4})[:\-]?[Qq]([1-4])$", v)
        if m:
            out.iloc[idx] = pd.Timestamp(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)
            continue
        m = re.match(r"^(\d{4})[:\-]?[Mm](\d{1,2})$", v)
        if m and 1 <= int(m.group(2)) <= 12:
            out.iloc[idx] = pd.Timestamp(int(m.group(1)), int(m.group(2)), 1)
            continue
        if re.match(r"^(19|20)\d{2}$", v):  # bare 4-digit year
            out.iloc[idx] = pd.Timestamp(int(v), 1, 1)
            continue
    nonblank = (s.notna() & (s.str.strip() != "")).sum()
    return out, out.notna().sum() / max(1, nonblank)


def _as_str(col: pd.Series) -> pd.Series:
    return col.astype("string").str.strip()


def parse_workbook(content: bytes, file_stem: str, always_prefix: bool = False):
    """Melt every data sheet of an xlsx workbook into long rows:
    dict(sheet, period, date, dimension, series, value)."""
    xl = pd.ExcelFile(io.BytesIO(content))
    rows = []
    multi = len(xl.sheet_names) > 1
    prefix_sheet = multi or always_prefix
    for sh in xl.sheet_names:
        if _META_SHEET.search(sh.strip()):
            continue
        raw = xl.parse(sh, header=None)
        if raw.empty or raw.shape[1] < 2:
            continue
        # Header row: first row (of first ~15) carrying a date-ish label, else the
        # first row with >= 2 non-null cells.
        hr = None
        for i in range(min(15, len(raw))):
            cells = [str(c).strip() for c in raw.iloc[i].tolist()]
            if any(_DATE_HDR.search(c) for c in cells if c and c.lower() != "nan"):
                hr = i
                break
        if hr is None:
            for i in range(min(15, len(raw))):
                if raw.iloc[i].notna().sum() >= 2:
                    hr = i
                    break
        if hr is None:
            continue
        header = [str(c).strip() for c in raw.iloc[hr].tolist()]
        body = raw.iloc[hr + 1:].reset_index(drop=True)
        body.columns = range(body.shape[1])
        if body.empty:
            continue
        # Time-axis column = the column with the best date-parse fraction, with a
        # bonus for a date-ish header. Require >= 0.6 to treat the sheet as a series.
        best = None  # (score, col_index, parsed_dates)
        for ci in range(min(body.shape[1], 8)):
            parsed, ok = _parse_period_strings(_as_str(body[ci]))
            name = header[ci] if ci < len(header) else ""
            score = ok + (0.5 if name and _DATE_HDR.search(name) else 0.0)
            if ok >= 0.6 and (best is None or score > best[0]):
                best = (score, ci, parsed)
        if best is None:
            continue
        _, dci, date_parsed = best
        period_raw = _as_str(body[dci])
        keep = period_raw.notna() & (period_raw != "") & (period_raw.str.lower() != "nan")
        kmask = keep.to_numpy()
        body = body[kmask].reset_index(drop=True)
        period_raw = period_raw[kmask].reset_index(drop=True)
        date_parsed = date_parsed[kmask].reset_index(drop=True)
        n = len(body)
        if n == 0:
            continue
        sheet_tag = f"{file_stem}:{sh.strip()}" if prefix_sheet else sh.strip()
        is_panel = period_raw.duplicated(keep=False).sum() > 0.3 * n
        value_cols, dim_cols = [], []
        for ci in range(body.shape[1]):
            if ci == dci:
                continue
            name = header[ci] if ci < len(header) else ""
            if not name or name.lower() in ("nan", "none", ""):
                continue  # drop unnamed / index columns
            col = body[ci]
            num = pd.to_numeric(
                col.astype("string").str.replace(",", "", regex=False), errors="coerce"
            )
            numfrac = num.notna().sum() / max(1, col.notna().sum())
            if numfrac >= 0.6:
                value_cols.append((name, num))
            else:
                dim_cols.append((name, _as_str(col)))
        if is_panel and dim_cols:
            dim_vals = []
            for i in range(n):
                parts = [str(dc[1].iloc[i]) for dc in dim_cols if dc[1].iloc[i] is not pd.NA]
                dim_vals.append(" | ".join(parts) if parts else None)
        else:
            dim_vals = [None] * n
        for name, num in value_cols:
            arr = num.to_numpy()
            for i in range(n):
                v = arr[i]
                if v is None or (isinstance(v, float) and np.isnan(v)):
                    continue
                d = date_parsed.iloc[i]
                rows.append({
                    "sheet": sheet_tag,
                    "period": None if period_raw.iloc[i] is pd.NA else str(period_raw.iloc[i]),
                    "date": None if pd.isna(d) else d.date(),
                    "dimension": dim_vals[i],
                    "series": name,
                    "value": float(v),
                })
    return rows


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
@transient_retry()
def _get(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _discover_xlsx(slug: str) -> list[str]:
    resp = _get(f"{HUB}{slug}/")
    urls = []
    for m in _XLSX_LINK.finditer(resp.text):
        u = m.group(1)
        if not u.startswith("http"):
            u = "https://www.frbsf.org" + u
        if u not in urls:
            urls.append(u)
    return urls


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    slug = node_id[len(PREFIX):] if node_id.startswith(PREFIX) else node_id
    urls = _discover_xlsx(slug)
    if not urls:
        raise RuntimeError(f"{slug}: no .xlsx download link found on indicator page {HUB}{slug}/")
    multi_file = len(urls) > 1
    rows = []
    for url in urls:
        resp = _get(url)
        stem = url.rstrip("/").split("/")[-1].rsplit(".", 1)[0]
        rows.extend(parse_workbook(resp.content, stem, always_prefix=multi_file))
    if not rows:
        raise RuntimeError(
            f"{slug}: parsed 0 rows from {len(urls)} workbook(s) "
            f"({[u.split('/')[-1] for u in urls]}) — layout likely changed"
        )
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per indicator. Thin parse-and-type pass: keep dated,
# non-null observations in the shared tidy long shape.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)   AS date,
                period,
                sheet,
                series,
                dimension,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
              AND date IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
