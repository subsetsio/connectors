"""IRENA — International Renewable Energy Agency (IRENASTAT PxWeb v1).

Each published .px table has its own dimension list (a distinct schema), so each
is one publishable Delta table. We fetch via the PxWeb v1 JSON API at
https://pxweb.irena.org/api/v1/en/IRENASTAT.

Fetch strategy (stateless full re-pull):
  - The whole corpus is small and re-pulls in minutes; there is no incremental
    query parameter on PxWeb, so every run re-fetches each table in full.
  - Table ids embed the publication cycle (e.g. `Country_ELECCAP_2026_H1_v-PX 1.px`)
    and change every release, so we never hardcode them: each fetch walks the
    database (root -> folders -> tables), slugs every table id by stripping the
    cycle suffix, and matches the slug to the node's entity id.
  - PxWeb enforces maxCells=100000 per query, so an empty-query full-table POST
    403s for the larger Power tables. We chunk every table by its Year dimension
    (one POST per year code); per-year cell counts stay well under the cap for
    all seven tables.
  - Rate limit is maxCalls=10 per 10s; nodes run sequentially (DAG_PARALLELISM=1)
    and we throttle to 8 calls / 10s for headroom.

json-stat2 responses carry dimension category LABELS (country names, technology
names, year text), which is what we publish. We unfold the (possibly sparse)
value array into long rows and normalize dimension codes to snake_case columns.

License: IRENA terms permit non-commercial reuse with attribution; see
research/curation metadata for the full conditional license record.
"""

import re
import urllib.parse

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    get,
    post,
    save_raw_parquet,
)

ROOT = "https://pxweb.irena.org/api/v1/en/IRENASTAT"

# Map a node id (irena-<slug>) to the stable slug. The slug is derived from the
# table-id prefix with the changing cycle token removed (see _slug).
ENTITY_IDS = [
    "country-eleccap",
    "country-elecgen",
    "heatgen",
    "pubfin",
    "re-share",
    "region-eleccap",
    "region-elecgen",
]

# Dimension-code -> published column name. Codes carry slashes/spaces upstream;
# we normalize to clean snake_case so the SQL transforms reference stable names.
DIM_NAME_MAP = {
    "Country/area": "country",
    "Region/country/area": "region",
    "Region": "region",
    "Technology": "technology",
    "Grid connection": "grid_connection",
    "Data Type": "data_type",
    "Indicator": "indicator",
    "Year": "year",
}


# ----------------------------------------------------------------------------- transport


@sleep_and_retry
@limits(calls=8, period=10)  # ~80% of the documented 10 calls / 10s window
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@sleep_and_retry
@limits(calls=8, period=10)
def _post_json(url: str, body: dict):
    resp = post(url, json=body, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


# ----------------------------------------------------------------------------- helpers


def _slug(table_id: str) -> str:
    stem = table_id.rsplit(".px", 1)[0]
    stem = re.split(r"[_\- ]\d{4}", stem)[0]
    stem = stem.replace("_", "-").replace(" ", "-").lower()
    stem = re.sub(r"-+", "-", stem).strip("-")
    return stem


def _normalize_dim(code: str) -> str:
    if code in DIM_NAME_MAP:
        return DIM_NAME_MAP[code]
    return re.sub(r"[^a-z0-9]+", "_", code.lower()).strip("_")


def _discover() -> dict:
    """Walk the database; return {slug: (folder_name, table_id)}."""
    out: dict = {}
    folders = _get_json(ROOT)
    for folder in folders:
        if folder.get("type") != "l":
            continue
        fname = folder["id"]
        furl = f"{ROOT}/{urllib.parse.quote(fname)}"
        for tbl in _get_json(furl):
            if tbl.get("type") != "t":
                continue
            out[_slug(tbl["id"])] = (fname, tbl["id"])
    return out


def _table_url(folder: str, table_id: str) -> str:
    return f"{ROOT}/{urllib.parse.quote(folder)}/{urllib.parse.quote(table_id)}"


def _unfold_jsonstat(payload: dict) -> list[dict]:
    """Convert a JSON-stat 2.0 dataset into long-format rows keyed by dim code."""
    dimensions = payload["id"]
    sizes = payload["size"]
    values = payload["value"]
    dim_meta = payload["dimension"]

    cat_orders: list[list[tuple[str, str]]] = []
    for dim_id in dimensions:
        cat = dim_meta[dim_id]["category"]
        index = cat["index"]
        labels = cat.get("label", {})
        if isinstance(index, dict):
            ordered = sorted(index.items(), key=lambda kv: kv[1])
        else:
            ordered = [(code, i) for i, code in enumerate(index)]
        cat_orders.append([(code, labels.get(code, code)) for code, _ in ordered])

    strides = [1] * len(sizes)
    for i in range(len(sizes) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]

    if isinstance(values, dict):
        cells = ((int(k), v) for k, v in values.items())
    else:
        cells = enumerate(values)

    rows: list[dict] = []
    for linear, value in cells:
        if value is None:
            continue
        rem = linear
        row = {}
        for dim_idx, stride in enumerate(strides):
            idx = rem // stride
            rem -= idx * stride
            row[dimensions[dim_idx]] = cat_orders[dim_idx][idx][1]
        row["value"] = value
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------- fetch


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len("irena-"):]

    catalog = _discover()
    if slug not in catalog:
        raise RuntimeError(
            f"IRENA table for slug '{slug}' not found in current catalog "
            f"(available: {sorted(catalog)})"
        )
    folder, table_id = catalog[slug]
    url = _table_url(folder, table_id)

    meta = _get_json(url)
    variables = meta["variables"]
    dim_codes = [v["code"] for v in variables]
    year_var = next((v for v in variables if v["code"] == "Year"), None)
    if year_var is None:
        raise RuntimeError(f"IRENA table '{table_id}' has no Year dimension: {dim_codes}")

    # Chunk by year to stay under the 100k-cell server cap.
    rows: list[dict] = []
    for year_code in year_var["values"]:
        body = {
            "query": [
                {"code": "Year", "selection": {"filter": "item", "values": [year_code]}}
            ],
            "response": {"format": "json-stat2"},
        }
        payload = _post_json(url, body)
        rows.extend(_unfold_jsonstat(payload))

    if not rows:
        raise RuntimeError(f"IRENA table '{table_id}' returned no observations")

    # Explicit schema (stable per asset): every dimension is a string label,
    # Year is an int, the cell value is a double.
    fields = []
    for code in dim_codes:
        name = _normalize_dim(code)
        fields.append((name, pa.int32() if code == "Year" else pa.string()))
    fields.append(("value", pa.float64()))
    schema = pa.schema(fields)

    out_rows = []
    for r in rows:
        rec = {}
        for code in dim_codes:
            name = _normalize_dim(code)
            val = r[code]
            rec[name] = int(val) if code == "Year" else val
        rec["value"] = float(r["value"])
        out_rows.append(rec)

    table = pa.Table.from_pylist(out_rows, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"irena-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
