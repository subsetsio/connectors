"""DESNZ (UK Dept for Energy Security & Net Zero) — data.gov.uk catalog connector.

Mechanism (from research): CKAN action API as the enumeration spine, bulk file
download for the data. The DESNZ publisher org exposes ~62 packages; the rank
step accepted 44. Each package is one subset (one published Delta table).

There is no datastore behind these packages — every resource is a human-formatted
Excel/ODS/CSV statistical workbook (cover/contents banner rows, multiple sheets,
bespoke per-package layouts). There is no machine-readable schema and no two
packages share one. The only faithful, *uniform* representation across the whole
heterogeneous catalog is a **tidy long melt**: for every tabular resource in a
package we detect each sheet's data block (skip the banner rows, find the header
row) and emit one row per (resource, sheet, row label, column header) cell, with
the value kept both as text and as a parsed number. Every package therefore lands
as the same six-column long table, which is what makes 44 bespoke workbooks
queryable through one stable schema.

Fetch shape: **stateless full re-pull** (shape 1). The corpus is dozens of packages
of modest spreadsheets; re-enumerating CKAN and re-downloading each refresh is
cheap and picks up revisions/new periods for free. Resource URLs are hash-based
/media/<hash>/ paths that rotate on republish, so we always resolve them fresh
from CKAN at fetch time and never cache them. No watermark, no cursor.
"""
import io
import json
import logging
from urllib.parse import urlparse, parse_qs

import httpx
from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, raw_writer
from constants import ENTITY_CKAN

log = logging.getLogger("desnz")

CKAN = "https://ckan.publishing.service.gov.uk/api/3/action"

# Resource formats that carry tabular data. Everything else (pdf, webpage, html,
# document, zip, ...) is a supplementary/landing resource and is dropped.
TABULAR_FORMATS = {"csv", "xlsx", "xls", "ods"}

# A detected sheet block must have at least this many populated data rows to be
# emitted. Cuts the small cover/contents/highlights blocks while keeping every
# real data table.
MIN_DATA_ROWS = 5

# Raw long-format schema — same six columns for every package.
RAW_COLUMNS = ["resource", "sheet", "row_label", "series", "value_text", "value_num"]


@transient_retry()
def _ckan_package(name):
    resp = get(f"{CKAN}/package_show", params={"id": name}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {name}: {body.get('error')}")
    return body["result"]


@transient_retry()
def _download(url):
    resp = get(url, timeout=(15.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _unwrap_url(url):
    """data.gov.uk sometimes stores resource URLs wrapped in an Outlook safelinks
    redirect; the real target is the `url` query param. Unwrap it so we hit
    assets.publishing.service.gov.uk directly."""
    if not url:
        return None
    if "safelinks.protection.outlook.com" in url:
        qs = parse_qs(urlparse(url).query)
        inner = qs.get("url", [None])[0]
        if inner:
            return inner
    return url


def _parse_num(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _read_sheets(content, fmt, url):
    """Return [(sheet_name, grid)] where grid is list[list[cell|None]]. Sniffs the
    real container from the magic bytes — CKAN format labels are unreliable (an
    'XLS' resource often points at an .xlsx file)."""
    import pandas as pd

    head = content[:8]
    sheets = []
    if head[:4] == b"PK\x03\x04":
        # Zip container: xlsx or ods. Try the modern Excel reader, fall back to ODF.
        try:
            xl = pd.ExcelFile(io.BytesIO(content), engine="openpyxl")
        except Exception:
            xl = pd.ExcelFile(io.BytesIO(content), engine="odf")
        for sn in xl.sheet_names:
            sheets.append((str(sn), _df_to_grid(xl.parse(sn, header=None, dtype=object))))
    elif head[:4] == b"\xd0\xcf\x11\xe0":
        # OLE2 container: legacy .xls.
        xl = pd.ExcelFile(io.BytesIO(content), engine="xlrd")
        for sn in xl.sheet_names:
            sheets.append((str(sn), _df_to_grid(xl.parse(sn, header=None, dtype=object))))
    elif fmt == "csv" or (url or "").lower().split("?")[0].endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content), header=None, dtype=object,
                         on_bad_lines="skip", encoding_errors="replace")
        sheets.append(("", _df_to_grid(df)))
    # else: mislabeled non-tabular payload (html landing page, etc.) — skip silently.
    return sheets


def _df_to_grid(df):
    import pandas as pd

    grid = []
    for row in df.itertuples(index=False, name=None):
        grid.append([None if (c is None or (isinstance(c, float) and pd.isna(c))) else c
                     for c in row])
    return grid


def _detect_table(grid):
    """Find the header row of a sheet's main data block: skip leading banner rows,
    pick the first richly-populated row that is followed by data. Returns
    (header_idx, label_col, value_cols, header_cells) or None."""
    counts = [sum(1 for c in r if c not in (None, "")) for r in grid]
    if not counts or max(counts) < 2:
        return None
    thresh = max(2, int(0.6 * max(counts)))
    for i in range(min(len(grid), 60)):
        if counts[i] >= thresh and i + 1 < len(grid) and counts[i + 1] >= 2:
            header_cells = grid[i]
            cols = [j for j, c in enumerate(header_cells) if c not in (None, "")]
            if len(cols) < 2:
                continue
            return i, cols[0], cols[1:], header_cells
    return None


def _iter_resource_rows(content, fmt, url, resource_name):
    """Detect each sheet's table and yield one long-format dict per populated
    cell: (resource, sheet, row_label, series, value_text, value_num)."""
    for sheet_name, grid in _read_sheets(content, fmt, url):
        det = _detect_table(grid)
        if det is None:
            continue
        h, label_col, value_cols, header = det
        data = grid[h + 1:]
        block = [r for r in data if label_col < len(r) and r[label_col] not in (None, "")]
        if len(block) < MIN_DATA_ROWS:
            continue
        series_names = {c: str(header[c]).strip() for c in value_cols}
        for r in block:
            row_label = str(r[label_col]).strip()
            for c in value_cols:
                if c >= len(r):
                    continue
                v = r[c]
                if v in (None, ""):
                    continue
                yield {
                    "resource": resource_name,
                    "sheet": sheet_name,
                    "row_label": row_label,
                    "series": series_names[c],
                    "value_text": str(v).strip(),
                    "value_num": _parse_num(v),
                }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("desnz-"):]
    ckan_name = ENTITY_CKAN[entity_id]

    pkg = _ckan_package(ckan_name)
    # Stream long-format rows straight to a gzip ndjson asset — the big packages
    # melt to millions of rows, far past what fits in memory as one list.
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for res in pkg.get("resources", []):
            fmt = (res.get("format") or "").lower().lstrip(".")
            if fmt not in TABULAR_FORMATS:
                continue
            url = _unwrap_url(res.get("url"))
            if not url:
                continue
            resource_name = (res.get("name") or res.get("id") or url).strip()
            try:
                content = _download(url)
                for row in _iter_resource_rows(content, fmt, url, resource_name):
                    out.write(json.dumps(row, separators=(",", ":")) + "\n")
                    n += 1
            except httpx.HTTPStatusError as e:
                # Permanent per-resource failure (e.g. 410 Gone when a file is
                # withdrawn, 404). Skip this resource, keep the rest of the package.
                code = e.response.status_code
                if code == 429 or code >= 500:
                    raise  # transient — let the retry/runner handle it
                log.warning("desnz: skipping resource %s (HTTP %s): %s", url, code, resource_name)
                continue
            except Exception as e:
                # A malformed/corrupt workbook is a permanent per-resource fault;
                # log url + exception class and keep going rather than failing the
                # whole package. (Real programming bugs surface in the logs.)
                log.warning("desnz: failed to parse resource %s (%s): %s",
                            url, type(e).__name__, e)
                continue
    log.info("desnz: %s wrote %d rows", asset, n)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"desnz-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_CKAN
]


# One published Delta table per package. The SQL is a thin type-and-filter pass
# over the long raw: keep populated cells, expose value_num as a real double.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                resource,
                sheet,
                row_label,
                series,
                value_text,
                TRY_CAST(value_num AS DOUBLE) AS value_num
            FROM "{s.id}"
            WHERE value_text IS NOT NULL
              AND length(value_text) > 0
        ''',
    )
    for s in DOWNLOAD_SPECS
]
