"""GPIH (UC Davis Global Price and Income History Group) connector.

Each rank-accepted subset is one Excel workbook served from the flat static
directory https://gpih.ucdavis.edu/files/ . The workbooks are hand-built
academic spreadsheets (medieval era to ~1950): title rows, multi-row headers,
"Notes" sheets, blank spacer columns, repeated column blocks — no uniform
schema. SQL transforms can only read parquet/ndjson/csv, so each download fn
fetches the workbook bytes and normalizes them to records here, in Python, then
saves ndjson (drifty/heterogeneous → ndjson per the raw-format rubric).

Normalization is deliberately generic (one fn for all 198 workbooks): for every
data-bearing sheet we autodetect the header row, name columns positionally,
emit one record per data row tagged with its source sheet, and enforce a single
consistent JSON type per column across the whole file so DuckDB reads it back
cleanly. This is a faithful raw extraction, not a per-dataset hand-parse — the
source is too heterogeneous to type each workbook individually.

Fetch shape: stateless full re-pull (shape 1). Workbooks are small (tens of KB
to ~1.3MB) static files with no incremental filter; re-fetch in full each run.
"""

import io
import math
import re
import urllib.parse

import numpy as np
import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS, ENTITY_FILES

BASE = "https://gpih.ucdavis.edu/files/"
PREFIX = "gpih-"


@transient_retry()  # 6 attempts, exponential backoff on transient/5xx/429
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _is_na(v) -> bool:
    if v is None:
        return True
    try:
        if isinstance(v, float) and math.isnan(v):
            return True
    except TypeError:
        pass
    try:
        return bool(pd.isna(v))
    except (TypeError, ValueError):
        return False


def _norm_value(v):
    """Coerce one cell to a JSON-friendly scalar (or None)."""
    if _is_na(v):
        return None
    if isinstance(v, (pd.Timestamp,)):
        return v.isoformat()
    if hasattr(v, "isoformat"):  # datetime/date
        try:
            return v.isoformat()
        except Exception:
            return str(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        f = float(v)
        return None if math.isnan(f) else f
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, (bool, int, float, str)):
        return v
    return str(v)


def _clean_name(raw, idx: int) -> str:
    """Build a column name from a header cell, falling back to positional c{idx}."""
    if _is_na(raw):
        return f"c{idx}"
    s = str(raw).strip()
    # numbers-as-headers (e.g. a year used as a column label) keep their text
    s = re.sub(r"\s+", " ", s).replace("\n", " ").strip()
    if not s:
        return f"c{idx}"
    return s[:60]


def _dedupe(names):
    seen = {}
    out = []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
        else:
            seen[n] = 1
            out.append(n)
    return out


_NOTES_SHEET = re.compile(r"^\s*(sources?\b|notes?\b|read\s*me|metadata|legend|key\b)", re.IGNORECASE)


def _is_notes_sheet(name: str) -> bool:
    return bool(_NOTES_SHEET.match(str(name)))


def _records_from_sheet(df: pd.DataFrame, sheet: str):
    """Extract data records from one sheet's raw (header=None) grid."""
    df = df.dropna(how="all").dropna(axis=1, how="all")
    if df.shape[0] < 2 or df.shape[1] < 2:  # single-column sheets are notes/text
        return []
    grid = df.values.tolist()
    ncols = df.shape[1]

    # Header row = the widest row (most non-null cells) within the first rows;
    # the real header in these workbooks sits below title/blank rows.
    look = min(20, len(grid))
    header_idx = max(range(look), key=lambda i: sum(1 for c in grid[i] if not _is_na(c)))
    data = grid[header_idx + 1:]
    if not data:  # header was the last row → treat the whole grid as data
        header_idx, data = -1, grid

    header = grid[header_idx] if header_idx >= 0 else [None] * ncols
    names = _dedupe([_clean_name(header[i] if i < len(header) else None, i) for i in range(ncols)])

    records = []
    for row in data:
        if all(_is_na(c) for c in row):
            continue
        rec = {"__sheet__": sheet}
        for i in range(ncols):
            rec[names[i]] = _norm_value(row[i] if i < len(row) else None)
        records.append(rec)
    return records


def _enforce_consistent_types(records):
    """Make each column a single JSON type across the whole file: a column is
    kept numeric only if every present value is a real number, else stringified.
    Guarantees DuckDB infers one stable type per key on read."""
    keys = set()
    for r in records:
        keys.update(r.keys())
    for k in keys:
        numeric = True
        for r in records:
            v = r.get(k)
            if v is None:
                continue
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                numeric = False
                break
        if not numeric:
            for r in records:
                v = r.get(k)
                if v is not None and not isinstance(v, str):
                    r[k] = str(v)
    return records


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id = node_id[len(PREFIX):] if node_id.startswith(PREFIX) else node_id
    filename = ENTITY_FILES[entity_id]
    url = BASE + urllib.parse.quote(filename)

    content = _download(url)
    engine = "openpyxl" if filename.lower().endswith("xlsx") else "xlrd"
    xls = pd.ExcelFile(io.BytesIO(content), engine=engine)

    records = []
    for sheet in xls.sheet_names:
        if _is_notes_sheet(sheet):
            continue
        df = pd.read_excel(xls, sheet_name=sheet, header=None, dtype=object)
        records.extend(_records_from_sheet(df, sheet))

    # Safety net: never emit an empty table. If no sheet parsed as tabular,
    # fall back to the densest sheet dumped row-by-row as text.
    if not records:
        best, best_score = None, -1
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet, header=None, dtype=object)
            score = int(df.notna().sum().sum())
            if score > best_score:
                best, best_score = (sheet, df), score
        if best and best_score > 0:
            sheet, df = best
            for ridx, row in enumerate(df.values.tolist()):
                cells = [str(_norm_value(c)) for c in row if not _is_na(c)]
                if cells:
                    records.append({"__sheet__": sheet, "row": ridx, "text": " | ".join(cells)})

    if not records:
        raise AssertionError(f"{asset}: workbook {filename!r} produced no rows")

    _enforce_consistent_types(records)
    save_raw_ndjson(records, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per workbook. The raw ndjson is already a faithful,
# consistently-typed extraction, so the transform is a thin pass-through that
# republishes every row (DuckDB unions the per-row keys by name).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
