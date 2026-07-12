"""Philippine Statistics Authority — OpenSTAT (PXWeb v1) connector.

One raw asset per PXWeb leaf table. A catalog connector: every
download node shares one generic ``fetch_one`` that recovers the verbatim
PXWeb path from its spec id (via ``constants.ENTITY_PATHS``), pulls the whole
table, and writes tidy long-format rows (one row per cell: a column per
dimension carrying that dimension's value label, plus a numeric ``value``).

Fetch shape: **stateless full re-pull** (the default). PXWeb has no incremental
filter — each run re-fetches the whole table and overwrites. The only wrinkle is
the server's per-query cell ceiling: the published ``?config`` advertises
``maxValues=1000`` but the real ceiling is ~50k–100k cells (probed: 50,500 OK,
101,000 → HTTP 403). We chunk every table's full cartesian selection into blocks
of <= ``CHUNK_CELLS`` cells (binary-splitting the largest dimension) and stream
each block as a parquet row group, so even the largest cross-tabs (~1.9M cells)
stay memory-bounded. Rate limit: config says 10 calls / 10s; we self-throttle to
8/10s and rely on ``subsets_utils`` HTTP retries for transient failures.
"""

import fcntl
import json
import random
import re
import tempfile
import time
from pathlib import Path

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    post,
    raw_parquet_writer,
)
from constants import ENTITY_PATHS

SLUG = "philippine-statistics-authority"
BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"

# Real per-query cell ceiling is ~50k–100k (probed); 40k leaves safe margin.
CHUNK_CELLS = 40000

HTTP_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://openstat.psa.gov.ph",
    "Referer": "https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
}

# spec id -> verbatim case-sensitive PXWeb path. Spec ids are SLUG + entity id,
# and entity ids are already lower/dash slugs, so no further transform is needed.
SPEC_TO_PATH = {f"{SLUG}-{eid}": path for eid, path in ENTITY_PATHS.items()}


# --- rate limiting -----------------------------------------------------------
# PSA's PXWeb config advertises 10 calls / 10s. The runtime may execute many
# download nodes in parallel, so process-local throttles still overrun the
# source. Coordinate all worker processes on the same runner through one lock.
THROTTLE_PATH = Path(tempfile.gettempdir()) / "psa-openstat-throttle.json"
REQUEST_INTERVAL_S = 1.15
RATE_LIMIT_STATUSES = {403, 429}


def _tick() -> None:
    THROTTLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with THROTTLE_PATH.open("a+", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.seek(0)
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                state = {}
            last = float(state.get("last_request_at") or 0.0)
            wait = REQUEST_INTERVAL_S - (time.monotonic() - last)
            if wait > 0:
                time.sleep(wait)
            f.seek(0)
            f.truncate()
            json.dump({"last_request_at": time.monotonic()}, f)
            f.flush()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _request_json(method: str, url: str, *, payload: dict | None = None):
    for attempt in range(8):
        _tick()
        if method == "GET":
            r = get(url, timeout=(10.0, 120.0), headers=HTTP_HEADERS)
        else:
            r = post(url, json=payload, timeout=(10.0, 180.0),
                     headers=HTTP_HEADERS)
        if r.status_code not in RATE_LIMIT_STATUSES:
            r.raise_for_status()
            return r.json()
        sleep_s = min(300.0, 20.0 * (2 ** attempt)) + random.uniform(0, 5)
        time.sleep(sleep_s)
    r.raise_for_status()
    return r.json()


def _get_json(url: str):
    return _request_json("GET", url)


def _post_json(url: str, payload: dict):
    return _request_json("POST", url, payload=payload)


# --- schema / column helpers -------------------------------------------------
def _colname(code: str, used: set) -> str:
    """Sanitize a PXWeb variable code into a snake_case column name, unique
    within the table."""
    base = re.sub(r"[^a-z0-9]+", "_", code.lower()).strip("_") or "dim"
    name = base
    i = 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    return name


def _variables(meta: dict) -> list:
    """Return [(code, [value_codes], [labels])] for each variable, robust to
    PXWeb's `valueTexts` being absent."""
    out = []
    for v in meta.get("variables", []):
        codes = list(v.get("values") or [])
        texts = list(v.get("valueTexts") or [])
        if len(texts) != len(codes):
            texts = codes
        out.append((v["code"], codes, texts))
    return out


def _chunks(variables: list):
    """Partition the full cartesian selection into blocks of <= CHUNK_CELLS
    cells by binary-splitting the largest dimension. Yields lists of selected
    value-code lists, aligned to `variables` order."""
    init = [list(codes) for _, codes, _ in variables]
    stack = [init]
    while stack:
        sel = stack.pop()
        prod = 1
        for s in sel:
            prod *= max(len(s), 1)
        if prod <= CHUNK_CELLS or all(len(s) <= 1 for s in sel):
            yield sel
            continue
        i = max(range(len(sel)), key=lambda k: len(sel[k]))
        half = len(sel[i]) // 2 or 1
        a = list(sel)
        b = list(sel)
        a[i] = sel[i][:half]
        b[i] = sel[i][half:]
        stack.append(a)
        stack.append(b)


def _decode(js: dict, code_to_col: dict) -> list:
    """Decode a json-stat2 dataset response into long-format rows: one dict per
    cell with a column per dimension (its value label) and a numeric `value`."""
    dim_codes = js["id"]
    sizes = js["size"]
    # per-dimension: position -> human label
    pos_labels = []
    for d in dim_codes:
        cat = js["dimension"][d]["category"]
        index = cat["index"]
        labels = cat.get("label", {}) or {}
        if isinstance(index, dict):
            pos2code = {p: c for c, p in index.items()}
            codes_in_order = [pos2code[p] for p in range(len(pos2code))]
        else:  # list of codes in position order
            codes_in_order = list(index)
        pos_labels.append([labels.get(c, c) for c in codes_in_order])

    values = js.get("value", [])
    sparse = isinstance(values, dict)
    total = 1
    for s in sizes:
        total *= s

    cols = [code_to_col[c] for c in dim_codes]
    rows = []
    for flat in range(total):
        rem = flat
        coords = [0] * len(sizes)
        for k in range(len(sizes) - 1, -1, -1):
            coords[k] = rem % sizes[k]
            rem //= sizes[k]
        if sparse:
            raw = values.get(str(flat), values.get(flat))
        else:
            raw = values[flat] if flat < len(values) else None
        try:
            val = float(raw) if raw is not None else None
        except (TypeError, ValueError):
            val = None
        row = {cols[i]: pos_labels[i][coords[i]] for i in range(len(dim_codes))}
        row["value"] = val
        rows.append(row)
    return rows


# --- the generic fetch -------------------------------------------------------
def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    path = SPEC_TO_PATH[node_id]  # KeyError here = a coverage bug; let it raise
    url = BASE + path

    meta = _get_json(url)
    variables = _variables(meta)

    used = set()
    code_to_col = {code: _colname(code, used) for code, _, _ in variables}
    schema = pa.schema(
        [(code_to_col[code], pa.string()) for code, _, _ in variables]
        + [("value", pa.float64())]
    )

    with raw_parquet_writer(asset, schema) as w:
        for sel in _chunks(variables):
            query = {
                "query": [
                    {"code": variables[i][0],
                     "selection": {"filter": "item", "values": sel[i]}}
                    for i in range(len(variables))
                    if len(sel[i]) > 0
                ],
                "response": {"format": "json-stat2"},
            }
            js = _post_json(url, query)
            rows = _decode(js, code_to_col)
            if rows:
                w.write_table(pa.Table.from_pylist(rows, schema=schema))


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_PATHS
]
