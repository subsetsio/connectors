"""U.S. Department of Education Open Data Platform (data.ed.gov).

The portal is CKAN. Each accepted entity is one CKAN package, and each package
can contain several tabular resources with different local schemas. Fetching
normalizes every readable CSV/Excel member into NDJSON rows. Provenance columns
identify the package/resource/file/sheet; source columns are kept as strings.
"""

from __future__ import annotations

import csv
import io
import json
import re
import warnings
import zipfile
from collections.abc import Iterable
from pathlib import PurePosixPath

import pandas as pd

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_ndjson

SLUG = "u-s-department-of-education"
PREFIX = f"{SLUG}-"
CKAN = "https://data.ed.gov/api/3/action"
USER_AGENT = "subsets.io u-s-department-of-education connector"

TABULAR_FORMAT_HINTS = (
    "csv",
    "tsv",
    "xls",
    "excel",
    "zip",
    "dat",
    "sas",
    "spss",
    "sav",
    "stata",
    "dta",
    "txt",
    "text",
    "ascii",
    "mdb",
    "accdb",
    "json",
)

SKIP_FORMAT_HINTS = (
    "pdf",
    "doc",
    "word",
    "html",
    "arcgis",
    "geojson",
    "kml",
    "gdb",
    "gpkg",
)

TEXT_EXTENSIONS = {".csv", ".tsv", ".txt", ".dat", ".asc", ".ascii"}
EXCEL_EXTENSIONS = {".xls", ".xlsx", ".xlsm"}
JSON_EXTENSIONS = {".json"}


class UnsupportedResourceError(ValueError):
    pass


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}; expected prefix {PREFIX!r}")
    return node_id[len(PREFIX):]


def _ckan(action: str, **params) -> dict:
    resp = get(
        f"{CKAN}/{action}",
        params=params,
        headers={"User-Agent": USER_AGENT},
        timeout=120.0,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN {action} failed: {data!r}")
    return data["result"]


def _download(url: str) -> bytes:
    resp = get(url, headers={"User-Agent": USER_AGENT}, timeout=240.0)
    resp.raise_for_status()
    return resp.content


def _clean_col(value, pos: int) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        text = f"column_{pos + 1}"
    return text


def _stringify(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if pd.isna(value):
        return None
    return str(value)


def _records_from_frame(df: pd.DataFrame, provenance: dict) -> Iterable[dict]:
    if df.empty:
        return
    df = df.dropna(how="all")
    cols = [_clean_col(c, i) for i, c in enumerate(df.columns)]
    seen = {}
    unique_cols = []
    for col in cols:
        n = seen.get(col, 0) + 1
        seen[col] = n
        unique_cols.append(col if n == 1 else f"{col}_{n}")
    df.columns = unique_cols
    for row_number, row in enumerate(df.itertuples(index=False, name=None), start=1):
        out = dict(provenance)
        out["row_number"] = row_number
        out.update({col: _stringify(value) for col, value in zip(unique_cols, row)})
        yield out


def _read_delimited(content: bytes, filename: str, provenance: dict) -> Iterable[dict]:
    sample = content[:8192].decode("utf-8-sig", "replace")
    delimiter = "\t" if filename.lower().endswith(".tsv") else None
    if delimiter is None:
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",\t|;").delimiter
        except csv.Error:
            delimiter = ","
    text = io.BytesIO(content)
    try:
        df = pd.read_csv(
            text,
            sep=delimiter,
            dtype=str,
            engine="python",
            on_bad_lines="skip",
            encoding="utf-8-sig",
        )
    except Exception:
        lines = content.decode("utf-8-sig", "replace").splitlines()
        df = pd.DataFrame({"line": lines})
    yield from _records_from_frame(df, provenance)


def _read_excel(content: bytes, provenance: dict) -> Iterable[dict]:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unknown extension is not supported")
        sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str)
    for sheet_name, df in sheets.items():
        sheet_provenance = {**provenance, "sheet_name": str(sheet_name)}
        yield from _records_from_frame(df, sheet_provenance)


def _read_json(content: bytes, provenance: dict) -> Iterable[dict]:
    data = json.loads(content.decode("utf-8-sig"))
    if isinstance(data, list):
        iterable = data
    elif isinstance(data, dict):
        iterable = data.get("data") or data.get("results") or data.get("records") or [data]
    else:
        iterable = [{"value": data}]
    for row_number, item in enumerate(iterable, start=1):
        out = dict(provenance)
        out["row_number"] = row_number
        if isinstance(item, dict):
            out.update({str(k): _stringify(v) for k, v in item.items()})
        else:
            out["value"] = _stringify(item)
        yield out


def _read_member(content: bytes, filename: str, provenance: dict) -> Iterable[dict]:
    suffix = PurePosixPath(filename.split("?", 1)[0]).suffix.lower()
    if _looks_like_html(content):
        raise UnsupportedResourceError("resource returned HTML")
    if suffix in EXCEL_EXTENSIONS:
        yield from _read_excel(content, provenance)
    elif suffix in JSON_EXTENSIONS:
        yield from _read_json(content, provenance)
    else:
        yield from _read_delimited(content, filename, provenance)


def _read_zip(content: bytes, provenance: dict) -> Iterable[dict]:
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            suffix = PurePosixPath(name).suffix.lower()
            if suffix not in TEXT_EXTENSIONS | EXCEL_EXTENSIONS | JSON_EXTENSIONS:
                continue
            member_provenance = {**provenance, "archive_member": name}
            with zf.open(info) as fh:
                yield from _read_member(fh.read(), name, member_provenance)


def _looks_like_html(content: bytes) -> bool:
    head = content[:512].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def _resource_is_tabular(resource: dict) -> bool:
    fmt = str(resource.get("format") or "").lower()
    name = str(resource.get("name") or resource.get("url") or "").lower()
    combined = f"{fmt} {name}"
    if any(hint in combined for hint in SKIP_FORMAT_HINTS):
        return any(hint in combined for hint in TABULAR_FORMAT_HINTS if hint not in {"json"})
    return any(hint in combined for hint in TABULAR_FORMAT_HINTS)


def fetch_one(node_id: str) -> None:
    package_id = _entity_id(node_id)
    package = _ckan("package_show", id=package_id)
    rows = []
    skipped = 0

    for resource in package.get("resources") or []:
        url = resource.get("url")
        if not url or not _resource_is_tabular(resource):
            skipped += 1
            continue

        provenance = {
            "package_id": package_id,
            "package_title": package.get("title") or package_id,
            "resource_id": resource.get("id"),
            "resource_name": resource.get("name"),
            "resource_format": resource.get("format"),
            "resource_position": resource.get("position"),
        }
        content = _download(url)
        filename = url.rsplit("/", 1)[-1] or str(resource.get("name") or "resource")
        suffix = PurePosixPath(filename.split("?", 1)[0]).suffix.lower()
        try:
            if suffix == ".zip" or (suffix not in EXCEL_EXTENSIONS and zipfile.is_zipfile(io.BytesIO(content))):
                rows.extend(_read_zip(content, provenance))
            else:
                rows.extend(_read_member(content, filename, provenance))
        except UnsupportedResourceError:
            skipped += 1
            continue
        except Exception as exc:
            raise RuntimeError(
                f"{package_id}: failed parsing resource {resource.get('id')} "
                f"({resource.get('name')!r}, format={resource.get('format')!r}, url={url})"
            ) from exc

    if not rows:
        raise RuntimeError(f"{package_id}: no tabular rows parsed; skipped {skipped} resources")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
