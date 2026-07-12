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
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import ENTITY_IDS

BASE = "https://data.iadb.org/api/3/action"
TABULAR_FILE_FORMATS = {"CSV", "TSV", "TXT", "XLSX", "XLS", "XLSM"}
BATCH_ROWS = 50_000
SQL_PAGE = 30_000          # keyset page size for datastore_search_sql
MAX_SQL_PAGES = 5_000      # safety ceiling (≈150M rows) — raises, never silent
DEFERRED_ENTITY_IDS = {
    "2010-infrascope-index-for-latin-america-and-the-caribbean",
    "2018-global-microscope-on-financial-inclusion-dataset",
    "2019-idb-climate-finance-database",
    "2019-pension-indicators-for-latin-america-and-the-caribbean",
    "2020-better-jobs-index-database-latin-america",
    "2020-idb-climate-finance-database",
    "2020-pension-indicators-for-latin-america-and-the-caribbean",
    "2021-idb-climate-finance-database",
    "2022-idb-climate-finance-database",
    "2022-suriname-survey-of-living-conditions",
    "barbados-survey-of-living-conditions-2016",
    "baseline-salud-mesoamerica-guatemala-health-facility-survey-2015",
    "baseline-salud-mesoamerica-guatemala-household-survey-2015",
    "baseline-salud-mesoamerica-honduras-health-facility-survey-2015",
    "baseline-salud-mesoamerica-mexico-health-facility-survey-2015",
    "baseline-salud-mesoamerica-mexico-household-survey-2015",
    "baseline-salud-mesoamerica-panama-health-facility-survey-2015",
    "benchmarking-index-2009-economist-intelligence-unit",
    "bibliographic-database-on-the-bolivian-labor-market-2011-2019",
    "bolivia-labor-market-survey-supply-2022-aggregated-data",
    "cost-simulation-tool-for-long-term-care-systems-in-latin-america-and-the-ca",
    "data-associated-with-aging-in-latin-america-and-the-caribbean-social-protec",
    "data-associated-with-development-effects-of-rural-electrification",
    "data-associated-with-overview-of-aging-and-dependency-in-latin-america-and-",
    "data-associated-with-social-pulse-in-latin-america-and-the-caribbean-2016",
    "data-associated-with-social-pulse-in-latin-america-and-the-caribbean-2017",
    "data-associated-with-urban-integration-and-coexistence-program-results-of-t",
    "database-of-equivalent-fiscal-pressure-1990-2018",
    "dataset-for-the-national-day-care-service-program-cuna-ms",
    "dataset-learning-better-public-policy-for-skills-development-1990-2016",
    "departmental-gdp-data-and-regional-inequality-analysis-in-peru-1795-2017",
    "freight-transport-and-logistics-statistics-yearbook-2012-2014",
    "harmonized-latin-american-innovation-surveys-database-lais-firm-level-micro",
    "idb-data-portals",
    "idb-group-data-wall-2026",
    "labor-market-survey-data-in-bolivia-2015-2016",
    "latin-america-and-the-caribbean-public-debt-database-dec-2019",
    "latin-america-and-the-caribbean-public-debt-database-dec-2020",
    "latin-america-and-the-caribbean-public-debt-database-dec-2021",
    "latin-america-and-the-caribbean-public-debt-database-dec-2022",
    "latin-america-and-the-caribbean-public-debt-database-dec-2023",
    "latin-america-and-the-caribbean-public-debt-database-jun-2019",
    "latin-america-and-the-caribbean-public-debt-database-jun-2022",
    "latin-america-and-the-caribbean-public-debt-database-jun-2023",
    "latin-american-public-opinion-project-victimization-and-crime-survey-bahama",
    "model-for-estimating-the-costs-of-managing-recyclable-waste-with-the-inclus",
    "replication-data-for-spoon-continuous-program-to-improve-nutrition-baseline",
    "replication-data-for-the-role-of-pension-systems-in-retirement-across-development",
    "sample-code-for-creating-public-payroll-indicators-a-methodological-guide",
}

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
    """Parse a workbook, choosing the sheet with the most data rows (workbooks
    here often lead with a cover/contents sheet — e.g. 'Portada' before
    'Datos')."""
    import pandas as pd

    xl = pd.ExcelFile(io.BytesIO(raw))
    best, best_rows = None, -1
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, dtype=str)
        df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
        if df.shape[1] == 0:
            continue
        if len(df) > best_rows:
            best, best_rows = df, len(df)
    if best is None or best.shape[1] == 0:
        return [], []
    best = best.where(best.notna(), None)
    cols = [str(c) for c in best.columns]
    _NA = {"nan", "NaN", "NaT", "None", ""}
    rows = [
        {k: (None if (v is None or (isinstance(v, str) and v in _NA)) else v) for k, v in rec.items()}
        for rec in best.to_dict(orient="records")
    ]
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
    # Prefer the datastore (uniform, gives columns + row count cheaply). But
    # datastore_active is sometimes set on resources whose datastore table was
    # never populated (xloader failed to parse an XLS, etc.) — datastore_search
    # then returns success:false / no fields. In that case fall back to the
    # original file below.
    if rr.get("datastore_active"):
        try:
            res = _api("datastore_search", resource_id=rid, limit=0)
            cols = [f["id"] for f in res.get("fields", []) if not f["id"].startswith("_")]
        except Exception as e:  # noqa: BLE001 - degraded datastore; try the file
            print(f"[idb] datastore_search failed for {rid}: {e}; falling back to file")
            cols = []
        if cols:
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


@transient_retry()
def _sql_page(rid: str, last_id: int, limit: int) -> list[dict]:
    """One keyset page of a datastore resource, ordered by the internal _id."""
    sql = f'SELECT * FROM "{rid}" WHERE _id > {last_id} ORDER BY _id ASC LIMIT {limit}'
    resp = get(f"{BASE}/datastore_search_sql", params={"sql": sql}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"datastore_search_sql failed for {rid}: {str(body.get('error'))[:200]}")
    return body["result"]["records"]


def _iter_datastore_rows(rid: str, cols: tuple, total):
    """Stream every row of a datastore resource via keyset pagination on _id.

    Each page is an independent, retryable request (vs the chunked /dump stream,
    which silently truncated a 15M-row table when the connection closed early).
    Termination is on an empty page — never on a short page — so a server-side
    row cap below SQL_PAGE can't truncate us. Completeness is asserted against
    the datastore's reported total."""
    last_id, seen, pages = 0, 0, 0
    while True:
        recs = _sql_page(rid, last_id, SQL_PAGE)
        if not recs:
            break
        pages += 1
        if pages > MAX_SQL_PAGES:
            raise RuntimeError(f"{rid}: exceeded {MAX_SQL_PAGES} pages — runaway pagination")
        for rec in recs:
            last_id = int(rec["_id"])
            seen += 1
            yield rec
    if total and seen < int(total) * 0.99:
        raise ValueError(f"{rid}: streamed {seen} rows but datastore reports {total} — truncated")


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
    # Prefer datastore-backed groups: the CKAN datastore is the canonical,
    # machine-parsed table, whereas attached XLSX files are frequently
    # human-oriented summaries or cross-year roll-ups whose "largest sheet"
    # is not the year-specific data (and can collide across sibling datasets).
    # Only fall back to file-only groups when no resource has a usable datastore.
    groups: dict[tuple, list] = {}
    for p in probes:
        groups.setdefault(p["cols"], []).append(p)
    ds_groups = {c: m for c, m in groups.items() if any(x["kind"] == "datastore" for x in m)}
    pool = ds_groups or groups
    winner_cols = max(pool, key=lambda c: sum(x["weight"] for x in pool[c]))
    winner = pool[winner_cols]

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
            rows = (
                _iter_datastore_rows(p["rid"], winner_cols, p["weight"])
                if p["kind"] == "datastore"
                else iter(p["rows"])
            )
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
    if eid not in DEFERRED_ENTITY_IDS
]
