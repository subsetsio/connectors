"""IDB (Inter-American Development Bank) Open Data — CKAN catalog connector.

Mechanism: CKAN Action API at https://data.iadb.org/api/3/action (v3, no auth).
One download node per rank-accepted CKAN package (CKAN type:dataset). Each
package holds 1..N resources whose schemas can differ (a data table, a codebook,
a dictionary, hundreds of per-indicator slices, ...). We can't know a package's
schema ahead of time, so per package we:

  1. probe every tabular resource for its column-set + row count,
  2. group resources by identical column-set,
  3. publish the *dominant* group (largest by total rows) as ONE all-string
     table, streamed to parquet.

This yields a single coherent schema per published table and avoids redundant
double-counting (e.g. the Social Indicators package exposes one 15M-row master
table AND ~529 per-indicator slices of it — the master wins and the slices are
dropped). Values are kept as strings: column types are not knowable across 68
heterogeneous packages, and a string passthrough is the faithful generic choice.

Resource access:
  - datastore-active resources (the common case, incl. all the mega packages)
    are read via the CKAN datastore CSV dump (/datastore/dump/<rid>), streamed
    line-by-line so a 15M-row table never materializes in memory.
  - plain file resources (CSV/TSV/TXT/XLSX/XLS/XLSM) are downloaded and parsed.
  - non-tabular resources (PDF/DOC/URL/...) are skipped.

Stateless full re-pull: the whole corpus is small enough (~68 packages) to
re-fetch each refresh, so there is no watermark/cursor. CKAN does expose an
fq=metadata_modified delta filter, but it is not needed at this scale.
"""

import csv
import io
import re

import httpx
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

BASE = "https://data.iadb.org/api/3/action"
DUMP = "https://data.iadb.org/datastore/dump"
TABULAR_FILE_FORMATS = {"CSV", "TSV", "TXT", "XLSX", "XLS", "XLSM"}
BATCH_ROWS = 50_000

csv.field_size_limit(64 * 1024 * 1024)


@transient_retry()
def _api(action: str, **params):
    resp = get(f"{BASE}/{action}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()["result"]


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _sanitize(name: str, used: set) -> str:
    """Make a parquet/Delta-safe, unique column name."""
    n = re.sub(r'[\s,;{}()\t\n=/\\"\'`]+', "_", (name or "").strip()).strip("_")
    if not n:
        n = "col"
    base, i = n, 2
    while n in used:
        n = f"{base}_{i}"
        i += 1
    used.add(n)
    return n


def _parse_csv_bytes(raw: bytes, delimiter: str = ",") -> tuple[list[dict], list[str]]:
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    header = next(reader, None)
    if not header:
        return [], []
    rows = [{header[i]: (r[i] if i < len(r) else None) for i in range(len(header))} for r in reader]
    return rows, list(header)


def _parse_excel_bytes(raw: bytes) -> tuple[list[dict], list[str]]:
    import pandas as pd

    df = pd.read_excel(io.BytesIO(raw), sheet_name=0, dtype=str)
    df = df.where(df.notna(), None)
    cols = [str(c) for c in df.columns]
    rows = df.to_dict(orient="records")
    return rows, cols


def _load_file_resource(url: str, fmt: str) -> tuple[list[dict], list[str]]:
    raw = _get_bytes(url)
    if fmt in ("XLSX", "XLS", "XLSM"):
        return _parse_excel_bytes(raw)
    delimiter = "\t" if fmt == "TSV" else ","
    return _parse_csv_bytes(raw, delimiter)


def _probe_resource(rr: dict) -> dict | None:
    """Return {cols, weight, kind, name, ...} for a tabular resource, else None."""
    fmt = (rr.get("format") or "").upper()
    rid = rr.get("id")
    url = rr.get("url") or ""
    if rr.get("datastore_active"):
        res = _api("datastore_search", resource_id=rid, limit=0)
        cols = [f["id"] for f in res.get("fields", []) if not f["id"].startswith("_")]
        if not cols:
            return None
        return {
            "cols": tuple(cols),
            "weight": res.get("total") or 0,
            "kind": "datastore",
            "rid": rid,
            "name": rr.get("name") or rid,
        }
    if url.startswith("http") and fmt in TABULAR_FILE_FORMATS:
        rows, cols = _load_file_resource(url, fmt)
        if not cols:
            return None
        return {
            "cols": tuple(cols),
            "weight": len(rows),
            "kind": "memory",
            "rows": rows,
            "name": rr.get("name") or rid,
        }
    return None


def _iter_dump_rows(rid: str, cols: tuple):
    """Stream a datastore resource's full CSV dump, yielding dicts for `cols`."""
    url = f"{DUMP}/{rid}"
    client = get_client()
    with client.stream("GET", url, timeout=httpx.Timeout(30.0, read=600.0)) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines())
        header = next(reader, None)
        if not header:
            return
        pos = {c: i for i, c in enumerate(header)}
        idx = [(c, pos[c]) for c in cols if c in pos]
        for row in reader:
            yield {c: (row[i] if i < len(row) else None) for c, i in idx}


def _to_str(v):
    return None if v is None or (isinstance(v, str) and v == "") else str(v)


def fetch_one(node_id: str) -> None:
    asset = node_id
    pid = node_id[len("idb-"):]
    rec = _api("package_show", id=pid)

    probes = []
    for rr in rec.get("resources") or []:
        try:
            p = _probe_resource(rr)
        except httpx.HTTPStatusError as e:
            # Permanent per-resource failure (e.g. 404 on a stale file) — skip
            # this resource, keep building the package.
            print(f"[idb] {asset}: skip resource {rr.get('id')} ({rr.get('format')}): {e}")
            continue
        if p:
            probes.append(p)

    if not probes:
        raise ValueError(f"{asset}: no tabular resource found in package {pid!r}")

    # Group by identical column-set; publish the dominant group (most rows).
    groups: dict[tuple, list] = {}
    for p in probes:
        groups.setdefault(p["cols"], []).append(p)
    winner_cols = max(groups, key=lambda c: sum(x["weight"] for x in groups[c]))
    winner = groups[winner_cols]

    used: set = set()
    safe = [_sanitize(c, used) for c in winner_cols]
    res_col = _sanitize("source_resource", used)
    schema = pa.schema([(s, pa.string()) for s in safe] + [(res_col, pa.string())])

    with raw_parquet_writer(asset, schema) as writer:
        buf: list[list] = []

        def flush():
            if not buf:
                return
            arrays = [
                pa.array([row[i] for row in buf], pa.string())
                for i in range(len(safe) + 1)
            ]
            writer.write_batch(pa.record_batch(arrays, schema=schema))
            buf.clear()

        for p in winner:
            rname = p["name"]
            rows = _iter_dump_rows(p["rid"], winner_cols) if p["kind"] == "datastore" else iter(p["rows"])
            for row in rows:
                buf.append([_to_str(row.get(c)) for c in winner_cols] + [rname])
                if len(buf) >= BATCH_ROWS:
                    flush()
        flush()


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"idb-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Thin passthrough: raw parquet is already one clean all-string schema per
# package; the transform publishes it as the Delta table (and the runtime's
# 0-row check is the correctness gate on the fetch).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
