"""Danmarks Nationalbank — StatBank tables via the api.statbank.dk v1 API.

Each of the ~107 'DN'-prefixed StatBank tables is one publishable subset. The
StatBank exposes them through the modern Statistics-Denmark JSON API:

  - GET  /v1/tableinfo/<id>  -> dimension variable codes (+ which is time)
  - POST /v1/data            -> the data, requested in 'BULK' format (no cell cap)

Fetch shape: **stateless full re-pull** (the default). Every refresh pulls each
table in its entirety and overwrites; no watermark is trusted, so revisions and
late corrections are picked up for free.

Why the data request is chunked: the BULK endpoint reliably 500s / drops the
connection (incomplete chunked read) when asked to stream a single
multi-hundred-MB response (several of these tables are 600MB-950MB as one
extract — DNSUBOH, DNVP2, DNVPDKF, DNVPDKR2). So instead of one POST with
Tid=["*"], we pull the table in slices kept to ~TARGET_ROWS rows each.

The slice size is set from *actual* row counts, not the dense cardinality
product: many tables are extremely sparse (e.g. DNVPDKR2's dense cross-product is
~100M cells, yet one month is only ~0.7M real rows in 158MB), so a dense estimate
either over-splits into hundreds of thousands of tiny requests or — worse —
under-splits because it can't see that a *single* period already blows past the
limit. We instead probe the most-recent (largest) period to learn rows/period,
then either pack several periods per request (small tables) or pull one period at
a time while splitting the widest non-time dimension into batches (giant tables).
Every fetch is additionally wrapped in a reactive splitter: if a slice still
drops after the transient retries, it is bisected along its widest axis and
retried, guaranteeing forward progress regardless of the size estimate.

Raw format: NDJSON (gzip). The tables are heterogeneous — each has its own
dimension list — and all cell fields are written as JSON strings (the StatBank
value field uses '..' for missing), so a fixed parquet schema would be wrong
here. The transform re-types the value column to DOUBLE.
"""

import json

from subsets_utils import (
    NodeSpec,
    get,
    get_client,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS

SLUG = "danmarks-nationalbank"
API = "https://api.statbank.dk/v1"

# Target *actual rows* per /v1/data request. Sized from a live probe (not the
# dense cardinality product). ~200k rows is a few tens of MB per response — well
# under the multi-hundred-MB single-shot extracts that make the server drop the
# connection, while keeping the request count sane for the giant sparse tables.
TARGET_ROWS = 200_000
# Safety ceiling on periods per slice, independent of the row estimate.
MAX_PERIODS_PER_CHUNK = 2_000
# Dense-product ceiling for an individual oversized-table request. The real
# output is sparse, but keeping the Cartesian box bounded prevents pathological
# single-period streams such as DNVPDKR2 from staying multi-hundred-MB wide.
DENSE_PRODUCT_TARGET = 200_000
# Max recursive bisections in the reactive splitter before giving up.
MAX_SPLIT_DEPTH = 32


def _table_id(node_id: str) -> str:
    """Recover the StatBank table id from the node/asset id."""
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


@transient_retry()
def _tableinfo(table_id: str) -> dict:
    resp = get(f"{API}/tableinfo/{table_id}", params={"format": "JSON"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _column_keys(header: str, time_codes: set) -> list:
    """Map BULK CSV header columns to JSON keys: value column -> 'value', the
    time dimension -> 'time', every other dimension -> its lowercased code."""
    keys = []
    for raw in header.split(";"):
        c = raw.strip()
        cu = c.upper()
        if cu == "INDHOLD":
            keys.append("value")
        elif cu in time_codes:
            keys.append("time")
        else:
            keys.append(c.lower())
    return keys


@transient_retry()
def _fetch_slice(body: dict, time_codes: set) -> list:
    """Fetch one slice as a list of record dicts. Bounded by TARGET_ROWS, so it
    fits comfortably in memory; retried cleanly as a whole on transient errors
    (no partial writes leak — the caller writes only on success)."""
    rows = []
    with get_client().stream("POST", f"{API}/data", json=body, timeout=(10.0, 600.0)) as resp:
        resp.raise_for_status()
        lines = resp.iter_lines()
        header = next(lines, None)
        if header is None:
            return rows
        keys = _column_keys(header, time_codes)
        ncols = len(keys)
        for line in lines:
            if not line:
                continue
            parts = line.split(";")
            if len(parts) != ncols:
                # Defensive: a stray embedded ';' would desync the row; skip it
                # rather than silently mis-key columns.
                continue
            rows.append({keys[i]: parts[i] for i in range(ncols)})
    return rows


def _emit_box(table_id: str, var_specs: list, time_codes: set, emit, depth: int = 0) -> None:
    """Fetch one box (explicit value lists on every dimension) and emit its rows.

    The reactive safety net: every dimension is passed as an explicit value list
    (never "*"), so if the request still drops after the transient retries, we
    bisect the widest axis and recurse on the halves — guaranteeing forward
    progress no matter how wrong the up-front size estimate was."""
    body = {"table": table_id, "lang": "en", "format": "BULK", "variables": var_specs}
    try:
        rows = _fetch_slice(body, time_codes)
    except Exception:
        widest = max(range(len(var_specs)), key=lambda i: len(var_specs[i]["values"]))
        if depth >= MAX_SPLIT_DEPTH or len(var_specs[widest]["values"]) < 2:
            raise
        vals = var_specs[widest]["values"]
        mid = len(vals) // 2
        for half in (vals[:mid], vals[mid:]):
            sub = [dict(s) for s in var_specs]
            sub[widest] = {"code": var_specs[widest]["code"], "values": half}
            _emit_box(table_id, sub, time_codes, emit, depth + 1)
        return
    emit(rows)


def _dense_product(var_specs: list) -> int:
    product = 1
    for spec in var_specs:
        product *= max(1, len(spec["values"]))
    return product


def _partition_specs(var_specs: list, target: int = DENSE_PRODUCT_TARGET) -> list:
    """Split non-time dimensions into bounded Cartesian boxes.

    The StatBank response is sparse, so this is not a row-count guarantee. It is
    still a useful upper bound on request breadth for giant tables whose single
    latest-period probe would otherwise stream for a long time before failing.
    """
    boxes = [[{"code": s["code"], "values": list(s["values"])} for s in var_specs]]
    out = []
    while boxes:
        box = boxes.pop()
        if _dense_product(box) <= target:
            out.append(box)
            continue
        widest = max(range(len(box)), key=lambda i: len(box[i]["values"]))
        vals = box[widest]["values"]
        if len(vals) < 2:
            out.append(box)
            continue
        mid = len(vals) // 2
        for half in (vals[:mid], vals[mid:]):
            sub = [dict(s) for s in box]
            sub[widest] = {"code": box[widest]["code"], "values": half}
            boxes.append(sub)
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table_id = _table_id(node_id)
    info = _tableinfo(table_id)
    variables = info["variables"]

    time_var = next((v for v in variables if v.get("time")), None)
    time_codes = {time_var["id"].upper()} if time_var else set()
    # Explicit value lists per non-time dimension (so any axis is bisectable).
    nt_specs = [
        {"code": v["id"], "values": [x["id"] for x in v["values"]]}
        for v in variables if not v.get("time")
    ]

    written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        def emit(rows):
            nonlocal written
            for rec in rows:
                f.write(json.dumps(rec, separators=(",", ":")))
                f.write("\n")
                written += 1

        if time_var is None:
            # No time dimension: a single full extract (these are small).
            _emit_box(table_id, nt_specs, time_codes, emit)
        else:
            time_code = time_var["id"]
            periods = [val["id"] for val in time_var["values"]]

            # Probe the most-recent (largest) period to learn actual rows/period.
            recent = periods[-1]
            before = written
            _emit_box(table_id, nt_specs + [{"code": time_code, "values": [recent]}],
                      time_codes, emit)
            rows_recent = max(1, written - before)
            remaining = periods[:-1]

            if rows_recent <= TARGET_ROWS:
                # Small enough to pack several periods into one request.
                per_chunk = min(MAX_PERIODS_PER_CHUNK, max(1, TARGET_ROWS // rows_recent))
                for i in range(0, len(remaining), per_chunk):
                    chunk = remaining[i:i + per_chunk]
                    _emit_box(table_id, nt_specs + [{"code": time_code, "values": chunk}],
                              time_codes, emit)
            else:
                # A single period already exceeds the target: pull one period at a
                # time and pre-partition the non-time Cartesian box. This keeps
                # wide sparse tables from spending an hour in one doomed stream.
                boxes = _partition_specs(nt_specs)
                for p in remaining:
                    for box in boxes:
                        specs = [dict(s) for s in box]
                        specs.append({"code": time_code, "values": [p]})
                        _emit_box(table_id, specs, time_codes, emit)

    if written == 0:
        # An active table that yields no rows means the BULK contract changed.
        raise AssertionError(f"{table_id}: BULK extract produced 0 data rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
