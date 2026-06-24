"""Public Health Scotland — Scottish Health and Social Care Open Data (CKAN).

Catalog connector. One download node per rank-accepted CKAN *package*; each
package bundles one-to-many CSV *resources* (geographic and/or temporal cuts,
and sometimes genuinely distinct sub-tables). We publish ONE Delta table per
package (1:1 entity->subset), so a package's CSV resources are unioned by
column name into a single wide all-string table, tagged with the resource each
row came from (``resource_id`` / ``resource_name``).

Mechanism (from research): CKAN Action API for catalog discovery, per-resource
datastore CSV dump for bulk data:
  - columns:  GET /api/3/action/datastore_search?resource_id=<id>&limit=0  -> fields
  - data:     GET /datastore/dump/<resource_id>                            -> full CSV

Stateless full re-pull: each refresh re-fetches every resource and overwrites.
The dump is a full snapshot with no incremental/since filter, so there is no
watermark to carry. Columns are kept as VARCHAR — 70 heterogeneous package
schemas cannot be hand-typed, and the transform publishes them as-is.
"""

import csv
import io
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

from constants import ENTITY_IDS

SLUG = "public-health-scotland"
PREFIX = f"{SLUG}-"
API = "https://www.opendata.nhs.scot/api/3/action"
DUMP = "https://www.opendata.nhs.scot/datastore/dump"
WRITE_CHUNK = 50_000  # rows per parquet row-group flush


@transient_retry()
def _api(action: str, **params) -> dict:
    resp = get(f"{API}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN success=false for {action} {params}")
    return payload["result"]


@transient_retry()
def _dump_text(resource_id: str) -> str:
    # Full CSV for one resource. No bom -> clean ASCII header (no BOM on col 0).
    resp = get(f"{DUMP}/{resource_id}", timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def _sanitize(name: str) -> str:
    """Delta/parquet-safe column name: keep [A-Za-z0-9_], collapse the rest."""
    name = name.lstrip("﻿").strip()
    s = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_")
    return s or "col"


def _csv_resources(pkg: str) -> list[tuple[str, str]]:
    rec = _api("package_show", id=pkg)
    out = []
    for r in rec.get("resources", []) or []:
        if (r.get("format") or "").upper() != "CSV":
            continue
        # Only datastore-active resources can be pulled via /datastore/dump/.
        # Non-active CSVs (archives, lagging monthly loads, supplementary
        # cross-boundary files) 404 on the dump endpoint, so skip them.
        if not r.get("datastore_active"):
            print(f"[skip] {pkg}: resource {r['id']} ({r.get('name')}) "
                  "not datastore_active")
            continue
        out.append((r["id"], r.get("name") or r["id"]))
    return out


def _resource_fields(resource_id: str) -> list[str]:
    """Column names for a resource via the datastore (cheap, no data rows)."""
    try:
        res = _api("datastore_search", resource_id=resource_id, limit=0)
        return [f["id"] for f in res.get("fields", []) if f.get("id") != "_id"]
    except Exception as exc:  # noqa: BLE001 - permanent (non-datastore) resource
        print(f"[fields] {resource_id}: datastore_search failed ({type(exc).__name__}); "
              "will derive header from dump")
        return []


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pkg = node_id[len(PREFIX):]

    resources = _csv_resources(pkg)
    if not resources:
        raise RuntimeError(f"{pkg}: no CSV resources found in package_show")

    # Pass 1 — build the union column order across all resources. Prefer the
    # datastore field list; fall back to the dump header, caching that text so
    # the streaming pass below doesn't re-download it.
    col_order: list[str] = []
    seen: set[str] = set()
    cached: dict[str, str] = {}
    res_meta: list[tuple[str, str]] = []  # (resource_id, resource_name)

    for rid, rname in resources:
        fields = _resource_fields(rid)
        if not fields:
            text = _dump_text(rid)
            cached[rid] = text
            header = next(csv.reader(io.StringIO(text)), [])
            fields = [h for h in header if h.lstrip("﻿") != "_id"]
        for f in fields:
            s = _sanitize(f)
            if s not in seen:
                seen.add(s)
                col_order.append(s)
        res_meta.append((rid, rname))

    cols = ["resource_id", "resource_name"] + col_order
    schema = pa.schema([(c, pa.string()) for c in cols])

    # Pass 2 — stream each resource's CSV into one parquet, mapped onto the
    # union schema (missing columns -> null, empty strings -> null).
    with raw_parquet_writer(asset, schema) as writer:
        total = 0
        for rid, rname in res_meta:
            text = cached.pop(rid, None) or _dump_text(rid)
            reader = csv.DictReader(io.StringIO(text))
            buf: list[dict] = []
            for row in reader:
                rec = {c: None for c in col_order}
                for k, v in row.items():
                    if k is None:
                        continue
                    sk = _sanitize(k)
                    if sk == "_id" or sk not in seen:
                        continue
                    rec[sk] = v if (v is not None and v != "") else None
                rec["resource_id"] = rid
                rec["resource_name"] = rname
                buf.append(rec)
                if len(buf) >= WRITE_CHUNK:
                    writer.write_table(pa.Table.from_pylist(buf, schema=schema))
                    total += len(buf)
                    buf = []
            if buf:
                writer.write_table(pa.Table.from_pylist(buf, schema=schema))
                total += len(buf)
        if total == 0:
            raise RuntimeError(f"{pkg}: all resources empty (0 rows total)")
        print(f"[fetch] {asset}: {len(res_meta)} resources, {total} rows, {len(cols)} cols")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per package. The raw is already typed (all VARCHAR)
# and unioned across resources, so the transform is a straight passthrough.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
