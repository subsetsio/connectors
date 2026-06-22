"""Statistics Denmark (StatBank / Statistikbanken) connector.

One download node per rank-active table. Each node fetches the full table from
the StatBank REST API using the streaming BULK format (semicolon-CSV) which
bypasses the 1,000,000-cell cap on non-streaming formats. The matching transform
publishes the table as-is, casting the value column (INDHOLD) to DOUBLE.
"""

import csv

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    transient_retry,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

SLUG = "statistics-denmark"
BASE = "https://api.statbank.dk/v1"
_BATCH = 50_000


def _table_id(node_id: str) -> str:
    """Recover the upstream table id from the spec id. Spec ids lowercase and
    hyphenate the table id; map back via the canonical entity list."""
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


def fetch_one(node_id: str) -> None:
    asset = node_id
    table_id = _table_id(node_id)
    info = _tableinfo(table_id)

    body = {
        "table": table_id,
        "format": "BULK",
        "lang": "en",
        "variables": [{"code": v["id"], "values": ["*"]} for v in info["variables"]],
    }

    @transient_retry()
    def _stream_to_parquet() -> int:
        client = get_client()
        with client.stream("POST", f"{BASE}/data", json=body, timeout=600) as resp:
            resp.raise_for_status()
            reader = csv.reader(resp.iter_lines(), delimiter=";")
            header = next(reader, None)
            if not header:
                raise ValueError(f"{table_id}: empty BULK response (no header)")
            cols = [c.strip() for c in header]
            schema = pa.schema([(c, pa.string()) for c in cols])
            ncol = len(cols)

            total = 0
            batch: list[list[str]] = []

            def flush(writer):
                nonlocal batch
                if not batch:
                    return
                columns = [
                    pa.array([row[j] if j < len(row) else None for row in batch], type=pa.string())
                    for j in range(ncol)
                ]
                writer.write_batch(pa.record_batch(columns, schema=schema))
                batch = []

            with raw_parquet_writer(asset, schema) as writer:
                for row in reader:
                    if not row or (len(row) == 1 and row[0] == ""):
                        continue
                    batch.append(row)
                    total += 1
                    if len(batch) >= _BATCH:
                        flush(writer)
                flush(writer)
            return total

    rows = _stream_to_parquet()
    if rows == 0:
        raise ValueError(f"{table_id}: BULK returned 0 data rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# Generic transform: publish every column as-is, but cast the StatBank value
# column INDHOLD to DOUBLE (".." / "." / "" = confidential/unavailable -> NULL).
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
