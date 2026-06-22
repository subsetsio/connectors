"""Danmarks Nationalbank — StatBank tables via the api.statbank.dk v1 API.

Each of the ~107 'DN'-prefixed StatBank tables is one publishable subset. The
StatBank exposes them through the modern Statistics-Denmark JSON API:

  - GET  /v1/tableinfo/<id>  -> dimension variable codes (+ which is time)
  - POST /v1/data            -> the data, requested in 'BULK' format (no cell cap)

Fetch shape: **stateless full re-pull** (the default). Every refresh pulls each
table in its entirety via one BULK POST with every variable selected as ["*"],
then overwrites. BULK is mandatory — the JSON/CSV formats are capped at 1,000,000
cells and several of these tables (DNVPU ~1.2M rows, DNVALD ~0.7M) blow past it.
Revisions and late corrections are picked up for free because no watermark is
trusted. The BULK response is streamed line-by-line into gzip NDJSON so process
memory stays bounded no matter how large the table is.

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


def _table_id(node_id: str) -> str:
    """Recover the StatBank table id from the node/asset id."""
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


@transient_retry()
def _tableinfo(table_id: str) -> dict:
    resp = get(f"{API}/tableinfo/{table_id}", params={"format": "JSON"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _stream_bulk(asset: str, table_id: str, body: dict, time_codes: set) -> None:
    """Stream a BULK extract into gzip NDJSON. Reopened (overwritten) on retry."""
    written = 0
    with get_client().stream("POST", f"{API}/data", json=body, timeout=(10.0, 600.0)) as resp:
        resp.raise_for_status()
        lines = resp.iter_lines()
        header = next(lines)
        cols = [c.strip() for c in header.split(";")]
        # Map each CSV column to a JSON key: the value column -> "value",
        # the time dimension -> "time", every other dimension -> its lowercased code.
        keys = []
        for c in cols:
            cu = c.upper()
            if cu == "INDHOLD":
                keys.append("value")
            elif cu in time_codes:
                keys.append("time")
            else:
                keys.append(c.lower())
        ncols = len(keys)
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
            for line in lines:
                if not line:
                    continue
                parts = line.split(";")
                if len(parts) != ncols:
                    # Defensive: a stray embedded ';' would desync the row; skip it
                    # rather than silently mis-key columns.
                    continue
                rec = {keys[i]: parts[i] for i in range(ncols)}
                f.write(json.dumps(rec, separators=(",", ":")))
                f.write("\n")
                written += 1
    if written == 0:
        # An active table that yields no rows means the BULK contract changed.
        raise AssertionError(f"{table_id}: BULK extract produced 0 data rows")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table_id = _table_id(node_id)
    info = _tableinfo(table_id)
    varcodes = [v["id"] for v in info["variables"]]
    time_codes = {v["id"].upper() for v in info["variables"] if v.get("time")}
    body = {
        "table": table_id,
        "lang": "en",
        "format": "BULK",
        "variables": [{"code": c, "values": ["*"]} for c in varcodes],
    }
    _stream_bulk(asset, table_id, body, time_codes)


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
