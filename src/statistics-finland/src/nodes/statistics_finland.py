"""Statistics Finland (StatFin) — PxWeb v1 catalog connector.

One download node per StatFin table (the rank-accepted entity union, listed in
``constants.ENTITY_PATHS``). Each node:

  1. GETs the table's PxWeb metadata (dimensions + value codes),
  2. POSTs a json-stat2 query selecting every value of every dimension,
     chunked so no single request exceeds the 100k-cell server cap, and
  3. expands the json-stat2 hypercube into tidy long-format rows — one row per
     cell, one column per dimension (English label), plus a numeric ``value``.

The matching transform publishes that tidy table 1:1.
"""

import re
import time

from subsets_utils import NodeSpec, SqlNodeSpec, get, post, save_raw_ndjson, transient_retry
from constants import ENTITY_PATHS

_BASE = "https://pxdata.stat.fi/PXWeb/api/v1/en"
_PREFIX = "statistics-finland-"
_CELL_LIMIT = 90000  # stay safely under PxWeb's 100,000-cell-per-query cap (403 over it)


@transient_retry(attempts=8, max_wait=90)
def _get_meta(url):
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()


@transient_retry(attempts=8, max_wait=90)
def _post_data(url, query):
    body = {"query": query, "response": {"format": "json-stat2"}}
    r = post(url, json=body, timeout=(10.0, 180.0))
    r.raise_for_status()
    return r.json()


def _sanitize(text, used):
    """Turn a dimension label into a unique snake_case column name."""
    name = re.sub(r"[^0-9a-z]+", "_", text.strip().lower()).strip("_") or "dim"
    if name == "value":  # reserve `value` for the numeric measure
        name = "value_dim"
    base, i = name, 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    return name


def _chunks(dims, limit):
    """Yield query selections (code -> [value codes]) each <= ``limit`` cells.

    ``dims`` is a list of (code, values) sorted descending by cardinality, so the
    largest dimension is split first; very large tables recurse onto further dims.
    """
    total = 1
    for _, v in dims:
        total *= len(v)
    if total <= limit:
        yield {c: list(v) for c, v in dims}
        return
    code0, vals0 = dims[0]
    rest = dims[1:]
    rest_total = 1
    for _, v in rest:
        rest_total *= len(v)
    if rest_total <= limit:
        step = max(1, limit // rest_total)
        for i in range(0, len(vals0), step):
            sel = {code0: vals0[i:i + step]}
            for c, v in rest:
                sel[c] = list(v)
            yield sel
    else:
        for val in vals0:
            for sub in _chunks(rest, limit):
                out = {code0: [val]}
                out.update(sub)
                yield out


def _expand(doc, colmap):
    """Expand a json-stat2 dataset doc into tidy row dicts."""
    ids = doc["id"]
    sizes = doc["size"]
    values = doc["value"]
    dim = doc["dimension"]
    # position -> code, and code -> label, per dimension
    pos2code = {}
    code2label = {}
    for c in ids:
        cat = dim[c]["category"]
        idx = cat["index"]
        if isinstance(idx, dict):
            arr = [None] * len(idx)
            for code, p in idx.items():
                arr[p] = code
        else:
            arr = list(idx)
        pos2code[c] = arr
        code2label[c] = cat.get("label", {})
    n = len(values)
    for k in range(n):
        v = values[k]
        if v is None:
            continue
        rem = k
        row = {}
        for i in range(len(ids) - 1, -1, -1):
            c = ids[i]
            p = rem % sizes[i]
            rem //= sizes[i]
            code = pos2code[c][p]
            row[colmap[c]] = code2label[c].get(code, code)
        row["value"] = v
        yield row


def fetch_one(node_id):
    asset = node_id
    entity = node_id[len(_PREFIX):] if node_id.startswith(_PREFIX) else node_id
    url = f"{_BASE}/{ENTITY_PATHS[entity]}"

    meta = _get_meta(url)
    variables = meta["variables"]
    # Stable column names from the English dimension labels.
    used = set()
    colmap = {v["code"]: _sanitize(v["text"], used) for v in variables}
    # Dimensions sorted descending by cardinality for chunking.
    dims = sorted(((v["code"], v["values"]) for v in variables),
                  key=lambda cv: len(cv[1]), reverse=True)

    def rows():
        first = True
        for sel in _chunks(dims, _CELL_LIMIT):
            if not first:
                time.sleep(0.3)  # be gentle: PxWeb caps ~30 queries / 10s
            first = False
            query = [{"code": code, "selection": {"filter": "item", "values": vals}}
                     for code, vals in sel.items()]
            doc = _post_data(url, query)
            yield from _expand(doc, colmap)

    save_raw_ndjson(rows(), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"statistics-finland-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_PATHS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
