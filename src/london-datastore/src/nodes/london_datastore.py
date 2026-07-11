"""London Datastore connector.

Each download node is one accepted CKAN package. A package can contain one or
more tabular resources with different schemas, so the raw asset is normalized
to a fixed string-typed row table: package/resource metadata plus `data_json`,
the original source row encoded as JSON.
"""

from __future__ import annotations

import io
import json
import re
import zipfile
from collections.abc import Iterable
from pathlib import PurePosixPath

import pandas as pd
import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "london-datastore"
PREFIX = f"{SLUG}-"
API = "https://data.london.gov.uk/api/action"

SUPPORTED_EXTENSIONS = {".csv", ".xls", ".xlsx", ".json"}
TABULAR_FORMATS = {"csv", "xls", "xlsx", "json", "zip"}
BASE_COLUMNS = [
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_url",
    "member_path",
    "sheet_name",
    "source_row_number",
    "data_json",
]


def _api(action: str, **params):
    resp = get(f"{API}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"CKAN {action} returned success!=true for {params}")
    return body["result"]


def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _extension(url_or_name: str) -> str:
    path = PurePosixPath(str(url_or_name).split("?", 1)[0].lower())
    suffix = path.suffix
    if suffix == ".gz":
        return PurePosixPath(path.stem).suffix
    return suffix


def _resource_format(resource: dict) -> str:
    fmt = str(resource.get("format") or "").strip().lower()
    if fmt:
        return fmt
    ext = _extension(resource.get("url") or "")
    return ext.lstrip(".")


def _is_supported_resource(resource: dict) -> bool:
    fmt = _resource_format(resource)
    if fmt in TABULAR_FORMATS:
        return True
    return _extension(resource.get("url") or "") in SUPPORTED_EXTENSIONS


def _safe_name(raw: object, fallback: str) -> str:
    name = re.sub(r"[^0-9A-Za-z_]+", "_", str(raw or "").strip().lower())
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = fallback
    if name[0].isdigit():
        name = f"col_{name}"
    return name


def _dedupe(names: Iterable[object]) -> list[str]:
    used: set[str] = set()
    out: list[str] = []
    for i, raw in enumerate(names):
        base = _safe_name(raw, f"col_{i + 1}")
        candidate = base
        n = 1
        while candidate in used or candidate in BASE_COLUMNS:
            n += 1
            candidate = f"{base}_{n}"
        used.add(candidate)
        out.append(candidate)
    return out


def _stringify(value: object) -> str | None:
    if pd.isna(value):
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=True, sort_keys=True)
    text = str(value).strip()
    return text or None


def _rows_from_frame(frame: pd.DataFrame, *, sheet_name: str | None) -> list[dict]:
    if frame.empty:
        return []
    frame = frame.dropna(how="all")
    if frame.empty:
        return []
    frame.columns = _dedupe(frame.columns)
    rows: list[dict] = []
    for row_number, record in enumerate(frame.to_dict(orient="records"), start=1):
        row = {col: _stringify(value) for col, value in record.items()}
        if any(value is not None for value in row.values()):
            row["source_row_number"] = str(row_number)
            row["sheet_name"] = sheet_name
            rows.append(row)
    return rows


def _read_csv(content: bytes) -> list[dict]:
    frame = pd.read_csv(
        io.BytesIO(content),
        dtype=str,
        keep_default_na=False,
        na_values=[],
        encoding_errors="replace",
    )
    return _rows_from_frame(frame, sheet_name=None)


def _read_excel(content: bytes) -> list[dict]:
    workbook = pd.read_excel(
        io.BytesIO(content),
        sheet_name=None,
        dtype=str,
        keep_default_na=False,
    )
    rows: list[dict] = []
    for sheet_name, frame in workbook.items():
        rows.extend(_rows_from_frame(frame, sheet_name=str(sheet_name)))
    return rows


def _read_json(content: bytes) -> list[dict]:
    data = json.loads(content.decode("utf-8-sig"))
    if isinstance(data, dict):
        for key in ("result", "results", "data", "records", "rows"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list):
        data = [data]
    frame = pd.json_normalize(data, sep="_")
    return _rows_from_frame(frame, sheet_name=None)


def _read_tabular(content: bytes, name: str) -> list[dict]:
    ext = _extension(name)
    if ext == ".csv":
        return _read_csv(content)
    if ext in {".xls", ".xlsx"}:
        return _read_excel(content)
    if ext == ".json":
        return _read_json(content)
    return []


def _read_zip(content: bytes) -> list[dict]:
    rows: list[dict] = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for member in archive.infolist():
            if member.is_dir() or _extension(member.filename) not in SUPPORTED_EXTENSIONS:
                continue
            member_rows = _read_tabular(archive.read(member), member.filename)
            for row in member_rows:
                row["member_path"] = member.filename
            rows.extend(member_rows)
    return rows


def _resource_rows(resource: dict) -> list[dict]:
    url = resource.get("url")
    if not url:
        return []
    content = _download(url)
    fmt = _resource_format(resource)
    if fmt == "zip" or _extension(url) == ".zip":
        return _read_zip(content)
    return _read_tabular(content, url)


def _metadata_row(status: str, message: str) -> dict:
    return {
        "_subsets_status": status,
        "_subsets_message": message,
    }


def _table_from_rows(rows: list[dict]) -> pa.Table:
    normalized = []
    for row in rows:
        data = {
            key: value
            for key, value in row.items()
            if key not in BASE_COLUMNS and value is not None
        }
        normalized.append(
            {
                **{col: row.get(col) for col in BASE_COLUMNS if col != "data_json"},
                "data_json": json.dumps(data, ensure_ascii=True, sort_keys=True),
            }
        )
    schema = pa.schema([(col, pa.string()) for col in BASE_COLUMNS])
    return pa.Table.from_pylist(normalized, schema=schema)


def fetch_one(node_id: str) -> None:
    entity_id = node_id[len(PREFIX):]
    package = _api("package_show", id=entity_id)
    resources = [
        resource
        for resource in package.get("resources") or []
        if _is_supported_resource(resource)
    ]
    if not resources:
        raise RuntimeError(f"{entity_id}: no supported tabular resources")

    rows: list[dict] = []
    for resource in resources:
        try:
            resource_rows = _resource_rows(resource)
        except Exception as exc:
            resource_rows = [
                _metadata_row("resource_error", f"{type(exc).__name__}: {exc}")
            ]
        if not resource_rows:
            resource_rows = [
                _metadata_row(
                    "metadata_only",
                    "supported resource contained no CSV/XLS/XLSX/JSON rows",
                )
            ]
        for row in resource_rows:
            row.update(
                {
                    "package_id": str(package.get("name") or entity_id),
                    "package_title": str(package.get("title") or ""),
                    "resource_id": str(resource.get("id") or ""),
                    "resource_name": str(resource.get("name") or ""),
                    "resource_format": _resource_format(resource),
                    "resource_url": str(resource.get("url") or ""),
                    "member_path": row.get("member_path"),
                    "sheet_name": row.get("sheet_name"),
                    "source_row_number": row.get("source_row_number"),
                }
            )
        rows.extend(resource_rows)

    if not rows:
        rows = [
            {
                **_metadata_row("metadata_only", "package has no supported resources"),
                "package_id": str(package.get("name") or entity_id),
                "package_title": str(package.get("title") or ""),
            }
        ]
    save_raw_parquet(_table_from_rows(rows), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
