"""ELSTAT (Hellenic Statistical Authority) connector.

Mechanism (from research): there is NO public JSON/SDMX API. ELSTAT publishes
each statistical product as a "publication" with a stable code (e.g. SDT03,
DKT87, SEL15) at https://www.statistics.gr/en/statistics/-/publication/<CODE>/-.
Each publication page (static, server-rendered HTML) exposes its attachments as
Liferay JSF resource links keyed by a portlet INSTANCE id + an integer
documentID. The data-bearing attachments are Excel workbooks (.xlsx / legacy
.xls); the rest are PDF press releases / methodology (out of scope).

Per publication we: fetch the page, harvest every document link, GET each and
keep the ones the server returns as Excel, dedup language editions (prefer the
English / bilingual one), then melt every workbook into long format — one record
per numeric cell, tagged with the cell's row label (leftmost text of its row)
and column label (the detected header row, forward-filled across merged cells).
This orientation-agnostic melt handles both row-oriented timeseries (period in
rows, measures in columns) and column-oriented cross-tabs (years in columns).

Full re-pull every run (stateless): each workbook is a cumulative snapshot that
grows with each release, there is no incremental filter, and the whole corpus is
small. Freshness gating is the maintain step's job.
"""

import io
import math
import re

import pandas as pd

from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

PUBLICATION_URL = "https://www.statistics.gr/en/statistics/-/publication/{code}/-"

# Liferay document download links on a publication page. We do NOT rely on the
# portlet INSTANCE id to tell data from non-data (it is not constant across
# publications) — we classify by the Content-Type the server returns.
_DOC_LINK_RE = re.compile(
    r'(https?://www\.statistics\.gr[^"\']*?'
    r'documents_WAR_publicationsportlet_INSTANCE_[A-Za-z0-9]+[^"\']*?'
    r'documentID=\d+[^"\']*?)["\']'
)
_DOCID_RE = re.compile(r"documentID=(\d+)")
_FILENAME_RE = re.compile(r'filename="?([^";]+)')
_EXCEL_CT = (
    "officedocument.spreadsheetml",      # .xlsx
    "application/vnd.ms-excel",          # legacy .xls
)

# --- generic workbook -> long-format melt ----------------------------------

_SKIP = {"", "nan", "nat", "none", "-", ".", "..", "...", ":", "n/a", "na", "n.a.", "*", "**"}


def _clean(v):
    """Stripped, whitespace-collapsed string, or None for blank/sentinel cells."""
    if v is None:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    if s.lower() in _SKIP:
        return None
    return s


def _to_num(v):
    """Parse a cell into a finite float, or None. Handles EU/US separators."""
    s = _clean(v)
    if s is None:
        return None
    s2 = s.replace(" ", "").replace(" ", "")
    if "," in s2 and "." in s2:
        if s2.rfind(",") > s2.rfind("."):
            s2 = s2.replace(".", "").replace(",", ".")
        else:
            s2 = s2.replace(",", "")
    elif "," in s2:
        parts = s2.split(",")
        if len(parts) == 2 and len(parts[1]) != 3:
            s2 = s2.replace(",", ".")
        else:
            s2 = s2.replace(",", "")
    try:
        f = float(s2)
    except ValueError:
        return None
    return f if math.isfinite(f) else None


def _melt_sheet(grid, source_file, sheet):
    g = [list(r) for r in grid]
    nrows = len(g)
    if nrows == 0:
        return []
    ncols = max((len(r) for r in g), default=0)
    for r in g:
        r += [None] * (ncols - len(r))

    def num_cells(row):
        return sum(1 for j in range(1, ncols) if _to_num(row[j]) is not None)

    first_data = None
    for i, row in enumerate(g):
        if num_cells(row) >= 2:
            first_data = i
            break
    if first_data is None:
        for i, row in enumerate(g):
            if num_cells(row) >= 1:
                first_data = i
                break
    if first_data is None:
        return []

    cand = list(range(max(0, first_data - 6), first_data))

    def nonempty(row):
        return sum(1 for c in row if _clean(c) is not None)

    header_idx = max(cand, key=lambda i: nonempty(g[i])) if cand else None
    header = g[header_idx] if header_idx is not None else [None] * ncols
    filled, last = [], None
    for c in header:
        cc = _clean(c)
        if cc is not None:
            last = cc
        filled.append(last)

    out = []
    for i in range(first_data, nrows):
        row = g[i]
        if num_cells(row) == 0:
            continue
        rl = None
        for j in range(ncols):
            c = _clean(row[j])
            if c is not None and _to_num(row[j]) is None:
                rl = c
                break
        if rl is None:
            for j in range(ncols):
                c = _clean(row[j])
                if c is not None:
                    rl = c
                    break
        for j in range(ncols):
            n = _to_num(row[j])
            if n is None:
                continue
            cl = filled[j] if j < len(filled) else None
            if cl is None or cl == rl:
                cl = f"col{j}"
            out.append({
                "source_file": source_file,
                "sheet": str(sheet)[:120],
                "row_label": (rl or "")[:300],
                "col_label": cl[:300],
                "row_idx": i,
                "col_idx": j,
                "value": n,
            })
    return out


def _melt_workbook(content, source_file):
    sheets = pd.read_excel(io.BytesIO(content), header=None, dtype=str, sheet_name=None)
    rows = []
    for sheet, df in sheets.items():
        grid = df.where(pd.notna(df), None).values.tolist()
        rows.extend(_melt_sheet(grid, source_file, sheet))
    return rows


_LANG_RE = re.compile(r"_([A-Za-z?]{2})(?:_\d+)?\.(?:xlsx?|XLSX?)$")


def _select_excel(files):
    """files: list of (filename, content). Prefer the English (then bilingual)
    edition of each table to avoid duplicating data across language variants."""
    def lang(fn):
        m = _LANG_RE.search(fn)
        return m.group(1).upper() if m else ""

    def stem(fn):
        return _LANG_RE.sub("", fn).upper()

    groups = {}
    for fn, content in files:
        groups.setdefault(stem(fn), []).append((fn, content))
    pref = {"EN": 0, "BI": 1, "": 2}
    chosen = []
    for members in groups.values():
        members.sort(key=lambda fc: pref.get(lang(fc[0]), 3))
        chosen.append(members[0])
    return chosen


# --- HTTP ------------------------------------------------------------------

@transient_retry()
def _get_page(code):
    resp = get(PUBLICATION_URL.format(code=code), timeout=(10.0, 90.0))
    resp.raise_for_status()
    html = resp.text
    if "documentID=" not in html:
        # The publication portlets sometimes render empty under load; treat a
        # page with no document links as transient and let the retry re-fetch.
        raise RuntimeError(f"publication page for {code} carried no document links")
    return html


@transient_retry()
def _get_doc(url):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _excel_attachments(code):
    html = _get_page(code)
    seen = set()
    files = []
    for m in _DOC_LINK_RE.finditer(html):
        url = m.group(1).replace("&amp;", "&")
        did = _DOCID_RE.search(url).group(1)
        if did in seen:
            continue
        seen.add(did)
        resp = _get_doc(url)
        ct = resp.headers.get("content-type", "").lower()
        if not any(x in ct for x in _EXCEL_CT):
            continue
        cd = resp.headers.get("content-disposition", "")
        fn = _FILENAME_RE.search(cd)
        fn = fn.group(1).strip() if fn else f"{code}_{did}.xlsx"
        files.append((fn, resp.content))
    return files


def fetch_one(node_id: str) -> None:
    asset = node_id                                  # the spec id IS the asset name
    code = node_id[len("elstat-"):].upper()
    files = _select_excel(_excel_attachments(code))
    rows = []
    for fn, content in files:
        try:
            rows.extend(_melt_workbook(content, fn))
        except Exception as exc:                     # one corrupt workbook must not sink the publication
            print(f"elstat: failed to parse workbook {fn} for {code}: {type(exc).__name__}: {exc}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"elstat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per publication: the long-format numeric observations.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                source_file,
                sheet,
                row_label,
                col_label,
                CAST(row_idx AS BIGINT) AS row_idx,
                CAST(col_idx AS BIGINT) AS col_idx,
                CAST(value AS DOUBLE)   AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
