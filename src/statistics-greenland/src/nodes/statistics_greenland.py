"""Statistics Greenland (Gronlands Statistik 'Statbank') connector.

Catalog connector over the PxWeb v1 API at https://bank.stat.gl/api/v1/en/Greenland/.
Each rank-accepted entity is one PxWeb statistical table (a multi-dimensional
time-series cube). For each table we GET its metadata (variables + value codes),
POST a full selection query (chunked to respect the API's 1,000,000-value-per-call
ceiling), and write one long-format raw row per non-null observation.

Strategy: stateless full re-pull (shape 1). PxWeb exposes no incremental/`since`
filter, so every refresh re-pulls each table in full and overwrites. Each table
fits comfortably in memory for all but the largest cubes, which we stream to
NDJSON batch-by-batch via the raw_writer context manager.

Raw shape is heterogeneous across tables (every table has its own dimension
codes), so raw is NDJSON: each row is a flat dict {<DIM_CODE>: <category label>,
..., "obs_value": float, "obs_time": <time label or null>}. DuckDB infers each
table's own column set on read, so the transform is a uniform `SELECT *`.
"""

import json

from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_PATHS, ENTITY_IDS

BASE = "https://bank.stat.gl/api/v1/en/Greenland/"
SLUG = "statistics-greenland"

# The only documented cap is 1,000,000 values per single call (no documented
# per-minute rate limit; not observed during probing). Stay well under the cell
# ceiling with headroom; PxWeb has no separate per-variable cap here, so keep
# that generous (the cell budget is the real constraint).
MAX_CELLS = 800_000
MAX_VALUES = 100_000


# ---- HTTP, rate-limited + retried -----------------------------------------

# No documented limit; a gentle self-pace keeps a 400+ node crawl polite. The
# DAG runs nodes sequentially by default, so this per-process limiter is
# effectively the global pace.
@sleep_and_retry
@limits(calls=50, period=10)
def _throttle() -> None:
    return None


@transient_retry()
def _get_json(url: str):
    _throttle()
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _post_json(url: str, query: dict):
    _throttle()
    resp = post(url, json=query, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


# ---- value resolution ------------------------------------------------------

def _resolve_values(url: str, variables):
    """Return {var_code: [value_codes...]} for every variable.

    Most variables inline their value codes in the table metadata. Any variable
    PxWeb omits the codes for (empty `values`) is discovered with a
    `filter:"all"` query on that one variable, pinning every other variable to a
    single value so the response stays small. The response's category index
    lists all codes in order.
    """
    resolved = {}
    empty = []
    for v in variables:
        vals = v.get("values") or []
        if vals:
            resolved[v["code"]] = list(vals)
        else:
            empty.append(v["code"])

    for target in empty:
        query = {"query": [], "response": {"format": "json-stat2"}}
        for v in variables:
            code = v["code"]
            if code == target:
                sel = {"filter": "all", "values": ["*"]}
            elif resolved.get(code):
                sel = {"filter": "item", "values": [resolved[code][0]]}
            else:
                # another uncountable variable -- grab any single value
                sel = {"filter": "top", "values": ["1"]}
            query["query"].append({"code": code, "selection": sel})
        js = _post_json(url, query)
        index = js["dimension"][target]["category"]["index"]
        if isinstance(index, dict):
            codes = [None] * len(index)
            for cval, pos in index.items():
                codes[pos] = cval
        else:
            codes = list(index)
        resolved[target] = codes
    return resolved


# ---- query planning: respect the value ceiling -----------------------------

def _plan_blocks(resolved):
    """Split the full selection (all values of every variable) into query blocks
    each <= MAX_CELLS cells and with no single variable selecting > MAX_VALUES
    values. Splits the largest offending variable's value list in half until
    every block is within limits. Returns a list of {code: [value_codes...]}.
    """
    full = {code: list(vals) for code, vals in resolved.items()}

    def cells(block):
        n = 1
        for vals in block.values():
            n *= max(1, len(vals))
        return n

    def ok(block):
        if cells(block) > MAX_CELLS:
            return False
        return all(len(vals) <= MAX_VALUES for vals in block.values())

    blocks = [full]
    out = []
    guard = 0
    while blocks:
        guard += 1
        if guard > 5_000_000:
            raise RuntimeError("query planner exceeded split guard -- table far larger than expected")
        b = blocks.pop()
        if ok(b):
            out.append(b)
            continue
        over = [c for c, vals in b.items() if len(vals) > MAX_VALUES]
        if over:
            split_code = max(over, key=lambda c: len(b[c]))
        else:
            split_code = max(b, key=lambda c: len(b[c]))
        vals = b[split_code]
        if len(vals) <= 1:
            others = [c for c in b if c != split_code and len(b[c]) > 1]
            if not others:
                out.append(b)
                continue
            split_code = max(others, key=lambda c: len(b[c]))
            vals = b[split_code]
        mid = len(vals) // 2
        left = dict(b)
        right = dict(b)
        left[split_code] = vals[:mid]
        right[split_code] = vals[mid:]
        blocks.append(left)
        blocks.append(right)
    return out


# ---- json-stat2 -> long rows ----------------------------------------------

def _iter_rows(js):
    """Yield one flat dict per cell of a json-stat2 dataset response.

    Columns are the variable codes (value = the category *label*), plus
    `obs_value` (float|None) and `obs_time` (the time dimension's label, or
    None). Cells with a null value are skipped -- PxWeb cubes are sparse.
    """
    order = js["id"]            # dimension codes in value-array order
    size = js["size"]
    dims = js["dimension"]
    values = js["value"]
    time_codes = set(js.get("role", {}).get("time", []) or [])

    pos_to_code = {}
    code_to_label = {}
    for code in order:
        cat = dims[code]["category"]
        index = cat["index"]
        labels = cat.get("label", {})
        if isinstance(index, dict):
            p2c = [None] * len(index)
            for cval, pos in index.items():
                p2c[pos] = cval
        else:
            p2c = list(index)
        pos_to_code[code] = p2c
        code_to_label[code] = labels

    ndim = len(order)
    strides = [1] * ndim
    for i in range(ndim - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]

    for flat, val in enumerate(values):
        if val is None:
            continue
        row = {}
        time_label = None
        rem = flat
        for i, code in enumerate(order):
            pos = (rem // strides[i]) % size[i]
            cval = pos_to_code[code][pos]
            label = code_to_label[code].get(cval, cval)
            row[code] = label
            if code in time_codes:
                time_label = label
        row["obs_value"] = float(val) if not isinstance(val, str) else None
        row["obs_time"] = time_label
        yield row


# ---- fetch -----------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id
    stem = node_id[len(SLUG) + 1:]          # strip "statistics-greenland-"
    px_path = ENTITY_PATHS[stem]
    url = BASE + px_path

    meta = _get_json(url)
    variables = meta["variables"]
    resolved = _resolve_values(url, variables)
    blocks = _plan_blocks(resolved)

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for block in blocks:
            query = {
                "query": [
                    {"code": code, "selection": {"filter": "item", "values": vals}}
                    for code, vals in block.items()
                ],
                "response": {"format": "json-stat2"},
            }
            js = _post_json(url, query)
            for row in _iter_rows(js):
                fh.write(json.dumps(row, ensure_ascii=False))
                fh.write("\n")


# ---- specs -----------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{stem}", fn=fetch_one, kind="download")
    for stem in ENTITY_IDS
]

# Uniform transform: every table's raw NDJSON carries its own dimension columns
# plus obs_value/obs_time. Publish the natural per-table columns, typing the
# value and dropping the (already-excluded) null cells defensively.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (CAST(obs_value AS DOUBLE) AS obs_value)
            FROM "{s.id}"
            WHERE obs_value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
