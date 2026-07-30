"""ODEPA (Oficina de Estudios y Politicas Agrarias, Chile) connector.

Source: https://datos.odepa.gob.cl — a standard CKAN 3 portal. Each of the 6
packages partitions its data into one CSV resource per year. We discover the
resource list per package via the CKAN `package_show` action API, then download
every yearly CSV at its stable per-resource download URL (one GET each, full
content, no pagination) and concatenate them into one raw ndjson asset per
subset.

Fetch shape: stateless full re-pull. The whole corpus is small (agricultural
price/trade tables, tens of MB per subset) and CKAN exposes no reliable
modified-since filter, so we re-fetch every yearly CSV each run and overwrite.
Only the current/recent year files actually change upstream; re-pulling the
historical years is cheap and picks up any revisions for free.

Raw format: parquet (streamed, zstd). CSV headers are stable within each package
across all years (verified 1998..2026 for trade, 2008..2026 for consumer prices,
1999..2025 for the fruit cadastre), but values are kept as strings — several
numeric columns use a decimal comma ("11890,000000"), which the transform SQL
normalises. Parquet keeps the multi-million-row price tables columnar so the
SQL transform does not have to repeatedly scan compressed JSON over R2.

`comercio-exterior` is published as two subsets: exports (Region origen / Pais
destino / USD FOB) and imports (Pais origen / USD CIF) carry different column
lists, so each is its own table.
"""

import csv
import io

from constants import ENTITY_SPECS
import pyarrow as pa
from subsets_utils import NodeSpec, get, raw_parquet_writer, transient_retry

CKAN = "https://datos.odepa.gob.cl/api/3/action"
BATCH_ROWS = 50_000


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise AssertionError(f"CKAN reported failure for {url}: {payload.get('error')}")
    return payload["result"]


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _csv_resources(package: str, flow: str | None) -> list[dict]:
    pkg = _get_json(f"{CKAN}/package_show?id={package}")
    resources = [r for r in pkg.get("resources", []) if (r.get("format") or "").upper() == "CSV"]
    if flow:
        resources = [
            r for r in resources
            if flow in (r.get("name") or "").lower() or flow in (r.get("url") or "").lower()
        ]
    return resources


def _write_rows(writer, schema: pa.Schema, fieldnames: list[str], reader: csv.DictReader) -> int:
    rows = []
    rows_written = 0
    for row in reader:
        # Drop the ragged-row overflow key csv.DictReader emits as None.
        row.pop(None, None)
        rows.append({name: row.get(name) for name in fieldnames})
        if len(rows) >= BATCH_ROWS:
            table = pa.Table.from_pylist(rows, schema=schema)
            writer.write_table(table)
            rows_written += table.num_rows
            rows.clear()
    if rows:
        table = pa.Table.from_pylist(rows, schema=schema)
        writer.write_table(table)
        rows_written += table.num_rows
    return rows_written


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len("odepa-"):]
    spec = ENTITY_SPECS[entity_id]

    resources = _csv_resources(spec["package"], spec["flow"])
    if not resources:
        raise AssertionError(f"no CSV resources discovered for {entity_id} (package={spec['package']})")

    rows_written = 0
    first_text = _get_bytes(resources[0]["url"]).decode("utf-8-sig", errors="replace")
    first_reader = csv.DictReader(io.StringIO(first_text))
    fieldnames = list(first_reader.fieldnames or [])
    if not fieldnames:
        raise AssertionError(f"no CSV header found for {entity_id} at {resources[0]['url']}")

    schema = pa.schema([(name, pa.string()) for name in fieldnames])
    with raw_parquet_writer(asset, schema) as writer:
        rows_written += _write_rows(writer, schema, fieldnames, first_reader)
        for res in resources[1:]:
            url = res["url"]
            text = _get_bytes(url).decode("utf-8-sig", errors="replace")
            reader = csv.DictReader(io.StringIO(text))
            rows_written += _write_rows(writer, schema, fieldnames, reader)

    if rows_written == 0:
        raise AssertionError(f"fetched 0 rows for {entity_id} across {len(resources)} resources")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"odepa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_SPECS
]
