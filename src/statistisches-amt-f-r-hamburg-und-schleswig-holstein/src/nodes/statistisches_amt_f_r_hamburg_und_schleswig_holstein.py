from __future__ import annotations

import io
from datetime import date, datetime
from decimal import Decimal
from urllib.parse import urlparse

import pandas as pd
from subsets_utils import NodeSpec, get, save_raw_ndjson

from constants import ENTITY_IDS


SLUG = "statistisches-amt-f-r-hamburg-und-schleswig-holstein"
SPEC_PREFIX = f"{SLUG}-"
CKAN_ACTION = "https://opendata.schleswig-holstein.de/api/3/action"
TABULAR_FORMAT_PRIORITY = ("xlsx", "csv", "xls")


def _entity_id_from_asset(asset_id: str) -> str:
    if not asset_id.startswith(SPEC_PREFIX):
        raise ValueError(f"unexpected asset id {asset_id!r}")
    return asset_id[len(SPEC_PREFIX) :]


def _package_show(entity_id: str) -> dict:
    response = get(f"{CKAN_ACTION}/package_show", params={"id": entity_id}, timeout=60.0)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {entity_id}: {payload!r}")
    return payload["result"]


def _resource_format(resource: dict) -> str:
    fmt = (resource.get("format") or "").strip().lower()
    if fmt:
        return fmt
    path = urlparse(resource.get("url") or "").path.lower()
    if path.endswith(".xlsx"):
        return "xlsx"
    if path.endswith(".xls"):
        return "xls"
    if path.endswith(".csv"):
        return "csv"
    return ""


def _pick_resource(package: dict) -> dict:
    resources = package.get("resources") or []
    for wanted in TABULAR_FORMAT_PRIORITY:
        for resource in resources:
            if _resource_format(resource) == wanted and resource.get("url"):
                return resource
    formats = sorted({_resource_format(r) or "unknown" for r in resources})
    raise RuntimeError(f"no supported tabular resource for {package.get('name')}: {formats}")


def _clean_scalar(value) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    text = str(value).strip()
    return text or None


def _dataframe_cells(df: pd.DataFrame, *, sheet: str, package: dict, resource: dict):
    package_id = package.get("name") or package.get("id")
    resource_id = resource.get("id")
    resource_name = resource.get("name") or resource.get("description") or resource_id
    fmt = _resource_format(resource)
    for row_index, row in df.iterrows():
        for column_index, value in enumerate(row.tolist(), start=1):
            text = _clean_scalar(value)
            if text is None:
                continue
            yield {
                "package_id": package_id,
                "package_title": package.get("title"),
                "resource_id": resource_id,
                "resource_name": resource_name,
                "resource_format": fmt,
                "sheet_name": sheet,
                "row_number": int(row_index) + 1,
                "column_number": column_index,
                "value_text": text,
            }


def _read_csv_cells(content: bytes, *, package: dict, resource: dict) -> list[dict]:
    last_error = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(
                io.BytesIO(content),
                header=None,
                dtype=object,
                keep_default_na=False,
                sep=None,
                engine="python",
                encoding=encoding,
            )
            return list(_dataframe_cells(df, sheet="csv", package=package, resource=resource))
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"could not parse CSV resource {resource.get('id')}: {last_error}")


def _read_excel_cells(content: bytes, *, package: dict, resource: dict) -> list[dict]:
    fmt = _resource_format(resource)
    engine = "xlrd" if fmt == "xls" else "openpyxl"
    sheets = pd.read_excel(
        io.BytesIO(content),
        sheet_name=None,
        header=None,
        dtype=object,
        engine=engine,
    )
    rows = []
    for sheet_name, df in sheets.items():
        rows.extend(_dataframe_cells(df, sheet=str(sheet_name), package=package, resource=resource))
    return rows


def fetch_one(asset_id: str) -> None:
    entity_id = _entity_id_from_asset(asset_id)
    package = _package_show(entity_id)
    resource = _pick_resource(package)
    response = get(resource["url"], timeout=(20.0, 180.0))
    response.raise_for_status()
    fmt = _resource_format(resource)
    if fmt == "csv":
        rows = _read_csv_cells(response.content, package=package, resource=resource)
    elif fmt in {"xls", "xlsx"}:
        rows = _read_excel_cells(response.content, package=package, resource=resource)
    else:
        raise RuntimeError(f"unsupported selected resource format {fmt!r} for {entity_id}")
    if not rows:
        raise RuntimeError(f"parsed zero non-empty cells for {entity_id}")
    save_raw_ndjson(rows, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id.lower().replace('_', '-')}", fn=fetch_one)
    for entity_id in ENTITY_IDS
]
