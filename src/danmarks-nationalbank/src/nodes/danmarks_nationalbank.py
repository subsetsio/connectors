"""Danmarks Nationalbank — StatBank tables via the api.statbank.dk v1 API.

Each of the ~107 'DN'-prefixed StatBank tables is one publishable subset. The
StatBank exposes them through the modern Statistics-Denmark JSON API:

  - GET  /v1/tableinfo/<id>  -> dimension variable codes (+ which is time)
  - POST /v1/data            -> the data, requested in 'BULK' format (no cell cap)

Fetch shape: **stateless full re-pull** (the default). Every refresh pulls each
table in its entirety and overwrites; no watermark is trusted, so revisions and
late corrections are picked up for free.

Why the data request is chunked by time: the BULK endpoint reliably 500s / drops
the connection when asked to stream a single multi-hundred-MB response (several
of these tables are 600MB-950MB as one extract — DNSUBOH, DNVP2, DNVPDKF,
DNVPDKR2). So instead of one POST with Tid=["*"], we pull the table in slices of
consecutive time periods, sized adaptively from the table's dimension
cardinalities so each response stays ~TARGET_CELLS small, and stream every slice
into the same gzip NDJSON asset. The non-time dimensions are always pulled in
full ("*") within each slice.

Raw format: NDJSON (gzip). The tables are heterogeneous — each has its own
dimension list — and all cell fields are written as JSON strings (the StatBank
value field uses '..' for missing), so a fixed parquet schema would be wrong
here. The transform re-types the value column to DOUBLE.
"""

import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS

SLUG = "danmarks-nationalbank"
API = "https://api.statbank.dk/v1"

# Target cells per /v1/data request. Kept well under the giant single-shot
# responses that make the server 500; an over/under estimate of a few × still
# lands far below the failing multi-million-cell extracts.
TARGET_CELLS = 250_000
# Safety ceiling on periods per slice, independent of the cardinality estimate.
MAX_PERIODS_PER_CHUNK = 2_000


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
    """Fetch one time-slice as a list of record dicts. Bounded by TARGET_CELLS,
    so it fits comfortably in memory; retried cleanly as a whole on transient
    errors (no partial writes leak — the caller writes only on success)."""
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


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table_id = _table_id(node_id)
    info = _tableinfo(table_id)
    variables = info["variables"]
    varcodes = [v["id"] for v in variables]

    time_var = next((v for v in variables if v.get("time")), None)
    time_codes = {time_var["id"].upper()} if time_var else set()

    written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        if time_var is None:
            # No time dimension: a single full extract (these are small).
            body = {
                "table": table_id, "lang": "en", "format": "BULK",
                "variables": [{"code": c, "values": ["*"]} for c in varcodes],
            }
            for rec in _fetch_slice(body, time_codes):
                f.write(json.dumps(rec, separators=(",", ":")))
                f.write("\n")
                written += 1
        else:
            time_code = time_var["id"]
            period_ids = [val["id"] for val in time_var["values"]]
            # Size each slice from the non-time cardinality so a slice's response
            # stays ~TARGET_CELLS regardless of how wide the table is.
            other_cells = 1
            for v in variables:
                if not v.get("time"):
                    other_cells *= max(1, len(v["values"]))
            per_chunk = max(1, TARGET_CELLS // max(1, other_cells))
            per_chunk = min(per_chunk, MAX_PERIODS_PER_CHUNK)
            non_time = [c for c in varcodes if c != time_code]

            for i in range(0, len(period_ids), per_chunk):
                chunk = period_ids[i:i + per_chunk]
                body = {
                    "table": table_id, "lang": "en", "format": "BULK",
                    "variables": (
                        [{"code": c, "values": ["*"]} for c in non_time]
                        + [{"code": time_code, "values": chunk}]
                    ),
                }
                for rec in _fetch_slice(body, time_codes):
                    f.write(json.dumps(rec, separators=(",", ":")))
                    f.write("\n")
                    written += 1

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


# One published Delta table per subset. Generic parse-and-type pass: keep every
# dimension column + time as-is (string), drop missing-value cells ('..') and any
# non-numeric, and cast the value column to DOUBLE. All raw fields are JSON
# strings, so the value column is reliably VARCHAR before the cast.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * EXCLUDE (value),
                   TRY_CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value <> '..'
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
