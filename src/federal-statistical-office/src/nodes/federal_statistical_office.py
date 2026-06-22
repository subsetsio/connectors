"""Federal Statistical Office (Switzerland) — PxWeb cube connector.

Mechanism: the FSO PxWeb API (https://www.pxweb.bfs.admin.ch/api/v1/{lang}/...).
Each accepted entity is one PxWeb data cube. We GET the cube metadata (variables
+ value codes), then POST one or more json-stat2 selections to pull the data and
reshape it to a long ("tidy") table — one row per non-null cell, one column per
cube dimension (human labels), plus a numeric `value` and provenance columns.

Sizing: a single PxWeb selection is rejected (HTTP 403) somewhere above
~100k cells, so large cubes are fetched in rectangular chunks each kept under
SAFE_CELLS_PER_QUERY. Cubes whose full size exceeds MAX_CELLS were gated out at
rank (not feasibly extractable through this capped API), so every entity here
fetches in a bounded number of chunks. Raw is streamed to gzipped NDJSON so
memory stays bounded by one chunk regardless of cube size.

Shape: stateless full re-pull (the default). Each run re-fetches the whole cube
and overwrites; PxWeb exposes no usable incremental/`since` filter (selections
filter by value code, not modification date), so a stored watermark would be
meaningless. The maintain step (authored later) decides whether a node runs.
"""

import json
from itertools import product as iproduct

from subsets_utils import NodeSpec, SqlNodeSpec, get, post, raw_writer, transient_retry
from constants import ENTITY_IDS

SLUG = "federal-statistical-office"
PREFIX = f"{SLUG}-"
BASE = "https://www.pxweb.bfs.admin.ch/api/v1"
LANGS = ("en", "de", "fr", "it")  # prefer English labels, fall back to CH languages

# Observed empirically: ~71k cells/selection succeeds, ~142k returns 403.
# Stay well under the boundary; bigger chunks also mean bigger responses.
SAFE_CELLS_PER_QUERY = 50_000
# Cubes larger than this were gated out at rank; defended here so an unexpectedly
# grown cube fails loudly instead of launching tens of thousands of requests.
MAX_CELLS = 2_000_000

RESERVED = {"value", "cube_id", "updated"}


def _node_to_cube(node_id):
    """Recover the original cube id (with underscores) from a spec/asset id.

    The spec id is `f"{SLUG}-{cube_id.lower().replace('_','-')}"`; that mapping
    is lossy (cube ids also contain hyphens), so we resolve it against the known
    entity list rather than trying to invert the replace."""
    if not hasattr(_node_to_cube, "_map"):
        _node_to_cube._map = {
            f"{PREFIX}{c.replace('_', '-')}": c for c in ENTITY_IDS
        }
    return _node_to_cube._map[node_id]


@transient_retry()
def _get_meta(url):
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code in (400, 404):
        # "not published in this language" — not transient, signal to fall back.
        return None
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_jsonstat(url, query):
    resp = post(
        url,
        json={"query": query, "response": {"format": "json-stat2"}},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _fetch_meta(cube):
    """GET cube metadata, trying languages in preference order.

    A cube may be missing in some languages (400) AND a given language endpoint
    can throw a transient 5xx; in both cases we fall through to the next
    language and only give up once every language has been tried. This is what
    makes the fetch robust across a long full run where any single endpoint can
    blip a 500."""
    last = None
    for lang in LANGS:
        url = f"{BASE}/{lang}/{cube}/{cube}.px"
        try:
            meta = _get_meta(url)
        except Exception as e:  # transient 5xx exhausted retries on this language
            last = f"{url}: {type(e).__name__}: {e}"
            continue
        if isinstance(meta, dict) and meta.get("variables"):
            return lang, url, meta
        last = f"{url}: unavailable in this language"
    raise RuntimeError(f"cube {cube}: no metadata in any language (last: {last})")


def _sanitize(text, fallback):
    out = []
    for ch in (text or "").lower():
        out.append(ch if ch.isalnum() else "_")
    name = "".join(out).strip("_")
    while "__" in name:
        name = name.replace("__", "_")
    if not name or name[0].isdigit():
        name = f"d_{name}" if name else fallback
    return name


def _column_map(meta):
    """Map each variable code -> a unique, SQL-safe column name (from its label)."""
    used = set(RESERVED)
    colmap = {}
    for i, v in enumerate(meta["variables"]):
        code = v["code"]
        name = _sanitize(v.get("text") or code, f"dim_{i}")
        base = name
        n = 2
        while name in used:
            name = f"{base}_{n}"
            n += 1
        used.add(name)
        colmap[code] = name
    return colmap


def _plan_chunks(dim_codes, value_lists):
    """Yield rectangular selections {dim_code: [value_codes]} each <= SAFE cells.

    Picks the fewest large dimensions to iterate ('outer') so the product of the
    remaining 'inner' dims fits under the cap, then batches the smallest outer
    dim to pack each query close to the cap."""
    n = len(dim_codes)
    sizes = [len(v) for v in value_lists]
    total = 1
    for s in sizes:
        total *= s
    if total > MAX_CELLS:
        raise AssertionError(f"cube exceeds MAX_CELLS ({total} > {MAX_CELLS}); should have been gated")

    order = sorted(range(n), key=lambda i: -sizes[i])
    inner = set(range(n))
    outer = []
    prod = total
    k = 0
    while prod > SAFE_CELLS_PER_QUERY and k < n:
        i = order[k]
        outer.append(i)
        inner.discard(i)
        prod //= sizes[i]
        k += 1

    if not outer:
        yield {dim_codes[i]: value_lists[i] for i in range(n)}
        return

    inner_prod = 1
    for i in inner:
        inner_prod *= sizes[i]
    inner_prod = max(inner_prod, 1)

    batch_dim = outer[-1]
    head = outer[:-1]
    batch = max(1, SAFE_CELLS_PER_QUERY // inner_prod)
    head_ranges = [range(sizes[i]) for i in head]

    for combo in (iproduct(*head_ranges) if head else [()]):
        for start in range(0, sizes[batch_dim], batch):
            sel = {}
            for hpos, i in enumerate(head):
                sel[dim_codes[i]] = [value_lists[i][combo[hpos]]]
            sel[dim_codes[batch_dim]] = value_lists[batch_dim][start:start + batch]
            for i in inner:
                sel[dim_codes[i]] = value_lists[i]
            yield sel


def _reshape(js, colmap, cube, updated):
    """Yield one long row per non-null cell of a json-stat2 sub-cube."""
    ids = js["id"]
    sizes = js["size"]
    values = js["value"]
    dims = []
    for did in ids:
        cat = js["dimension"][did]["category"]
        index = cat["index"]
        inv = [None] * len(index)
        for code, pos in index.items():
            inv[pos] = code
        dims.append((colmap[did], inv, cat.get("label", {})))

    n = len(sizes)
    strides = [1] * n
    for i in range(n - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]

    for flat, v in enumerate(values):
        if v is None:
            continue
        row = {}
        rem = flat
        for i in range(n):
            pos = rem // strides[i]
            rem -= pos * strides[i]
            name, inv, labels = dims[i]
            code = inv[pos]
            row[name] = labels.get(code, code)
        row["value"] = v
        row["cube_id"] = cube
        row["updated"] = updated
        yield row


def fetch_one(node_id):
    asset = node_id  # the spec id IS the asset name
    cube = _node_to_cube(node_id)
    lang, url, meta = _fetch_meta(cube)
    colmap = _column_map(meta)
    dim_codes = [v["code"] for v in meta["variables"]]
    value_lists = [list(v["values"]) for v in meta["variables"]]
    updated = meta.get("updated")

    n_rows = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for sel in _plan_chunks(dim_codes, value_lists):
            query = [
                {"code": c, "selection": {"filter": "item", "values": sel[c]}}
                for c in dim_codes
            ]
            js = _post_jsonstat(url, query)
            for row in _reshape(js, colmap, cube, updated):
                f.write(json.dumps(row, ensure_ascii=False))
                f.write("\n")
                n_rows += 1
    print(f"  {asset}: wrote {n_rows} rows ({lang})")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
