"""Statistics Estonia (Statistikaamet) — PxWeb statistical database connector.

Mechanism: PxWeb v1 API at https://andmed.stat.ee/api/v1/en/stat (research-chosen).
Each rank-accepted entity is one PxWeb table (px id). For each we GET the table
metadata (variable codes), POST a json-stat2 query selecting every value of every
variable, and melt the resulting cube into a long table — one column per dimension
(named by the dimension's English label) plus a numeric ``value`` column. Schema is
per-table (different tables expose different dimensions), so raw is written as NDJSON
and each transform is a thin passthrough that publishes the table as-is.

Fetch shape: stateless full re-pull (shape 1). PxWeb tables are small-to-medium and
the API exposes no incremental/since filter, so every refresh re-pulls each table in
full and overwrites. Documented limits: 1000 calls / 10s, 1,000,000 values / call —
tables exceeding the value cap are fetched in chunks along their largest dimension.
"""

import math
import re
import unicodedata
import urllib.parse

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_PATHS

ROOT = "https://andmed.stat.ee/api/v1/en/stat"
SLUG = "statistics-estonia"
# Safety headroom under the documented 1,000,000-values-per-call cap.
CELL_LIMIT = 500_000
RETIRED_TABLES = {
    "rr306.px": "Upstream PxWeb table RR306.PX is no longer listed and its metadata endpoint returns HTTP 400.",
    "sk23.px": "Upstream PxWeb table SK23.px is no longer listed and its metadata endpoint returns HTTP 400.",
}


def _table_url(path: str) -> str:
    """Build the table URL, URL-encoding each tree path segment (some PxWeb
    folder ids contain spaces / non-ASCII)."""
    segs = [urllib.parse.quote(s, safe="") for s in path.split("/")]
    return ROOT + "/" + "/".join(segs)


@transient_retry()
def _get_meta(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_data(url: str, query: list) -> dict:
    resp = post(
        url,
        json={"query": query, "response": {"format": "json-stat2"}},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _slug(s: str) -> str:
    if not s:
        return "col"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return s or "col"


def _ordered_codes(category: dict) -> list:
    idx = category.get("index", {})
    if isinstance(idx, dict):
        return [c for c, _ in sorted(idx.items(), key=lambda kv: kv[1])]
    return list(idx)


def _colnames(dim_ids, dims) -> list:
    """One ASCII snake_case column per dimension, from its English label,
    deduped on collision."""
    names, seen = [], {}
    for did in dim_ids:
        nm = _slug(dims[did].get("label") or did)
        if nm == "value":  # never shadow the measure column
            nm = "value_dim"
        if nm in seen:
            seen[nm] += 1
            nm = f"{nm}_{seen[nm]}"
        else:
            seen[nm] = 0
        names.append(nm)
    return names


def _melt(data: dict) -> list:
    """Melt a json-stat2 dataset into long-format rows (row-major value array,
    last dimension varies fastest)."""
    dim_ids = data["id"]
    sizes = data["size"]
    dims = data["dimension"]
    values = data["value"]
    names = _colnames(dim_ids, dims)
    codes = [_ordered_codes(dims[d].get("category", {})) for d in dim_ids]
    labels = [dims[d].get("category", {}).get("label", {}) or {} for d in dim_ids]
    ndim = len(dim_ids)
    rows = []
    for i in range(len(values)):
        rem = i
        row = {}
        for d in range(ndim - 1, -1, -1):
            pos = rem % sizes[d]
            rem //= sizes[d]
            code = codes[d][pos]
            row[names[d]] = labels[d].get(code, code)
        v = values[i]
        row["value"] = float(v) if isinstance(v, (int, float)) else None
        rows.append(row)
    return rows


def _full_query(variables) -> list:
    return [
        {"code": v["code"], "selection": {"filter": "all", "values": ["*"]}}
        for v in variables
    ]


def _fetch_table(url: str, meta: dict) -> list:
    """Fetch the whole table, chunking along the largest dimension if the full
    selection would exceed the per-call value cap."""
    variables = meta["variables"]
    sizes = [max(1, len(v.get("values", []))) for v in variables]
    total = math.prod(sizes)

    if total <= CELL_LIMIT:
        return _melt(_post_data(url, _full_query(variables)))

    # Chunk along the dimension with the most values. Prefer the time variable
    # so chunks are contiguous periods.
    chunk_idx = next(
        (i for i, v in enumerate(variables) if v.get("time")),
        max(range(len(variables)), key=lambda i: sizes[i]),
    )
    other = total // sizes[chunk_idx]
    per_chunk = max(1, CELL_LIMIT // max(1, other))
    chunk_var = variables[chunk_idx]
    chunk_values = chunk_var["values"]

    rows = []
    for start in range(0, len(chunk_values), per_chunk):
        subset = chunk_values[start:start + per_chunk]
        query = []
        for i, v in enumerate(variables):
            if i == chunk_idx:
                query.append({"code": v["code"],
                              "selection": {"filter": "item", "values": subset}})
            else:
                query.append({"code": v["code"],
                              "selection": {"filter": "all", "values": ["*"]}})
        rows.extend(_melt(_post_data(url, query)))
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_key = node_id[len(SLUG) + 1:]  # strip "statistics-estonia-"
    path = ENTITY_PATHS[entity_key]
    if entity_key in RETIRED_TABLES:
        save_raw_ndjson([{
            "source_path": path,
            "retired_upstream": True,
            "note": RETIRED_TABLES[entity_key],
        }], asset)
        return
    url = _table_url(path)
    meta = _get_meta(url)
    rows = _fetch_table(url, meta)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{key}", fn=fetch_one, kind="download")
    for key in ENTITY_PATHS
]
