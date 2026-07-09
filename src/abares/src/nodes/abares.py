"""ABARES connector — Australian Bureau of Agricultural and Resource Economics
and Sciences, via the national data.gov.au CKAN instance (organization 'abares').

Each accepted entity is one CKAN package. We publish one Delta table per package
from its primary tabular resource. The primary resource is fetched from CKAN's
**datastore** (`datastore_search`) when it is datastore-active — typed rows served
directly by data.gov.au — falling back to a CSV file download from data.gov.au's
own storage for upload-type CSV resources. We deliberately never touch the legacy
data.daff.gov.au warehouse (broken TLS cert, host unreliable); the rank step
demoted every package that depends solely on it.

Stateless full re-pull: each refresh re-fetches the whole resource and overwrites.
The resources are small (tens to ~40k rows), so there is no need for incremental
state, watermarks, or batching.
"""
import io
import csv
import re
from urllib.parse import urlparse

import pandas as pd

from subsets_utils import (
    NodeSpec,
    get,
    configure_http,
    save_raw_ndjson,
)
from constants import ENTITY_IDS

API = "https://data.gov.au/data/api/3/action"
DL = "https://data.gov.au/data/dataset"

# spec id -> CKAN package name. The spec id lowercases and hyphenates the entity
# id, which is lossy (- vs _), so we keep an explicit reverse map.
ID_BY_SPEC = {f"abares-{e.lower().replace('_', '-')}": e for e in ENTITY_IDS}

_TABULAR = {"csv", "tsv", "xls", "xlsx", "xlsm", "xlsb"}


def _is_tabular(fmt: str) -> bool:
    f = (fmt or "").lower().strip()
    return (
        f in _TABULAR
        or "excel" in f
        or "csv" in f
        or f.endswith(".xlsx")
        or f.endswith(".csv")
    )


def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(15.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(15.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _safe_key(key: str) -> str:
    """Delta-safe column name: lowercase snake_case, ASCII only.

    Delta Lake rejects spaces and a handful of punctuation in column names, and
    ABARES datastore field names carry en-dashes, newlines, and asterisks
    (e.g. 'VALUE *', '2011–12', '2016\\n Q2'). Normalise them."""
    k = str(key).strip().lower()
    k = k.replace("–", "-").replace("—", "-")  # en/em dash
    k = re.sub(r"[^0-9a-z]+", "_", k).strip("_")
    if not k:
        k = "col"
    if k[0].isdigit():
        k = "c_" + k
    return k


def _clean(records: list) -> list:
    """Drop CKAN internal columns and normalise keys to Delta-safe names,
    de-duplicating any collisions produced by normalisation."""
    cleaned = []
    for rec in records:
        row, seen = {}, {}
        for k, v in rec.items():
            if k in ("_id", "_full_text"):
                continue
            sk = _safe_key(k)
            if sk in seen:
                seen[sk] += 1
                sk = f"{sk}_{seen[sk]}"
            else:
                seen[sk] = 1
            row[sk] = v
        cleaned.append(row)
    return cleaned


def _fetch_datastore(resource_id: str) -> list:
    """Page the full resource out of CKAN's datastore."""
    out, offset, limit, total = [], 0, 10000, None
    while True:
        result = _get_json(
            f"{API}/datastore_search",
            {"resource_id": resource_id, "limit": limit, "offset": offset},
        )["result"]
        if total is None:
            total = result.get("total", 0)
        records = result.get("records", [])
        if not records:
            break
        out.extend(records)
        offset += len(records)
        if total and offset >= total:
            break
        if offset > 5_000_000:  # safety ceiling: raise, never silently truncate
            raise RuntimeError(f"{resource_id}: datastore paging exceeded 5M rows")
    return out


def _download_url(package_id: str, resource: dict) -> str:
    url = resource.get("url") or ""
    if "data.gov.au/data/dataset" in url:
        return url
    filename = url.rsplit("/", 1)[-1].split("?", 1)[0] or "data"
    return f"{DL}/{package_id}/resource/{resource['id']}/download/{filename}"


def _fetch_csv(package_id: str, resource: dict) -> list:
    """Download a CSV upload from data.gov.au storage and parse it."""
    text = _get_bytes(_download_url(package_id, resource)).decode(
        "utf-8-sig", errors="replace"
    )
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def _fetch_excel(package_id: str, resource: dict) -> list:
    """Download an Excel upload and flatten non-empty worksheet rows."""
    content = _get_bytes(_download_url(package_id, resource))
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, dtype=str)
    rows = []
    for sheet_name, frame in sheets.items():
        frame = frame.dropna(axis=0, how="all").dropna(axis=1, how="all")
        if frame.empty:
            continue
        frame = frame.where(pd.notna(frame), None)
        for row_number, row in enumerate(frame.to_dict(orient="records"), start=2):
            out = {"source_sheet": sheet_name, "source_row_number": row_number}
            out.update(row)
            rows.append(out)
    return rows


def _pick_resource(resources: list):
    """Choose the primary tabular resource: datastore-active first (typed rows,
    served by CKAN), then a CSV/Excel upload hosted on data.gov.au."""
    tabs = [r for r in resources if _is_tabular(r.get("format"))]
    for r in tabs:
        if r.get("datastore_active"):
            return "datastore", r
    for r in tabs:
        host = urlparse(r.get("url") or "").netloc
        fmt = (r.get("format") or "").lower()
        if "data.gov.au" in host and ("csv" in fmt or "xls" in fmt or "excel" in fmt):
            return "file", r
    raise RuntimeError("no datastore-active or data.gov.au-hosted tabular resource found")


def fetch_one(node_id: str) -> None:
    configure_http(
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
    )
    package = ID_BY_SPEC[node_id]
    pkg = _get_json(f"{API}/package_show", {"id": package})["result"]
    mode, resource = _pick_resource(pkg["resources"])
    if mode == "datastore":
        records = _fetch_datastore(resource["id"])
    elif "csv" in (resource.get("format") or "").lower():
        records = _fetch_csv(pkg["id"], resource)
    else:
        records = _fetch_excel(pkg["id"], resource)
    records = _clean(records)
    if not records:
        raise RuntimeError(f"{node_id}: resource returned 0 rows")
    save_raw_ndjson(records, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"abares-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
