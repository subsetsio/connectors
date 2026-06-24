"""Statistics Denmark (StatBank / Statistikbanken) connector.

One download node per rank-active table. Each table is fetched from the StatBank
REST API in the streaming BULK format (semicolon-CSV), which bypasses the
1,000,000-cell cap of the non-streaming formats. To stay robust against
server-side connection drops on very large tables, the BULK request is split
into bounded chunks along the table's highest-cardinality dimension and the
chunks are concatenated into one Parquet asset. The matching transform publishes
the table as-is, casting the value column (INDHOLD) to DOUBLE.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    transient_retry,
    raw_parquet_writer,
    load_raw_parquet,
)
from constants import ENTITY_IDS

SLUG = "statistics-denmark"
BASE = "https://api.statbank.dk/v1"
_ROW_BUDGET = 300_000  # target max data rows per BULK request
# The StatBank /data endpoint returns HTTP 500 when a single variable's explicit
# value list is large (empirically it breaks between ~4000 and ~6000 ids — daily
# time series like DNRENTD have 10k+ Tid values). A wildcard "*" selection of the
# same dimension streams fine, so the limit is on enumerated selections, not on
# response size. Cap the per-request chunk well under that ceiling.
_MAX_SELECT = 3000


def _table_id(node_id: str) -> str:
    suffix = node_id[len(SLUG) + 1:]
    for eid in ENTITY_IDS:
        if eid.lower().replace("_", "-") == suffix:
            return eid
    raise ValueError(f"no table id matches node {node_id!r}")


@transient_retry()
def _tableinfo(table_id: str) -> dict:
    r = get(f"{BASE}/tableinfo/{table_id}", params={"format": "JSON", "lang": "en"})
    r.raise_for_status()
    return r.json()


@transient_retry()
def _fetch_bulk(body: dict) -> pa.Table:
    """POST a bounded BULK request and parse the semicolon-CSV to an all-string
    table. Non-streaming buffered read — each chunk is intentionally small."""
    r = post(f"{BASE}/data", json=body, timeout=600)
    r.raise_for_status()
    content = r.content
    nl = content.find(b"\n")
    if nl == -1:
        raise ValueError("BULK response has no header line")
    names = [h.strip() for h in content[:nl].decode("utf-8").rstrip("\r").split(";")]
    table = pacsv.read_csv(
        io.BytesIO(content),
        read_options=pacsv.ReadOptions(use_threads=True),
        parse_options=pacsv.ParseOptions(delimiter=";"),
        convert_options=pacsv.ConvertOptions(column_types={n: pa.string() for n in names}),
    )
    return table


def _already_complete(asset: str) -> bool:
    """Safe self-resume: skip only a fully-readable, non-empty Parquet. A node
    killed mid-write leaves a footer-less file that fails this read, so it is
    re-fetched rather than trusted."""
    try:
        return load_raw_parquet(asset).num_rows > 0
    except Exception:
        return False


def fetch_one(node_id: str) -> None:
    asset = node_id
    if _already_complete(asset):
        return

    table_id = _table_id(node_id)
    info = _tableinfo(table_id)
    variables = info["variables"]

    # Chunk along the highest-cardinality dimension to bound each response size.
    chunk_var = max(variables, key=lambda v: len(v.get("values") or []))
    others = [v for v in variables if v is not chunk_var]
    rows_per_unit = 1
    for v in others:
        rows_per_unit *= max(1, len(v.get("values") or []))
    per_req = max(1, _ROW_BUDGET // max(1, rows_per_unit))

    chunk_values = [val["id"] for val in (chunk_var.get("values") or [])]
    if not chunk_values:
        slices = [["*"]]
    else:
        slices = [chunk_values[i:i + per_req] for i in range(0, len(chunk_values), per_req)]

    schema = None
    total = 0
    writer_cm = None
    writer = None
    try:
        for sel in slices:
            body = {
                "table": table_id,
                "format": "BULK",
                "lang": "en",
                "variables": [{"code": chunk_var["id"], "values": sel}]
                + [{"code": v["id"], "values": ["*"]} for v in others],
            }
            table = _fetch_bulk(body)
            if table.num_rows == 0:
                continue
            if schema is None:
                schema = pa.schema([(n, pa.string()) for n in table.column_names])
                writer_cm = raw_parquet_writer(asset, schema)
                writer = writer_cm.__enter__()
            else:
                table = table.select(schema.names)
            writer.write_table(table.cast(schema))
            total += table.num_rows
    finally:
        if writer_cm is not None:
            writer_cm.__exit__(None, None, None)

    if total == 0:
        raise ValueError(f"{table_id}: BULK returned 0 data rows across all chunks")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# Generic transform: publish every dimension column as-is and cast the StatBank
# value column INDHOLD to DOUBLE ('..' / '.' = confidential/unavailable -> NULL).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                * EXCLUDE (INDHOLD),
                TRY_CAST(NULLIF(NULLIF(TRIM(INDHOLD), '..'), '.') AS DOUBLE) AS value
            FROM "{s.id}"
        ''',
    )
    for s in DOWNLOAD_SPECS
]
