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
import os

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    post,
    raw_parquet_writer,
    save_raw_parquet,
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


def _tableinfo(table_id: str) -> dict:
    r = get(f"{BASE}/tableinfo/{table_id}", params={"format": "JSON", "lang": "en"})
    r.raise_for_status()
    return r.json()


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
    """Continuation-leg resume, scoped to THIS run.

    A 6h GHA cap retriggers the job under the same RUN_ID, so an asset the
    manifest already carries for this run is done. A prior run's object must
    NOT count: raw is addressable across runs, so trusting it would freeze
    every table at its first-ever fetch and make scheduled refreshes no-ops.
    An object written but never committed (node killed mid-write) has no
    manifest entry, so it is refetched rather than trusted.
    """
    frag = list_raw_fragments(asset, "parquet").get("full")
    return bool(frag) and frag.get("run_id") == os.environ.get("RUN_ID", "unknown")


def _flatten_subjects(subjects: list[dict]) -> list[dict]:
    rows = []

    def walk(items: list[dict], parent_id: str | None, depth: int) -> None:
        for item in items:
            subject_id = str(item["id"])
            rows.append(
                {
                    "id": subject_id,
                    "parent_id": parent_id,
                    "description": item.get("description"),
                    "active": bool(item.get("active")),
                    "has_subjects": bool(item.get("hasSubjects")),
                    "depth": depth,
                }
            )
            walk(item.get("subjects") or [], subject_id, depth + 1)

    walk(subjects, None, 0)
    return rows


def _fetch_subjects(asset: str) -> None:
    if _already_complete(asset):
        return

    r = get(f"{BASE}/subjects", params={"format": "JSON", "lang": "en", "recursive": "true"})
    r.raise_for_status()
    rows = _flatten_subjects(r.json())
    if not rows:
        raise ValueError("subjects endpoint returned no subject rows")
    schema = pa.schema(
        [
            ("id", pa.string()),
            ("parent_id", pa.string()),
            ("description", pa.string()),
            ("active", pa.bool_()),
            ("has_subjects", pa.bool_()),
            ("depth", pa.int64()),
        ]
    )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), asset)


def fetch_one(node_id: str) -> None:
    asset = node_id
    if _already_complete(asset):
        return

    table_id = _table_id(node_id)
    if table_id == "subjects":
        _fetch_subjects(asset)
        return

    info = _tableinfo(table_id)
    variables = info["variables"]

    # Chunk along the highest-cardinality dimension to bound each response size.
    chunk_var = max(variables, key=lambda v: len(v.get("values") or []))
    others = [v for v in variables if v is not chunk_var]
    rows_per_unit = 1
    for v in others:
        rows_per_unit *= max(1, len(v.get("values") or []))
    per_req = max(1, _ROW_BUDGET // max(1, rows_per_unit))
    per_req = min(per_req, _MAX_SELECT)  # keep enumerated selections under the 500 ceiling

    chunk_values = [val["id"] for val in (chunk_var.get("values") or [])]
    if not chunk_values:
        slices = [["*"]]
    elif len(chunk_values) <= per_req:
        # One request covers the whole dimension — use "*" instead of enumerating,
        # which both shrinks the body and sidesteps the explicit-list 500.
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
