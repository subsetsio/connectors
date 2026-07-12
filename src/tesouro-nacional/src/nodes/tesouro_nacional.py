"""Tesouro Nacional CKAN bulk-resource connector.

Tesouro Transparente exposes a CKAN catalog where each accepted package has one
or more tabular resources. The node id maps 1:1 to a CKAN package slug; each run
resolves the package metadata fresh, downloads CSV/Excel resources, unpacks
CSV/Excel files from ZIP/GZ containers, and writes one NDJSON stream per package.
"""

from __future__ import annotations

import gzip
import io
import json
import re
import zipfile
from collections.abc import Iterable, Iterator
from datetime import date, datetime
from pathlib import PurePosixPath
from typing import Any

import pandas as pd

from subsets_utils import NodeSpec, get, raw_writer

from constants import ENTITY_IDS


SLUG = "tesouro-nacional"
CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"
TABULAR_FORMATS = {"CSV", "XLS", "XLSX", "ZIP", "GZ", "TSV", "ODS"}
SKIP_FORMATS = {"PDF", "API", "HTML", "PNG", "RDATA", "VISUALIZACAO", "VISUALIZAÇÃO", ""}
MAX_SHEETS_PER_WORKBOOK = 50


def _entity_id_from_node(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id for {SLUG}: {node_id}")
    return node_id[len(prefix) :]


def _package_show(entity_id: str) -> dict[str, Any]:
    resp = get(f"{CKAN}/package_show", params={"id": entity_id}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {entity_id}: {payload}")
    return payload["result"]


def _resource_format(resource: dict[str, Any]) -> str:
    return str(resource.get("format") or "").strip().upper()


def _tabular_resources(package: dict[str, Any]) -> list[dict[str, Any]]:
    resources = []
    for resource in package.get("resources") or []:
        fmt = _resource_format(resource)
        url = str(resource.get("url") or "")
        if not url:
            continue
        if fmt in TABULAR_FORMATS:
            resources.append(resource)
    return resources


def _safe_column(value: object, fallback: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^0-9a-zA-Z_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    if not text:
        text = fallback
    if text[0].isdigit():
        text = f"col_{text}"
    return text[:120]


def _normalize_columns(columns: Iterable[object]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for idx, col in enumerate(columns, start=1):
        base = _safe_column(col, f"column_{idx}")
        count = seen.get(base, 0)
        seen[base] = count + 1
        out.append(base if count == 0 else f"{base}_{count + 1}")
    return out


def _clean_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if pd.isna(value):
        return None
    return str(value)


def _rows_from_frame(df: pd.DataFrame) -> Iterator[dict[str, Any]]:
    df = df.dropna(how="all")
    df.columns = _normalize_columns(df.columns)
    for record in df.to_dict(orient="records"):
        yield {key: _clean_value(value) for key, value in record.items()}


def _read_csv_bytes(content: bytes, *, sep: str | None = None) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "latin1"):
        try:
            return pd.read_csv(
                io.BytesIO(content),
                dtype=str,
                encoding=encoding,
                sep=sep,
                engine="python",
                on_bad_lines="warn",
            )
        except Exception as exc:  # try the next common Brazilian open-data encoding
            last_error = exc
    raise RuntimeError(f"could not parse CSV resource: {last_error}") from last_error


def _iter_csv(content: bytes, source_file: str | None = None) -> Iterator[tuple[str | None, dict[str, Any]]]:
    frame = _read_csv_bytes(content, sep="\t" if source_file and source_file.lower().endswith(".tsv") else None)
    for row in _rows_from_frame(frame):
        yield None, row


def _iter_excel(content: bytes, source_file: str | None = None) -> Iterator[tuple[str | None, dict[str, Any]]]:
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str, engine=None)
    if len(sheets) > MAX_SHEETS_PER_WORKBOOK:
        raise RuntimeError(f"{source_file or 'workbook'} has {len(sheets)} sheets; expected <= {MAX_SHEETS_PER_WORKBOOK}")
    for sheet_name, frame in sheets.items():
        for row in _rows_from_frame(frame):
            yield str(sheet_name), row


def _iter_zip(content: bytes) -> Iterator[tuple[str, str | None, dict[str, Any]]]:
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            name = member.filename
            lower = name.lower()
            data = archive.read(member)
            if lower.endswith((".csv", ".txt")):
                for sheet, row in _iter_csv(data, name):
                    yield name, sheet, row
            elif lower.endswith((".xlsx", ".xls", ".ods")):
                for sheet, row in _iter_excel(data, name):
                    yield name, sheet, row


def _iter_resource(resource: dict[str, Any], content: bytes) -> Iterator[tuple[str | None, str | None, dict[str, Any]]]:
    fmt = _resource_format(resource)
    url_path = PurePosixPath(str(resource.get("url") or "").split("?", 1)[0])
    filename = url_path.name
    lower = filename.lower()

    if fmt == "ZIP" or lower.endswith(".zip"):
        yield from _iter_zip(content)
    elif fmt == "GZ" or lower.endswith(".gz"):
        inner = filename[:-3] if lower.endswith(".gz") else filename
        for sheet, row in _iter_csv(gzip.decompress(content), inner):
            yield inner, sheet, row
    elif fmt in {"XLS", "XLSX", "ODS"} or lower.endswith((".xls", ".xlsx", ".ods")):
        for sheet, row in _iter_excel(content, filename):
            yield filename, sheet, row
    elif fmt == "TSV" or lower.endswith(".tsv"):
        for sheet, row in _iter_csv(content, filename):
            yield filename, sheet, row
    else:
        for sheet, row in _iter_csv(content, filename):
            yield filename, sheet, row


def _write_record(
    handle,
    *,
    node_id: str,
    entity_id: str,
    package: dict[str, Any],
    resource: dict[str, Any],
    source_file: str | None,
    sheet_name: str | None,
    source_row_number: int,
    data: dict[str, Any],
) -> None:
    record = {
        "source_node_id": node_id,
        "source_entity_id": entity_id,
        "source_package_id": package.get("id"),
        "source_package_name": package.get("name"),
        "source_package_title": package.get("title"),
        "source_package_modified": package.get("metadata_modified"),
        "source_resource_id": resource.get("id"),
        "source_resource_name": resource.get("name"),
        "source_resource_format": _resource_format(resource),
        "source_resource_url": resource.get("url"),
        "source_file": source_file,
        "source_sheet": sheet_name,
        "source_row_number": source_row_number,
    }
    record.update(data)
    handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    package = _package_show(entity_id)
    resources = _tabular_resources(package)
    if not resources:
        formats = sorted({_resource_format(r) for r in package.get("resources") or []})
        raise RuntimeError(f"{entity_id}: no tabular CKAN resources found; formats={formats}")

    rows_written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as handle:
        for resource in resources:
            url = str(resource.get("url") or "")
            resp = get(url, timeout=(10.0, 900.0))
            resp.raise_for_status()

            resource_rows = 0
            for source_file, sheet_name, row in _iter_resource(resource, resp.content):
                resource_rows += 1
                rows_written += 1
                _write_record(
                    handle,
                    node_id=node_id,
                    entity_id=entity_id,
                    package=package,
                    resource=resource,
                    source_file=source_file,
                    sheet_name=sheet_name,
                    source_row_number=resource_rows,
                    data=row,
                )

    if rows_written == 0:
        raise RuntimeError(f"{entity_id}: parsed tabular resources but wrote zero rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
