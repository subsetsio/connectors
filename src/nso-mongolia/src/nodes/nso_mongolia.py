"""NSO Mongolia — PxWeb v1 API (https://data.1212.mn/api/v1/en/NSO).

One download spec per accepted .px table (1160 total). Each table is fetched by:

1. GET the table's full path (NSO/<subject folders...>/<id>.px) for metadata:
   the ordered list of variables, each with its value codes + English
   valueTexts.
2. POST one or more JSON-stat2 queries selecting value codes. A table whose full
   cross-product would exceed the API's per-request caps (100k values per the
   terms of use; maxCells=1,000,000 / maxValues=3000 per ?config) is split by
   binary-halving the largest dimension until every block fits, then the blocks
   are concatenated.

The json-stat2 response is unrolled into long rows: one column per table
dimension (keyed by the dimension's English label, cell = the category's English
label) plus a numeric ``value`` and, when the source declares one, a ``unit``.
Null cells are dropped. Schemas differ table-to-table (and a value can be null),
so raw is written as NDJSON. PxWeb exposes no incremental filter — every run is a
full re-pull; revisions are picked up for free.
"""

import time
import urllib.parse
from itertools import product

from subsets_utils import NodeSpec, get, post, save_raw_ndjson
from constants import ENTITY_PATHS

BASE = "https://data.1212.mn/api/v1/en/NSO"

# Per-request caps. Terms of use: max 100,000 values per request (HTTP 403 when
# exceeded). ?config: maxCells=1,000,000, maxValues=3000 distinct values per
# variable selection. Stay under the tightest (the 100k terms cap).
CELL_LIMIT = 90_000
MAXVALUES = 3_000

# Politeness throttle between HTTP calls in this process (terms: <=1 rps per IP).
# subsets_utils.get/post already retry 429/5xx with backoff.
_SLEEP = 0.4

# node_id lower-cases + hyphenates the entity id; recover the exact id. The
# accepted union is verified collision-free under this mapping.
_NODE_TO_ENTITY = {
    f"nso-mongolia-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_PATHS
}


def _table_url(entity_id: str) -> str:
    parts = list(ENTITY_PATHS[entity_id]) + [entity_id + ".px"]
    return BASE + "/" + "/".join(urllib.parse.quote(p, safe="") for p in parts)


def _fetch_metadata(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _query(url: str, selection: dict) -> dict:
    """POST a json-stat2 query. `selection` maps var code -> list of value codes."""
    body = {
        "query": [
            {"code": code, "selection": {"filter": "item", "values": values}}
            for code, values in selection.items()
        ],
        "response": {"format": "json-stat2"},
    }
    resp = post(url, json=body, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _blocks(variables):
    """Yield selection dicts (var code -> value codes), each within the caps.

    Binary-splits the largest dimension until product(sizes) <= CELL_LIMIT and
    every per-variable selection <= MAXVALUES.
    """
    codes = {v["code"]: list(v["values"]) for v in variables}

    def cells(sel):
        n = 1
        for vals in sel.values():
            n *= len(vals)
        return n

    def fits(sel):
        return cells(sel) <= CELL_LIMIT and all(len(v) <= MAXVALUES for v in sel.values())

    stack = [codes]
    while stack:
        sel = stack.pop()
        if fits(sel):
            yield sel
            continue
        split_code = max(sel, key=lambda c: len(sel[c]))
        vals = sel[split_code]
        if len(vals) <= 1:
            yield sel  # cannot split further (should not happen given the caps)
            continue
        mid = len(vals) // 2
        for half in (vals[:mid], vals[mid:]):
            nxt = dict(sel)
            nxt[split_code] = half
            stack.append(nxt)


def _unit_lookup(dataset: dict):
    """Best-effort measure unit. Returns (varying_measure_code_or_None,
    {catcode: unit_base}). Handles an eliminated single-unit ContentsCode and a
    varying measure dimension. Never raises."""
    try:
        ids = set(dataset.get("id", []))
        for dim_code, dim in dataset.get("dimension", {}).items():
            units = (dim.get("category") or {}).get("unit")
            if not units:
                continue
            bases = {}
            for catcode, u in units.items():
                base = u.get("base") if isinstance(u, dict) else None
                if base is not None:
                    bases[catcode] = base
            if bases:
                return (dim_code if dim_code in ids else None), bases
    except Exception:
        pass
    return None, {}


def _rows_from_dataset(dataset: dict):
    """Unroll a json-stat2 dataset into long rows, dropping null cells."""
    ids = dataset["id"]
    dims = dataset["dimension"]

    # Column name per dimension (English label), de-duplicated.
    col_names, seen = {}, set()
    for code in ids:
        label = (dims[code].get("label") or code).strip() or code
        name, i = label, 2
        while name in seen:
            name = f"{label} ({code})"
            if name in seen:
                name = f"{label}_{i}"
                i += 1
        seen.add(name)
        col_names[code] = name

    # Ordered category (code, label) per dimension, sorted by json-stat index.
    ordered = {}
    for code in ids:
        cat = dims[code]["category"]
        index = cat.get("index", {})
        labels = cat.get("label", {})
        catcodes = sorted(index, key=lambda cc: index[cc])
        ordered[code] = [(cc, (labels.get(cc, cc) or cc).strip()) for cc in catcodes]

    measure_code, unit_bases = _unit_lookup(dataset)
    const_unit = None
    if measure_code is None and unit_bases:
        const_unit = next(iter(unit_bases.values()))

    values = dataset["value"]
    sparse = isinstance(values, dict)
    axes = [ordered[code] for code in ids]

    for flat, combo in enumerate(product(*axes)):
        v = values.get(str(flat)) if sparse else (values[flat] if flat < len(values) else None)
        if v is None:
            continue
        row = {col_names[code]: catlabel for code, (catcode, catlabel) in zip(ids, combo)}
        row["value"] = v
        if const_unit is not None:
            row["unit"] = const_unit
        elif measure_code is not None:
            for code, (catcode, _lbl) in zip(ids, combo):
                if code == measure_code:
                    row["unit"] = unit_bases.get(catcode)
                    break
        yield row


def fetch_one(node_id: str) -> None:
    entity_id = _NODE_TO_ENTITY.get(node_id) or node_id[len("nso-mongolia-"):]
    if entity_id not in ENTITY_PATHS:
        raise KeyError(f"no entity for node {node_id!r}")

    url = _table_url(entity_id)
    meta = _fetch_metadata(url)
    variables = meta.get("variables", [])
    if not variables:
        raise ValueError(f"{entity_id}: table metadata has no variables")

    rows = []
    for selection in _blocks(variables):
        time.sleep(_SLEEP)
        rows.extend(_rows_from_dataset(_query(url, selection)))

    if not rows:
        raise ValueError(f"{entity_id}: query returned no non-null rows")

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nso-mongolia-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_PATHS
]
