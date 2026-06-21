"""NSO Mongolia connector — PxWeb v1 API at https://data.1212.mn/api/v1/en/NSO.

Catalog connector: one download node per rank-accepted .px table (1101 total).
Each table has its own dimension list, so raw is written as NDJSON (heterogeneous
columns per table) and published 1:1 by a generic SELECT-* transform.

Fetch strategy (stateless full re-pull — PxWeb exposes no incremental filter):
  1. GET the table's metadata (variables: code/text/values/valueTexts).
  2. POST a json-stat2 query selecting all values for every variable. When the
     full cross-product would exceed the documented caps (maxCells=1_000_000,
     maxValues=3000), chunk along the largest dimension and concatenate.
  3. Flatten json-stat2 (flat row-major `value` array over `id`/`size`) into one
     row per cell: a column per dimension (English valueText) plus a `value`
     measure. Null cells are dropped.

Source caps (from ?config): maxValues=3000, maxCells=1_000_000, maxCalls=1000 per
100s. Re-fetch is full every run; revisions are picked up for free.
"""

import itertools
import urllib.parse

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import CATALOG

BASE = "https://data.1212.mn/api/v1/en/NSO"

# Stay safely under the documented PxWeb caps (maxCells=1e6, maxValues=3000).
CELL_CAP = 800_000
VAL_CAP = 2_800
MEASURE = "value"


def _table_url(node_id: str) -> str:
    rec = CATALOG[node_id]
    segs = [urllib.parse.quote(s, safe="") for s in rec["path"]]
    segs.append(urllib.parse.quote(rec["file"], safe=""))
    return BASE + "/" + "/".join(segs)


@transient_retry(attempts=8, min_wait=2, max_wait=60)
def _get_meta(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry(attempts=8, min_wait=2, max_wait=60)
def _post_query(url: str, body: dict) -> dict:
    resp = post(url, json=body, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _col_names(variables):
    """English column name per variable, de-duplicated; never collides with the
    measure column."""
    names = []
    seen = {}
    for v in variables:
        raw = (v.get("text") or v["code"]).strip() or v["code"]
        name = raw
        if name == MEASURE:
            name = f"{raw}_dim"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        names.append(name)
    return names


def _flatten_jsonstat2(js, col_names):
    """Expand a json-stat2 dataset into row dicts. `value` is row-major over the
    dimensions listed in `id`; itertools.product yields that exact order."""
    dim_codes = js["id"]
    sizes = js["size"]
    value = js["value"]

    # position -> label for each dimension, in declared order
    ordered_labels = []
    for code in dim_codes:
        dim = js["dimension"][code]
        index = dim["category"]["index"]
        labels = dim["category"]["label"]
        if isinstance(index, dict):
            pos_to_code = {pos: c for c, pos in index.items()}
            seq = [labels.get(pos_to_code[p], pos_to_code[p]) for p in range(len(pos_to_code))]
        else:  # index is an ordered list of category codes
            seq = [labels.get(c, c) for c in index]
        ordered_labels.append([str(s).strip() for s in seq])

    sparse = isinstance(value, dict)
    rows = []
    for flat, combo in enumerate(itertools.product(*[range(s) for s in sizes])):
        v = value.get(str(flat)) if sparse else value[flat]
        if v is None:
            continue
        row = {col_names[k]: ordered_labels[k][combo[k]] for k in range(len(dim_codes))}
        row[MEASURE] = v
        rows.append(row)
    return rows


def _chunk_plan(variables):
    """Return a list of per-request `query` bodies. One request when the full
    table fits the caps; otherwise split the largest dimension into slices that
    keep both cell-count and value-count under the caps."""
    sizes = [len(v["values"]) for v in variables]
    total = 1
    for s in sizes:
        total *= s
    sel_all = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}} for v in variables]

    if total <= CELL_CAP and max(sizes) <= VAL_CAP and sum(sizes) <= VAL_CAP:
        return [sel_all]

    # Chunk along the largest dimension.
    big = max(range(len(sizes)), key=lambda i: sizes[i])
    others_product = 1
    others_sum = 0
    for i, s in enumerate(sizes):
        if i == big:
            continue
        others_product *= s
        others_sum += s
    by_cells = max(1, CELL_CAP // max(1, others_product))
    by_values = max(1, VAL_CAP - others_sum)
    chunk = max(1, min(by_cells, by_values, VAL_CAP))

    big_codes = variables[big]["values"]
    plans = []
    for start in range(0, len(big_codes), chunk):
        slice_codes = big_codes[start:start + chunk]
        query = []
        for i, v in enumerate(variables):
            if i == big:
                query.append({"code": v["code"], "selection": {"filter": "item", "values": slice_codes}})
            else:
                query.append({"code": v["code"], "selection": {"filter": "all", "values": ["*"]}})
        plans.append(query)
    return plans


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    url = _table_url(node_id)

    meta = _get_meta(url)
    variables = meta["variables"]
    col_names = _col_names(variables)

    rows = []
    for query in _chunk_plan(variables):
        js = _post_query(url, {"query": query, "response": {"format": "json-stat2"}})
        rows.extend(_flatten_jsonstat2(js, col_names))

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in CATALOG
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE "{MEASURE}" IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
