"""Shared CKAN catalog helpers for the ATO connector.

The ATO publishes through the data.gov.au CKAN portal (org
`australiantaxationoffice`). Our collect stage grouped the portal's ~1700
resources into ~489 logical tables by collapsing the per-income-year editions
of each recurring table into one entity (`<family>--<normalised-table>`), with
`income_year` lifted to a column. This module reconstructs that exact grouping
from the live catalog so a fetch fn can recover the CKAN resource ids behind a
given entity id and pull each year's flat datastore table.

The normalisation here MUST stay byte-for-byte identical to the collect stage's
(`data/sources/ato/work/code.py`) — the entity ids are derived from it and the
harness validates download-spec coverage against them.
"""

import csv
import io
import re
import zipfile

import openpyxl
import pandas as pd

from subsets_utils import get, transient_retry

BASE = "https://data.gov.au/data"
ORG = "australiantaxationoffice"

# Packages that are yearly editions of one recurring publication: the income
# year lives in the package id and the table set repeats each year. Merge them
# so a recurring table is one entity with income_year as a column.
_YEARLY_FAMILIES = [
    (re.compile(r"^taxation-statistics-(\d{4}-\d{2})$"), "taxation-statistics"),
    (re.compile(r"^international-related-party-dealings-(\d{4}-\d{2})$"),
     "international-related-party-dealings"),
]
_YEAR_TOKEN = re.compile(r"\b(19|20)\d{2}[-–]\d{2}\b|\bts\d{2}\b|\b(19|20)\d{2}\b",
                         re.IGNORECASE)


def _family_and_year(pkg_name: str):
    for pat, fam in _YEARLY_FAMILIES:
        m = pat.match(pkg_name)
        if m:
            return fam, m.group(1)
    return pkg_name, None


def _norm_table(name: str) -> str:
    s = (name or "").lower()
    s = _YEAR_TOKEN.sub(" ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unnamed"


def _entity_id(family: str, resource_name: str) -> str:
    """The collect entity id (== download spec id minus the 'ato-' prefix)."""
    key = f"{family}--{_norm_table(resource_name)}"
    return key.lower().replace("_", "-")


def safe_columns(names) -> dict:
    """Map raw CSV headers -> Delta-safe column names (lowercase snake_case),
    deduplicated. ATO headers carry spaces, newlines, dots and footnote markers
    that delta-rs rejects, so we normalise them and suffix any collisions.
    """
    out: dict[str, str] = {}
    used: dict[str, int] = {}
    for raw in names:
        s = re.sub(r"[^0-9a-zA-Z]+", "_", str(raw)).strip("_").lower() or "col"
        if s in used:
            used[s] += 1
            s = f"{s}_{used[s]}"
        else:
            used[s] = 0
        out[raw] = s
    return out


@transient_retry()
def _action(path: str, **params) -> dict:
    r = get(f"{BASE}/api/3/action/{path}", params=params, timeout=(10.0, 120.0))
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN action {path} returned success=false: {body!r}")
    return body["result"]


def fetch_catalog() -> list:
    """All ATO packages (with their resources inline), paginated."""
    out = []
    start = 0
    while True:
        res = _action("package_search", fq=f"organization:{ORG}", rows=50, start=start)
        batch = res.get("results", [])
        out.extend(batch)
        start += len(batch)
        if not batch or start >= res.get("count", 0):
            break
    return out


def build_groups() -> dict:
    """Reconstruct {entity_id -> [resource, ...]} from the live catalog.

    Each resource is a dict: {income_year, resource_id, format, datastore_active}.
    Mirrors the collect grouping exactly (PDF resources dropped).
    """
    groups: dict[str, list] = {}
    for pkg in fetch_catalog():
        fam, pkg_year = _family_and_year(pkg.get("name", ""))
        for res in pkg.get("resources", []):
            fmt = res.get("format") or ""
            if "pdf" in fmt.lower():
                continue
            rname = res.get("name") or res.get("id")
            eid = _entity_id(fam, rname)
            year = pkg_year
            if year is None:
                m = re.search(r"\b((?:19|20)\d{2}[-–]\d{2})\b", rname)
                if m:
                    year = m.group(1).replace("–", "-")
            groups.setdefault(eid, []).append({
                "income_year": year,
                "resource_id": res["id"],
                "name": rname,
                "format": (fmt or "").upper(),
                "url": res.get("url"),
                "datastore_active": bool(res.get("datastore_active")),
            })
    return groups


@transient_retry()
def _download(url: str) -> bytes:
    r = get(url, timeout=(10.0, 180.0))
    r.raise_for_status()
    return r.content


# ATO ships its dollar/count measures with thousands separators ("4,564,480,001",
# "-15,751,233,886"). Stored verbatim they're un-aggregatable text, so we strip the
# separators from any cell that is *unambiguously* a comma-grouped number (anchored,
# ≤3 leading digits, one or more `,000` groups, optional sign/decimals). Bucket
# labels ("a. 10,000 to less than 50,000"), ratios ("0.84") and "na" don't match the
# anchored pattern, so they pass through untouched. Values stay text (the union
# schema is heterogeneous), but a downstream cast now works.
_GROUPED_NUMBER = re.compile(r"^-?\d{1,3}(,\d{3})+(\.\d+)?$")


def _clean_value(v):
    if isinstance(v, str) and _GROUPED_NUMBER.match(v):
        return v.replace(",", "")
    return v


def _decode_table_text(content: bytes) -> str:
    if content.startswith((b"\xff\xfe", b"\xfe\xff")):
        return content.decode("utf-16")
    return content.decode("utf-8-sig", errors="replace")


def _csv_dialect(text: str):
    sample = text[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        return csv.excel


def csv_rows(url: str, income_year):
    """Download a CSV resource and yield each data row as a dict tagged with
    income_year. ATO publishes the flat, header-first CSV editions of its
    statistical tables here (datastore-derived XLSX tables are banner-polluted,
    so we deliberately read the CSV file, not the datastore).
    """
    text = _decode_table_text(_download(url))
    reader = csv.DictReader(io.StringIO(text), dialect=_csv_dialect(text))
    for rec in reader:
        # csv.DictReader keys ragged trailing fields under None; drop them.
        row = {k: _clean_value(v) for k, v in rec.items() if k is not None}
        row["income_year"] = income_year
        yield row


def _cell_row(resource, sheet_name, row_number, column_number, value):
    return {
        "source_resource_id": resource["resource_id"],
        "source_resource_name": resource.get("name"),
        "source_format": resource.get("format"),
        "source_url": resource.get("url"),
        "income_year": resource.get("income_year"),
        "sheet_name": sheet_name,
        "row_number": row_number,
        "column_number": column_number,
        "value": None if value is None else str(value),
    }


def _xlsx_cell_rows(content: bytes, resource, *, name_prefix=""):
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    for ws in wb.worksheets:
        sheet = f"{name_prefix}{ws.title}" if name_prefix else ws.title
        for r_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
            for c_idx, value in enumerate(row, start=1):
                if value is None or value == "":
                    continue
                yield _cell_row(resource, sheet, r_idx, c_idx, value)


def _xls_cell_rows(content: bytes, resource, *, name_prefix=""):
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, dtype=object)
    for sheet_name, frame in sheets.items():
        sheet = f"{name_prefix}{sheet_name}" if name_prefix else str(sheet_name)
        for r_idx, row in enumerate(frame.itertuples(index=False, name=None), start=1):
            for c_idx, value in enumerate(row, start=1):
                if pd.isna(value) or value == "":
                    continue
                yield _cell_row(resource, sheet, r_idx, c_idx, value)


def _csv_cell_rows(content: bytes, resource, *, name_prefix=""):
    text = _decode_table_text(content)
    reader = csv.reader(io.StringIO(text), dialect=_csv_dialect(text))
    sheet = name_prefix.rstrip(":") or "csv"
    for r_idx, row in enumerate(reader, start=1):
        for c_idx, value in enumerate(row, start=1):
            if value is None or value == "":
                continue
            yield _cell_row(resource, sheet, r_idx, c_idx, _clean_value(value))


def tabular_cell_rows(resource):
    """Yield fixed-schema cell records for workbook/archive resources.

    ATO's non-CSV resources are mostly human-oriented workbooks with banner
    rows, merged headers, and sheet-specific layouts. A normalized cell table
    is the stable raw contract for these assets; model/curate can then decide
    whether a richer table-specific reshape is warranted.
    """
    content = _download(resource["url"])
    fmt = (resource.get("format") or "").upper()
    url = (resource.get("url") or "").lower()
    is_zip = content.startswith(b"PK\x03\x04")
    is_xls = content.startswith(b"\xd0\xcf\x11\xe0")

    if (is_zip and url.endswith(".zip")) or "ZIP" in fmt or url.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                name = info.filename
                lower = name.lower()
                data = zf.read(info)
                prefix = f"{name}:"
                if lower.endswith(".csv"):
                    yield from _csv_cell_rows(data, resource, name_prefix=prefix)
                elif lower.endswith(".xlsx"):
                    yield from _xlsx_cell_rows(data, resource, name_prefix=prefix)
                elif lower.endswith(".xls"):
                    yield from _xls_cell_rows(data, resource, name_prefix=prefix)
        return

    if "CSV" in fmt or url.endswith(".csv"):
        yield from _csv_cell_rows(content, resource)
    elif is_xls or url.endswith(".xls"):
        yield from _xls_cell_rows(content, resource)
    elif is_zip or url.endswith(".xlsx") or "XLSX" in fmt:
        yield from _xlsx_cell_rows(content, resource)
    elif "XLS" in fmt:
        yield from _xls_cell_rows(content, resource)
