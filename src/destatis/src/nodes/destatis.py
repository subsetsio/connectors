"""Destatis (GENESIS-Online) connector.

One published subset per German official *statistic* (EVAS code). A statistic is
a survey/domain (population, foreign trade, consumer prices, ...); its data lives
in many GENESIS *tables* (multidimensional cubes). We publish one long/tidy Delta
table per statistic that unions all of that statistic's tables into a single
cell-per-row representation.

Access mechanism
----------------
Research's chosen mechanism is the token-gated genesisWS/rest/2020 API, but that
requires a (free) registered account whose credentials are not available in this
environment. The GENESIS web frontend ships an *anonymous* backend at
`genesis.destatis.de/genesis/api/rest/` — the same surface the public web UI
browses without a login — which exposes the identical catalogue and data:

  * GET /statistics/{code}/tables   -> list of tables belonging to a statistic
  * GET /tables/{id}/data           -> the table's full data as JSON-stat 2.0

The anonymous data endpoint was verified to return *complete* tables (no value
limit / truncation observed up to ~485k cells), so no per-table partitioning is
needed. This is the public-web-UI catalogue path collect already used.

Fetch shape: stateless full re-pull. The whole corpus re-downloads each run and
overwrites; revisions and late corrections are picked up for free. JSON-stat
cells are streamed to disk per statistic (ndjson.gz) so memory stays bounded even
for statistics with hundreds of large tables.

Raw format: zstd parquet — one row per data cell, written through a declared
schema. Cells across a statistic's tables have heterogeneous dimension sets, so
the classifying dimensions are serialized into a single JSON-string column
(`dims`) rather than fanned into drifting typed columns. Everything else is a
scalar.

`time` keeps GENESIS's own period label verbatim (mixed shapes: "2024",
"2024-12-31", "2020-05P1M"); `year` is the 4-digit calendar year parsed off the
front of it, as a typed integer, so freshness and range assertions have an
unambiguous column to bind to.
"""

from __future__ import annotations

import json
import re

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

_BASE = "https://genesis.destatis.de/genesis/api/rest"

# Explicit, stable scalar schema — one row per JSON-stat cell. Declared up front
# so every batch conforms and types never drift across statistics: `time` stays
# VARCHAR (GENESIS mixes ISO dates and bare years across a statistic's tables, so
# auto-detected DATE typing breaks; a string is unambiguous), `value` is DOUBLE,
# classifying dimensions are packed into the `dims` JSON string.
_SCHEMA = pa.schema([
    ("statistic_code", pa.string()),
    ("table_code", pa.string()),
    ("table_name", pa.string()),
    ("time", pa.string()),
    ("year", pa.int32()),
    ("measure_code", pa.string()),
    ("dims", pa.string()),
    ("value", pa.float64()),
    ("status", pa.string()),
])

# Flush accumulated cells to a Parquet row group at this many rows, bounding
# peak memory for statistics with hundreds of large tables.
_BATCH_ROWS = 100_000

# Time dimensions in GENESIS are anchored on a 4-digit year, optionally with a
# start month / day and/or an ISO-8601 period designator marking the interval:
#   year         "2024"          (JAHR)
#   date         "2024-12-31"    (STAG / Stichtag)
#   school year  "2001-P1Y"      (SLJAHR)
#   month        "2020-05P1M"    (SMONAT)
#   semester     "1999-10P6M"    (SEMEST)
# Region/classification codes are non-numeric (GES, NAT, WZ08-011) or wider than
# four leading digits (KREISE "01001"), so this pattern cleanly isolates the time
# axis without swallowing them.
_TIME_RE = re.compile(
    r"^\d{4}(-(\d{2}(-\d{2})?(P\d+[YMWD])?|P\d+[YMWD]))?$"
)

# The two pseudo-dimensions JSON-stat always carries: the (constant) statistic
# axis and the content/measure axis. Handled specially, never packed into dims.
_PSEUDO_DIMS = ("statistic", "content")


@transient_retry()
def _get_json(path: str):
    resp = get(_BASE + path, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


def _en(localized) -> str:
    """English label from a {de, en, wiki} object, falling back to de."""
    if isinstance(localized, dict):
        return localized.get("en") or localized.get("de") or ""
    return localized or ""


def _year(time_val) -> int | None:
    """Calendar year off the front of a GENESIS period label.

    Every code on the time axis matched `_TIME_RE`, so it is anchored on exactly
    four leading digits; a cell with no time axis has none.
    """
    if not time_val:
        return None
    return int(time_val[:4])


def _unroll(dataset: dict):
    """Unroll one JSON-stat 2.0 dataset into long cell rows.

    Yields (time, content_code, dims_dict, value, status) per cell. `value` is
    the flat row-major array indexed across the `id` dimension order (last
    dimension varies fastest).
    """
    ids = dataset.get("id") or []
    size = dataset.get("size") or []
    values = dataset.get("value") or []
    status = dataset.get("status") or []
    dims_meta = dataset.get("dimension") or {}

    if not ids or not size or len(ids) != len(size):
        return

    # Position -> category code for every dimension.
    dim_codes: dict[str, list] = {}
    for name in ids:
        index = (((dims_meta.get(name) or {}).get("category")) or {}).get("index")
        if isinstance(index, dict):
            arr = [None] * len(index)
            for code, pos in index.items():
                if isinstance(pos, int) and 0 <= pos < len(arr):
                    arr[pos] = code
        elif isinstance(index, list):
            arr = list(index)
        else:
            arr = []
        dim_codes[name] = arr

    # Row-major strides (last dimension fastest).
    strides = [1] * len(size)
    for i in range(len(size) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]

    # Identify the single time axis (first dimension whose every category code
    # looks like a year or ISO date), if any.
    time_dim = None
    for name in ids:
        if name in _PSEUDO_DIMS:
            continue
        codes = dim_codes.get(name) or []
        if codes and all(c and _TIME_RE.match(c) for c in codes):
            time_dim = name
            break

    n = len(values)
    for flat in range(n):
        time_val = None
        content = None
        dims: dict[str, str] = {}
        for d, name in enumerate(ids):
            arr = dim_codes[name]
            pos = (flat // strides[d]) % size[d]
            code = arr[pos] if pos < len(arr) else None
            if name == "content":
                content = code
            elif name == "statistic":
                continue
            elif name == time_dim:
                time_val = code
            else:
                dims[name] = code
        yield (
            time_val,
            content,
            dims,
            values[flat],
            status[flat] if flat < len(status) else None,
        )


def fetch_one(node_id: str) -> None:
    """Fetch every table of one statistic, unroll to long cells, stream ndjson.

    The runtime passes the spec id; the statistic's EVAS code is the suffix after
    the `destatis-` prefix.
    """
    statistic_code = node_id[len("destatis-"):]

    tables = _get_json(f"/statistics/{statistic_code}/tables")
    if not isinstance(tables, list):
        tables = []

    cols: dict[str, list] = {name: [] for name in _SCHEMA.names}
    pending = 0

    with raw_parquet_writer(node_id, _SCHEMA) as writer:

        def flush() -> None:
            nonlocal pending
            if not pending:
                return
            writer.write_batch(
                pa.record_batch([cols[name] for name in _SCHEMA.names], schema=_SCHEMA)
            )
            for name in cols:
                cols[name].clear()
            pending = 0

        for tbl in tables:
            table_code = tbl.get("code")
            if not table_code:
                continue
            table_name = _en(tbl.get("name"))
            try:
                payload = _get_json(f"/tables/{table_code}/data")
            except httpx.HTTPStatusError as exc:
                # Permanent per-table error (e.g. a 404 for a withdrawn table):
                # skip this table, keep the rest of the statistic.
                code = exc.response.status_code
                if code == 429 or 500 <= code < 600:
                    raise
                print(f"[destatis] skip table {table_code}: HTTP {code}")
                continue

            for dataset in payload.get("data") or []:
                for time_val, content, dims, value, status in _unroll(dataset):
                    cols["statistic_code"].append(statistic_code)
                    cols["table_code"].append(table_code)
                    cols["table_name"].append(table_name)
                    cols["time"].append(time_val)
                    cols["year"].append(_year(time_val))
                    cols["measure_code"].append(content)
                    cols["dims"].append(
                        json.dumps(dims, sort_keys=True, ensure_ascii=False)
                    )
                    cols["value"].append(
                        float(value) if isinstance(value, (int, float)) else None
                    )
                    cols["status"].append(status)
                    pending += 1
                    if pending >= _BATCH_ROWS:
                        flush()

        flush()


from constants import ENTITY_IDS


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"destatis-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# A generic passthrough transform per statistic. The graph requires every download
# node to have a transform consumer, so this comprehension covers all 331; the
# curated `src/transforms/<table>.sql` + `.yml` pairs override it per table (see
# orchestrator.load_nodes), and the transform stage is what authors those.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        temporal="time_label",
        sql=f'''
            SELECT
                statistic_code,
                table_code,
                table_name,
                "time"            AS time_label,
                measure_code,
                dims              AS dimensions,
                CAST(value AS DOUBLE) AS value,
                status
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
