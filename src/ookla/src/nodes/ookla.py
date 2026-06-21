"""Ookla Speedtest open data — global network performance tiles.

Source: the public, anonymous S3 bucket `ookla-open-data` (us-west-2), reachable
over plain HTTPS at https://ookla-open-data.s3.us-west-2.amazonaws.com/. One
immutable parquet per (type, year, quarter) partition holds global zoom-16
web-mercator tile aggregates of fixed-broadband and mobile-cellular network
performance, published quarterly from 2019 Q1 onward.

Shape: the collect catalog is a single homogeneous corpus (`performance`); the
type/year/quarter dimensions are column values, not separate tables. The corpus
is large (~60 partitions, ~5M rows each, ~300M rows total), so this uses the
batched firehose shape: ONE download spec whose fetch fn discovers every
partition from S3 and writes each as its own batch raw asset
(`ookla-performance-<type>-<year>-q<quarter>`), advancing a per-partition
watermark in state after each successful write. The transform's dep view
glob-unions every batch file automatically.

Each source parquet's bulky `tile` WKT polygon is dropped on read: the 16-char
`quadkey` (a Bing-Maps quadkey at zoom 16) already uniquely and deterministically
identifies the tile, so the polygon is redundant and would multiply published
storage many-fold. The `tile_x`/`tile_y` centroid (present from Q3 2023) and the
loaded-latency columns (present from Q4 2022) are carried through where the source
provides them and null otherwise.
"""

import io
import tempfile
import xml.etree.ElementTree as ET

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
    load_state,
    save_state,
)

STATE_VERSION = 1

BASE = "https://ookla-open-data.s3.us-west-2.amazonaws.com"
ROOT_PREFIX = "parquet/performance/"
_S3NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"

# Canonical raw schema. Optional columns (loaded latency, centroid) are nullable
# because early quarters do not carry them; the WKT `tile` polygon is dropped.
RAW_SCHEMA = pa.schema([
    ("quadkey", pa.string()),
    ("connection_type", pa.string()),
    ("year", pa.int32()),
    ("quarter", pa.int32()),
    ("avg_d_kbps", pa.int64()),
    ("avg_u_kbps", pa.int64()),
    ("avg_lat_ms", pa.int64()),
    ("avg_lat_down_ms", pa.int64()),
    ("avg_lat_up_ms", pa.int64()),
    ("tests", pa.int64()),
    ("devices", pa.int64()),
    ("tile_x", pa.float64()),
    ("tile_y", pa.float64()),
])

# Columns read from the source file (everything except the dropped `tile` WKT).
_SOURCE_COLS = [
    "quadkey",
    "avg_d_kbps",
    "avg_u_kbps",
    "avg_lat_ms",
    "avg_lat_down_ms",
    "avg_lat_up_ms",
    "tests",
    "devices",
    "tile_x",
    "tile_y",
]


@transient_retry()
def _list(prefix: str) -> ET.Element:
    """One ListObjectsV2 page (delimiter='/') as parsed XML."""
    resp = get(
        BASE + "/",
        params={"list-type": "2", "prefix": prefix, "delimiter": "/"},
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    return ET.fromstring(resp.content)


def _child_prefixes(prefix: str) -> list[str]:
    root = _list(prefix)
    out = []
    for cp in root.iter(_S3NS + "CommonPrefixes"):
        p = cp.findtext(_S3NS + "Prefix")
        if p:
            out.append(p)
    return out


def _list_partitions() -> list[dict]:
    """Discover every (type, year, quarter) partition and its object key from
    S3 — no hardcoded year range. Raises if the catalog looks empty (a silent
    listing break)."""
    partitions = []
    for type_pfx in _child_prefixes(ROOT_PREFIX):
        ctype = type_pfx.rstrip("/").rsplit("type=", 1)[-1]
        for year_pfx in _child_prefixes(type_pfx):
            year = int(year_pfx.rstrip("/").rsplit("year=", 1)[-1])
            for q_pfx in _child_prefixes(year_pfx):
                quarter = int(q_pfx.rstrip("/").rsplit("quarter=", 1)[-1])
                root = _list(q_pfx)
                key = None
                for c in root.iter(_S3NS + "Contents"):
                    k = c.findtext(_S3NS + "Key")
                    if k and k.endswith(".parquet"):
                        key = k
                        break
                if key is None:
                    continue
                partitions.append(
                    {"type": ctype, "year": year, "quarter": quarter, "key": key}
                )
    if len(partitions) < 40:
        raise AssertionError(
            f"discovered only {len(partitions)} partitions under {ROOT_PREFIX}; "
            "expected >=40 (2 types x >=8 years x 4 quarters) — S3 listing likely broke"
        )
    return partitions


@transient_retry(attempts=8, min_wait=4, max_wait=120)
def _download_parquet(key: str) -> bytes:
    resp = get(f"{BASE}/{key}", timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _normalize(batch: pa.Table, ctype: str, year: int, quarter: int) -> pa.Table:
    """Project one source row-group onto the canonical schema: keep present
    columns (cast to target type), fill missing optional columns with nulls,
    and append the constant partition columns."""
    n = batch.num_rows
    present = set(batch.column_names)
    cols = {}
    for field in RAW_SCHEMA:
        name = field.name
        if name == "connection_type":
            cols[name] = pa.array([ctype] * n, type=pa.string())
        elif name == "year":
            cols[name] = pa.array([year] * n, type=pa.int32())
        elif name == "quarter":
            cols[name] = pa.array([quarter] * n, type=pa.int32())
        elif name in present:
            cols[name] = batch.column(name).cast(field.type)
        else:
            cols[name] = pa.nulls(n, type=field.type)
    return pa.table(cols, schema=RAW_SCHEMA)


def _fetch_partition(asset: str, part: dict) -> None:
    """Stream one partition parquet → canonical raw asset, bounded memory."""
    content = _download_parquet(part["key"])
    with tempfile.NamedTemporaryFile(suffix=".parquet") as tmp:
        tmp.write(content)
        tmp.flush()
        del content
        pf = pq.ParquetFile(tmp.name)
        read_cols = [c for c in _SOURCE_COLS if c in pf.schema_arrow.names]
        with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
            for rg in range(pf.num_row_groups):
                table = pf.read_row_group(rg, columns=read_cols)
                writer.write_table(
                    _normalize(table, part["type"], part["year"], part["quarter"])
                )


def fetch_performance(node_id: str) -> None:
    """Discover all partitions and write each as a batch raw asset, advancing a
    per-partition watermark in state. Idempotent: already-done partitions are
    skipped. No self-imposed run budget — loops until every partition is drained;
    the supervisor interrupts and the next run resumes from saved state."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "done": []}
    done = set(state.get("done", []))

    for part in _list_partitions():
        batch_key = f"{part['type']}-{part['year']}-q{part['quarter']}"
        if batch_key in done:
            continue
        asset = f"{node_id}-{batch_key}"
        _fetch_partition(asset, part)  # write raw FIRST
        done.add(batch_key)
        save_state(node_id, {  # then advance state
            "schema_version": STATE_VERSION,
            "done": sorted(done),
        })


DOWNLOAD_SPECS = [
    NodeSpec(id="ookla-performance", fn=fetch_performance, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ookla-performance-transform",
        deps=["ookla-performance"],
        sql='''
            SELECT
                quadkey,
                connection_type,
                CAST(year AS INTEGER)    AS year,
                CAST(quarter AS INTEGER) AS quarter,
                make_date(year, (quarter - 1) * 3 + 1, 1) AS period_start,
                avg_d_kbps      AS avg_download_kbps,
                avg_u_kbps      AS avg_upload_kbps,
                avg_lat_ms      AS avg_latency_ms,
                avg_lat_down_ms AS avg_latency_download_ms,
                avg_lat_up_ms   AS avg_latency_upload_ms,
                tests,
                devices,
                tile_x,
                tile_y
            FROM "ookla-performance"
            WHERE quadkey IS NOT NULL
        ''',
    ),
]
